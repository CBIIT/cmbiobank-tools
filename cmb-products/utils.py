import re
import os
import shlex
import shutil
import tempfile
import pyexcel
import xlsxwriter
import subprocess
import json
import logging
from subprocess import run
from datetime import datetime
from pathlib import Path
from pdb import set_trace

logger = logging.getLogger("cmb-products")

def rave2dme(dumpdir, folder, conf, desc=None, stage_dir=None, dry_run=False):
    """
    :param dumpdir: RAVE dump directory
    :param folder: DME clinical run folder name (yyyymmdd)
    :param conf: configuration dictionary (from cmb-products.yaml)
    :param desc: Custom description of this dump (default: None)
    :param stage_dir: local dir for tarball creation
    :param dry_run: if True, do not run but emit log messages (default:False)
    """
    DME_RAVE_path = Path(conf['paths']['DME_RAVE_path'])
    pth = Path(dumpdir)
    arc_pth = (Path(stage_dir) if stage_dir else Path.cwd()) / pth.name
    logger.info("Creating tarball of '{pth}' in '{stg}'".format(pth=str(pth),stg=str(arc_pth)))
    if not dry_run:
        tarf = shutil.make_archive(str(arc_pth), "gztar", pth.parent, pth.name)
    else:
        tarf = arc_pth.with_suffix(".tar.gz")
    dt_re = re.compile(".*(202[0-9]{5})")
    metadata = {
        'pull_date': dt_re.match(pth.name).group(1),
        'description': desc or "RAVE clinical data for Cancer Moonshot Biobank (10323)",
    }
    dest = DME_RAVE_path / folder / Path(tarf).name
    logger.info("Pushing tarball '{arc}' to DME at '{dest}'".format(arc=str(tarf), dest=str(dest)))
    if not dry_run:
        rc = _file2dme(Path(tarf), dest, metadata, conf, dry_run=dry_run)
    else:
        rc = type('CompletedProcess',(object,),{"returncode":0, "args":"dry run"})()
    return rc


def _get_dme_rave_folders(conf):
    """Return the names of available RAVE run folders and files."""
    DME_ENV = conf['envs']['DME_ENV']
    DME_ENV['PATH'] = ":".join([DME_ENV['PATH'],os.environ['PATH']])
    DME_RAVE_path = Path(conf['paths']['DME_RAVE_path'])
    query = {
        "detailedResponse": False,
        "compoundQuery": {
            "operator": "AND",
            "queries": [
                {
	            "attribute":"collection_type",
	            "value": "Clinical",
	            "operator": "EQUAL"
                },
            ]
        },
        "page": 1,
        "totalCount": True,
    }
    obj_paths = []
    done = False
    while not done:
        q_tfp = tempfile.NamedTemporaryFile("w+")
        json.dump(query, q_tfp)
        q_tfp.seek(0)
        cmd = ["dm_query_dataobject", q_tfp.name, DME_RAVE_path]
        rc = run(cmd, capture_output=True, env=DME_ENV)
        if rc.returncode != 0:
            logger.error("DME query for folders failed: {}".format(rc.stderr))
            return None
        out = json.loads(rc.stdout)
        obj_paths.extend(out['dataObjectPaths'])
        if out['totalCount'] <= len(obj_paths):
            done = True
        else:
            query["page"] += 1 
    folders = {}
    for p in obj_paths:
        p = Path(p)
        folder = re.match(".*RAVE/([0-9]+)/", str(p)).group(1)
        if folder in folders:
            folders[folder].append(p.name)
        else:
            folders[folder] = [p.name]
    return folders

    

def _file2dme(file_pth, dest, metadata, conf, stage_dir=None, dry_run=False):
    """file_pth, dest: pathlib.Path objects"""
    DME_ENV = conf['envs']['DME_ENV']
    DME_ENV['PATH'] = ":".join([DME_ENV['PATH'],os.environ['PATH']])
    stage_dir = stage_dir or Path.cwd()
    mdata = { "object_name": file_pth.name,
              "metadataEntries": []}
    for att in metadata:
        md = {
            "attribute": att,
            "value": metadata[att],
        }
        if att.find("date") >=0:
            md["dateFormat"] = "yyyyMMdd"
        mdata["metadataEntries"].append(md)
    mdata_fp = tempfile.NamedTemporaryFile("w+")
    json.dump(mdata, mdata_fp)
    mdata_fp.seek(0)
    cmd = ["dm_register_dataobject", "-o", "dm-register-return.json", "-D", "dm-register-response.txt",
           mdata_fp.name, shlex.quote(str(dest)), shlex.quote(str(file_pth))]
    logger.info("Push file {dump} to DME location {dest}".format(dump=file_pth.name,
                                                                      dest=str(dest)))
    if dry_run:
        logger.info("DME push would have run with this command: {}".format(" ".join(cmd)))
        rc = type('CompletedProcess',(object,),{"returncode":0, "args":cmd})()
    else:
        rc = run(cmd, capture_output=True, cwd=str(stage_dir), env=DME_ENV)
    logger.debug("dm_register_dataobject run with args: {}".format(rc.args))
    if rc.returncode != 0:
        logger.error("Push to DME failed with error: '{}'".format(rc.stderr))
    return rc


def run_rave_reduce(strategy, optdict, dumpdir, rr,
                    outnm=None, newnm=None,  stage_dir=None, dry_run=False,
                    create_xlsx=False):
    opts = []
    aud = []
    for i in optdict:
        opts.extend([i,str(optdict[i])])
        if re.match(".*file.*",i):
            aud.append(Path(optdict[i]).name)
    cmd = [rr, "-s", strategy] + opts + [str(dumpdir)]
    logger.debug("cmd: {}".format(" ".join(cmd)))
    if not dry_run:
        try:
            run(cmd, capture_output=True, cwd=stage_dir, check=True)
        except subprocess.CalledProcessError as e:
            logger.error("On run: {}\nR stderr:\n {}\nR stdout:\n {}".format(
                " ".join(cmd), e.stderr, e.stdout))
            raise e
        logger.debug("Rename rave-reduce output from {} to {}".format(outnm, newnm))
        (stage_dir / Path(outnm)).rename( stage_dir / Path(newnm) )
        if create_xlsx:
            logger.info("Create xlsx file from {}".format( (stage_dir / Path(newnm) )))
            tsv2xlsx( stage_dir / Path(newnm) )
        if len(aud):
            logger.info("Create new audit file {}".format((stage_dir / Path(newnm)).with_suffix(".audit")))
            (stage_dir / Path(newnm)).with_suffix(".audit").write_text("\n".join(aud)+"\n")

def tsv2xlsx(tsv_path):
    xlsx_path = tsv_path.with_suffix(".xlsx")
    tsv = pyexcel.get_sheet(file_name=str(tsv_path))
    wb = xlsxwriter.Workbook(str(xlsx_path))
    ws = wb.add_worksheet(tsv_path.name[0:31])
    bold = wb.add_format({"bold":True})
    date = wb.add_format({"num_format":"d-mmm-yy"})
    hidden_rows=[]
    col_max_width=[]
    # headers
    hdrs = tsv.array[0]
    # filter out inactive records and remove the 'active' flag column
    if 'active' in hdrs:
        inactive = [ i for i in range(0, len(tsv))
                     if tsv.row_at(i)[hdrs.index('active')] == 'FALSE' ]
        tsv.filter(row_indices=inactive)
        tsv.filter(column_indices=[hdrs.index('active')])
    hdrs = tsv.array[0]  # update hdrs
    ws.set_row(0,None,bold)
    ws.write_row(0,0,hdrs)
    col_max_width = [len(x) for x in hdrs]
    for row, data in enumerate(tsv.array[1:]):
        row=row+1
        for col, item in enumerate(data):
            col_max_width[col] = col_max_width[col] if col_max_width[col] >= len(str(item)) else len(str(item))
            if hdrs[col]=="ctep_id" and item=="NA":
                hidden_rows.append(row)
            if re.match(".*date.*",hdrs[col],flags=re.I):
                dt = trydate(item)
                item = dt if dt else item
                ws.write(row,col,item, date)
            else:
                if item == "NA":
                    ws.write_blank(row,col,None)
                else:
                    ws.write(row,col,item)
    
    ws.autofilter(0,0,len(tsv.array)-1,len(tsv.array[0])-1)
    if "ctep_id" in hdrs:
        ws.filter_column(hdrs.index("ctep_id"), 'x != NA')
    for row in hidden_rows:
        ws.set_row(row, options={'hidden':True})
    for col in range(len(hdrs)):
        ws.set_column(col,col,col_max_width[col])
    wb.close()
        
def trydate(dt):
    ret = None
    try:
        ret = datetime.strptime(dt,"%d %b %Y")
    except:
        pass
    if not ret:
        try:
            ret = datetime.strptime(dt,"%d %B %Y")
        except:
            pass
    return ret

def cpy(p,tgt,dry_run=False):
    logger.info("Copy {} to {}".format(str(p),str(tgt)))
    cp = " ".join( ["cp", shlex.quote(str(p)), shlex.quote(str(tgt))] )
    logger.debug("cmd: {}".format(cp))
    if not dry_run:
        os.popen(cp)
    
