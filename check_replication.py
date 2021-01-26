# Module Imports
import mariadb
import sys
from tabulate import tabulate
import configparser

config = configparser.ConfigParser()
config.read("config.ini")


# Connect to MariaDB Platform
try:
    conn = mariadb.connect(
        user=config['LOGIN']['user'],
        password=config['LOGIN']['password'],
        host=config['LOGIN']['host'],
        port=3306
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
cur = conn.cursor()


ideals = {
    "log_bin": "ON",
    "version_comment": "Ubuntu 20.04",
    "server_id": "1"
}

correct = 0


for name in ideals:

    cur.execute("SHOW VARIABLES LIKE '%s'" % (name) )
    myresult = cur.fetchall()
    myresult[0] = myresult[0] + (ideals[name], )

    if ideals[name] == myresult[0][1]:
        correct += 1
        continue

    print(tabulate(myresult, headers=['Name', 'Value', 'Expected'], tablefmt='psql'))


print(correct, "settings are correctly configured. ")
