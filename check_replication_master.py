# Module Imports
import mariadb
import sys
from tabulate import tabulate
import configparser
import configurator



config = configparser.ConfigParser()
config.read("config.ini")


# Connect to MariaDB Platform
try:
    conn = mariadb.connect(
        user=config['MASTER']['user'],
        password=config['MASTER']['password'],
        host=config['MASTER']['host'],
        port=int(config['MASTER']['port'])
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
cur = conn.cursor()


ideals = {
    "log_bin": "ON",
    "binlog_do_db": "[database names]",
#    "binlog_format": "ROW",
#    "log_slave_updates": "ON",
#    "version_comment": "Ubuntu 20.04",
    "server_id": "10",
    "skip_networking": "OFF"
}

correct = 0


for name in ideals:

    cur.execute("SHOW VARIABLES LIKE '%s'" % (name) )
    myresult = cur.fetchall()

    if len(myresult) == 0:
        print(name, "was not found.")
        continue

    myresult[0] = myresult[0] + (ideals[name], )

    if ideals[name] == myresult[0][1]:
        correct += 1
        continue

    print(tabulate(myresult, headers=['Name', 'Value', 'Expected'], tablefmt='psql'))


# print(correct, "settings are correctly configured. ")


# if input("Do you want to start this as master?") == 'y':
#    cur.execute("START MASTER")

print(configurator.query_dump(cur, "SHOW MASTER STATUS"))
print(configurator.query_dump(cur, "SHOW BINARY LOGS"))
print(configurator.query_dump(cur, "SHOW BINLOG EVENTS LIMIT 20"))
print(configurator.query_dump(cur, "SHOW SLAVE HOSTS"))

