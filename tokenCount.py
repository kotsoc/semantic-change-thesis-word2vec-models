import click
from fileinput import filename
import os
from collections import Counter

PATH1 = '/2011-2013/'
PATH2 = '/2017/'
PATHS = ['2011-2013/', '2017/']

res= {}

def count_rows_per_month():
    sum = 0
    for fn in os.listdir(os.getcwd()+PATH1):
        if "tokenized" in fn:
            with open(os.path.join(os.getcwd()+PATH1, fn), 'r') as f:
                res[fn[0:7]] = len(f.readlines())
                sum=+res[fn[0:7]]

    res['sum1'] = sum
    sum = 0
    for fn in os.listdir(os.getcwd()+PATH2):
        if "tokenized" in fn:
            with open(os.path.join(os.getcwd()+PATH2, fn),  'r') as f:
                res[fn[0:7]] = len(f.readlines())
                sum=sum+res[fn[0:7]]
                print(sum)

    res['sum2'] = sum
    with open("tokCount.txt", 'a') as f:
        for key,value in res.items():
            f.write(key + ": " + str(value)+'\n')

    f.close()

def count_word_frequencies(input, resultFile, vocab_threshold):
    train_dir = "train/"
    token_counts = Counter()
    with open(train_dir+input, 'r') as f:
        for line in f.readlines():
            tokens = line.strip().split()
            token_counts.update(tokens)
    with open(resultFile, 'w') as f:
        for word, freq in token_counts.most_common():
            if(freq >=  vocab_threshold):
                f.write(word + " "+str(freq)+"\n")
            else:
                break

@click.command()
@click.argument("inputfile")
@click.argument("change_file")
@click.option("--vocab-threshold", type=int, 
        prompt='Vocab threshold (min count per corpus)',
        help="Minmum occurance (in each year) to be included in the final vocab.")
def cli(inputfile, change_file, vocab_threshold):
    count_word_frequencies(inputfile, change_file, vocab_threshold)

if __name__ == "__main__":
    cli(obj={})