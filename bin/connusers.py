#!/usr/local/bin/python3 -I

from sys import exit
import subprocess

def checkconns():
    try:
        conntable = open("/var/www/htdocs/table.connusers", "w")
    except:
        print("Can't access connected user table. Who are you?")
        exit(0)

    connusers = list(set(subprocess.check_output("/usr/bin/who -q; exit 0", stderr=subprocess.STDOUT,shell=True).decode().splitlines()[0].split()))
    conntable.write("<ul>\n")
    for conn in connusers:
        conntable.write("<li><a href=\"https://"+ conn +".tilde.institute\">"+ conn +"</a></li>\n")

    conntable.write("</ul>\n")

if __name__ == '__main__':
    checkconns()
