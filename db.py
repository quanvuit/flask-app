import psycopg2

connection = psycopg2.connect(user="postgres",
                                  password="admin",
                                  host="localhost",
                                  port="5432",
                                  database="qly_sv")
# Create a cursor to perform database operations
cursor = connection.cursor()