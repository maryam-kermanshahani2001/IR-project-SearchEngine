from __future__ import unicode_literals
from hazm import Normalizer, Lemmatizer
from parsivar import FindStems, Tokenizer


class DataPreprocess:

    @staticmethod
    def stemming(tokens):
        stemmed = []
        my_stemmer = FindStems()
        for token in tokens:
            stemmed.append(my_stemmer.convert_to_stem(token))
        return stemmed

    @staticmethod
    def lemmatizing(tokens):
        lemmed = []
        my_lemmatizer = Lemmatizer()
        for token in tokens:
            lemmed.append(my_lemmatizer.lemmatize(token))

        return lemmed

    @staticmethod
    def stopwords_removing(tokens):
        tokens_with_removed_stopwords = []
        stop_words = []
        file = open("stopwords.txt", encoding="utf-8")
        stop_words = file.read().splitlines()
        for token in tokens:
            if not (token in stop_words):
                tokens_with_removed_stopwords.append(token)
        return tokens_with_removed_stopwords

    @staticmethod
    def normalizing(text):
        my_normalizer = Normalizer()
        return my_normalizer.normalize(text)

    @staticmethod
    def tokenizing(text):
        my_tokenizer = Tokenizer()
        return my_tokenizer.tokenize_words(text)
