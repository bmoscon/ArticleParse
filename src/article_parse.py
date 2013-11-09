#!/usr/bin/python

import sys
sys.path.append("lib/")
from analyzer import Analyzer


def usage(command):
    print "usage:", command, " <URL>"


def analyze(url):
    a = Analyzer(url = sys.argv[1])
    a.parse_sections(threshold = 50)
    sections = a.get_main_sections(threshold = 5.0)
    
    for item in sections:
        print item
        print "\n"

if __name__ == "__main__":
    if len(sys.argv) != 2:
        usage(sys.argv[0])
    else:
        analyze(sys.argv[1])
