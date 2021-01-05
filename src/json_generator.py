import json

def build_json(mc):
    # skeleton for json
    data = {}
    nodes = []
    edges = []

    # map nodes to numbers for json
    ids = {}

    # populate nodes list & map each node to a unique id for json     
    id = 0
    for source, dests in mc.items():
        nodes.append({'word': source, 'id': id})
        ids[source] = id
        id += 1

    # populate edge list for json
    for source, dests in mc.items():
        for dest, wt in dests.items():
            edges.append({'source': ids[source], 'target': ids[dest], 'weight': wt})

    data['nodes'] = nodes
    data['edges'] = edges

    with open('data.json', 'w') as outfile:
        json.dump(data, outfile, indent = 2)

    # we send over the json to index.html and let d3.js visualize the markov chain 
    # (python's networkx graph visualizer is pretty limited in comparison)