import os
import json
import gensim
import argparse
import nltk
import re
from multiprocessing import Pool
import pickle
import numpy as np
import pandas as pd
import wandb



from gensim.parsing.porter import PorterStemmer
from gensim.parsing.preprocessing import remove_stopwords


if __name__ == "__main__":
    folder = "wikiData"
    files = [file for file in os.listdir(folder) if file.endswith("-cleaned.pkl")]

    counter = 0
                # Convert the files to a pandas dataframe
    for file in files:
        try:
            # print(f"Processing {file}")
            df = pd.read_pickle(os.path.join(folder, file))
            for text, title, id in zip(df['text'], df['title'], df['id']):
                counter += 1
            print(f"Finished processing {file}")
        except Exception as e:
            print(f"Error: {e}")
            continue
    print(counter)