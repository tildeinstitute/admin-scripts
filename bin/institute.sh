#!/usr/local/bin/bash
####################################################
#
# This is the bash script used to automagically check for new submitted users
# and add them to the Tilde Institute system.
# It is intended to be run as a cron job every few minutes, or however long.
#
####################################################
#
#    Copyright (c) 2018 Ben Morrison, also known as "ahriman". All rights reserved.
#    Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
#     1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
#     2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
#     3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
#     THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
####################################################

#	First we check if new users have been submitted by the PHP script on the site
#	If no users have been submitted, do nothing.
#	If they have been submitted, begin by moving the newusers.csv file to a new location
if [[ -f /var/www/htdocs/newusers.csv ]] ; then
	mv /var/www/htdocs/newusers.csv /var/www/newusers.csv
	touch /var/www/htdocs/newusers.csv
    chmod 666 /var/www/htdocs/newusers.csv
#	assign the file to a variable to make it easier to work with
	newusers="/var/www/newusers.csv"
#	now read the file line by line and chop it up by field
	while IFS=: read -r f1
	do
#	Call the makeuser script I borrowed from Ben Harris of tilde.team
#	and modified for my own use
        echo $f1 >> /home/ahriman/users-to-add
#		exec '/home/ahriman/bin/makeuser $f1'
	done <"$newusers"

#	append list of new users created this run for later review
#	then delete the csv file
	cat /var/www/newusers.csv >> /var/www/logs/newusers.log
	rm -f /var/www/newusers.csv

#	reload the httpd config
#	httpdpid=`pgrep httpd | awk 'NR==1{print $1}'`
#	kill -HUP $httpdpid
fi
