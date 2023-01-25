import math
import matplotlib.pyplot as plt
from preprocessor import DataPreprocess
import numpy as np


class Plot:
    def __init__(self, contents):
        self.contents = contents
        self.preprocess = DataPreprocess()
        self.my_dictionary = {}

    def tokenize(self, stopwords_flag):
        count = 0
        self.my_dictionary = {}

        for content in self.contents:
            # punctuated = self.preprocess.remove_punctuations(content)
            # normalized_contents = self.preprocess.normalizing(punctuated)
            tokens_of_a_sentence = self.preprocess.tokenizing(content)
            if stopwords_flag == 1:
                final_tokens = self.preprocess.stopwords_removing(tokens_of_a_sentence)
            else:
                final_tokens = tokens_of_a_sentence

            for token in final_tokens:
                if token in self.my_dictionary:
                    self.my_dictionary[token] = self.my_dictionary[token] + 1

                else:
                    self.my_dictionary[token] = 1

    def sort_by_frequency(self):
        return dict(reversed(sorted(self.my_dictionary.items(), key=lambda item: item[1])))

    def zipf_execute(self, stopwords_flag):
        self.tokenize(stopwords_flag)
        if stopwords_flag == 1:
            title = "after removing stopword"
        else:
            title = "before removing stopword"
        sorted_dictionary_by_freq = self.sort_by_frequency()
        rank_log = []
        ranks = []
        cf_log = []
        cfs = []
        rank = 1
        for token, frequency in sorted_dictionary_by_freq.items():
            rank_log.append(math.log(rank))
            ranks.append(rank)
            cf_log.append(math.log(frequency))
            cfs.append(frequency)
            rank += 1
        # plt.hist2d(rank_log, cf_log)
        plt.plot(rank_log, cf_log)
        # plt.plot(ranks, cfs)
        # print(sorted_dictionary_by_freq)

        plt.ylabel("log(cf)")
        plt.xlabel("log(rank)")
        plt.title(title)
        plt.show()

    def paint_zipf_plot(self):
        stopwords_flag = 0
        self.zipf_execute(stopwords_flag)
        stopwords_flag = 1
        self.zipf_execute(stopwords_flag)

    def heaps_law_without_stemming(self):
        all_tokens = []
        terms_set = set()
        heaps_question_result = {}

        for i, content in enumerate(self.contents):

            tokens_of_a_sentence = self.preprocess.tokenizing(content)
            for t in tokens_of_a_sentence:
                all_tokens.append(t)
                terms_set.add(t)

            if i == 500 or i == 1000 or i == 1500 or i == 2000:
                heaps_question_result[i] = [len(all_tokens), len(terms_set)]
        print(heaps_question_result)

        print("Heaps law without stemming")
        print(len(all_tokens))
        print(len(terms_set))

        title = "Without Stemming"
        self.show_heaps_result_on_plot(heaps_question_result, len(terms_set), title)

    def show_heaps_result_on_plot(self, res, dict_len, title):
        x = np.array([math.log10(t[1]) for t in list(res.values())])
        y = [math.log10(t[0]) for t in list(res.values())]
        m, b = np.polyfit(x, y, 1)

        plt.subplot(1, 2, 1)
        plt.scatter(x, y, color='orange')
        plt.plot(x, m * x + b)
        plt.xlabel("log10 T")
        plt.ylabel("log10 M")
        plt.title(title)

        plt.show()


    def heaps_law_with_stemming(self):
        all_tokens = []
        terms_set = set()
        heaps_question_result = {}

        for i, content in enumerate(self.contents):
            tokens_of_a_sentence = self.preprocess.tokenizing(content)
            stemmed = self.preprocess.stemming(tokens_of_a_sentence)
            for t in stemmed:
                all_tokens.append(t)
                terms_set.add(t)
            if i == 500 or i == 1000 or i == 1500 or i == 2000:
                heaps_question_result[i] = [len(all_tokens), len(terms_set)]
        print(heaps_question_result)

        print("Heaps law with stemming")
        print(f" Real T (All tokens size) = {len(all_tokens)}")
        print(f" Real M (Vocabulary size) = {len(terms_set)}")
        title = "Without Stemming"
        self.show_heaps_result_on_plot(heaps_question_result, len(terms_set), title)
