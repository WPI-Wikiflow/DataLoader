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



from gensim.parsing.porter import PorterStemmer
from gensim.parsing.preprocessing import remove_stopwords

class MyCorpus():
    def __init__(self, folder = "wikiData"):
        self.folder = folder
        
    def __iter__(self):
            files = [file for file in os.listdir(self.folder) if file.endswith("-cleaned.pkl")]
            print(files)
            # Convert the files to a pandas dataframe
            for file in files:
                try:
                    # print(f"Processing {file}")
                    df = pd.read_pickle(os.path.join(self.folder, file))
                    for text, title, id in zip(df['text'], df['title'], df['id']):
                        yield gensim.models.doc2vec.TaggedDocument(text, [title, id])
                except Exception as e:
                    print(f"Error: {e}")
                    continue

if __name__ == "__main__":
    data = MyCorpus()
    model = gensim.models.doc2vec.Doc2Vec(vector_size=300, min_count=2, epochs=40, workers=os.cpu_count())
    pickle.dump(model, open("model.pickle", 'wb'))  
    model.build_vocab(data)
    model.train(data, total_examples=model.corpus_count, epochs=model.epochs)
    model.save("model.bin")
    model.save_word2vec_format("model.txt", binary=False)