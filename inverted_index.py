from __future__ import unicode_literals

import collections
import json
from preprocess import DataPreprocess

from doc_pos import DocPos


class InvertedIndex:

    def __init__(self):
        self.all_data = {}
        self.file_path = 'IR_data_news_12k.json'
        self.preprocess = DataPreprocess()

    def read_data(self):
        contents = []
        flag = 0
        # num_of_data = 0
        with open(self.file_path, 'r') as f:
            data = json.load(f)
            for k in data.keys():
                if flag >= 10:
                    break
                # print(k)
                # print(data[k])
                idx = k + ''  # to make the id string as the json file
                self.all_data[idx] = {'title': data[idx]['title'],
                                      'content': data[idx]['content'],
                                      'url': data[idx]['url'],
                                      }
                contents.append(data[idx]['content'])
                flag += 1
        return self.all_data, contents

    def create_postings_list(self, contents):
        my_dictionary = {}  # you can change it to a dictionary which means term id, term
        for doc_id, content in enumerate(contents):
            normalized_contents = self.preprocess.normalizing(content)
            tokens_of_a_sentence = self.preprocess.tokenizing(normalized_contents)
            stemmed = self.preprocess.stemming(tokens_of_a_sentence)
            removed_stopwords = self.preprocess.stopwords_removing(stemmed)
            final_tokens_of_a_sentence = self.preprocess.lemmatizing(removed_stopwords)
            for index_of_a_token, token in enumerate(final_tokens_of_a_sentence):

                # if token in my_dictionary.keys():
                if token in my_dictionary:
                    doc_pos_of_token = my_dictionary[token]
                    if doc_id in doc_pos_of_token.my_map.keys():
                        doc_pos_of_token.add_position(doc_id, index_of_a_token)
                    else:
                        doc_pos_of_token.new_doc_id(doc_id, index_of_a_token)

                else:
                    temp = {}
                    doc_pos = DocPos()
                    doc_pos.new_doc_id(doc_id, index_of_a_token)
                    my_dictionary[token] = doc_pos

        return my_dictionary

    @staticmethod
    def sort_tokens(input_dict):
        return collections.OrderedDict(sorted(input_dict.items()))

    def execute(self):
        all_data = {}
        all_data, contents = self.read_data()
        print(all_data)
        # contents = []
        # contents = make_content_list(all_data)
        main_dictionary = self.tokenize(contents)
        sorted_main_dictionary = self.sort_tokens(main_dictionary)
        for k in sorted_main_dictionary:
            print("")
            print(f'{k}-> {sorted_main_dictionary[k].my_map}')
        return sorted_main_dictionary


# if __name__ == '__main__':
#     data_proc = DataPreprocess()
#     data_proc.execute()
#     print("end")
