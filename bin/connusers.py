#!/usr/local/bin/python3 -I

# Lists currently connected users for https://tilde.institute/stats
# gbmor <ben@gbmor.dev>

# 'ps' truncates usernames at 8 characters (called by 'showwhoison' to find mosh users)
# so I'm matching the potentially-partial username to a home directory to retrieve
# the full username.

from sys import exit
import subprocess

def checkconns():
    try:
        conntable = open("/var/www/htdocs/table.connusers", "w")
    except:
        print("Can't access connected user table. Who are you?")
        exit(0)

    connusers = sorted(list(subprocess.check_output("/usr/local/bin/showwhoison | sed -n '1!p'; exit 0", stderr=subprocess.STDOUT,shell=True).decode().split("\n")))
    conntable.write("<ul>\n")

    lastusers = list(subprocess.check_output("/bin/ls /home", stderr=subprocess.STDOUT,shell=True).decode().split("\n"))

    seen = set()
    for conns in connusers:
        split = conns.split(' ')
        for conn in split:
            if conn != "" and conn != " " and conn != "root" and conn not in seen:
                seen.add(conn)
                match = ''.join([s for s in lastusers if conn in s])
                conntable.write("<li><a href=\"https://"+ match +".tilde.institute\">"+ match +"</a></li>\n")


    conntable.write("</ul>\n")

if __name__ == '__main__':
    checkconns()
