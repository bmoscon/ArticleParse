"""
Copyright (C) 2013-2016  Bryant Moscon - bmoscon@gmail.com

Please see the LICENSE file for the terms and conditions 
associated with this software.
"""

from articleparse.analyzer import Analyzer
import sys

def usage(command):
    print("usage:", command, " <URL>")

# Example of how one might use the analyzer module
def analyze(url):
    # set up with URL (provided on command line)
    a = Analyzer(url = sys.argv[1])
    # parse with a section length threshold of 50 characters (including spaces)
    a.parse_sections(threshold = 100)

    sections = a.analyze_sections()

    for item in sections:
        if item['probability'] >= 0.8:
            print(item['content'])  

if __name__ == "__main__":
    if len(sys.argv) != 2:
        usage(sys.argv[0])
    else:
        analyze(sys.argv[1])
