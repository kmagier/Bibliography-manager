import os

DB_TYPE = 'postgresql'
DB_CONNECTOR = 'psycopg2'
USERNAME = 'karol'
PASSWORD = '123456'
PORT = '5432'
HOST = 'postgresdb' + ':' + PORT
DB_NAME = 'database'

DB_URI = DB_TYPE + "+" + DB_CONNECTOR +'://' + USERNAME +':' + PASSWORD + "@" + HOST + '/' + DB_NAME