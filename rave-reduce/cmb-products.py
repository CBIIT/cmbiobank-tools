import os
import re
import sys
import shlex
import logging
import argparse
from pathlib import Path
from subprocess import run
import yaml
from file_series import file_series as fs
from yaml import CLoader as loader
from pdb import set_trace

parser = argparse.ArgumentParser()
parser.add_argument('--dry-run', action="store_true",
                    help="log rave-reduce commands, but do not run them")
parser.add_argument('--conf-file', default="cmb-products.yaml")
parser.add_argument('--verbose','-v',action="count")
parser.add_argument('--quiet','-q',action="count")
parser.add_argument('--stage-dir', default=".cmb-build",help="directory for staging built products")

sys.argv.extend(['--dry-run'])
args = parser.parse_args()


logging.basicConfig(style='{')
logger = logging.getLogger("cmb-products")
stage_dir = Path(args.stage_dir)

if not stage_dir.exists():
    stage_dir.mkdir()

if not args.quiet and not args.verbose:
    logger.setLevel(logging.WARNING)
elif args.verbose==1:
    logger.setLevel(logging.INFO)
elif args.verbose > 1:
    logger.setLevel(logging.DEBUG)
elif args.quiet==1:
    logger.setLevel(logging.ERROR)
elif args.quiet > 1:
    logger.setLevel(logging.CRITICAL)

if args.dry_run:
    logger.setLevel(logging.DEBUG)
    
logger.info("Loading config yaml")
conf = yaml.load(open(args.conf_file,"r"),Loader=loader)
locs = conf['paths']
base = (Path(locs["base_path"]) if locs.get("base_path") else Path("."))
logger.info("Base path is {}".format(base))

# process locations (dirs) from yaml
for loc in locs:
    if loc == 'base_path':
        continue
    if Path(locs[loc]).is_absolute():
        locs[loc] = Path(locs[loc])
    else:
        locs[loc] = base / Path(locs[loc])
    logger.debug("'{}' is at {}".format(loc, locs[loc]))

# sources
entity_ids = fs.FileSeries(locs["entity_id_source"])
entity_ids_rds = entity_ids.by_suffix(".rds")
rave_dumps = fs.FileSeries(locs["rave_dump_source"])
vari_inventory = fs.FileSeries(locs["vari_inventory_source"])

#local sinks
tcia_local = fs.FileSeries(locs["tcia_local"])
uams_local = fs.FileSeries(locs["uams_local"])
iroc_local = fs.FileSeries(locs["iroc_local"])

# workflow
cmd = []

# Each product has an associated .audit file. Each line in the
# audit file is the dirname or filename of the input data merged
# into the given product file via rave-reduce.

# also assume that the entire historical series of all rave dumps and
# all vari inventory files are in the source directories
# so - rave_dumps.paths_until( entity_ids_rds.latest_date ).latest_path
# is the last rave dump included in the latest entity ids file 

# update ids

id_rds = entity_ids_rds.latest_path
id_rds_date = entity_ids_rds.latest.date
id_rds_tag = re.match("entity_ids[.](.*)[.]rds",id_rds.name).group(1)

if (not id_rds_tag) or ( entity_ids_rds.latest_date.strftime("%Y%m%d") not in id_rds_tag):
    logger.error("Entity id filename {} is non-standard; can't detect datestamp".format(id_rds.name))
    raise RuntimeError("Entity id filename is non-standard: can't detect datestamp")

logger.info("Entity ids starting rds file: {}".format(id_rds))

id_rds_audit = id_rds.with_suffix(".audit")
if not id_rds_audit.exists():
    logger.error("No audit file {} found for starting entity id rds".format(id_rds_audit))
    raise RuntimeException("No audit file found")

with id_rds_audit.open() as f:
    aud = [ x.rstrip() for x in f ]

# rave dumps not present in audit file
cur = { x[1].name for x in rave_dumps }
rave_dumps_to_do = fs.FileSeries(seq=[ x for x in rave_dumps if x[1].name in cur-set(aud) ])
# inventories not present in audit file
cur = { x[1].name for x in vari_inventory }
vari_inv_to_do = fs.FileSeries(seq=[ x for x in vari_inventory if x[1].name in cur-set(aud)])

# merge new rave dumps, earliest to latest
if rave_dumps_to_do:

    for rdump in rave_dumps_to_do.iter_from_earliest():
        logger.info("Merge rave dump {}".format(rdump[1].name))
        cmd = [ '../rave-reduce.r',
                '-s','update_ids',
                '--ids-file',str(id_rds),
                '-d', shlex.quote(
                    rdump[0].strftime("%d %b %Y")),
                str(rdump[1]) ]
        logger.debug("cmd: {}".format(" ".join(cmd)))
        next_id_rds_tag = rdump[0].strftime("%Y%m%d")
        while (stage_dir/Path("entity_ids.{}.rds".format(next_id_rds_tag))).exists():
            mtch = re.match"^(202[0-9]{5})[.]([0-9]+)$",next_id_rds_tag)
            if mtch.group(2):
                next_id_rds_tag = "{}.{}".format(mtch.group(1),int(mtch.group(2))+1)
            else:
                next_id_rds_tag = "{}.1".format(mtch.group(1))
        next_id_rds = stage_dir / Path("entity_ids.{}.rds".format(next_id_rds_tag))
        logger.info("Creating intermediate id file {}".format(next_id_rds))
        if not args.dry_run:
            rc = run(cmd, capture_output=True, cwd=stage_dir)
            try:
                rc.check_returncode()
            except subprocess.CalledProcessError as e:
                logger.error("On run: {}\nstderr: {}\nstdout {}".format(
                    " ".join(e.args), e.stderr, e.stdout))
                raise e
            (stage_dir / Path("entity_ids.update.rds")).rename(next_id_rds)
        logger.debug("Add {} to audit list".format(rdump[1].name))
        aud.extend( [rdump[1].name] )
        id_rds = next_id_rds
        id_rds_date = datetime.date(int(next_id_rds_tag[0:4]),
                                    int(next_id_rds_tag[4:6]),
                                    int(next_id_rds_tag[6:8]))                                    

# then merge new var inventories, earliest to latest
if vari_inv_to_do:

    for vi in vari_inv_to_do.iter_from_earliest():
        logger.info("Merge vari inventory {}".format(vi[1].name))
        cmd = [ '../rave-reduce.r',
                '-s', 'update_ids',
                '--ids-file',str(id_rds),
                '--bcr-file',str(vi[1]),
                '-d', shlex.quote(
                    vi[0].strftime("%d %b %Y")),
                str(rdump[1])]
        logger.debug("cmd: {}".format(" ".join(cmd)))
        if vi[0] > id_rds_date:
            next_id_rds_tag = vi[0].strftime("%Y%m%d")
        else:
            next_id_rds_tag = id_rds_date.strftime("%Y%m%d")
        while (stage_dir/Path("entity_ids.{}.rds".format(next_id_rds_tag))).exists():
            mtch = re.match"^(202[0-9]{5})[.]([0-9]+)$",next_id_rds_tag)
            if mtch.group(2):
                next_id_rds_tag = "{}.{}".format(mtch.group(1),int(mtch.group(2))+1)
            else:
                next_id_rds_tag = "{}.1".format(mtch.group(1))
        next_id_rds = stage_dir / Path("entity_ids.{}.rds".format(next_id_rds_tag))
        logger.info("Creating intermediate id file {}".format(next_id_rds))
        if not args.dry_run:
            rc = run(cmd, capture_output=True, cwd=stage_dir)
            try:
                rc.check_returncode()
            except subprocess.CalledProcessError as e:
                logger.error("On run: {}\nstderr: {}\nstdout {}".format(
                    " ".join(e.args), e.stderr, e.stdout))
                raise e
            (stage_dir / Path("entity_ids.update.rds")).rename(next_id_rds)
        logger.debug("Add {} to audit list".format(vi[1].name))
        aud.extend( [ vi[1].name ] )
        id_rds = next_id_rds
        id_rds_date = datetime.date(int(next_id_rds_tag[0:4]),
                                    int(next_id_rds_tag[4:6]),
                                    int(next_id_rds_tag[6:8]))                                    
# Now id_rds is the latest entity ids file - if any updates were performed
# this is in the stage directory (otherwise, is the original in the source
# directory
# Create any required outgoing products in the stage directory:






