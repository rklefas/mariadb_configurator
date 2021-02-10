# Module Imports
import mariadb
import sys
from tabulate import tabulate
import configparser




def query_dump(cursor, query):
    cursor.execute(query)
    return "    " + query + "\n" + tabulate(cursor.fetchall(), tablefmt='psql')


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
    "binlog_format": "ROW",
    "log_slave_updates": "ON",
    "version_comment": "Ubuntu 20.04",
    "server_id": "[UNIQUE FOR EACH SERVER.  IP?]",
    "skip_networking": "OFF"
}

# cur.execute("INSERT INTO sample VALUES (%d, %s, %s)",
#    (2, 'A "string" with double quotes.', '2020-01-02'))

# print(config['SLAVE']['host'])
# sys.exit()

params = (config['SLAVE']['host'], config['SLAVE']['user'], config['SLAVE']['password'], int(config['SLAVE']['port']) )

# params = (config['SLAVE']['host'])

print(params)

cur.execute("STOP SLAVE")


masterQuery = "CHANGE MASTER TO MASTER_HOST = '%s' , MASTER_USER = '%s' , MASTER_PASSWORD = '%s' , MASTER_PORT = %d" % params
# masterQuery = "CHANGE MASTER TO MASTER_HOST = '%s'" % params

print(masterQuery)

cur.execute(masterQuery)
cur.execute("START SLAVE")

# print(query_dump(cur, "SHOW PROCESSLIST"))
