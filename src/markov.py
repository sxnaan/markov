import math

def truncate(num, digits):
    stepper = 10.0 ** digits
    return math.trunc(stepper * num) / stepper

def clean(word):
    bad_chars = ['“', '”', '"', '.', '!', '?', ',', ';', '(', ')']
    for char in bad_chars:
        word = word.replace(char,'')
    word = word.lower()
    
    return word

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

def build_mkch(lines):

    mc = {}     # treat graph as adj list stored as a dict: {source_word -> {target_word -> weight}}

    for i, line in enumerate(lines):    
        words = line.split()            
        for j, word in enumerate(words):
            curr = clean(word)
            
            if len(curr) == 0:
                continue 

            next = None
            if j == len(words) - 1 and i != len(lines) - 1:     # next word is first word of next line, skip if line is blank:
                temp_words = lines[i+1].split() 
                next = clean(temp_words[0])
            else:
                # get next word as expected, unless we're at the end
                next = None if (j == len(words) - 1) else clean(words[j+1])
            
            if next != None and len(next) > 0:
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
