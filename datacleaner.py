import pandas as pd
import numpy as np
import gensim
import nltk
from multiprocessing import Pool
import json
import os
import re
import swifter

def clean_text(text):
    out = []
    for word in text:
        word = re.sub(r'[^a-zA-Z0-9\s]', '', word)
        # Remove new line characters
        word = word.replace("\\n", " ")
        # Remove all duplicate whitespace
        word = re.sub(r'\s+', ' ', word)
        word = word.lower()
        # Remove the stopwords
        if word in nltk.corpus.stopwords.words('english'):
            continue
        # Lemmatize the word
        word = nltk.stem.WordNetLemmatizer().lemmatize(word)
        out.append(word)
    return out

if __name__ == "__main__":
    folder = "wikiData"
    # get all .json files in the folder
    files = [file for file in os.listdir(folder) if file.endswith(".pkl")]
    print(files)
    # Convert the files to a pandas dataframe
    for file in files:
        print(f"Processing {file}")
        df = pd.read_pickle(os.path.join(folder, file))

        # Get the first 10 articles
        # df = df.head(10)
        # Clean the text
        with Pool(os.cpu_count()) as p:
            df['text'] = p.map(clean_text, df['text'])
        # Print the first 10 articles
        print(df.head(10))
        # Save the dataframe to file-cleaned.plk
        df.to_pickle(os.path.join(folder, file.replace(".pkl", "-cleaned.pkl")))
        print(f"Saved {file.replace('.pkl', '-cleaned.pkl')}")

