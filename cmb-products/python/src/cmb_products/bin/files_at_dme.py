#!/usr/bin/env python
import json
import yaml
from sys import stdout
from cmb_products.utils import _get_dme_genomic_data as get_files
from yaml import CLoader as loader

def do():
    conf = yaml.load(open("cmb-products.yaml","r"),Loader=loader)
    files = get_files(conf)
    json.dump(files, stdout, indent=2)
