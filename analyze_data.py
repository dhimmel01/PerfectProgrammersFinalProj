import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

def visualize_album_data(db_file):
    conn = sqlite3.connect(db_file)
    albums_df = pd.read_sql_query("SELECT * FROM albums", conn)

    # Convert release_date column to datetime with flexible parsing
    albums_df['release_date'] = pd.to_datetime(albums_df['release_date'], errors='coerce')

    # Drop rows with NaT (unparseable dates)
    albums_df.dropna(subset=['release_date'], inplace=True)

    # Group albums by release year
    albums_df['release_year'] = albums_df['release_date'].dt.year
    albums_by_year = albums_df.groupby('release_year').size()

    # Plotting
    plt.figure(figsize=(10, 6))
    custom_colors = ['skyblue', 'salmon', 'lightgreen', 'orange', 'lightcoral']  # Specify custom colors
    albums_by_year.plot(kind='bar', color=custom_colors)
    plt.title('Number of Albums Released by Year')
    plt.xlabel('Release Year')
    plt.ylabel('Number of Albums')

    plt.tight_layout()
    plt.show()

    conn.close()

if __name__ == '__main__':
    db_file = 'spotify.db'
    visualize_album_data(db_file)

