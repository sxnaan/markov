# My Beautiful Dark Twisted Markov Chain (MBDTMC)*
`version 0.1.0 | Sinaan Younus`

![Sweater Weather Markov Chain](https://github.com/sxnaan/markov/blob/main/demos/gif/sweaterweather-theneighbourhood.gif?raw=true)

---
## Background

I learned about stochastic models in my ***Applications of Linear Algebra*** class last semester, and Markov chains were the primary topic of discussion in that chapter. I recently stumbled upon a Youtube video that mentioned them in the context of lexicons, and this helped remind me that maths and language are not so unrelated. 

This project bridges the gap between the two disciplines in a visual manner, uniting the mathematical model of Markov chains with the linguistic nature of song lyrics -- using the web-scraping powers of Python and the data visualization tools of Javascript to do so. 

**In case it wasn't clear, I named the project after Kanye West's 5th studio album, My Beautiful Dark Twisted Fantasy (MBDTF)*

---
## Functionality

1. `driver.py` | Prompt user to provide a song: 
```
> What's the song you want to visualize? Sweater Weather
> And who's it by? The Neighbourhoud
```

2. `scraper.py` | Using the given song and artist name, use azlyrics.com as the dataset to scrape the song's lyrics (using **Beautiful Soup**). This is convenient for a few main reasons with respect to web scraping:
    - As one of the oldest lyrics pages on the web (© 2000), AZ Lyrics is an extensive lyrics library (they don't provide an exact number of songs, but refer to themselves as *“a place where all searches end!”* -- in my experience, this was true)
    - AZ Lyrics' pages are the closest thing to raw HTML, with minimized ads and little, if any, dynamic content 
    - Almost all of AZ Lyrics' song pages are formatted with the following URL: https://www.azlyrics.com/lyrics/[artist-name]/[song-name], which makes it easy to find the correct page for most songs using the **Requests** library in tandemn with **Beautiful Soup** 

3. `scraper.py` | One limitation of AZ Lyrics is that their lyrics container/div has no unique id/class, so to process the lyrics, we must extract them after parsing all the text on the page -- but with some **Regex**-powered pattern matching, we can easily do this in one pass through the scraped lines

4. `scraper.py` | After the lyrics have been scraped, again use **Regex** -- this time to clean it (all words will be lowercase, with no ending-punctuation, commas, parens, brackets, etc.)

5. `markov.py` | With the lyrics in an array (each word is one element), process them and build the Markov chain (weighted, directed graph) using the following definitions & algorithm:
    - **Nodes:** Unique words in the lyrics
    - **Edges:**  Links between any two words that appear next to each other in the song (`source` is the first of the two words, `target` is the one immediately following it)
    - **Weights:** The probability* that `source` will be followed by `target` at any occurance of `source` in the song
> **Algorithm**
> 1. Process the words two by two -- at each iteration keep track of the current word, as well as the word that follows. 
> 2. If the current word isn't already in the Markov chain, add it (same with the next word)
> 3. If the next word isn't already in current word's edge list, add it & set the weight to 1
> 4. Else, the next word is already in current word's edge list, so incrememnt the weight by 1
> 5. Normalize the weights to change them from counts to probabilities* by dividing each edge-weight by the sum of total weights for its source node's edge list)

    * Note, these aren't exactly probabilities -- if we could see the entire lyrics, we'd know that the probability of a certain word following another is either 0 or 1 (either it follows or it doesn't); but the fundamental idea of a Markov chain is that a transition from state A to state B is only dependent on the current state (A). All other states (previous/following lyrics in our case) are irrelevant.

6. `json_generator.py` | Extract the nodes and edges from the graph’s adjacency list representation; write this data to a JSON file (`data.json`) 

7. `index.html` | Using this JSON object as the dataset, use the **D3.js** library to create a force-directed graph visualization of the song’s Markov chain as an SVG. Nodes are labeled with the word they represemt, and edge weights, instead of being labeled, are represented by edge thickness (higher probabilities correspond to higher stroke-widths, lower probabilities correspond to lower stroke-widths 

---
## Demos 
- You can find demos of 6 songs in `/demos` in `.gif` and `.mp4` format, similar to the gif of Sweater Weather at the top of this file

- Check out https://sxnaan.github.io/markov/ for a live, interactive demo of Coldplay's "Yellow"

---
## Usage
- If you want to create a visualization of your favorite song, follow these steps:
    1. Download the `/src`, `/docs`, and `/d3` folders
    2. Run `driver.py`, type in the song & artist name as prompted
    3. This will automatically populate `index.json` with the nodes/edges of your song's Markov chain
    4. Depending on your browser's CORS settings, you might not be able to see the graph when you save and open 'docs/index.html'
        - If this is the case, publish your JSON file somehwhere online, and update `line 50` of `index.html` with that path 
    5. Done! Drag, zoom, enjoy!

---
## To-Do
- [ ] Fix some bugs regarding non-English song titles, currently the algorithm works for most songs (run some data analysis to find this exact percentage)  
- [ ] Use the ReGraph React.js library to make the markov chain visualization interactive
