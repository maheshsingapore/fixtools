#!/usr/bin/env python
import os
import re
import sys

p = re.compile('.*([^0-9]8=FIX(.*)\x0110=[0-9]{1,4}\x01).*')


def usage():
    print "ft extract <filter condition> <log file>"
    print "     E.g.: ft extract '35=' any.application.log"
    print "     E.g.: less -f any.application.log| ft extract '35='"


def main():
    filter_present = len(sys.argv) > 2 and not os.path.exists(sys.argv[-1])
    if len(sys.argv) > 2 and os.path.exists(sys.argv[-1]):
        processFile(filter_present)
    else:
        processStdin(filter_present)


def processFile(filter_present):
    for line in open(sys.argv[-1]):
        processLine(line, filter_present)


def processStdin(filter_present):
    for line in sys.stdin:
        processLine(line, filter_present)


def processLine(line, filter_present):
    if filter_present:
        if sys.argv[2] in line:
            m = p.match(line)
            if m:
                print m.group(1)
    else:
        m = p.match(line)
        if m:
            print m.group(1)


if __name__ == "__main__":
    main()
