# GeniusNoTokenScraper: 

[![Python version](https://img.shields.io/badge/python-3.x-brightgreen.svg)](https://pypi.org/project/lyricsgenius/)


A Python program that scrapes the Genius and Spotify album page for lyrics, annotation, and URI data without the need a client access token.

# Usage
You are free to fork or just copy the source to use in your project according the GNU GENERAL PUBLIC LICENSE.

# Example

```python
album_spotify_link = "https://open.spotify.com/album/41GuZcammIkupMPKH2OJ6I"
album_genius_link = "https://genius.com/albums/Travis-scott/Astroworld"
singer = "Travis Scott"
year = "2018"
get_album_data_csv(album_genius_link, album_spotify_link, singer, year)
csv_to_json("data.csv")
```

Result: 
Initiall the album in parsed in a CSV file: [data.csv](https://github.com/MentalN/Genius-NoToken-Scraper/blob/master/data.csv)
and then the final results are outputed as a JSON file [data.JSON](https://github.com/MentalN/Genius-NoToken-Scraper/blob/master/data.json)
