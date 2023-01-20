from __future__ import unicode_literals
# from hazm import Normalizer, Lemmatizer
# from parsivar import FindStems, Tokenizer

import hazm
import parsivar

import must_removed_things


class DataPreprocess:

    @staticmethod
    def stemming(tokens):
        stemmed = []
        my_stemmer = parsivar.FindStems()
        # my_stemmer = hazm.Stemmer()
        for token in tokens:
            stemmed.append(my_stemmer.convert_to_stem(token))
            # stemmed.append(my_stemmer.stem(token))
        return stemmed

    @staticmethod
    def lemmatizing(tokens):
        lemmed = []
        # my_lemmatizer = parsivar.Lemmatizer()
        my_lemmatizer = hazm.Lemmatizer()
        for token in tokens:
            lemmed.append(my_lemmatizer.lemmatize(token))

        return lemmed

    @staticmethod
    def stopwords_removing(tokens):
        tokens_with_removed_stopwords = []
        stop_words = hazm.stopwords_list()
        # file = open("stopwords.txt", encoding="utf-8")
        # stop_words = file.read().splitlines()
        for token in tokens:
            if not (token in stop_words):
                tokens_with_removed_stopwords.append(token)
        return tokens_with_removed_stopwords

    @staticmethod
    def normalizing(text):

        # my_normalizer = hazm.Normalizer()
        my_normalizer = parsivar.Normalizer()
        return my_normalizer.normalize(text)

    @staticmethod
    def tokenizing(text):
        my_tokenizer = parsivar.Tokenizer()
        # my_tokenizer = hazm.word_tokenize()
        # return hazm.word_tokenize(text)
        return my_tokenizer.tokenize_words(text)

    @staticmethod
    def remove_punctuations(text):
        punctuations = must_removed_things.persian_punctuations
        punctuated = text
        for punc in punctuations:
            punctuated = punctuated.replace(punc, " ")
        return punctuated

    def preprocess(self, content):
        punctuated_content = self.remove_punctuations(content)
        # english_removed_content = self.preprocess.remove_english_chars_and_numbers(punctuated_content)
        normalized_content = self.normalizing(punctuated_content)
        tokens_of_a_sentence = self.tokenizing(normalized_content)
        stemmed = self.stemming(tokens_of_a_sentence)
        removed_stopwords = self.stopwords_removing(stemmed)
        final_tokens_of_a_sentence = self.lemmatizing(removed_stopwords)
        return final_tokens_of_a_sentence

    # def query_preprocess(self, content):
    #     punctuated_content = self.remove_punctuations(content)
    #     normalized_content = self.normalizing(punctuated_content)
    #     tokens_of_a_sentence = self.tokenizing(normalized_content)
    #     stemmed = self.stemming(tokens_of_a_sentence)
    #     final_tokens_of_a_sentence = self.lemmatizing(stemmed)
    #
    #     return final_tokens_of_a_sentence


    # @staticmethod
    # def equalize_chars(token):
    #     # remove vowels and equalize chars
    #     arabic_to_persian = {'ؤ': 'و', 'ي': 'ی', 'أ': 'ا', 'إ': 'ا', 'آ': 'ا', 'ك': 'ک', 'ة': 'ه'}
    #     new_word = token.translate(str.maketrans(arabic_to_persian))
    #     if new_word != token:
    #         return new_word
    #     else:
    #         return token

    # @staticmethod
    # def remove_english_chars_and_numbers(text):
    #     english_chars = must_removed_things.english_chars
    #     english_numbers = must_removed_things.english_numbers
    #
    #     edited = text
    #     for char in english_chars:
    #         edited = edited.replace(char, " ")
    #
    #     for num in english_numbers:
    #         edited = edited.replace(num, " ")
    #
    #     return edited
