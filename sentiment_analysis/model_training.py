from nltk.tag import pos_tag
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import NaiveBayesClassifier
from nltk.tokenize import word_tokenize

import re, string, os

import pickle
import pandas as pd
import config
import pymongo

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def remove_noise(tweet_tokens, stop_words=()):
    cleaned_tokens = list()

    for token, tag in pos_tag(tweet_tokens):
        token = re.sub(
            "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
            "",
            token,
        )
        token = re.sub("(@[A-Za-z0-9_]+)", "", token)

        if tag.startswith("NN"):
            pos = "n"
        elif tag.startswith("VB"):
            pos = "v"
        else:
            pos = "a"

        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)

        if (
            len(token) > 0
            and token not in string.punctuation
            and token.lower() not in stop_words
        ):
            cleaned_tokens.append(token.lower())

    return cleaned_tokens


if __name__ == "__main__":
    command = input("train(t) / use(u): ")

    if command == "t":
        print("List of datasets:\n")

        for file in os.listdir(f"{ROOT_DIR}/datasets/"):
            print(file)

        filename = input("\nWhat dataset use for training?: ")
        data = pd.read_csv(f"{ROOT_DIR}/datasets/{filename}")

        filename = input("\nWhat filename use for model file?: ")

        text_count = data.index[-1]
        stop_words = stopwords.words("russian")
        cleaned_tokenized_data = list()

        for index in data.index:
            cleaned_tokenized_data.append(
                (
                    dict(
                        [token, True]
                        for token in remove_noise(
                            word_tokenize(data.loc[index, "Text"]), stop_words
                        )
                    ),
                    data.loc[index, "Class"],
                )
            )
            print(f"{index}/{text_count}")

        classifier = NaiveBayesClassifier.train(cleaned_tokenized_data)

        with open(f"{ROOT_DIR}/models/{filename}", "wb") as file:
            pickle.dump(classifier, file)

        print("Model trained!")

    elif command == "u":
        print("List of models:\n")

        for file in os.listdir(f"{ROOT_DIR}/models/"):
            print(file)

        filename = input("\nWhich model use?: ")

        with open(f"{ROOT_DIR}/models/{filename}", "rb") as file:
            classifier = pickle.load(file)

        connection = f"mongodb+srv://{config.username}:{config.password}@cluster0.8ngl3.mongodb.net"
        client = pymongo.MongoClient(connection, serverSelectionTimeoutMS=5000)
        db = client["articles_analysis"]
        collection = db["articles"]

        count_articles = collection.count_documents(
            {"facts": {"$exists": True}, "sentiment": {"$exists": False}}
        )
        count_class_articles = 0

        for article in collection.find(
            {"facts": {"$exists": True}, "sentiment": {"$exists": False}}
        ):
            cleaned_tokenized_text = dict(
                [token, True] for token in remove_noise(word_tokenize(article["text"]))
            )
            sentiment = classifier.classify(cleaned_tokenized_text)
            collection.update_one(
                {"_id": article["_id"]}, {"$set": {"sentiment": sentiment}}
            )
            count_class_articles += 1
            print(f"{count_class_articles}/{count_articles}")
