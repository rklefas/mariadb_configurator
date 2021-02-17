# Module Imports
import configurator
import configparser



config = configparser.ConfigParser()
config.read("config.ini")



# Get Cursor
mcur = configurator.get_database_connection( config['MASTER'] ).cursor()
scur = configurator.get_database_connection( config['SLAVE'] ).cursor()


# reset master can be used when there are no slaves

# cur.execute("PURGE BINARY LOGS")




print(configurator.query_execute(scur, "STOP SLAVE"))

print(configurator.query_execute(scur, "RESET SLAVE ALL"))


params = (config['MASTER']['host'], config['MASTER']['user'], config['MASTER']['password'], int(config['MASTER']['port']) )
masterQuery = "CHANGE MASTER TO MASTER_HOST = '%s' , MASTER_USER = '%s' , MASTER_PASSWORD = '%s' , MASTER_PORT = %d" % params


print(configurator.query_execute(scur, masterQuery))

print(configurator.query_execute(mcur, "RESET MASTER"))

print(configurator.query_execute(scur, "START SLAVE"))

