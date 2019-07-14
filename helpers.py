import os
import re

import gensim.downloader as api

from gensim.models import Word2Vec, KeyedVectors
from gensim.models.fasttext import FastText

if not 'KAGGLE_CONFIG_DIR' in os.environ.keys():
    os.environ['KAGGLE_CONFIG_DIR'] = os.getcwd()

import kaggle

def download_dataset(url, dest, unzip=True):
    try:
        dataset = re.search(r'kaggle.com/([^/]+)/([^/]+)', url).group()
        if not 'kaggle.com/' in dataset:
            raise ValueError
        else:
            dataset = dataset.replace('kaggle.com/', '')
            kaggle.api.authenticate()
            kaggle.api.dataset_download_files(dataset, path=dest, unzip=unzip)
    except (AttributeError, ValueError):
        print('Check your url: {}'.format(url))
        exit()

def correct_spelling(text):
    model = api.load('glove-wiki-gigaword-100')
    print(model.most_similar(text))