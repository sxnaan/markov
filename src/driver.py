import networkx as nx
import matplotlib.pyplot as plt
import json

import markov
import scraper

def main():
    
    song = input("What's the song you want to visualize? ")
    artist = input("And who's it by? ")

    lyrics = scraper.parse(song, artist)
    mc = markov.build_mkch(lyrics)
    
    # stuff for json
    data = {}
    nodes = []
    links = []

    # stuff for networkx
    # node_labels = {}
    # for key in mc.keys():
    #    node_labels[key] = key
    # e_labels = {}

    # build graph from adj list, also populate nodes and links for json
    
    # G = nx.DiGraph()
    for source, dests in mc.items():
        nodes.append({'id': source})
        for dest, wt in mc[source].items():
            # G.add_edge(source, dest, weight=wt)
            # e_labels[(source, dest)] = wt
            links.append({'source': source, 'target': dest, 'weight': wt})

    data['nodes'] = nodes
    data['links'] = links

    with open('data.json', 'w') as outfile:
        json.dump(data, outfile, indent = 4)

    markov.print_mkch(mc)

    # nx.draw(G)
    # nx.draw_networkx_labels(G, pos=nx.spring_layout(G), labels=node_labels)
    # nx.draw_networkx_edge_labels(G, pos=nx.spring_layout(G), edge_labels=e_labels)
    # plt.show()

main()