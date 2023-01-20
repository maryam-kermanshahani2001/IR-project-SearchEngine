import math
import matplotlib.pyplot as plt
from preprocessor import DataPreprocess


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
        for content in self.contents:
            tokens_of_a_sentence = self.preprocess.tokenizing(content)
            for t in tokens_of_a_sentence:
                all_tokens.append(t)
                terms_set.add(t)

        print("Heaps law without stemming")
        print(len(all_tokens))
        print(len(terms_set))

    def heaps_law_with_stemming(self):
        all_tokens = []
        terms_set = set()
        for content in self.contents:
            tokens_of_a_sentence = self.preprocess.tokenizing(content)
            stemmed = self.preprocess.stemming(tokens_of_a_sentence)
            for t in stemmed:
                all_tokens.append(t)
                terms_set.add(t)

        print("Heaps law with stemming")
        print(len(all_tokens))
        print(len(terms_set))
