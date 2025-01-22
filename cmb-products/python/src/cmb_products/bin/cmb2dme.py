#! /usr/bin/env python
import argparse
import difflib
import logging
import re
import time
import yaml
from pathlib import Path
import cmb_products.file_series as fs
import cmb_products.utils as utils
from yaml import CLoader as loader
from pdb import set_trace

def do():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action="store_true",
                        help="log file and push commands, but do not run them")
    parser.add_argument('--conf-file', default="cmb-products.yaml",
                        help="cmb-products config file"),
    parser.add_argument('--log-file',default="cmb2dme.log",
                        help="Append log to named file")
    parser.add_argument('--no-log-file', action="store_true",
                        help="Do not log to file")
    parser.add_argument('--stage-dir', default=".cmb-build",help="directory for staging built products")
    parser.add_argument('--verbose','-v',action="count",default=0)
    parser.add_argument('--quiet','-q',action="count",default=0)
    args = parser.parse_args()

    logger = logging.getLogger("cmb-products")
    logger.setLevel(logging.DEBUG)

    if not args.no_log_file:
        logfile = logging.FileHandler(args.log_file)
        logfile.setFormatter(logging.Formatter(
            datefmt="%Y-%m-%d %H:%M:%S",fmt="%(asctime)s (%(name)s): [%(levelname)s] %(message)s"))
        logfile.setLevel(logging.DEBUG)
        logger.addHandler(logfile)

    logstream = logging.StreamHandler()
    logstream.setFormatter(logging.Formatter(
            datefmt="%Y-%m-%d %H:%M:%S",fmt="%(asctime)s (%(name)s): [%(levelname)s] %(message)s"))

    logger.addHandler(logstream)

    verb = 3 + args.verbose - args.quiet
    if verb == 3:
        logstream.setLevel(logging.WARNING)
    elif verb == 4:
        logstream.setLevel(logging.INFO)
    elif verb == 5:
        logstream.setLevel(logging.DEBUG)
    elif verb == 2:
        logstream.setLevel(logging.ERROR)
    elif verb == 1:
        logstream.setLevel(logging.CRITICAL)
    else:
        pass

    # diff entity_id audit files to determine appropriate
    # DME locations for dumps, inventory
    stage_dir = Path(args.stage_dir)
    if not stage_dir.exists():
        stage_dir.mkdir()
    logger.info("Stage directory is '{}'".format(str(stage_dir)))


    logger.info("Loading config yaml")
    conf = yaml.load(open(args.conf_file,"r"),Loader=loader)
    locs = conf['paths']
    base = (Path(locs["base_path"]) if locs.get("base_path") else Path("."))
    logger.info("Base path is {}".format(base))

    # process locations (dirs) from yaml
    for loc in locs:
        if loc == 'base_path':
            continue
        if loc == 'distro_file':
            locs[loc] = stage_dir / Path(locs[loc])
            continue
        if Path(locs[loc]).is_absolute():
            locs[loc] = Path(locs[loc])
        else:
            locs[loc] = base / Path(locs[loc])
        logger.debug("'{}' is at {}".format(loc, locs[loc]))

    manifests = {}
    audits = fs.FileSeries(locs["ids_local"]).by_suffix(".audit")
    for i in range(0,len(audits)-1):
        a0 = open(audits.series[i][2])
        a1 = open(audits.series[i+1][2])
        dif = difflib.ndiff(a1.readlines(), a0.readlines())
        key = audits.series[i][0].strftime("%Y%m%d")
        if key not in manifests:
            manifests[key] = {"dumps":[], "inventories":[]}
        for line in [x for x in dif if re.match("^[+]",x)]:
            line = line.rstrip().lstrip("+ ")
            if re.match("^#",line):
                continue
            elif re.match("10323",line):
                manifests[key]["dumps"].append(line)
            elif re.match("^Moonshot",line):
                manifests[key]["inventories"].append(line)
            else:
                logger.debug("Unparsed diff line skipped: '{}'".format(line))

    dme_folders = {}

    if Path("dme_folders.yaml").exists():
        dme_folders = yaml.load(open("dme_folders.yaml"),Loader=yaml.CLoader)
    else:
        logger.info("Retrieving file and folder info from DME")
        dme_folders = utils._get_dme_rave_folders(conf)
        yaml.dump(dme_folders, open("dme_folders.yaml","w"))


    # determine what needs pushing to dme
    # if dme Rave folder is not present for specified manifest key
    # (the pull date), ignore all the files for that key.
    # if a dump or inventory file in the manifest is already
    # in the dme (based on string matching to corresponding dme folder),
    # ignore that file.

    def look(x,y):
        found = any(map(lambda w: w.find(x) >= 0, y))
        if found:
            logger.debug("File '{}' already present in DME".format(x))
        return found


    for m in manifests:
        if m not in dme_folders:
            manifests[m]['dumps'] = []
            manifests[m]['inventories'] = []
            continue
        dumps = [x for x in manifests[m]['dumps'] if not look(x,dme_folders[m])]
        inventories = [x for x in manifests[m]['inventories'] if not look(re.sub(" ","_",x), dme_folders[m])]
        manifests[m]['dumps'] = dumps
        manifests[m]['inventories'] = inventories

    for m in manifests:
        if not manifests[m]['dumps'] and not manifests[m]['inventories']:
            continue
        logger.info("Pushing manifest for folder '{}'".format(m))
        for d in manifests[m]['dumps']:
            d = locs['rave_dump_source'] / d
            utils.rave2dme(str(d), m, conf, stage_dir=stage_dir, dry_run=args.dry_run)
            if not args.dry_run:
                time.sleep(1)
        for d in manifests[m]['inventories']:
            d = locs['vari_inventory_source'] / d
            stg = stage_dir / re.sub(" ","_",d.name)  # replace spaces in filename for DME
            utils.cpy(d,stg,args.dry_run)
            dest = locs['DME_RAVE_path'] / m / stg.name
            utils._file2dme(Path(stg.name), dest, {"description": "Van Andel sample inventory spreadsheet"},
                            conf, stage_dir=stage_dir, dry_run=args.dry_run)
            if not args.dry_run:
                time.sleep(1)  # give endpt a break
    pass

if __name__ == "__main__":
    do()
    
