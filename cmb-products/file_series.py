"""
file_series
===========
CMB data product scripting

This module contains the class FileSeries. This class stores a list 
of duples (datetime.date, pathlib.Path) of paths in a specified 
directory. The paths that are stored must contain a datestamp of a
specified format in their names to be registered in the FileSeries.
"""

import datetime
import re
from pathlib import Path

# product naming convention: <prefix>.<yyyy><mm><dd>.<ext>
#  example date 20211010. This is the pull date of the underlying source data
#  not the creation date
#  - date of the rave dump, date in the vari xlsx file name

# rave dump directory naming convention: 10323_<dddd>_<yyyymmdd>_<hhmmss>
#  - <yyyymmdd> is pull date

# vari biospecimen inventory xlsx naming convention:
#  "Moonshot Report <(m)m>.<(d)d>d.<yyyy>.xlsx"
#  single-digit months and days present

# vari slide data export xlsx naming convention: "<Monthname> Export.xlsx"
#  - filenames are handled in rave-reduce.r - these do not require a file series
#    in cmb-products


date_re = re.compile(".*(202[0-9]{5})([.]([0-9]+))?[._]")
date_iroc_re = re.compile(".*(202[0-9])-([0-9]{2})-([0-9]{2})([.]([0-9]+))?[._]")
date_vari_re = re.compile(".* ([0-9]{1,2})[.]([0-9]{1,2})[.](202[0-9])([.]([0-9]+))?[.]xlsx")

class FileSeries(object):
    def __init__(self, path=None, seq=None):
        self.series = []
        if path:
            ar = [x for x in path.iterdir() if date_re.match(x.name)]
            for p in ar:
                date_str = date_re.match(p.name).group(1)
                ver = int(date_re.match(p.name).group(3) or 0)
                dt=datetime.date(int(date_str[0:4]),
                                 int(date_str[4:6]),
                                 int(date_str[6:8]))
                self.series.extend([(dt,ver,p)])
            # iroc kludge
            if not ar:
                ar = [x for x in path.iterdir() if date_iroc_re.match(x.name)]
                for p in ar:
                    mtch = date_iroc_re.match(p.name)
                    dt=datetime.date(int(mtch.group(1)),
                                     int(mtch.group(2)),
                                     int(mtch.group(3)))
                    ver = int(mtch.group(5) or 0)
                    self.series.extend([(dt,ver,p)])
            # vari kludge
            if not ar:
                ar = [x for x in path.iterdir() if date_vari_re.match(x.name)]
                for p in ar:
                    mtch = date_vari_re.match(p.name)
                    dt=datetime.date(int(mtch.group(3)),
                                     int(mtch.group(1)),
                                     int(mtch.group(2)))
                    ver = int(mtch.group(5) or 0)
                    self.series.extend([(dt,ver,p)])
            if not self.series:
                raise RuntimeError("path contains no files with dates in filename")
        if seq:
            self.series = seq
        self.series.sort(key=lambda x:(x[0],x[1]),reverse=True)

    def __len__(self):
        return len(self.series)
    def __getitem__(self, key):
        return self.series[key]
    
    @property
    def latest_date(self):
        if self.series:
            return self.series[0][0]
        else:
            return None
    @property
    def latest_path(self):
        if self.series:
            return self.series[0][2]
        else:
            return None
    @property
    def earliest_date(self):
        if self.series:
            return self.series[-1][0]
        else:
            return None
    @property
    def earliest_path(self):
        if self.series:
            return self.series[-1][2]
        else:
            return None

    def paths_since(self, date):
        """Returns a FileSeries, a subset of the invocant's files whose dates are strictly later than the date provided."""
        paths = [x for x in self.series if x[0] > date]
        if paths:
            return FileSeries(seq=paths)
        else:
            return None

    def paths_until(self, date):
        """Returns a FileSeries, a subset of the invocant's files whose dates are earlier than or equal to the date provided."""
        paths = [x for x in self.series if x[0] <= date]
        if paths:
            return FileSeries(seq=paths)
        else:
            return None

    def by_suffix(self, suffix):
        """Returns a FileSeries, the subset of the invocant's files with the given suffix."""
        paths = [x for x in self.series if x[2].suffix == suffix]
        if paths:
            return FileSeries(seq=paths)
        else:
            return None

    def iter_from_latest(self):
        """ Returns iterator that returns (date,path), latest to earliest."""
        return iter(self.series)

    def iter_from_earliest(self):
        """ Returns iterator that returns (date,path), earliest to latest."""
        return iter(reversed(self.series))

    def pop_latest(self):
        if self.series:
            return self.series.pop(0)
        else:
            return None

    def pop_earliest(self):
        if self.series:
            return self.series.pop()
        else:
            return None
        
