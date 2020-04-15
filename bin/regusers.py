#!/usr/local/bin/python3

# Lists all the currently registered users extant on the system
# for the stats page at https://tilde.institute/stats
# ben@gbmor.dev

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
        is_system = user.startswith("_")
        is_hidden_dir = user.startswith(".")
        if user != "lost+found" and user != "uucp" and user != "admins" and is_system == False and is_hidden_dir == False:
            usertable.write("<li><a href=\"https://"+ user +".tilde.institute\">"+ user +"</a></li>\n")
    usertable.write("</ul>\n")
