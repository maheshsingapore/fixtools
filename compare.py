__author__ = 'mv29256'
#!/usr/bin/env python
import subprocess, socket, re, os, shutil,sys
from tabulate import Table
from optparse import OptionParser

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
                        k,v = l.split("=", 1)
                        props[k]=v
        return props

def main():
        tagnames = getTagNames()
        messageCounter = 0
        messagesMap = {}
        tagSuperset = {}
        tEntry =[]
        tEntries ={}
        parser = OptionParser()
        parser.add_option("-a", action="store_true", dest="displayAll")
        parser.add_option("-c", "--csv", action="store_true", dest="useCsv")
        (options, args) = parser.parse_args()
        for l in open("any.fix.feed"):
                messageCounter += 1
                messageMap = {}
                kvlist = l.split("\x01")
                for kv in kvlist:
                        keyvalue = kv.split("=")
                        if (len(keyvalue) > 1):
                                counter = 1
                                key = keyvalue[0]
                                while (messageMap.has_key(key)):
                                        key = keyvalue[0] + "." + str(counter)
                                        counter += 1
                                messageMap[str(key)] = keyvalue[1]
                                tagSuperset[key] = ""
                messagesMap[messageCounter] = messageMap
        header =["Msg"]
        allTags = sorted(tagSuperset.keys())
        for tag in allTags:
                tagHasDifferingValue = None
                prevTagValue = ""
                for messageNumber in messagesMap.keys():
                        message = messagesMap[messageNumber]
                        currentTagValue = ""
                        if message.has_key(tag):
                                currentTagValue = message[tag]
                        tagHasDifferingValue = tagHasDifferingValue or (prevTagValue != "" and prevTagValue != currentTagValue)
                        prevTagValue = currentTagValue
                        tEntry.append(currentTagValue)
                if len(args) > 1:
                        if tag in sys.argv[1:]:
                                header.append(tag)
                                tEntries[tag] = tuple(tEntry)
                elif options.displayAll or tagHasDifferingValue:
                        header.append(tag)
                        tEntries[tag] = tuple(tEntry)
                del tEntry[:]
        table = Table(tuple(header), useCsv=options.useCsv)
        for messageNumber in messagesMap.keys():
                row = [str(messageNumber)]
                for eachtag in sorted(tEntries.keys()):
                    tEntry = tEntries[eachtag]
                    row.append(tEntry[int(messageNumber - 1)])
                table.append(tuple(row))
        table.printTable()

if __name__ == "__main__":
        main()
