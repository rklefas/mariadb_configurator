# Module Imports
import mariadb
import sys
from tabulate import tabulate
import configparser




def query_dump(cursor, query):
    cursor.execute(query)

    headersAll = []

    for column in cursor.description:
        column_name = column[0]
        headersAll.append(column_name)

    return "    " + query + "\n" + tabulate(cursor.fetchall(), headers = headersAll, tablefmt='psql')


def query_dump_vertical(cursor, query):
    cursor.execute(query)
    result = cursor.fetchall()

    print(cursor.description)
#    print(mariadb.fieldinfo())

#    print(dir(cursor))

    for column in result[0]:
        print(column)




config = configparser.ConfigParser()
config.read("config.ini")


# Connect to MariaDB Platform
try:
    conn = mariadb.connect(
        user=config['SLAVE']['user'],
        password=config['SLAVE']['password'],
        host=config['SLAVE']['host'],
        port=int(config['SLAVE']['port'])
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
cur = conn.cursor()


ideals = {
    "log_bin": "ON",
    "binlog_do_db": "[database names]",
    "binlog_format": "MIXED",
    "log_slave_updates": "OFF",
    "version_comment": "Ubuntu 20.04",
    "server_id": "20",
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


print(correct, "settings are correctly configured. ")


# if input("Do you want to start this as master?") == 'y':
#    cur.execute("START MASTER")

print(query_dump_vertical(cur, "SHOW SLAVE STATUS"))
print(query_dump(cur, "SHOW PROCESSLIST"))
