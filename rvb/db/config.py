import os

DATABASE = {
	'drivername': 'postgresql+psycopg2',
	'database': 'rvb',
	'username': os.getenv('DB_USERNAME',None),
	'password': os.getenv('DB_PASSWORD',None),
	'port':  os.getenv('DB_PORT',None),
	'host':  os.getenv('DB_HOST',None)
}
