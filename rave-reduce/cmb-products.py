import os
import sys
import shlex
from pathlib import Path
from subprocess import run
import yaml
from file_series import file_series as fs
from yaml import CLoader as loader
from pdb import set_trace

conf = yaml.load(open("cmb-products.yaml","r"),Loader=loader)
locs = conf['paths']
base = (Path(locs["base_path"]) if locs.get("base_path") else Path("."))

# process locations (dirs) from yaml
for loc in locs:
    if loc == 'base_path':
        continue
    if Path(locs[loc]).is_absolute():
        locs[loc] = Path(locs[loc])
    else:
        locs[loc] = base / Path(locs[loc])

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

# assume a requirement: given an entity_ids file datestamp, it has
# incorporated all rave dump and vari inventory information with
# datestamps earlier or equal to that date
#
# also assume that the entire historical series of all rave dumps and
# all vari inventory files are in the source directories
# so - rave_dumps.paths_until( entity_ids_rds.latest_date ).latest_path
# is the last rave dump included in the latest entity ids file 

rave_dumps_to_do = rave_dumps.paths_since(entity_ids_rds.latest_date)
vari_inv_to_do = vari_inventory.paths_since(entity_ids_rds.latest_date)

if rave_dumps_to_do or vari_inv_to_do:
    
    id_rds = entity_ids_rds.latest_path
    rdump = rave_dumps.paths_until( entity_ids_rds.latest_date ).pop_latest()

    if (rave_dumps_to_do.earliest_date < vari_inv_to_do.earliest_date):
        # update ids
        rdump = rave_dumps_to_do.pop_earliest()
        cmd = [ '../rave-reduce.r',
                '-s','update_ids',
                '--ids-file',str(id_rds),
                '-d', shlex.quote(
                    rdump[0].strftime("%d %b %Y")),
                str(rdump[1]) ]
        # rc = run(cmd, capture_output=True, cwd=Path('try'))
        id_rds = locs["entity_id_source"] / Path("entity_ids.{}.rds".format( rdump[0].strftime("%Y%m%d") ))
    else:
        vi = vari_inv_to_do.pop_earliest()
        cmd = [ '../rave-reduce.r',
                '-s', 'update_ids',
                '--ids-file',str(id_rds),
                '--bcr-file',str(vi[1]),
                '-d', shlex.quote(
                    vi[0].strftime("%d %b %Y")),
                str(rdump[1])]
        # rc = run(cmd, capture_output=True, cwd=Path('try'))                    
        id_rds = locs["entity_id_source"] / Path("entity_ids.{}.rds".format( vi[0].strftime("%Y%m%d") ))


    pass

pass
            


