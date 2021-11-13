from nltk.tag import pos_tag
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import FreqDist, classify, NaiveBayesClassifier
from nltk.tokenize import word_tokenize

import re, string, random, json, os, codecs, time

import pickle

import pandas as pd

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def remove_noise(tweet_tokens, stop_words=()):
    cleaned_tokens = list()

    for token, tag in pos_tag(tweet_tokens):
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', token)
        token = re.sub('(@[A-Za-z0-9_]+)', '', token)

        if tag.startswith('NN'):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'

        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)

        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())

    return cleaned_tokens


if __name__ == '__main__':
    command = input('train(t) / use(u): ')

    if command == 't':
        stop_words = stopwords.words('russian')

        print(f'Start clean data {time.time()}')

        data = pd.read_csv(f'{ROOT_DIR}/datasets/reviews.csv', sep='\t')

        cleaned_tokenized_data = [(dict([token, True] for token in remove_noise(
            word_tokenize(data.loc[index, 'review']))), data.loc[index, 'sentiment']) for index in data.index]

        print(f'Finish clean data {time.time()}')

        print(f'dataset len = {len(data)}')
        print(f'Start training {time.time()}')

        classifier = NaiveBayesClassifier.train(cleaned_tokenized_data)

        print(f'Finish training {time.time()}')

        with open(f'{ROOT_DIR}/models/reviews_trained_model.data', 'wb') as file:
            pickle.dump(classifier, file)

    elif command == 'u':

        with open(f'{ROOT_DIR}/models/basic_500_news_model.data', 'rb') as file:
            classifier = pickle.load(file)

        for file in os.listdir(f'{ROOT_DIR}/../Word2Vec/Articles/Processed'):
            with open(f'{ROOT_DIR}/../Word2Vec/Articles/Processed/{file}') as text_file:
                text = text_file.read()

            cleaned_tokenized_text = dict([token, True] for token in remove_noise(word_tokenize(text)))
            print(text + '\n', classifier.classify(cleaned_tokenized_text))
            print()
            print()
