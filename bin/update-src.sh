#!/bin/sh
set -e

# literally just keeps the source tree up to date, per user request.
# one copy of stable, one copy of current.
# call this with cron.
# ~gbmor

cd /usr/src
printf '%s\n' 'Updating 7.1-STABLE ...'
nice -n 20 cvs -q up -Pd -rOPENBSD_7_1

cd /usr/src-current
printf '%s\n' 'Updating CURRENT ...'
nice -n 20 cvs -q up -Pd -A

