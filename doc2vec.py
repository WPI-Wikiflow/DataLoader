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

class MyCorpus():
    def __init__(self, folder = "wikiData"):
        self.folder = folder
        files = [file for file in os.listdir(self.folder) if file.endswith("-cleaned.pkl")]
        print(files)
        
    def __iter__(self):
            files = [file for file in os.listdir(self.folder) if file.endswith("-cleaned.pkl")]
            # Convert the files to a pandas dataframe
            for file in files:
                try:
                    # print(f"Processing {file}")
                    df = pd.read_pickle(os.path.join(self.folder, file))
                    for text, title, id in zip(df['text'], df['title'], df['id']):
                        yield gensim.models.doc2vec.TaggedDocument(text, [title, id])
                    print(f"Finished processing {file}")
                except Exception as e:
                    print(f"Error: {e}")
                    continue

if __name__ == "__main__":
    run = wandb.init(project="wikiData")
    vector_size = 300
    epochs = 300
    wandb.config = {
        "vector_size": vector_size,
        "epochs": epochs
    }  
    wandb.run.log_code(".")

    data = MyCorpus()
    model = gensim.models.doc2vec.Doc2Vec(vector_size=vector_size, min_count=2, workers=os.cpu_count())
    model.build_vocab(data)
    for epoch in range(epochs):
        print(f"Epoch {epoch}")
        model.train(data, total_examples=model.corpus_count, epochs=1)
        model.save("doc2vec.model")
        model_artifact = wandb.Artifact('doc2vecModel', type='model')
        model_artifact.add_file('doc2vec.model')
        wandb.log_artifact(model_artifact)
        model.save_word2vec_format("doc2vec.model.bin", binary=True)
        model_artifact = wandb.Artifact('doc2vecModelBin', type='model')
        model_artifact.add_file('doc2vec.model.bin')
        wandb.log_artifact(model_artifact)
        