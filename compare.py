__author__ = 'mv29256'
# !/usr/bin/env python
import sys
from optparse import OptionParser

from tabulate import Table


def usage():
    print "<any fix feed>| ft compare"
    print "<any fix feed>| ft compare [-a| exact tag numbers to compare]"
    print "     Eg.: ft extract '35=' any.application.log| ft compare"
    print "     Eg.: less -f any.fix.feed| ft compare 60"
    print "     Eg.: less -f any.fix.feed| ft compare -a"


def getTagNames():
    props = {}
    with open('config/alltags.csv', 'r') as f:
        for l in f:
            l = l.rstrip()
            k, v = l.split("=", 1)
            props[k] = v
    return props


def main():
    tagnames = getTagNames()
    messagecounter = 0
    messagesmap = {}
    tagsuperset = {}
    tentry = []
    tentries = {}
    parser = OptionParser()
    parser.add_option("-a", action="store_true", dest="displayAll")
    parser.add_option("-c", "--csv", action="store_true", dest="useCsv")
    (options, args) = parser.parse_args()

    for l in open("any.fix.feed"):
        messagecounter += 1
        messageMap = {}
        kvlist = l.split("\x01")
        for kv in kvlist:
            keyvalue = kv.split("=")
            if len(keyvalue) > 1:
                counter = 1
                key = keyvalue[0]
                while messageMap.has_key(key):
                    key = keyvalue[0] + "." + str(counter)
                    counter += 1
                messageMap[str(key)] = keyvalue[1]
                tagsuperset[key] = ""
        messagesmap[messagecounter] = messageMap
    header = ["Msg"]
    allTags = sorted(tagsuperset.keys())

    for tag in allTags:
        tagHasDifferingValue = None
        prevTagValue = ""
        for messageNumber in messagesmap.keys():
            message = messagesmap[messageNumber]
            currentTagValue = ""
            if message.has_key(tag):
                currentTagValue = message[tag]
            tagHasDifferingValue = tagHasDifferingValue or (prevTagValue != "" and prevTagValue != currentTagValue)
            prevTagValue = currentTagValue
            tentry.append(currentTagValue)

        if len(args) > 1:
            if tag in sys.argv[1:]:
                header.append(tag)
                tentries[tag] = tuple(tentry)
        elif options.displayAll or tagHasDifferingValue:
            header.append(tag)
            tentries[tag] = tuple(tentry)
        del tentry[:]
    table = Table(tuple(header), useCsv=options.useCsv)

    for messageNumber in messagesmap.keys():
        row = [str(messageNumber)]
        for eachtag in sorted(tentries.keys()):
            tentry = tentries[eachtag]
            row.append(tentry[int(messageNumber - 1)])
        table.append(tuple(row))
    table.printTable()


if __name__ == "__main__":
    main()
