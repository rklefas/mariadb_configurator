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

cur.execute("""SHOW VARIABLES WHERE variable_name LIKE '%repl%' 
OR variable_name LIKE 'wsrep%' 
OR variable_name LIKE '%binlog%' 
OR variable_name LIKE 'log_bin_%'
OR variable_name LIKE 'gtid_%'
""")
myresult = cur.fetchall()

print(tabulate(myresult, headers=['Name', 'Value'], tablefmt='psql'))
