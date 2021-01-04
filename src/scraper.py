import requests
from bs4 import BeautifulSoup
import re

def clean(word):
    bad_chars = [' ', '(', ')', '[', ']']
    for char in bad_chars:
        word = word.replace(char,'')
    word = word.lower()
    
    return word

def parse(song, artist):
    PATH = 'https://www.azlyrics.com/lyrics/'

    song_url = clean(song)
    artist_url = artist.replace(' ', '').lower()

    URL = PATH + artist_url + '/' + song_url + '.html'
 
    req = requests.get(URL)
    soup = BeautifulSoup(req.content, 'html.parser')
    text = soup.get_text().splitlines()

    title = song.title().strip()

    start_pattern = '\"' + title + '\"'
    start_idx = None

    end_pattern = 'Submit Corrections'
    end_idx = None

    for idx, line in enumerate(text):
        start_match = re.search("^%s$" % start_pattern, line)
        if start_match:
            start_idx = idx

        end_match = re.search("%s" % end_pattern, line)
        if end_match:
            end_idx = idx
            break

    print(start_idx)

    lyrics = text[start_idx:end_idx]

    # remove blank lines in-place
    lyrics[:] = [x for x in lyrics if x != '']

    # remove non-lyric lines in-place
    lyrics[:] = [x for x in lyrics if x[0] != '[']

    # for lyric in lyrics:
    #    print(lyric)

    return lyrics