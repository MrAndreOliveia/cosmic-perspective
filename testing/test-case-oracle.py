"""
		Title: connect_db.py        					 										 
		Description: Connection to oracle database
		Creation Date: 01-Jul 2018		
		Last Update: 01-Jul 2018																	 
		Author: André Oliveira																	 
"""

# Import Oracle library.
import cx_Oracle


try:
  # Create a connection.
  db = cx_Oracle.connect('pythonhol/welcome@127.0.0.1/orcl')

  # Print a message.
  print "Connected to the Oracle " + db.version + " database."

  # Create a cursor.
  cur = db.cursor()

  # Execute a query.
  cur.execute("SELECT 'Hello world!' FROM dual")
 
  # Read the contents of the cursor.
  for row in cur:
    print (row[0])


except cx_Oracle.DatabaseError, e:
  error, = e.args
  print >> sys.stderr, "Oracle-Error-Code:", error.code
  print >> sys.stderr, "Oracle-Error-Message:", error.message

finally:
  # Close cursor and connection. 
  cur.close()
  db.close() 
