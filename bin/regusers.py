#!/usr/local/bin/python3

import os
import sys

def get_regusers(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]

if __name__ == "__main__":

    try:
        usertable = open("/var/www/htdocs/table.regusers", "w")
    except:
        print("Can't access registered user table. Are you root?")
        sys.exit(0)

    regusers = get_regusers("/home")
    usertable.write("<ul>\n")
    for user in sorted(regusers):
        if user != ".git" and user != "ahriman" and user != "uucp" and user != "admins":
            usertable.write("<li><a href=\"https://"+ user +".tilde.institute\">"+ user +"</a></li>\n")
    usertable.write("</ul>\n")
