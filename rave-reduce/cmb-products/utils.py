import re
import os
import pyexcel
import xlsxwriter
import subprocess
import logging
from subprocess import run
from datetime import datetime
from pathlib import Path

logger = logging.getLogger("cmb-products")

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
        rc = run(cmd, capture_output=True, cwd=stage_dir)
        try:
            rc.check_returncode()
        except subprocess.CalledProcessError as e:
            logger.error("On run: {}\nstderr: {}\nstdout {}".format(
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
    cp = " ".join( ["cp", str(p), str(tgt)] )
    logger.debug("cmd: {}".format(cp))
    if not dry_run:
        os.popen(cp)
    
