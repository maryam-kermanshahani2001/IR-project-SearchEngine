from __future__ import unicode_literals

from hazm import *
from parsivar import *
import json

data_url = 'IR_data_news_12k.json'


# num_of_data = 0


def read_data():
    num_of_data = 0
    with open(data_url, 'r') as f:
        data = json.load(f)
        for k in data.keys():
            # print(k)
            # print(data[k])
            idx = k + ''  # to make the id string as the json file
            all_data[idx] = {'title': data[idx]['title'],
                             'content': data[idx]['content'],
                             'url': data[idx]['url'],
                             }
    return all_data


def make_content_list(full_data):
    contents = []
    for item in full_data.items():
        contents.append(item[contents])
    return contents


# def normalize():


def tokenize(contents):
    dict = {}
    for doc_id, cont in enumerate(contents):
        tokens_of_a_sentence = cont.tokenize()
        for index_of_a_token, token in enumerate(tokens_of_a_sentence):

            if token in dict.keys():
                temp_dict = dict[token]
                if doc_id in temp_dict.keys():
                    temp_dict[doc_id].append(index_of_a_token)
                else:
                    index_of_tokens_list_temp = []
                    index_of_tokens_list_temp.append(index_of_a_token)
                    temp_dict[doc_id] = index_of_tokens_list_temp

            else:
                temp = {}
                list_temp = []
                list_temp.append(index_of_a_token)
                temp[doc_id] = list_temp
                dict[token] = temp
    return dict


if __name__ == '__main__':
    all_data = {}
    all_data = read_data()
    contents = []
    contents = make_content_list(all_data)
    main_dictionary = tokenize(contents)
