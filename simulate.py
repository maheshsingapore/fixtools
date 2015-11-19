#!/usr/bin/env python
import subprocess, socket, re, os, shutil, sys, random, string
def usage():
    print "ft simulate <template>"
    print "     E.g.: ft simulate templates/Execution.template"
template = sys.argv[2] if len(sys.argv) > 2 and os.path.exists(sys.argv[2]) else usage()
varToReplaceRegex = "(\{(.*?)=(.*?)\})"
bodyRegex = "(.*?)9=(\d+)\x01(.*?)10\=000(.*)"
variables = dict()
def calculateBodyLength():
    return -1
def getKey(key):
    return variables[key]
def randomString(length):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))
def main():
    fh = open(template, "r")
    for line in fh.readlines():
        p = re.compile(varToReplaceRegex)
        iterator = p.finditer(line)
        substitution = line
        for i in iterator:
            searchString = i.group(1)
            evaluation = eval(i.group(3))
            variables[i.group(2)] = evaluation
            substitution = substitution.replace(searchString, evaluation, 1)
        body = re.search(bodyRegex, substitution)
        substitution = substitution.replace(body.group(2), str(len(body.group(3))))
        print substitution
    fh.close()
if __name__ == "__main__":
        main()
