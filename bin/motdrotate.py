#!/usr/local/bin/python3

import sys
import random

##############################################
## Uses a skeleton motd plus a random quote ##
## to produce a motd with a nifty quote.    ##
##------------------------------------------##
## <gbmor> ben@gbmor.dev                    ##
##############################################

def pullfile(filename):
    with open(filename, 'r') as filesrc:
        filedata = filesrc.read()
        return filedata

def rotatemotd(motd):
    motdmsgs = ['Abandon hope all ye who enter here',
            'We are such stuff as dreams are made on, and our little life is rounded with a sleep. - Prospero, The Tempest',
            '"New technology is not good or evil in and of itself. It\'s all about how people choose to use it."',
            '"If we lose love and self-respect for each other, this is how we finally die." - Maya Angelou',
            '"We live in a society exquisitely dependent on science and technology, in which hardly anyone knows anything about science and technology." - Carl Sagan',
            '"Any sufficiently advanced technology is indistinguishable from magic." - Arthur C Clarke',
            '"The biggest mistake I made was believing if I cast a beautiful net, I\'d catch only beautiful things."',
            '"A punk rock song won\'t ever change the world, but I can tell you about a couple that changed me." - Pat the Bunny',
            '"What we know is a drop, what we don\'t know is an ocean." - Isaac Newton']
    motdchoice = random.choice(motdmsgs)
    try:
        with open("/etc/motd", "w") as etcmotd:
            etcmotd.write(motd)
            etcmotd.write(motdchoice)
            etcmotd.write("\n")
            etcmotd.write("\n")
    except:
        print("Unable to open /etc/motd for writing. Who are you?")
        sys.exit(0)

if __name__=="__main__":
    motdskel = pullfile("/admin/misc/motd.txt")
    rotatemotd(motdskel)

