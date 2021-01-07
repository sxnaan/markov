import math
import re

def truncate(num, digits):
    stepper = 10.0 ** digits
    return math.trunc(stepper * num) / stepper

def normalize_weights(mkch):
    mc = mkch.copy()
    weight_sums = {}

    for source, dest in mc.items():
        weight_sums[source] = 0
        for word, weight in mc[source].items():
            weight_sums[source] += weight

    for source, dest in mc.items():
        for word, weight in mc[source].items():
            probability = weight / weight_sums[source]
            mc[source][word] = truncate(probability, 3)

    return mc

def build_mkch(words):

    mc = {}     # treat graph as adj list stored as a dict: {source_word -> {target_word -> weight}}

    for i, curr in enumerate(words):
        next = None if i == len(words) - 1 else words[i+1] 
        if next:
            if curr not in mc:
                mc[curr] = {}       # add curr word to the graph 
            if next not in mc:
                mc[next] = {}       # add next word to the graph

            if next not in mc[curr]:     # if the next word isn't in the current word's adj list yet
                mc[curr][next] = 1
            else:
                mc[curr][next] += 1

    mc = normalize_weights(mc)
    return mc

def print_mkch(mc):
    num_uniq_wrds = 0
    num_links = 0

    for source, dests in mc.items():
        num_links += len(dests) 
        num_uniq_wrds += 1
        print(source, ' : ')
        for word, weight in dests.items():
            print('\t', word,' : ', weight)
        print()

    print('There are ' + str(num_uniq_wrds) + ' words in this markov chain, with ' + str(num_links) + ' links!')
