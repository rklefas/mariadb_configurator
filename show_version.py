# Module Imports
import mariadb
import sys
from tabulate import tabulate
import configparser
import configurator

config = configparser.ConfigParser()
config.read("config.ini")

server = configurator.get_server_type()


# Connect to MariaDB Platform
try:
    conn = mariadb.connect(
        user=config[server]['user'],
        password=config[server]['password'],
        host=config[server]['host'],
        port=int(config[server]['port'])
    )
except mariadb.Error as e:
    print(f"{e}")
    print("")

    if str(e).startswith("Can't connect to MySQL server"):
        print("- Open config file, probably at:  /etc/mysql/mariadb.conf.d/50-server.cnf")
        print("- Ensure the server is accessiible with the bind-address config option.")
        print("- Restart server:  /etc/init.d/mysql restart")
    elif str(e).startswith("Access denied for user"):
        print("- Ensure the connection credentials in config.ini are correct. ")
    print("")
    sys.exit(1)


# Get Cursor
cur = conn.cursor()

print(configurator.query_dump(cur, "SHOW GRANTS"))

print(configurator.query_dump(cur, "SHOW VARIABLES LIKE '%version%'"))
