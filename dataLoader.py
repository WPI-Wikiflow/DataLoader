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

def load_wiki_corpus(input_file, output_file):
    """Convert Wikipedia xml dump file to text corpus"""
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    wiki = WikiCorpus(input_file, metadata=True, dictionary={})
    i = 0
    # Convert the wiki corpus to text json format   
    out_json = {}
    for text in wiki.get_texts():
        out_json[text[1][0]] = {"text": text[0], "title": text[1][1]}
        i = i + 1
        if (i % 10000 == 0):
            logging.info(f"Saved {str(i)} articles")

    with open(output_file, 'w') as output:
        json.dump(out_json, output)
    logging.info(f"Finished Saved {str(i)} articles to {output_file}")

if __name__ == '__main__':
    # Find the list of dumps by scraping https://dumps.wikimedia.org/enwiki/latest/
    page = requests.get('https://dumps.wikimedia.org/enwiki/latest/')
    soup = bs(page.content, 'html.parser')
    links = soup.find_all('a')
    # https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles1.xml-p1p41242.bz2-rss.xml
    dumps = [link.get('href') for link in links if "enwiki-latest-pages-articles" in link.get('href') and "xml-" in link.get('href') and "rss" not in link.get('href')]
    print(dumps)
    for dump in dumps:
        
        if not os.path.exists(dump):
            print(f"Downloading {dump}")
            wget.download(f'https://dumps.wikimedia.org/enwiki/latest/{dump}')

        print(f"Converting {dump}")
        # Replace everything after .xml- with .json
        output_file = re.sub(r'\.xml\-.+', '.json', dump)
        print(f"Output file: {output_file}")
        load_wiki_corpus(dump, output_file)


    