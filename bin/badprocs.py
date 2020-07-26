#!/usr/local/bin/python3

# Checks the process list for anything that could be potentially worrisome.
# If something is found, emails the admins@tilde.institute account.
# gbmor <ben@gbmor.dev>

from shlex import quote
import subprocess
import time


def getBadProcs(procsList):
    procsFound = []
    procsRunning = list(
        subprocess.check_output("/bin/ps aux", stderr=subprocess.STDOUT, shell=True)
        .decode()
        .split("\n")
    )

    for proc in procsRunning:
        for badproc in procsList:
            if badproc in proc.lower():
                procsFound.append("Found {0} :: {1}".format(badproc, proc))

    return procsFound


def mailAdmins(procsFound):
    msg = "WARNING: Check the following processes manually\n\n"
    msg += "\n".join(procsFound)
    msg += "\noutput from badprocs.py\n"

    cmd = "echo {0} | mail -s 'WARNING: Found potential bad processes' admins@tilde.institute".format(
        quote(msg)
    )

    subprocess.run(cmd, shell=True)


if __name__ == "__main__":
    procsList = [
        "crowdserv",  # sauerbraten
        "eggdrop",
        "miner",  # lots of btc miners have this in the name
        "nmap",
        "regen2",  # sauerbraten
        "sauer",  # sauerbraten
        "torrent",
        "transmission",
        "tshark",
        "xmr",  # lots of monero miners have this in the name
    ]

    procsFound = getBadProcs(procsList)

    if len(procsFound) > 0:
        mailAdmins(procsFound)
