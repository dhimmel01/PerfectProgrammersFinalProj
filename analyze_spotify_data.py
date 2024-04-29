import sqlite3
import pandas as pd

def visualize_album_data(db_file):
    conn = sqlite3.connect(db_file)

    query = '''
    SELECT albums.release_date, artists.id
    FROM albums
    JOIN artists ON albums.artist_id = artists.id
    '''


    albums_with_artists_df = pd.read_sql_query(query, conn)

    albums_with_artists_df['release_date'] = pd.to_datetime(albums_with_artists_df['release_date'], errors='coerce')


    albums_with_artists_df.dropna(subset=['release_date'], inplace=True)


    albums_with_artists_df['release_year'] = albums_with_artists_df['release_date'].dt.year
    albums_by_year = albums_with_artists_df.groupby('release_year').size()


    average_albums_per_year = albums_by_year.mean()


    with open("average_albums_per_year.txt", "w") as file:
        file.write(f"Average Albums Released Per Year: {average_albums_per_year}")

    conn.close()

if __name__ == '__main__':
    db_file = 'spotify.db'
    visualize_album_data(db_file)
