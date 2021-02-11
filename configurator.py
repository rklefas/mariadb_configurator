from tabulate import tabulate


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




def query_dump(cursor, query):

    cursor.execute(query)
    headersAll = []

    for column in cursor.description:
        headersAll.append(column[0])

    return "    " + query + "\n" + tabulate(cursor.fetchall(), headers = headersAll, tablefmt='psql')


def query_dump_vertical(cursor, query):

    cursor.execute(query)
    result = cursor.fetchall()

    headersAll = []

    for column in cursor.description:
        headersAll.append(column[0])

    colNum = 0 
    lineAll = []

    for column in result[0]:
        lineAll.append( (colNum + 1, headersAll[colNum], column, ) )
        colNum += 1
		
    displayHeaders = ["Column #", "Column Name", "Row #1 Value"]

    return "    " + query + "\n" + tabulate(lineAll, headers = displayHeaders, tablefmt='psql')

