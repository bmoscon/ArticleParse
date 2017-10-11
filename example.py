#!/usr/bin/python3
"""
Copyright (C) 2013-2017  Bryant Moscon - bmoscon@gmail.com

Please see the LICENSE file for the terms and conditions
associated with this software.
"""
import argparse
from articleparse import Analyzer


def main():
    """
    prompt user to enter a url or a file

    outputs a list of "sections" that have been determined to be
    non boilerplate text
    """
    parser = argparse.ArgumentParser()
    g = parser.add_mutually_exclusive_group(required=True)
    g.add_argument("--url", help="URL to parse")
    g.add_argument("--file", help="file to parse")
    parser.add_argument("--threshold", type=int, help="section length threshold", default=100)
    parser.add_argument("--probability", type=float,
                        help="section probability threshold", default=0.8)

    args = parser.parse_args()
    
    url = args.url
    fp = args.file

    a = Analyzer(url = url, fp = fp)
    a.parse_sections(threshold = args.threshold)
    
    for item in a.analyze_sections():
        if item['probability'] >= args.probability:
            print(item['content'])


if __name__ == "__main__":
    main()
