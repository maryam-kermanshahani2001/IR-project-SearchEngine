import itertools
import math
import operator

from preprocessor import DataPreprocess
import json
import collections
import heapq

from tfidf_postings_list import TfIdfPostingsList


class Phase2:
    def __init__(self):
        self.all_data = {}
        self.file_path = '../IR_data_news_12k.json'
        self.preprocessor = DataPreprocess()
        self.query_freq_dictionary = {}
        self.main_inv_index = {}
        self.number_of_docs = 0
        self.docs_lengths = {}
        self.k_answers = 10

    def read_data(self):
        contents = []
        flag = 0
        # num_of_data = 0
        with open(self.file_path, 'r') as f:
            data = json.load(f)
            for k in data.keys():
                # if flag >= 1001:
                #     break
                # print(k)
                # print(data[k])
                idx = k + ''  # to make the id string as the json file
                self.all_data[idx] = {'title': data[idx]['title'],
                                      'content': data[idx]['content'],
                                      'url': data[idx]['url'],
                                      }
                contents.append(data[idx]['content'])
                flag += 1
        self.number_of_docs = len(contents)
        return self.all_data, contents

    # def create_index(self, tokens, doc_id):
    #     my_dictionary = {}
    #     for t in tokens:

    def create_inverted_index(self, contents):
        # my_index = []
        my_dictionary = {}  # you can change it to a dictionary which means term id, term
        doc_len_dict = {}
        # {'Maryam': [idf, {doc1: tf, doc2: tf, ...}]}
        # or
        # {'Maryam': pl}
        # class pl: idf, map = {} =========> map = {doc1: tf, doc2: tf, ....}
        for doc_id, content in enumerate(contents):
            final_tokens_of_a_sentence = self.preprocessor.preprocess(content)
            # self.create_index(final_tokens_of_a_sentence, doc_id)
            for index_of_a_token, token in enumerate(final_tokens_of_a_sentence):

                # if token in my_dictionary.keys():
                if token in my_dictionary:
                    pl_object = my_dictionary[token]
                    if doc_id in pl_object.my_map.keys():
                        pl_object.add_tf(doc_id)
                    else:
                        pl_object.new_doc_id(doc_id)
                # 'maryam': docid:1: tf = 1, idf = 1
                # 'maryam: docid = 1: tf = 2, idf = 1
                # 'nika': doc
                else:
                    tfidf_pl = TfIdfPostingsList()
                    tfidf_pl.new_doc_id(doc_id)
                    my_dictionary[token] = tfidf_pl

                temp_dict = {}
                # {'maryam' => pl}
                # {docid=1:{'token': tf, 'nika': tf22}}
                temp_dict[token] = temp_dict.get(token, 0) + 1
                doc_len_dict[doc_id] = temp_dict

        self.docs_lengths = doc_len_dict
        my_dictionary = self.sort_tokens(my_dictionary)
        # my_dictionary = collections.OrderedDict(sorted(my_dictionary.items()))
        return my_dictionary

    @staticmethod
    def sort_tokens(input_dict):
        return collections.OrderedDict(sorted(input_dict.items()))

    def create_query_freq_dictionary(self, query):
        query_freq = {}
        tokenized_query = self.preprocessor.preprocess(query)
        # {'mary':tf}
        for t in tokenized_query:
            query_freq[t] = query_freq.get(t, 0) + 1

        self.query_freq_dictionary = query_freq

    def find_similarity(self):
        scores = {}
        # footsal asia footsal
        # {'footsal':2 , 'asia':tf2}
        # lnc.ltc
        # logarithm_doc_tf, logarithm_query_tf
        # w_tf_q = logq, w_idf_q = logidfd, w_tf_doc=logtf, w_idf_doc=idf
        for qterm in self.query_freq_dictionary.keys():
            w_tf_q = 1 + math.log(self.query_freq_dictionary[qterm], 10)
            qterm_postings_list_object = self.main_inv_index.get(qterm)
            if qterm_postings_list_object is None: continue

            qterm_map = qterm_postings_list_object.my_map
            # qterm_docs = qterm_map.keys()
            w_idf = math.log(self.number_of_docs / qterm_postings_list_object.idf, 10)
            w_q = w_tf_q * w_idf
            # {docid: tf, doc2:tf2, doc3: tf3}
            for doc, tf in qterm_map.items():
                w_tf_d = 1 + math.log(tf, 10)
                scores[doc] = scores.get(doc, 0) + (w_q * w_tf_d)

        for doc in scores.keys():
            length = 0

            # {docid=1:{'token': tf, 'nika': tf22}}
            for tf in self.docs_lengths[doc].values():
                length += (1 + math.log(tf, 10)) ** 2
            length = math.sqrt(length)
            scores[doc] = scores.get(doc, 0) / length
        print(scores)
        return scores

    def find_similarity_with_champion_list(self, champions_list):
        scores = {}
        for qterm in self.query_freq_dictionary.keys():
            w_tf_q = 1 + math.log(self.query_freq_dictionary[qterm], 10)
            qterm_postings_list_object = champions_list.get(qterm)
            if qterm_postings_list_object is None: continue
            qterm_map = qterm_postings_list_object.my_map
            # qterm_docs = qterm_map.keys()
            idf = math.log(self.number_of_docs / qterm_postings_list_object.idf, 10)
            w_q = w_tf_q * idf

            for doc, tf in qterm_map.items():
                w_tf_d = 1 + math.log(tf, 10)
                scores[doc] = scores.get(doc, 0) + (w_q * w_tf_d)

        if len(scores) < self.k_answers:
            scores = self.find_similarity()

        for doc in scores.keys():
            length = 0
            for tf in self.docs_lengths[doc].values():
                length += (1 + math.log(tf, 10)) ** 2
            length = math.sqrt(length)
            scores[doc] = scores.get(doc, 0) / length
        print(scores)
        return scores

    def create_champions_list(self):
        champion_list_size = 12
        inv_ind_copy = self.main_inv_index.copy()
        champions_list = {}
        # {'maryam': 1..20} => {'maryam': 1..10}
        # {'mary':obj => idf, my_map = {doc:tf1, doc2:tf2}}
        # object.my_map = sorted_dict[1..10]
        for t, v in inv_ind_copy.items():
            # champions_list[t] = []
            sorted_dict = dict(sorted(v.my_map.items(), key=operator.itemgetter(1), reverse=True))
            sorted_dict = dict(itertools.islice(sorted_dict.items(), champion_list_size))
            tfidf_pl = TfIdfPostingsList()
            tfidf_pl.my_map = sorted_dict
            tfidf_pl.idf = v.idf
            champions_list[t] = tfidf_pl
            # champions_list[t].append()[:champion_list_size]

        return champions_list

    def select_k_top_results_with_heap(self, scores):
        best_results = []
        heap = []
        # {doc:score}
        for doc, score in scores.items():
            s = -score
            # Heap elements can be tuples.
            # This is useful for assigning comparison values (such as task priorities)
            # alongside the main record being tracked
            # for more information go to this website: https://docs.python.org/3/library/heapq.html

            heapq.heappush(heap, (s, doc))
        for i in range(min(self.k_answers, len(heap))):
            score_doc_tuple = heapq.heappop(heap)
            real_score = -score_doc_tuple[0]
            doc = score_doc_tuple[1]
            best_results.append((real_score, doc))
        return best_results

    def get_results_links(self, top_k_scores, all_data):
        top_k_results = {}
        # top_k_results = []
        for a in top_k_scores:
            doc = a[1]
            score = a[0]
            v = f"{doc}"
            doc_link = all_data[v]["url"]
            doclinks_scores_tuple = (doc_link, score)
            top_k_results[doc] = doclinks_scores_tuple
            # top_k_results.append(doc_link)
        return top_k_results

    def execute(self):
        # all_data = {}
        all_data, contents = self.read_data()

        # print(all_data)

        self.main_inv_index = self.create_inverted_index(contents)
        # print(dictionary)
        for k in self.main_inv_index:
            print("")
            print(f'{k}-> {self.main_inv_index[k].my_map}         {self.main_inv_index[k].idf}')
            for val in self.main_inv_index[k].my_map.keys():
                v = f"{val}"
                print(f' {all_data[v]["url"]} + {all_data[v]["title"]}')

        q = "فوتبال آسیا"
        self.test(q, all_data)
        q = "جام باشگاه های آسیا"
        self.test(q, all_data)
        q = "بوندسلیگا"
        self.test(q,all_data)
        q = "پیمان رضایی و آیدین رحمانی"
        self.test(q, all_data)

    def test(self, q, all_data):
        self.create_query_freq_dictionary(q)
        scoress = self.find_similarity()
        print("")
        print("-------------------------------- USING CHAMPIONS LIST -----------------------------------")
        print("")
        champions_list = self.create_champions_list()
        final_scores = self.find_similarity_with_champion_list(champions_list)
        top_k_doc_scores = self.select_k_top_results_with_heap(final_scores)
        top_k_doclink_scores = phase2.get_results_links(top_k_doc_scores, all_data)
        print(top_k_doclink_scores)


if __name__ == '__main__':
    phase2 = Phase2()
    phase2.execute()
    # q = "فوتسال آسیا"
    # phase2.create_query_freq_dictionary(q)
    # scores = phase2.find_similarity()
    # print("")
    # print("-------------------------------- USING CHAMPIONS LIST -----------------------------------")
    # print("")
    # champions_list = phase2.create_champions_list()
    # final_scores = phase2.find_similarity_with_champion_list(champions_list)
    # topk_doc_scores = phase2.select_k_top_results_with_heap(final_scores)
    # phase2.get_results_links(topk_doc_scores, all_data)
    #
    # print(final_links)
