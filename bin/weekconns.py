#!/usr/local/bin/python3 -I

from sys import exit
import subprocess

def weekconns():
    try:
        conntable = open("/var/www/htdocs/table.weekconns", "w")
    except:
        print("Can't access connected user table. Who are you?")
        exit(0)

    weekconns = list(set(subprocess.check_output("last | grep tty | awk '{print $1}'; exit 0", stderr=subprocess.STDOUT,shell=True).decode().strip()))
    conntable.write(str(len(weekconns)))
    conntable.close()

if __name__ == '__main__':
    weekconns()
