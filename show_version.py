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

cur.execute("SHOW VARIABLES LIKE '%version%'")
myresult = cur.fetchall()

print(tabulate(myresult, headers=['Name', 'Value'], tablefmt='psql'))
