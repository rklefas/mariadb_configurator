from tabulate import tabulate
import textwrap
import mariadb
import sys


def get_database_connection(configs):
    
	# Connect to MariaDB Platform
    try:
        conn = mariadb.connect(
            user=configs['user'],
            password=configs['password'],
            host=configs['host'],
            port=int(configs['port'])
        )
    except mariadb.Error as e:
        print("Role: " + configs['role'])
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)


    return conn


def get_server_type():

    server = input("Connect to (M)ASTER or (S)LAVE server? ")
    server = server.upper()

    if server == "M" or server == "MASTER":
        server = "MASTER"
    elif server == "S" or server == "SLAVE":
        server = "SLAVE"
    else:
        server = get_server_type()

    return server





def control_output(output, outlines = 30):

    parts = output.split("\n")
    indexItem = 0
    chunks = 0
	
    for lineq in parts:

        print(lineq)
        indexItem += 1

        if indexItem >= outlines:
		
            if chunks >= 30:
                chunks = 0
		
            chunks += 1
            indexItem = 0
            input(">" * chunks)
			
    if chunks > 0:
        input((">" * chunks) + "=")

	

def query_execute(cursor, query):

    cursor.execute(query)
    output = "    " + query
    return output


def query_dump(cursor, query):

    cursor.execute(query)
    headersAll = []

    try:
        for column in cursor.description:
            headersAll.append(column[0])
    except TypeError:
        print ('No headers found')	
		
    output = "    " + query + "\n" + tabulate(cursor.fetchall(), headers = headersAll, tablefmt='psql')
    return output
	


def query_dump_vertical(cursor, query):

    cursor.execute(query)
    result = cursor.fetchall()

    headersAll = []

    try:
        for column in cursor.description:
            headersAll.append(column[0])
    except TypeError:
        print ('No headers found')	

    colNum = 0 
    lineAll = []

    for column in result[0]:
        lineAll.append( (colNum + 1, headersAll[colNum], textwrap.fill(str(column), 60), ) )
        colNum += 1
		
    displayHeaders = ["Column #", "Column Name", "Row #1 Value"]

    return "    " + query + "\n" + tabulate(lineAll, headers = displayHeaders, tablefmt='psql')

