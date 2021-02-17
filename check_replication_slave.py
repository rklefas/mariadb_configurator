# Module Imports
from tabulate import tabulate
import configparser
import configurator


config = configparser.ConfigParser()
config.read("config.ini")

# Get Cursor
cur = configurator.get_database_connection( config['SLAVE'] ).cursor()


ideals = {
    "binlog_format": "MIXED",
    "log_slave_updates": "OFF",
    "server_id": "20",
    "skip_networking": "OFF"
}

incorrect = 0


for name in ideals:

    cur.execute("SHOW VARIABLES LIKE '%s'" % (name) )
    myresult = cur.fetchall()

    if len(myresult) == 0:
        print(name, "was not found.")
        continue

    myresult[0] = myresult[0] + (ideals[name], )

    if ideals[name] == myresult[0][1]:
        continue
    else:
        incorrect += 1

    print(tabulate(myresult, headers=['Name', 'Value', 'Expected'], tablefmt='psql'))



if incorrect == 0:
    configurator.control_output(configurator.query_dump_vertical(cur, "SHOW SLAVE STATUS"))
    configurator.control_output(configurator.query_dump(cur, "SHOW RELAYLOG EVENTS LIMIT 20"))
