from gensim.corpora import WikiCorpus
import logging
import os
import sys
import re
import wget
from itertools import count
import requests
from bs4 import BeautifulSoup as bs
import json
import pandas as pd
import nltk

def clean_text(text):
    out = []
    for word in text:
        # print(word)
        word = re.sub(r'[^a-zA-Z0-9\s]', '', word)
        # Remove new line characters
        word = word.replace("\\n", " ")
        # Remove all duplicate whitespace
        word = re.sub(r'\s+', ' ', word)
        word = word.lower()
        # Remove the stopwords
        if word not in nltk.corpus.stopwords.words('english'):
            # Lemmatize the word
            word = nltk.stem.WordNetLemmatizer().lemmatize(word)
            out.append(word)
            # print(word)
    return out

def load_wiki_corpus(input_file, output_file):
    """Convert Wikipedia xml dump file to text corpus"""
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    wiki = WikiCorpus(input_file, metadata=True, dictionary={})
    i = 0
    df = pd.DataFrame(columns=['title', 'id', 'text'])
    # Convert the wiki corpus to a pandas dataframe
    for text in wiki.get_texts():
        title = text[1][1]
        textID = text[1][0]
        # cleaned_text = clean_text(text[0])
        # Convert to pandas dataframe
        df.loc[i] = [title, textID, text[0]]
        i += 1
        if i % 10000 == 0:
            print(f"Processed {i} articles")
    # Save the dataframe
    df.to_pickle(output_file)
    print(f"Saved {output_file}")
    

if __name__ == '__main__':
    nltk.download('omw-1.4')
    folder = "wikiData/"
    # Find the list of dumps by scraping https://dumps.wikimedia.org/enwiki/latest/
    page = requests.get('https://dumps.wikimedia.org/enwiki/latest/')
    soup = bs(page.content, 'html.parser')
    links = soup.find_all('a')
    # https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles1.xml-p1p41242.bz2-rss.xml
    dumps = [link.get('href') for link in links if "enwiki-latest-pages-articles" in link.get('href') and "xml-" in link.get('href') and "rss" not in link.get('href')]
    print(dumps)
    for dump in dumps:
        dump_file = folder + dump
        print(f"Processing {dump}")
        if not os.path.exists(dump_file):
            print(f"Downloading {dump} to {dump_file}")
            wget.download(f'https://dumps.wikimedia.org/enwiki/latest/{dump}', out=folder)

        output_file = result = folder + re.sub(r"\.xml(-\w+)\.bz2$", lambda match: f'{match.group(1)}.json', dump) 
        print(f"Output file: {output_file}")
        load_wiki_corpus(dump_file, output_file)