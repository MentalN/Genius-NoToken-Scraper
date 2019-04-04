#   File name: genius-scraper.py
#   Author: Nawaf Abdullah
#   Description: download songs, albums, and annotations info from genius given links.
#   Date Created: 30-March-2019


import json
import csv
from lxml import html
import requests
import io


def get_album_data_csv(genius_album_link, spotify_album_link, artist_name=None, album_year=None):
    song_links = []
    song_names = []
    song_uris = []

    #   Get album data from Genius
    page_genius = requests.get(genius_album_link)
    tree_genius = html.fromstring(page_genius.content)
    genius_elements = tree_genius.xpath('//a[@class="u-display_block"]')

    for i_elem in genius_elements:
        name = i_elem.text_content().replace("Lyrics", "")
        name = name.replace("\n", "")
        name = name.replace(",", "")
        song_names.append(name.strip())
        song_links.append(i_elem.get('href'))

    #   Get album data from Spotify
    page_spotify = requests.get(spotify_album_link)
    tree_spotify = html.fromstring(page_spotify.content)
    spotify_elements = tree_spotify.xpath('//meta[@property="music:song"]')

    for j_elem in spotify_elements:
        song_uris.append(j_elem.get('content').replace("https://open.spotify.com/track/", "spotify:track:"))

    while True:
        print(len(song_names))
        print(len(song_links))
        print(len(song_uris))
        cont_opt = input("continue (y/n)?")
        if cont_opt == 'y':
            break
        else:
            #   Fix song names list
            print("Song Names: ")
            for i_song in range(len(song_names)):
                print(str(i_song) + ' - ' + song_names[i_song])
            while True:
                del_index = int(input("Enter an index number for song deletion, enter 999 to quit deleting > "))
                if del_index == 999:
                    break
                else:
                    del song_names[del_index]
                    for i_song in range(len(song_names)):
                        print(str(i_song) + '- ' + song_names[i_song])
            #   Fix song links list
            print("Song Links: ")
            for i_link in range(len(song_links)):
                print(str(i_link) + ' - ' + song_links[i_link])
            while True:
                del_index = int(input("Enter an index number for song deletion, enter 999 to quit deleting > "))
                if del_index == 999:
                    break
                else:
                    del song_links[del_index]
                    for i_link in range(len(song_links)):
                        print(str(i_link) + '- ' + song_links[i_link])
            #   Fix song links list
            print("Song URIs: ")
            for i_uri in range(len(song_uris)):
                print(str(i_uri) + ' - ' + song_uris[i_uri])
            while True:
                del_index = int(input("Enter an index number for song deletion, enter 999 to quit deleting > "))
                if del_index == 999:
                    break
                else:
                    del song_uris[del_index]
                    for i_uri in range(len(song_uris)):
                        print(str(i_uri) + '- ' + song_uris[i_uri])

    print("Reached the end")

    f = io.open('data.csv', 'a', encoding="utf-8")
    for n in range(len(song_names)):
        f.write(artist_name + ',' + song_names[n] + ',' + album_year + ',' +
                song_links[n] + ',' + song_uris[n] + '\n')
    f.close()


def get_song_data(genius_link):
    page = requests.get(genius_link)
    tree = html.fromstring(page.content)

    elements = tree.xpath('//a[@class="referent"]')

    song_data = []
    for elem in elements:
        song_data.append([elem.text_content(), elem.get('data-id')])

    return song_data


def get_billboards(billboard_link):
    page = requests.get(billboard_link)
    tree = html.fromstring(page.content)
    elements = tree.xpath('//div[@class="chart-list-item  "]')
    elements = elements[:15]

    top_songs = []
    for elem in elements:
        artist_name = elem.get('data-artist')
        print(artist_name)
        in_verf = input("Verify artist name > ")
        if in_verf != 'ok':
            artist_name = in_verf

        song_name = elem.get('data-title')
        print(song_name)
        in_verf = input("Verify song name > ")
        if in_verf != 'ok':
            song_name = in_verf

        song_year = input("Enter year > ")

        genius_link = "https://genius.com/" + artist_name.replace(" ", "-") + "-" \
                      + song_name.replace(" ", "-") + "-lyrics"
        print(genius_link)
        in_verf = input("Verify song link > ")
        if in_verf != 'ok':
            genius_link = in_verf

        spotify_uri = input("Enter spotify URI > ")

        image_link  = input("Enter image link > ")

        top_songs.append([artist_name, song_name, song_year, genius_link, spotify_uri, image_link])


def csv_to_json(artist_csv):
    #   CSV Format: Artist,Song,Year,GeniusLink,SpotifyLink
    artist_data = []
    json_data = []

    #   Parse CSV
    try:
        with open(artist_csv, encoding='utf-8-sig') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                artist_data.append(row)
        #   Get the lyrics
        for i_song in artist_data:
            lyrics_data = get_song_data(i_song[3])
            for lyric_datum in lyrics_data:
                if "[" in lyric_datum[0]:
                    continue
                json_data.append({
                    'artist': i_song[0],
                    'song': i_song[1],
                    'year': i_song[2],
                    'lyric': lyric_datum[0],
                    'annotationId': lyric_datum[1],
                    'spotifyUri': i_song[4],
                })
    except KeyError:
        print(i_song)

    with open('data.json', 'w') as fp:
        json.dump(json_data, fp)


"""
#   For scraping multiple albums
#   Insert a list of albums, with a corresponding list of
albums = [
          ]

uris = [
        ]

years = [
         ]

singer = ""

for x in range(len(albums)):
    get_album_data_csv(albums[x], uris[x], singer, years[x])
csv_to_json("data.csv")
"""


#   Example for scraping one album
album_spotify_link = "https://open.spotify.com/album/41GuZcammIkupMPKH2OJ6I"
album_genius_link = "https://genius.com/albums/Travis-scott/Astroworld"
singer = "Travis Scott"
year = "2018"
get_album_data_csv(album_genius_link, album_spotify_link, singer, year)
csv_to_json("data.csv")


