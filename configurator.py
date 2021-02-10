from tabulate import tabulate


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
        lineAll.append( (colNum, headersAll[colNum], column, ) )
        colNum += 1
		
    displayHeaders = ["Column #", "Column Name", "Row #1 Value"]

    return "    " + query + "\n" + tabulate(lineAll, headers = displayHeaders, tablefmt='psql')

