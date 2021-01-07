import requests
from bs4 import BeautifulSoup
import re

def parse(song, artist):
    PATH = 'https://www.azlyrics.com/lyrics/'

    song_url = re.sub('[^A-Za-z0-9]+', '', song).lower()
    artist_url = artist.replace(' ', '').lower()

    URL = PATH + artist_url + '/' + song_url + '.html'
 
    req = requests.get(URL)
    soup = BeautifulSoup(req.content, 'html.parser')

    # AZ Lyrics does not have a special id/class for their lyrics container, so we have to parse all text first
    text = soup.get_text().splitlines()

    title = song.title().strip()

    # the layout of AZ Lyrics pages is as follows (lines represent arbitrary text)
    # ______________
    # ______________
    # "[song title]"      <- since the user provides the title, we can use this as the start point
    # [lyrics]
    # Submit Corrections      <- this is always the first non-empty line after the lyrics, use as end point
    # ______________
    # ______________

    start_pattern = '\"' + title + '\"'
    start_idx = None

    end_pattern = 'Submit Corrections'
    end_idx = None

    for idx, line in enumerate(text):
        if start_pattern == line:   # use == instead of regex to avoid issues w/ parens/brackets in the song title 
                                    # (more efficent than escaping all diff possibilities)

            start_idx = idx + 2     # add 2 because 1) we dont include the title in the lyrics 
                                    #           and 2) because of a a possible 'feat. ___' (will be a blank line if no feat)

        end_match = re.search('%s' % end_pattern, line)
        if end_match:
            end_idx = idx
            break

    lyrics = text[start_idx:end_idx]

    # remove blank lines in-place
    lyrics[:] = [x for x in lyrics if x != '']

    # remove non-lyric lines in-place (usually artist tags)
    lyrics[:] = [x for x in lyrics if x[0] != '[']

    # change lyrics from an array of lines to an array of words
    new_lyrics = []

    # go through lyrics and clean them -> remove special chars
    for line in lyrics:
        words = line.split()
        for word in words:
            new_word = re.sub('[^A-Za-z0-9]+', '', word).lower()
            new_lyrics.append(new_word)

    return new_lyrics