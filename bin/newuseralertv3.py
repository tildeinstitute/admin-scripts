#!/usr/local/bin/python3
#
# kneezle@tilde.institute

import os
import argparse
import http.client
import sys
import time

aboutme = """
# New User Monitor
# Created for tilde.institute and Ahriman by Kneezle
# BSD Rocks!

# Version 3.0
# This version supports hiding the gotify keys by passing them in via the CLI
# or using the gotifynotify ENV variable to hide from a PS lookup
"""

defaulttitle = "Alert: New Users"

defaultnewuserpath = "/admin/newusers.dat"

runcmdtemplate = """curl -X POST "https://gotify.tildeverse.org/message?token={}" -F "title=Alert: New Users" -F "message={}" -F "priority=5" """

ap = argparse.ArgumentParser()
ap.add_argument('--newuserpath', default=defaultnewuserpath,
                    help='sets the path for the new user txt file')

ap.add_argument('--title', default=defaulttitle,
                    help='sets the title')

ap.add_argument('--usecurl', default=False,
                    help='use curl or build in sockets')

ap.add_argument("-a", "--about", dest='about', action='store_true', help="about me")

ap.add_argument("--daemonize", dest='daemonize', action='store_true', help="run in a loop vs only run once")

ap.add_argument('--gotifykeys', nargs='+', default=[],help="the gotify keys of the people to send to")

ap.add_argument('--gotifykeypath', default=None,
                    help='Load CSV gotify keys from file')

ap.add_argument('--loopinterval', default=60,
                    help='sets loop interval (seconds) in daemon mode')

args = vars(ap.parse_args())

if args['about']:
    print(aboutme)
    exit()


title = args['title']
newuserpath = args['newuserpath']
usecurl = args['usecurl']
gotifytokens = args['gotifykeys']
daemonize = args['daemonize']
gotifykeypath = args['gotifykeypath']
loopinterval = int(args['loopinterval'])


if gotifykeypath is not None:
    with open(gotifykeypath) as f:
        first_line = f.readline()
        gotifytokens = first_line.rstrip("\n").split(',')


if len(gotifytokens) < 1:
    #we didn't get passed a token. lets try to get from ENV before giving up.
    try:
        envtokens = os.environ["gotifynotify"]
    except KeyError:
        print("You didn't provide a gotify token!")
        sys.exit(1)
    gotifytokens = envtokens.split(',')
    if len(gotifytokens) < 1:
        print("You didn't provide a gotify token!")
        sys.exit(1)


boilerplate = """New pending user found!

Username: {}
Email: {}

"""

#we have no do while in python so this will have to do
firstloop = True

previouslinecount = 0

while firstloop or daemonize:
    if not firstloop:
        time.sleep(loopinterval) #so we don't hammer the CPU in daemon mode

    with open(newuserpath) as fp:
        line = fp.readline()
        linecount = 1
        numnonblanklines = 0
        push_notification = ""
        while line:
            if line.strip() != "": #not a blank line
                numnonblanklines = numnonblanklines + 1
                print("New User Found: {} : {}".format(linecount, line.strip()))

                #lets extract the useful information
                x = line.split(" ")
                sshkey = ""
                itemno = 0
                for item in x:
                    if itemno > 1:
                        sshkey = sshkey + " " + item
                    itemno = itemno + 1
                sshkey = sshkey.replace('"', "")

                #Lets build the single push notification with all the details

                push_notification = push_notification + boilerplate.format(x[0], x[1])
            linecount = linecount + 1
            line = fp.readline()

    #notify is when handled
    if previouslinecount > numnonblanklines:
        for key in gotifytokens:
            if not usecurl:
                conn = http.client.HTTPSConnection("gotify.tildeverse.org")
                payload = """title={}&message={}&priority=5""".format("New users handled", "Someone on the admin team got it.")
                headers = {'content-type': "application/x-www-form-urlencoded"}
                conn.request("POST", "/message?token={}".format(key), payload, headers)
                res = conn.getresponse()
                data = res.read()
                print(data.decode("utf-8"))
            else:
                torun = runcmdtemplate.format(key, push_notification)
                os.system(torun)

    if numnonblanklines > 0 and numnonblanklines > previouslinecount:
        if numnonblanklines > 4:
            push_notification = "You have " + str(numnonblanklines) + " pending new users!"
        for key in gotifytokens:
            if not usecurl:
                conn = http.client.HTTPSConnection("gotify.tildeverse.org")
                payload = """title={}&message={}&priority=5""".format(title, push_notification)
                headers = {'content-type': "application/x-www-form-urlencoded"}
                conn.request("POST", "/message?token={}".format(key), payload, headers)
                res = conn.getresponse()
                data = res.read()
                print(data.decode("utf-8"))
            else:
                torun = runcmdtemplate.format(key, push_notification)
                os.system(torun)
    else:
        print("No new users pending")
    previouslinecount = numnonblanklines
    firstloop = False #no longer the first loop
    print("prev: " + str(previouslinecount))
