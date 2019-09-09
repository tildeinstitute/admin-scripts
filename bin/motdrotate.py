#!/usr/local/bin/python3

import sys
import random

##############################################
## Uses a skeleton motd plus a random quote ##
## to produce a motd with a nifty quote.    ##
##------------------------------------------##
## Created by ahriman - ben@gbmor.dev       ##
## --> BSD 3-clause license applies         ##
##############################################

def pullfile(filename):
    with open(filename, 'r') as filesrc:
        filedata = filesrc.read()
        return filedata

def rotatemotd(motd):
    motdmsgs = ['Abandon hope all ye who enter here',
            'We are such stuff as dreams are made on, and our little life is rounded with a sleep. - Prospero, The Tempest',
            'To err is human. To really foul up you need a computer.',
            '"In matters of life and death there is no cheating; there is only living and dying"',
            '"New technology is not good or evil in and of itself. It\'s all about how people choose to use it."',
            '"Technology is, of course, a double-edged sword. Fire can cook our food but also burn us."',
            '"If we lose love and self-respect for each other, this is how we finally die."',
            '"We live in a society exquisitely dependent on science and technology, in which hardly anyone knows anything about science and technology."',
            '"Any sufficiently advanced technology is indistinguishable from magic."']
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

