import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | S Conj S
PP -> P NP
NP -> N | Det NP | Adj NP | PP NP | NP PP | NP Adv
VP -> V | V NP | V PP | Adv VP | VP Adv | VP Conj VP
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    nltk.download('punkt')
    tokens = nltk.tokenize.word_tokenize(sentence)
    tokens = [token.lower() for token in tokens if sum(1 for c in token if c.isalpha())]
    return tokens


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    def contains_np(tree):
        if type(tree) != nltk.Tree:
            return
        for subtree in tree:
            if type(subtree) != nltk.Tree:
                continue
            if subtree.label() == 'NP' or contains_np(subtree):
                return True
        return False

    chunks = []

    def traverse(tree):
        if type(tree) != nltk.Tree:
            return
        for subtree in tree:
            if type(subtree) != nltk.Tree:
                continue
            if subtree.label() == 'NP' and not contains_np(subtree):
                chunks.append(subtree)
            traverse(subtree)
    traverse(tree)
    return chunks


if __name__ == "__main__":
    main()
