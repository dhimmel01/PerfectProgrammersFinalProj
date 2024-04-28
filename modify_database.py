import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('spotify_new.db')
c = conn.cursor()

# Retrieve data from the artist_info table
c.execute("SELECT * FROM artist_info")
artist_info_data = c.fetchall()

# Retrieve data from the artist_meta table
c.execute("SELECT * FROM artist_meta")
artist_meta_data = c.fetchall()

# Close the database connection
conn.close()

# Print the data from the artist_info table in a readable format
print("Table: artist_info")
for row in artist_info_data:
    print(row)

# Print the data from the artist_meta table in a readable format
print("\nTable: artist_meta")
for row in artist_meta_data:
    print(row)

