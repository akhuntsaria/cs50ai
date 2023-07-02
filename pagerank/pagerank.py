from functools import reduce
import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    prob_dist = {}
    for p in corpus:
        if not corpus[page]: # no outgoing links
            prob_dist[p] = 1 / len(corpus)
        elif p in corpus[page]: # outgoing link
            prob_dist[p] = (damping_factor / len(corpus[page])) + ((1 - damping_factor) / len(corpus))
        else: # random link
            prob_dist[p] = ((1 - damping_factor) / len(corpus))
    return prob_dist


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    counts = {}
    sample = None
    tm = None
    for sample_i in range(n):
        if not sample:
            sample = random.choice(list(corpus.keys()))
        else:
            tm = transition_model(corpus, sample, damping_factor)
            sample = random.choices(population=list(tm.keys()),weights=list(tm.values()),k=1)[0]
        counts[sample] = counts.get(sample, 0) + 1

    return {page: (counts[page] / n) for page in counts.keys()}


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    ranks = {page: (1 / len(corpus)) for page in corpus.keys()}
    random_factor = (1 - damping_factor) / len(corpus)

    while True:
        new_ranks = dict(ranks)

        for page in ranks.keys():
            new_ranks[page] = random_factor
            parents = [parent for parent in corpus.keys() if page in corpus[parent]]
            for parent in parents:
                num_links = len(corpus[parent]) if corpus[parent] else len(corpus)
                new_ranks[page] += damping_factor * (ranks[parent] / num_links)

        # Check if it converged
        if max(abs(ranks[key]-new_ranks[key]) for key in ranks.keys()) <= 0.001:
            return new_ranks
        
        ranks = new_ranks

if __name__ == "__main__":
    main()
