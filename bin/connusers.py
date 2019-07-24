#!/usr/local/bin/python3 -I

# Lists currently connected users for https://tilde.institute/stats
# ben@gbmor.dev

from sys import exit
import subprocess

def checkconns():
    try:
        conntable = open("/var/www/htdocs/table.connusers", "w")
    except:
        print("Can't access connected user table. Who are you?")
        exit(0)

    connusers = list(set(subprocess.check_output("/usr/local/bin/showwhoison | sed -n '1!p'; exit 0", stderr=subprocess.STDOUT,shell=True).decode().split("\n")))
    conntable.write("<ul>\n")

    seen = set()
    for conns in connusers:
        split = conns.split(' ')
        for conn in split:
            if conn != "" and conn != " " and conn != "root" and conn not in seen:
                seen.add(conn)
                conntable.write("<li><a href=\"https://"+ conn +".tilde.institute\">"+ conn +"</a></li>\n")


    conntable.write("</ul>\n")

if __name__ == '__main__':
    checkconns()
