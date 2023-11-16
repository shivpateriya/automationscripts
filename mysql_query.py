import mysql.connector
from datetime import date

# MySQL connection configuration
db_config = {
    'host': 'your_mysql_host',
    'user': 'your_username',
    'password': 'your_password',
    'database': 'MDL_DB'
}

# Establish a connection to the database
connection = mysql.connector.connect(**db_config)

# Create a cursor to execute SQL queries
cursor = connection.cursor()

# Define the SQL query
sql_query = "SELECT COUNT(*) FROM TBL_GAP_IEE WHERE DATE(created_at) = CURDATE()"

# Execute the query
cursor.execute(sql_query)

# Fetch the result
result = cursor.fetchone()

# Close the cursor and connection
cursor.close()
connection.close()

# Extract the count from the result
count = result[0]

# Check the count and send alert if it's 0
if count == 0:
    print("Send alert: No records found.")
else:
    print(f"Found {count} records.")
