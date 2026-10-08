import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    port=3306,
    database="cadastro_db",
    user="cadastro_user",
    password="cadastro123"
)

print(conn)