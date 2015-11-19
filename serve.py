#!/usr/bin/env python
import subprocess, socket, re, os, shutil, sys, SimpleHTTPServer, SocketServer
defaultDir = "messages" if os.path.exists("messages") else os.getcwd()
rootdir = sys.argv[2] if len(sys.argv) > 2 and os.path.exists(sys.argv[2]) else defaultDir
rootdir = os.path.abspath(rootdir)
port = sys.argv[3] if len(sys.argv) > 3 else 9899
linkFormat = "http://%s:%s/%s"
def usage():
        print "ft serve [path] [port]"
        print "     Eg.: ft serve"
        print "     Eg.: ft serve templates"
        print "     Eg.: ft serve ~ 9999"
class MyRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        return SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
def main():
        Handler = MyRequestHandler
        try:
                server = SocketServer.ThreadingTCPServer(('', int(port)), Handler)
                SocketServer.ThreadingTCPServer.allow_reuse_address = True
                print linkFormat % (socket.getfqdn(), port, "")
                print rootdir
                os.chdir(rootdir)
                print "-" * 120
                for f in sorted(os.listdir(rootdir), key=os.path.getctime, reverse=True):
                        print linkFormat % (socket.getfqdn(), port, f)
                server.serve_forever()
        except KeyboardInterrupt:
                print "Shutting down"
                server.shutdown()
                server.socket.close()
if __name__ == "__main__":
        main()
