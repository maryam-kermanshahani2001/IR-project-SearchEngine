import re
import sys

import string
from preprocessor import DataPreprocess


class QueryProcess:
    def __init__(self):
        self.preprocess = DataPreprocess()

    def query_preprocess(self, query):
        normalized_query = self.preprocess.normalizing(query)
        tokens_of_query = self.preprocess.tokenizing(normalized_query)
        stemmed_query = self.preprocess.stemming(tokens_of_query)
        removed_stopwords_query = self.preprocess.stopwords_removing(stemmed_query)
        return self.preprocess.lemmatizing(removed_stopwords_query)

    @staticmethod
    def process_one_word_query(query_list, inverted_index_dict):
        for term in inverted_index_dict:
            if term == query_list[0]:
                return list(inverted_index_dict[term].my_map.keys())

    @staticmethod
    def process_multi_word_query(query_list, inverted_index_dict):
        word_doc_dict = {}
        for i, query_term in enumerate(query_list):
            for term in inverted_index_dict:
                if term == query_term:
                    word_doc_dict[term] = list(inverted_index_dict[term].my_map.keys())
        doc_count_per_having_words_dict = {}
        for doc_list in word_doc_dict.values():
            for doc_num in doc_list:
                if doc_num in doc_count_per_having_words_dict.keys():
                    doc_count_per_having_words_dict[doc_num] += 1
                else:
                    doc_count_per_having_words_dict[doc_num] = 1
        print(doc_count_per_having_words_dict)
        sorted_dict_based_on_word_count = dict(
            sorted(doc_count_per_having_words_dict.items(),
                   key=lambda x: x[1],
                   reverse=True)
        )
        result_list = list(sorted_dict_based_on_word_count.keys())
        return result_list

    @staticmethod
    def find_not_subquery(query):
        query_list = query.split()
        for i, term in enumerate(query_list):
            if term == '!':
                return query_list[i + 1]
            else:
                if '!' in term:
                    return query_list[i][1:]
        return ''

    @staticmethod
    def process_not_query(not_query, inverted_index_dict, shared_docs):
        containing_docs = []
        for term in inverted_index_dict:
            if term == not_query:
                containing_docs = inverted_index_dict[term].my_map.keys()

        shared_docs_copy = shared_docs.copy()
        for doc in shared_docs_copy:
            if doc in containing_docs:
                shared_docs.remove(doc)
        return shared_docs

    @staticmethod
    def find_phrase_query(query):
        result = re.findall('"([^"]*)"', query)
        if not result:
            return ''
        else:
            return result

    @staticmethod
    def process_two_word_phrase_query(query_list, inverted_index_dict):
        combined_docs_dict_list = []
        combined_docs_list = []
        for i, query_term in enumerate(query_list):
            doc_pos_object = inverted_index_dict.get(query_term)
            if doc_pos_object is None:
                continue
            combined_docs_dict_list.append(doc_pos_object.my_map)
            combined_docs_list.append(list(doc_pos_object.my_map.keys()))
        result_list = []
        for doc_list in combined_docs_list:
            if not result_list:
                result_list = doc_list
            else:
                result_list = list(set(result_list) & set(doc_list))

        doc_pos_dict = {}
        for doc_id in result_list:
            doc_id_positions = []
            for doc_dict in combined_docs_dict_list:
                if doc_id in doc_dict.keys():
                    doc_id_positions.append(doc_dict[doc_id])
            doc_pos_dict[doc_id] = doc_id_positions
        # print(doc_pos_dict)
        phrase_satisfaction_list = []

        for doc in doc_pos_dict:
            flag = 0
            positions = doc_pos_dict[doc]
            if positions:
                print(positions)
                for pos in range(len(positions) - 1):
                    flag = 0
                    first_word_pos = positions[pos]
                    second_word_pos = positions[pos + 1]

                    for i in range(len(first_word_pos)):
                        if flag != 1:
                            for j in range(len(second_word_pos)):
                                if (first_word_pos[i]) > second_word_pos[j]:
                                    continue
                                if (first_word_pos[i]) < second_word_pos[j]:
                                    if (first_word_pos[i] - second_word_pos[j]) == -1:
                                        print(first_word_pos[i], second_word_pos[j])
                                        flag = 1
                                        break

            if not positions:
                flag = 0
            if flag == 1:
                phrase_satisfaction_list.append(doc)

        return phrase_satisfaction_list

    def process_phrase_and_normal_query(self):
        pass

    @staticmethod
    def process_phrase_query(processed_query_list, inverted_index):
        words = []
        # processed_query_list = self.query_preprocess(query)
        for i, q in enumerate(processed_query_list):
            if q in inverted_index.keys():
                doc_pos_object_my_map = inverted_index.get(q).my_map
                # result_list = list(map(list, doc_pos_object_my_map.items()))
                # query_postings_list[q] = resultList
                # words[q] = doc_pos_object_my_map
                words.append(doc_pos_object_my_map)
                # words[i] = result_list
        # [{doc1: positions, doc2: positions}, {doc2:positions}, {doc5: positions}]
        flag = 1
        flag0 = 1
        flag1 = 1
        result = {}
        doc_index_per_word = [0] * len(words)
        for doc in words[0].keys():
            position_index_per_word = [0] * len(words)

            # for i, word in enumerate(words):
            #     if i == 0:
            #         continue
            i = 1
            flag1 = 1
            while flag1 != 0:
                word = words[i]
                flag0 = 1

                if doc == list(word)[doc_index_per_word[i]]:
                    if i == len(words) - 1:
                        for position in words[0].get(doc):
                            if flag0 == 0:
                                break

                            j = 1
                            flag = 1
                            while flag != 0:
                                # if j >= len(words):
                                #     break
                                # if i == 0:
                                #     continue
                                pw = words[j]
                                if position_index_per_word[j] >= len(pw.get(doc)):
                                    doc_index_per_word[i] += 1
                                    # i += 1
                                    flag0 = 0
                                    break
                                if position + j == pw.get(doc)[position_index_per_word[j]]:
                                    if j == len(words) - 1:

                                        temp_list = result.get(doc, [])
                                        temp_list.append(position)
                                        result[doc] = temp_list
                                        # doc_index_per_word[i] += 1
                                        # result[doc].append(position)
                                        flag = 0  # or break
                                        # todo 1 match found
                                    else:
                                        j += 1
                                        continue
                                else:
                                    if position > pw.get(doc)[position_index_per_word[j]]:
                                        position_index_per_word[j] += 1
                                        continue
                                    else:
                                        # doc_index_per_word[i] += 1
                                        flag = 0  # or break
                        # doc_index_per_word[i] += 1
                        flag1 = 0
                    else:
                        i += 1
                        continue
                else:
                    if doc > list(word)[doc_index_per_word[i]]:
                        doc_index_per_word[i] += 1
                        continue
                    else:
                        # flag1 = 0
                        break
        return list(result.keys())

    def execute(self, query, inverted_index_dict):
        containing_list = []
        phrase_part_query = self.find_phrase_query(query)
        not_query_word = self.find_not_subquery(query)

        cleaned_query = query.translate(str.maketrans('', '', string.punctuation))
        processed_query_list = self.query_preprocess(cleaned_query)

        containing_list = self.process_two_word_phrase_query(processed_query_list, inverted_index_dict)
        print(containing_list)
        # non_phrase_words_list = []
        # if phrase_part_query:
        #     for word in processed_query_list:
        #         if word not in phrase_part_query[0]:
        #             non_phrase_words_list.append(word)

        # if non_phrase_words_list and (phrase_part_query != ''):
        #     if (len(phrase_part_query[0].split()) == 1) and (len(non_phrase_words_list) == 1):
        #         print("==")
        #         containing_list = self.process_multi_word_query(processed_query_list, inverted_index_dict)
        #
        #     if (len(phrase_part_query[0].split()) > 1) and (len(non_phrase_words_list) == 1):
        #         print(">=")
        #         phrase_containing_list = self.process_two_word_phrase_query(phrase_part_query, inverted_index_dict)
        #         non_containing_list = self.process_one_word_query(non_phrase_words_list, inverted_index_dict)
        #         combined_docs_list = [phrase_containing_list, non_containing_list]
        #
        #         for doc_list in combined_docs_list:
        #             if not containing_list:
        #                 containing_list = doc_list
        #             else:
        #                 containing_list = list(set(containing_list) & set(doc_list))
        #
        #     if (len(phrase_part_query[0].split()) > 1) and (len(non_phrase_words_list) > 1):
        #         print(">>")
        #         phrase_containing_list = self.process_two_word_phrase_query(phrase_part_query, inverted_index_dict)
        #         non_containing_list = self.process_multi_word_query(non_phrase_words_list, inverted_index_dict)
        #         combined_docs_list = [phrase_containing_list, non_containing_list]
        #         containing_list = []
        #         for doc_list in combined_docs_list:
        #             if not containing_list:
        #                 containing_list = doc_list
        #             else:
        #                 containing_list = list(set(containing_list) & set(doc_list))
        #
        #     if (len(phrase_part_query[0].split()) == 1) and (len(non_phrase_words_list) > 1):
        #         print("=>")
        #         phrase_containing_list = self.process_one_word_query(phrase_part_query, inverted_index_dict)
        #         non_containing_list = self.process_multi_word_query(non_phrase_words_list, inverted_index_dict)
        #         combined_docs_list = [phrase_containing_list, non_containing_list]
        #         containing_list = []
        #         for doc_list in combined_docs_list:
        #             if not containing_list:
        #                 containing_list = doc_list
        #             else:
        #                 containing_list = list(set(containing_list) & set(doc_list))
        #
        # else:
        #     print("here")
        #     if len(processed_query_list) == 1:
        #         containing_list = self.process_one_word_query(processed_query_list, inverted_index_dict)
        #
        #     if phrase_part_query == '':
        #         if len(processed_query_list) > 1:
        #             containing_list = self.process_multi_word_query(processed_query_list, inverted_index_dict)
        #     if (phrase_part_query != '') and (len(phrase_part_query[0].split()) > 1):
        #         print(phrase_part_query[0].split())
        #         print("in phrase")
        #         containing_list = self.process_two_word_phrase_query(processed_query_list, inverted_index_dict)
        if not_query_word != '':
            containing_list = self.process_not_query(not_query_word, inverted_index_dict, containing_list)
            print(containing_list)

        return containing_list

    # def phrase_process(self, inverted_index, query):
    #     # query_postings_list = {}
    #     query_postings_map = {}
    #     processed_query_list = self.query_preprocess(query)
    #     for q in processed_query_list:
    #         if q in inverted_index.keys():
    #             doc_pos_object_my_map = inverted_index.get(q).my_map
    #             # resultList = list(map(list, doc_pos_object_my_map.items()))
    #             # query_postings_list[q] = resultList
    #             query_postings_map[q] = doc_pos_object_my_map
    #
    #     match = []
    #     finger = sys.maxsize
    #     max_index = 0
    #     start_index = 0
    #     # for q in query:
    #     for q, doc_pos_map in query_postings_map.items():
    #         # if q in inverted_index.keys():
    #         #     doc_pos_object = inverted_index.get(q)
    #         #     doc_pos_object_my_map = doc_pos_object.my_map
    #         #     resultList = list(map(list, doc_pos_object_my_map.items()))
    #         #     match.append(resultList)
    #         # doc_pos_list = list(doc_pos_map.keys())
    #         match.append(doc_pos_map)
    #         if list(doc_pos_map)[0] < finger:
    #             finger =  list(doc_pos_map)[0]
    #             start_index += 1
    #         if  list(doc_pos_map)[-1] > max_index:
    #             max_index =  list(doc_pos_map)[-1]
    #
    #     while finger <= max_index:

    def phrase_query_search(self, inverted_index, query):
        words = []
        processed_query_list = self.query_preprocess(query)
        for i, q in enumerate(processed_query_list):
            if q in inverted_index.keys():
                doc_pos_object_my_map = inverted_index.get(q).my_map
                words.append(doc_pos_object_my_map)

        flag = 1
        flag0 = 1
        flag2 = 1
        flag3 = 1
        flag_main = 1
        result = {}
        doc_index_per_word = [0] * len(words)
        for doc in words[0].keys():
            position_index_per_word = [0] * len(words)
            flag2 = 1
            # for i, word in enumerate(words):

            # if i == 0:
            #     continue
            # if flag2 == 0:
            #     break
            flag0 = 1
            i = 1
            while flag0 != 0:
                if flag2 == 0:
                    break
                word = words[1]
                if doc == list(word)[doc_index_per_word[i]]:
                    if i == len(words) - 1:
                        for position in words[0].get(doc):

                            j = 1
                            flag = 1
                            flag3 = 1
                            # for k, pw in enumerate(words):
                            #     if k == 0:
                            #         continue
                            #     if flag3 == 0:
                            #         break
                            while flag != 0:
                                if flag3 == 0:
                                    break
                                # if j >= len(words):
                                #     break
                                # if i == 0:
                                #     continue
                                pw = words[j]
                                # pw = words[k]
                                # if position_index_per_word[j] >= len(pw.get(doc)):
                                #     break
                                if position + j == pw.get(doc)[position_index_per_word[j]]:
                                    # if position + k == pw.get(doc)[position_index_per_word[k]]:
                                    if j == len(words) - 1:
                                        # if k == len(words) - 1:

                                        temp_list = result.get(doc, [])
                                        temp_list.append(position)
                                        result[doc] = temp_list
                                        # position_index_per_word[k] += 1 #todo check if it is right
                                        # result[doc].append(position)
                                        flag = 0  # or break
                                        # todo 1 match found
                                    else:
                                        j += 1
                                        # k += 1
                                        continue
                                else:
                                    if position > pw.get(doc)[position_index_per_word[j]]:
                                        # if position > pw.get(doc)[position_index_per_word[k]]:
                                        # position_index_per_word[j] += 1
                                        t = 1
                                        while t:
                                            if position_index_per_word[j] + 1 <= len(pw.get(doc)) - 1:
                                                position_index_per_word[j] += 1
                                            else:
                                                if position + j != pw.get(doc)[position_index_per_word[j]]:
                                                   flag3 = 0
                                                t = 0
                                                break
                                            # if position > list(pw)[position_index_per_word[j]]:
                                            if position + j == pw.get(doc)[position_index_per_word[j]]:
                                                t = 0
                                                break
                                            if position + j < pw.get(doc)[position_index_per_word[j]]:
                                                # flag2 = 0
                                                flag3 = 0
                                                break
                                        # continue
                                        # continue
                                    else:
                                        # flag = 0  # or break

                                        break
                        # here
                        for n in range(len(words)):
                            doc_index_per_word[n] += 1
                        flag0 = 0

                    else:
                        i += 1
                        continue
                else:
                    if doc > list(word)[doc_index_per_word[i]]:

                        t = 1
                        while t:
                            if doc_index_per_word[i] + 1 <= len(word) - 1:
                                doc_index_per_word[i] += 1
                            else:
                                if doc != list(word)[doc_index_per_word[i]]:
                                    flag2 = 0
                                t = 0
                                break
                            if doc == list(word)[doc_index_per_word[i]]:
                                t = 0
                                break
                            elif doc < list(word)[doc_index_per_word[i]]:
                                # flag2 = 0
                                flag2 = 0
                                break

                        # continue
                    else:
                        break
        return list(result.keys())
