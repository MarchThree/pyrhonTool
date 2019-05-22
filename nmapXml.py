#!/usr/bin/env python
#
# nmapdb - Parse nmap's XML output files and insert them into an SQLite database
# Copyright (c) 2012 Patroklos Argyroudis <argp at domain census-labs.com>

import sys
import os
import getopt
import xml.dom.minidom

VERSION = "1.2"

true = 1
false = 0
vflag = false


def main(argv, environ):
    fname = argv[1]
    f=open(argv[2],'w')
    try:
        doc = xml.dom.minidom.parse(fname)
    except IOError:
        print("%s: error: file \"%s\" doesn't exist\n" % (argv[0], fname))
    except xml.parsers.expat.ExpatError:
        print("%s: error: file \"%s\" doesn't seem to be XML\n" % (argv[0], fname))
    for host in doc.getElementsByTagName("host"):
        try:
            address = host.getElementsByTagName("address")[0]
            ip = address.getAttribute("addr")
        except:
            pass
        try:
            ports = host.getElementsByTagName("ports")[0]
            ports = ports.getElementsByTagName("port")
        except:
            print("%s: host %s has no open ports\n" % (argv[0], ip))
            continue
        for port in ports:
            portItem = port.getAttribute("portid")
            if portItem=="80" or portItem=="443" or portItem=="8080":
                result=ip + ":" + portItem
                f.write(result+"\n")
                print(result)


if __name__ == "__main__":
    main(sys.argv, os.environ)
    sys.exit(0)

# EOF
