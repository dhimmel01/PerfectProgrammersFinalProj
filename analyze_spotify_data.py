import sqlite3
import pandas as pd

def visualize_album_data(db_file):
    conn = sqlite3.connect(db_file)

    query = '''
    SELECT albums.release_date, artists.id
    FROM albums
    JOIN artists ON albums.artist_id = artists.id
    '''
#Each row in the resulting table contains the release date of an album and the ID of the artist who created it.

    albums_with_artists_df = pd.read_sql_query(query, conn)
    #Takes data from alumb and artist tables
    #Takes release date from alumbs table, id from artist table

    albums_with_artists_df['release_date'] = pd.to_datetime(albums_with_artists_df['release_date'], errors='coerce')


    albums_with_artists_df.dropna(subset=['release_date'], inplace=True)


    albums_with_artists_df['release_year'] = albums_with_artists_df['release_date'].dt.year
    #Creates new DataFrame with the years
    albums_by_year = albums_with_artists_df.groupby('release_year').size()
    #Group by the year


    average_albums_per_year = albums_by_year.mean()


    with open("average_albums_per_year.txt", "w") as file:
        file.write(f"Average Albums Released Per Year: {average_albums_per_year}")

    conn.close()

if __name__ == '__main__':
    db_file = 'spotify.db'
    visualize_album_data(db_file)
