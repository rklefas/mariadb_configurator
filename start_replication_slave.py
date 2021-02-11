# Module Imports
import mariadb
import sys
import configparser



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

cur.execute("STOP SLAVE")

params = (config['MASTER']['host'], config['MASTER']['user'], config['MASTER']['password'], int(config['MASTER']['port']) )
masterQuery = "CHANGE MASTER TO MASTER_HOST = '%s' , MASTER_USER = '%s' , MASTER_PASSWORD = '%s' , MASTER_PORT = %d" % params

print(masterQuery)

cur.execute(masterQuery)
cur.execute("START SLAVE")

