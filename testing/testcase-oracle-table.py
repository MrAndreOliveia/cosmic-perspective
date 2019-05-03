# Connects to an Oracle database
# Queries the Database and prints the first two columns of a table
# Replace username, password, server, port and service
# Replace TABLENAME


import cx_Oracle

conn_str = u'username/password@server:port/service'
conn = cx_Oracle.connect(conn_str)
c = conn.cursor()


SQL="SELECT * FROM TABLENAME"
c.execute(SQL)


for row in c:
    print row[0], "-", row[1]
c.close()
conn.close()


