from __future__ import unicode_literals

import collections
import json

from plot import Plot
from preprocessor import DataPreprocess

from doc_pos import DocPos


class InvertedIndex:

    def __init__(self):
        self.all_data = {}
        self.file_path = '../IR_data_news_12k.json'
        self.preprocessor = DataPreprocess()

    def read_data(self):
        contents = []
        flag = 0
        # num_of_data = 0
        with open(self.file_path, 'r') as f:
            data = json.load(f)
            for k in data.keys():
            #     if flag <= 505:
            #         flag += 1
            #         continue
            #     if flag >= 1001:
            #         break
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
            final_tokens_of_a_sentence = self.preprocessor.preprocess(content)

            # if doc_id == 5:
            #     print(punctuated_content)
            #     print(normalized_content)
            #     print(tokens_of_a_sentence)
            #     print(stemmed)
            #     print(removed_stopwords)
            #     print(final_tokens_of_a_sentence)

            for index_of_a_token, token in enumerate(final_tokens_of_a_sentence):

                # if token in my_dictionary.keys():
                if token in my_dictionary:
                    doc_pos_of_token = my_dictionary[token]
                    if doc_id in doc_pos_of_token.my_map.keys():
                        doc_pos_of_token.add_position(doc_id, index_of_a_token)
                    else:
                        doc_pos_of_token.new_doc_id(doc_id, index_of_a_token)

                else:
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

        # print(all_data)

        for k, v in all_data.items():
            print(f"------doc id-------:{k}")
            print(v)
            print("")

        main_dictionary = self.create_postings_list(contents)
        sorted_main_dictionary = self.sort_tokens(main_dictionary)

        for k in sorted_main_dictionary:
            print("")
            print(f'{k}-> {sorted_main_dictionary[k].my_map}')
            for val in sorted_main_dictionary[k].my_map.keys():
                v = f"{val}"
                print(f' {all_data[v]["url"]} + {all_data[v]["title"]}')

        print("")
        print("------------------------------***************--------------------------------------------")
        print("")
        plot = Plot(contents)
        plot.paint_zipf_plot()
        plot.heaps_law_without_stemming()
        plot.heaps_law_with_stemming()

        return sorted_main_dictionary

# ii = InvertedIndex()
# ii.execute()
# print("end")
