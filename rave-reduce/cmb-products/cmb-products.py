#! /usr/bin/env python
import re
import logging
import argparse
import datetime
import yaml
from pathlib import Path
import file_series as fs
import utils
from yaml import CLoader as loader
from pdb import set_trace

parser = argparse.ArgumentParser()
parser.add_argument('--dry-run', action="store_true",
                    help="log rave-reduce commands, but do not run them")
parser.add_argument('--conf-file', default="cmb-products.yaml")
parser.add_argument('--verbose','-v',action="count")
parser.add_argument('--quiet','-q',action="count")
parser.add_argument('--stage-dir', default=".cmb-build",help="directory for staging built products")
parser.add_argument('--fake-file', action="store_true",help="touch files in stage directory")
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

logger.info("Loading rave-reduce config.yml")
rr_conf = yaml.load(locs["rave_reduce_config"].open(),Loader=loader)

# rave reduce
rave_reduce_r = str(locs["rave_reduce_r"])

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
id_rds_date = entity_ids_rds.latest_date
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
if len(rave_dumps_to_do):

    for rdump in rave_dumps_to_do.iter_from_earliest():
        logger.info("Merge rave dump {}".format(rdump[1].name))
        next_id_rds_tag = rdump[0].strftime("%Y%m%d")
        while (stage_dir/Path("entity_ids.{}.rds".format(next_id_rds_tag))).exists():
            mtch = re.match("^(202[0-9]{5})([.]([0-9]+))?$",next_id_rds_tag)
            if mtch.group(2):
                next_id_rds_tag = "{}.{}".format(mtch.group(1),int(mtch.group(3))+1)
            else:
                next_id_rds_tag = "{}.1".format(mtch.group(1))
        next_id_rds = stage_dir / Path("entity_ids.{}.rds".format(next_id_rds_tag))
        logger.info("Creating intermediate id file {}".format(next_id_rds))
        optdict = { '--ids-file':id_rds.resolve(),
                    '-d': rdump[0].strftime("%d %b %Y") }
        utils.run_rave_reduce(
            'update_ids', optdict, rdump[1], rave_reduce_r,
            outnm="entity_ids.update.rds",
            newnm="entity_ids.update.rds".replace("update",next_id_rds_tag),
            stage_dir=stage_dir,dry_run=args.dry_run)
                             
        if not args.dry_run:
            (stage_dir / Path("entity_ids.update.tsv")).rename(next_id_rds.with_suffix('.tsv'))
        if args.fake_file:
            next_id_rds.touch(exist_ok=True)
            next_id_rds.with_suffix('.tsv').touch(exist_ok=True)
        logger.debug("Add {} to audit list".format(rdump[1].name))
        aud.extend( [rdump[1].name] )
        id_rds = next_id_rds
        id_rds_date = datetime.date(int(next_id_rds_tag[0:4]),
                                    int(next_id_rds_tag[4:6]),
                                    int(next_id_rds_tag[6:8]))
        id_rds_tag = next_id_rds_tag

# then merge new var inventories, earliest to latest
if len(vari_inv_to_do):

    for vi in vari_inv_to_do.iter_from_earliest():
        logger.info("Merge vari inventory {}".format(vi[1].name))
        if vi[0] > id_rds_date:
            next_id_rds_tag = vi[0].strftime("%Y%m%d")
        else:
            next_id_rds_tag = id_rds_date.strftime("%Y%m%d")
        while (stage_dir/Path("entity_ids.{}.rds".format(next_id_rds_tag))).exists():
            mtch = re.match("^(202[0-9]{5})([.]([0-9]+))?$",next_id_rds_tag)
            if mtch.group(2):
                next_id_rds_tag = "{}.{}".format(mtch.group(1),int(mtch.group(3))+1)
            else:
                next_id_rds_tag = "{}.1".format(mtch.group(1))
        next_id_rds = stage_dir / Path("entity_ids.{}.rds".format(next_id_rds_tag))
        logger.info("Creating intermediate id file {}".format(next_id_rds))
        optdict = {'--ids-file': id_rds.resolve(),
                   '--bcr-file': vi[1],
                   '-d': vi[0].strftime("%d %b %Y")}
        utils.run_rave_reduce(
            'update_ids', optdict, rave_dumps.latest_path, rave_reduce_r,
            outnm="entity_ids.update.rds",
            newnm="entity_ids.update.rds".replace("update",next_id_rds_tag),
            stage_dir=stage_dir,dry_run=args.dry_run)
        if not args.dry_run:
            (stage_dir / Path("entity_ids.update.tsv")).rename(next_id_rds.with_suffix('.tsv'))
        if args.fake_file:
            next_id_rds.touch(exist_ok=True)
            next_id_rds.with_suffix('.tsv').touch(exist_ok=True)

        logger.debug("Add {} to audit list".format(vi[1].name))
        aud.extend( [ vi[1].name ] )
        id_rds = next_id_rds
        id_rds_date = datetime.date(int(next_id_rds_tag[0:4]),
                                    int(next_id_rds_tag[4:6]),
                                    int(next_id_rds_tag[6:8]))
        id_rds_tag = next_id_rds_tag
        
# Now id_rds is the latest entity ids file - if any updates were performed
# this is in the stage directory (otherwise, is the original in the source
# directory
# Create any required outgoing products in the stage directory:

# new audit file if nec
if id_rds != entity_ids_rds.latest_path:
    new_id_rds_audit = id_rds.with_suffix(".audit")
    logger.info("Create new audit file {}".format(new_id_rds_audit))
    if not args.dry_run:
        new_id_rds_audit.write_text( "\n".join(aud)+"\n" )
    if args.fake_file:
        new_id_rds_audit.touch(exist_ok=True)
    logger.info("Create xlsx from tsv {}".format(id_rds.with_suffix('.tsv')))
    if not args.dry_run:
       utils.tsv2xlsx(id_rds.with_suffix('.tsv'))
    if args.fake_file:
        id_rds.with_suffix('.xlsx').touch(exist_ok)
    

# create iroc registration

logger.info("Create iroc registration with date {}".format(id_rds_date))
optdict = { '-s':'iroc',
            '--ids-file':id_rds.resolve() }
outnm = [x for x in rr_conf["iroc"]["output"]][0]
newnm = outnm.replace('_','-').replace('txt',".".join([id_rds_date.strftime("%Y-%m-%d"),"txt"]))
utils.run_rave_reduce("iroc",optdict,rave_dumps.latest_path,rave_reduce_r,
                outnm=outnm,newnm=newnm,stage_dir=stage_dir,dry_run=args.dry_run)
if args.fake_file:
    (stage_dir / Path(newnm)).touch(exist_ok=True)
    (stage_dir / Path(newnm)).with_suffix(".audit").touch(exist_ok=True)

# slide table

logger.info("Create uams slide table with date {}".format(id_rds_date))
optdict = { '-s':'slide_table', '--ids-file':id_rds.resolve(),
        '--bcr-file':vari_inventory.latest_path.resolve(),
        '--bcr-slide-file-dir':locs['vari_slide_data_source'],
        '-d':id_rds_date.strftime("%d %b %Y")}
outnm = [x for x in rr_conf["slide_table"]["output"]][0]
newnm = outnm.replace("tsv",".".join([id_rds_date.strftime("%Y%m%d"),"tsv"]))
utils.run_rave_reduce("slide_table",optdict,rave_dumps.latest_path,rave_reduce_r,
                outnm=outnm,newnm=newnm,stage_dir=stage_dir,create_xlsx=True,
                dry_run=args.dry_run)
if args.fake_file:
    (stage_dir / Path(newnm)).touch(exist_ok=True)
    (stage_dir / Path(newnm)).with_suffix(".xlsx").touch(exist_ok=True)
    (stage_dir / Path(newnm)).with_suffix(".audit").touch(exist_ok=True)

# tcia metadata

logger.info("Create tcia metadata table with date {}".format(id_rds_date))
optdict = { '--ids-file':id_rds.resolve(),
            '--bcr-file':vari_inventory.latest_path.resolve(),
            '-d':id_rds_date.strftime("%d %b %Y")}
outnm = [x for x in rr_conf["tcia_metadata"]["output"]][0]
newnm = outnm.replace("tsv",".".join([id_rds_date.strftime("%Y%m%d"),"tsv"]))
utils.run_rave_reduce("tcia_metadata",optdict,rave_dumps.latest_path, rave_reduce_r,
                outnm=outnm,newnm=newnm,stage_dir=stage_dir,create_xlsx=True,
                dry_run=args.dry_run)
if args.fake_file:
    (stage_dir / Path(newnm)).touch(exist_ok=True)
    (stage_dir / Path(newnm)).with_suffix(".xlsx").touch(exist_ok=True)
    (stage_dir / Path(newnm)).with_suffix(".audit").touch(exist_ok=True)

