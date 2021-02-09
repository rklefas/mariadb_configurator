# Module Imports
import mariadb
import sys
from tabulate import tabulate
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

server = input("Read (M)ASTER or (S)LAVE server? ")
server = server.upper()

if server == "M":
    server = "MASTER"
elif server == "S":
    server = "SLAVE"


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
        print("1) Ensure the connection credentials in config.ini are correct. ")
    print("")
    sys.exit(1)

# Get Cursor
cur = conn.cursor()

cur.execute("SHOW VARIABLES LIKE '%version%'")
myresult = cur.fetchall()

print(tabulate(myresult, headers=['Name', 'Value'], tablefmt='psql'))
