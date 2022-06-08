import csv
import click
import numpy as np
import pandas as pd
from pathlib import Path
import util
from gensim.models import KeyedVectors
from multiprocessing import Pool

def context_words_iter(file_path):
    with open(file_path, "r") as f:
        reader = csv.DictReader(f)
        for entry in reader:
            yield entry['word']

def cos_sim(v1, v2):
    if not v1.shape == v2.shape:
        raise ValueError
    if v1.ndim == 1:
        axis = 0
    elif v1.ndim == 2:
        axis = 1
    else:
        raise ValueError
    val = (v1 * v2).sum(axis=axis) / (np.linalg.norm(v1, axis=axis) * np.linalg.norm(v2, axis=axis))
    # sometimes identical vectors produce 1.0000001. floating point problem?
    if v1.ndim == 1:
        return min(val,1)
    else:
        return np.minimum(val, np.ones_like(val))

def angular_distance(v1, v2):
    #return (1-cos_sim(v1,v2))
    return np.arccos(cos_sim(v1,v2)) / np.pi
    # return 1- np.dot(v1,v2)/(np.linalg.norm(v1)*np.linalg.norm(v2))
         

def cosine_change(wv1, wv2, vocab=None):
    """
    Takes two instances of gensim KeyedVectors objects and computes semantic
    distance scores for words in both vocabularies. Semantic distance is
    defined as the angular distance which fall in [0, 1]. If `vocab` is
    provided, it must be a subset of the intersection of the two
    KeyedVector vocabs.
    """
    # vocab is provided; restrict vectors to provided vocab
    if vocab:
        common_vocab = vocab
        vecs1 = np.stack([wv1[w] for w in common_vocab])
        vecs2 = np.stack([wv2[w] for w in common_vocab])
    # vocabs are different; restrict vectors to intersection
    elif wv1.index_to_key != wv2.index_to_key:  
        common_vocab = [w for w in wv1.index_to_key if w in wv2.index_to_key]
        vecs1 = np.stack([wv1[w] for w in common_vocab])
        vecs2 = np.stack([wv2[w] for w in common_vocab])
    # vocabs are the same; use full vector matrices
    else:
        common_vocab = wv1.index_to_key
        vecs1 = wv1.vectors
        vecs2 = wv2.vectors
    distances = angular_distance(vecs1, vecs2)
    return dict(zip(common_vocab, distances))

# cos_diff = lambda x,y: 1 - cos_sim(x,y)



@click.command()
@click.argument("model1")
@click.argument("model2")
@click.argument("change_file")
def cli(model1, model2, change_file):

    # Compute change on the genuine condition 
    wv1= KeyedVectors.load_word2vec_format(model1)
    wv2= KeyedVectors.load_word2vec_format(model2)
    change = cosine_change(wv1, wv2)
    with open(change_file, 'w') as f:
        f.writelines((f"{w}\t{delta}\n" for w,delta in change.items()))

def main():
    cli()
    # for word in context_words_iter("annotated_words.csv"):
    #     print(word)

if __name__ == "__main__":
    main()