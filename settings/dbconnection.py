from mysql.connector import connection
dict = {
  'user': 'root',
  'host': 'localhost',
  'database': 'pyapi',
  'password': 'cano'
}
def db():
	return connection.MySQLConnection(**dict)
