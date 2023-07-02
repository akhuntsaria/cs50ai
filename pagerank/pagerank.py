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
    res = {}
    for p in corpus:
        if not corpus[page]: # no outgoing links
            res[p] = 1 / len(corpus)
        elif p in corpus[page]: # outgoing link
            res[p] = (damping_factor / len(corpus[page])) + ((1 - damping_factor) / len(corpus))
        else: # random link
            res[p] = ((1 - damping_factor) / len(corpus))
    return res


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    counts = {}
    page = None
    tm = None
    for i in range(n):
        if not page:
            page = random.choice(list(corpus.keys()))
            tm = transition_model(corpus, page, damping_factor)
        else:
            page = random.choices(population=list(tm.keys()),weights=list(tm.values()),k=1)[0]
            tm = transition_model(corpus, page, damping_factor)
        counts[page] = counts.get(page, 0) + 1
    #TODO counts to res
    res = {}
    for page in counts.keys():
        res[page] = counts[page] / n
    return res


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pr = {}
    for page in corpus.keys():
        pr[page] = 1 / len(corpus)
    
    while True:
        new_pr = dict(pr)
        for page in pr.keys():
            sum = 0
            for i in links_to(corpus, page):
                sum += pr[i] / num_links(corpus, i)
            new_pr[page] = (1 - damping_factor) / len(corpus) + damping_factor * sum
        if converged(pr, new_pr):
            return new_pr
        pr = new_pr

def converged(a, b):
    for key in a.keys():
        if abs(a[key]-b[key]) > 0.001:
            return False
    return True

def links_to(corpus, page):
    res = []
    for p in corpus.keys():
        if page in corpus[p]:
            res.append(p)
    return res

def num_links(corpus, page):
    if not corpus[page]:
        return len(corpus)
    return len(corpus[page])

if __name__ == "__main__":
    main()
