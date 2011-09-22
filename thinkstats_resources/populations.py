"""This file contains code used in "Think Stats",
by Allen B. Downey, available from greenteapress.com

Copyright 2010 Allen B. Downey
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html
"""

import csv
import sys
import urllib


def Download(filename='populations.csv'):
    """Downloads files from the U.S. Census Bureau.
    
    Concatenates the contents of these pages and stores them in (filename).
    Files are numbered from 01 to 56, with a couple of gaps for future
    expansion (just kidding -- they are for U.S. territories).
    
    Args:
        filename: string name of file to store results
    """
    format = ('http://www.census.gov/popest/'
              'cities/tables/SUB-EST2007-04-%2.2d.csv')

    # loop through the state/territory codes
    out = open(filename, 'w')
    for i in range(1,57):
        url = format % i

        conn = urllib.urlopen(url)
        for line in conn.fp:
            out.write(line)
            
    out.close()

def Process(filename='populations.csv'):
    """Reads the previously-downloaded contents of (filename), parses
    it as CSV and extract all lines that seem to contain population
    information for a city or town.  For each line that is in the
    right format to be parsed, prints the population as of 2006.

    Args:
        filename: string name of file to store results
    """
    fp = open(filename)
    reader = csv.reader(fp)
    pops = []

    for t in reader:
        if len(t) != 11: continue

        try:
            name = t[0]
            if 'town' not in name and 'city' not in name: continue

            # use the second-to-last data point, which seems to
            # have fewer NAs
            pop = t[-2]
            pop = pop.replace(',', '')
            pop = int(pop)
            pops.append(pop)
        except:
            # if anything goes wrong, skip to the next one
            pass
            
    return pops


def main(script, *args):
    Download()
    pops = Process()

    for pop in pops:
        print pop


if __name__ == '__main__':
    main(*sys.argv)
