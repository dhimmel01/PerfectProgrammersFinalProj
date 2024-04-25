import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress

def fetch_data_from_database(conn):
    artists_data = pd.read_sql_query("SELECT * FROM artists", conn)
    return artists_data

def plot_followers_vs_popularity(artists_data):
    plt.figure(figsize=(10, 6))
    plt.scatter(artists_data['followers'], artists_data['popularity'], alpha=0.5)
    plt.title('Spotify Follower Count vs. Popularity Index')
    plt.xlabel('Follower Count')
    plt.ylabel('Popularity Index')
    plt.grid(True)

    # Perform linear regression
    slope, intercept, r_value, p_value, std_err = linregress(artists_data['followers'], artists_data['popularity'])
    line = slope * artists_data['followers'] + intercept

    # Plot the line of best fit
    plt.plot(artists_data['followers'], line, color='red', label=f'Fit: y = {slope:.2f}x + {intercept:.2f}')

    # Disable scientific notation
    plt.ticklabel_format(style='plain')

    # Show the equation of the line
    plt.text(0.1, 0.9, f'R-squared: {r_value**2:.2f}', transform=plt.gca().transAxes)
    plt.legend()
    plt.show()

def main():
    try:
        conn = sqlite3.connect('spotify.db')
        artists_data = fetch_data_from_database(conn)
        plot_followers_vs_popularity(artists_data)
        conn.close()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
