#!/usr/bin/env python
import csv
import json
import sys
from optparse import OptionParser

hashmap = {}
currTagsList = []


def usage():
    print "<any fix feed>| ft tabulate <list of space-separated tags to print as a table>"
    print "     Eg.: ft extract '35=' any.application.log| ft tabulate 35 37 11 41"
    print "     Eg.: less -f any.fix.feed| ft tabulate 35 37 11 41"
    print "     Eg.: less -f any.fix.feed| ft tabulate --csv 35 37 11 41"
    print "     Eg.: less -f any.fix.feed| ft tabulate -c 35 37 11 41"


def main():
    if len(sys.argv) < 3:
        usage()
        return
    parser = OptionParser()
    parser.add_option("-c", "--csv", action="store_true", dest="useCsv")
    (options, args) = parser.parse_args()
    table = Table(tuple(args[1:]), useCsv=options.useCsv)

    param_index = table.getParameterIndex()
    for l in sys.stdin:
        hashmap.clear()
        kvlist = l.split("\x01")

        for kv in kvlist:
            keyvalue = kv.split("=")

            if len(keyvalue) > 1:
                hashmap[keyvalue[0]] = keyvalue[1]

        for tag in sys.argv[param_index:]:
            value = hashmap[tag] if hashmap.has_key(tag) else ""
            currTagsList.append(value)

        table.append(tuple(currTagsList))
        del currTagsList[:]
    table.printTable()


def printSeparator():
    print "-" * (sum(fieldLengthsMap.values()) + 2 * len(fieldLengthsMap))


if __name__ == "__main__":
    paramIndex = 1
    main()


class Table:
    def __init__(self, args, **kwargs):
        if kwargs.has_key("useCsv") and kwargs["useCsv"]:
            self.delegate = CsvTable(tuple(args))
        else:
            self.delegate = AlignedTable(tuple(args))

    def append(self, list, **kwargs):
        self.delegate.append(list, **kwargs)

    def printTable(self):
        self.delegate.printTable()

    def getParameterIndex(self):
        return self.delegate.getParameterIndex()


class CsvTable:
    def __init__(self, header):
        self.header = tuple(header)
        self.entries = []

    def append(self, list, **kwargs):
        e = Entry(list, None)
        self.entries.append(e)

    def printTable(self):
        writer = csv.writer(sys.stdout, lineterminator='\n', quoting=csv.QUOTE_ALL)
        writer.writerow(self.header)
        for e in self.entries:
            writer.writerow(e.list)

    def getParameterIndex(self):
        return 3


class AlignedTable:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = "\033[1m"

    def __init__(self, header):
        self.header = tuple(header)
        self.fieldLengthsArray = []
        self.entries = []
        for index, value in enumerate(header):
            self.fieldLengthsArray.append(len(value))

    def add(self, List):
        print List

    def printSeparator(self):
        print "-" * (sum(self.fieldLengthsArray) + 2 * len(self.fieldLengthsArray))

    def append(self, list, **kwargs):
        for col, value in enumerate(list):
            if len(value) > self.fieldLengthsArray[col]:
                self.fieldLengthsArray[col] = len(value)
        color = None
        if kwargs.has_key("color"):
            color = kwargs.get("color")
        e = Entry(list, color)
        self.entries.append(e)

    def printTable(self):
        pFormat = ""
        for index, value in enumerate(self.fieldLengthsArray):
            pFormat = pFormat + " %-" + str(value) + "s|"

        self.printSeparator()
        
        print pFormat % (self.header)

        self.printSeparator()

        for index, instance in enumerate(self.entries):
            if instance.color is not None:
                print instance.color + pFormat % (instance.list) + AlignedTable.ENDC
            else:
                print pFormat % (instance.list)

        self.printSeparator()

    def toJson(self):
        return json.dumps(self.entries, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def getParameterIndex(self):
        return 2


class Entry:
    def __init__(self, list, color):
        self.list = list
        self.color = color
