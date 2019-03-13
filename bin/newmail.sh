#!/usr/local/bin/bash

NewMail(){
    NEWMAIL=$(mailx &)
    UNREAD=$(echo $NEWMAIL |grep -o 'messages.*new' | cut -f2 -d" ")
}
NewMail # call NewMail function
UNREAD=${UNREAD/>/}

if [ -n "$UNREAD" ]; then
    echo "`whoami` you have $UNREAD new mail(s) "
fi
