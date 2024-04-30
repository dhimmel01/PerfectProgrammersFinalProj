import sqlite3

def export_database_data(db_file, output_file):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Get the list of tables in the database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    # Open the output file for writing
    with open(output_file, 'w') as f:
        # Iterate over each table
        for table in tables:
            table_name = table[0]
            f.write(f"Table: {table_name}\n")

            # Execute a SQL query to select all data from the table
            cursor.execute(f"SELECT * FROM {table_name};")
            rows = cursor.fetchall()

            # Write the table data to the file
            for row in rows:
                f.write(str(row) + '\n')
            f.write('\n')

    # Close the connection
    conn.close()

# Specify the SQLite database file and output file
db_file = 'spotify.db'
output_file = 'database_data.txt'

# Export database data to the output file
export_database_data(db_file, output_file)
