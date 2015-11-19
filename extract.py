#!/usr/bin/env python
import subprocess, socket, re, os, shutil, sys
p = re.compile('.*([^0-9]8=FIX(.*)\x0110=[0-9]{1,4}\x01).*')
def usage():
        print "ft extract <filter condition> <log file>"
        print "     E.g.: ft extract '35=' any.application.log"
        print "     E.g.: less -f any.application.log| ft extract '35='"
def main():
        filterPresent = len(sys.argv) > 2 and not os.path.exists(sys.argv[-1])
        if len(sys.argv) > 2 and os.path.exists(sys.argv[-1]):
                processFile(filterPresent)
        else:
                processStdin(filterPresent)
def processFile(filterPresent):
        for line in open(sys.argv[-1]):
                processLine(line, filterPresent)
def processStdin(filterPresent):
        for line in sys.stdin:
                processLine(line, filterPresent)
def processLine(line, filterPresent):
        if filterPresent:
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
