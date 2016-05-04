#!/usr/bin/env python
import glob
import os
import sys


def usage():
    for m in glob.glob('*.py'):
        fname, fext = os.path.splitext(m)
        if fname != "ft":
            command = __import__(fname)
            print "-" * 80
            command.usage()
    print "-" * 80


def main():
    if len(sys.argv) < 2:
        usage()
        sys.exit(1)
    cmd = sys.argv[1]
    pdm = cmd + ".py"
    if os.path.exists(pdm):
        command = __import__(cmd)
        command.main()
    else:
        usage()


if __name__ == "__main__":
    main()
