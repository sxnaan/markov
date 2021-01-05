import markov
import scraper
import json_generator

def main():
    
    song = input("What's the song you want to visualize? ")
    artist = input("And who's it by? ")

    lyrics = scraper.parse(song, artist)
    mc = markov.build_mkch(lyrics)
    json_generator.build_json(mc)

    # this list is a text-based visualization of the markov chain (adjacency list)
    # each node is listed with all the words it links to, along with `the 'probability'
    # that a word in the edge-list follows the node
    
    markov.print_mkch(mc)

main()