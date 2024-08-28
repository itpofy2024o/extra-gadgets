import pandas as pd
import sys
import mysql.connector
from mysql.connector import Error

connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database=""
)

# cursor = connection.cursor()

query = "SELECT * FROM "
df = pd.read_sql(query, connection)

# Replace 'output_file.csv' with the desired name of your output file
df.to_csv(sys.argv[1], index=False)

# cursor.close()
connection.close()
