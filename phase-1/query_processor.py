import re
import sys

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
    def process_one_word_query(query_list, postings_list):
        for term in postings_list:
            if term == query_list[0]:
                return postings_list[term].my_map.key()

    @staticmethod
    def process_multi_word_query(query_list, postings_list):
        combined_docs_list = []
        for i, query_term in enumerate(query_list):
            for term in postings_list:
                if term == query_term:
                    combined_docs_list.append(list(postings_list[term].my_map.keys()))
        result_list = []
        for doc_list in combined_docs_list:
            if not result_list:
                result_list = doc_list
            else:
                result_list = list(set(result_list) & set(doc_list))
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
                else:
                    return ''

    @staticmethod
    def process_not_query(query, postings_list, shared_docs):
        containing_docs = []
        for term in postings_list:
            if term == query:
                containing_docs = postings_list[term].my_map.keys()
        return [a_i - b_i for a_i, b_i in zip(shared_docs, containing_docs)]

    @staticmethod
    def find_phrase_query(query):
        result = re.findall('"([^"]*)"', query)
        if not result:
            return ''
        else:
            return result

    @staticmethod
    def process_phrase_query(query_list, postings_list):
        combined_docs_dict_list = []
        combined_docs_list = []
        for i, query_term in enumerate(query_list):
            for term in postings_list:
                if term == query_term:
                    combined_docs_dict_list.append(postings_list[term].my_map)
                    combined_docs_list.append(list(postings_list[term].my_map.keys()))
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
                    doc_id_positions.append(doc_dict[doc_id][0])
            doc_pos_dict[doc_id] = doc_id_positions
        phrase_satisfaction_list = []

        for doc in doc_pos_dict:
            flag = 0
            positions = doc_pos_dict[doc]
            if positions:
                for pos in range(len(positions) - 1):
                    if (positions[pos] + 1) != positions[pos + 1]:
                        flag = 1
                        break
            if not positions:
                flag = 1
            if flag == 0:
                phrase_satisfaction_list.append(doc)

        return phrase_satisfaction_list

    def execute(self, query, postings_list):
        containing_list = []
        not_query_word = self.find_not_subquery(query)
        phrase_part_query = self.find_phrase_query(query)

        processed_query_list = self.query_preprocess(query)
        if len(processed_query_list) == 1:
            containing_list = self.process_one_word_query(processed_query_list, postings_list)

        if phrase_part_query == '':
            if len(processed_query_list) > 1:
                containing_list = self.process_multi_word_query(processed_query_list, postings_list)
        if phrase_part_query != '':
            containing_list = self.process_phrase_query(processed_query_list, postings_list)
        if not_query_word != '':
            self.process_not_query(not_query_word, postings_list, containing_list)

        return containing_list

    def phrase_process(self, query_postings_list, inverted_index):

        match = []
        finger = sys.maxsize
        max_index = 0
        for q in query_postings_list:
            if q in inverted_index.keys():
                doc_pos_object = inverted_index.get(q)
                doc_pos_object_my_map = doc_pos_object.my_map
                resultList = list(map(list, doc_pos_object_my_map.items()))
                match.append(resultList)
                if list(doc_pos_object_my_map.keys())[0] < finger:
                    finger = list(doc_pos_object_my_map.keys())[0]
                if list(doc_pos_object_my_map.keys())[-1] > max_index:
                    max_index = list(doc_pos_object_my_map.keys())[-1]
        result = {}
        pointers = [0] * len(match)
        while finger <= max_index:
            count = 0
            for i in range(len(match)):
                if pointers[i] < len(match[i]) and finger == match[i][pointers[i]]:
                    pointers[i] += 1
                    count += 1
            doc_id_list = result.get(count, [])
            result[count] = sorted(doc_id_list + [finger])
            min = max_index + 1
            for i in range(len(match)):
                if pointers[i] < len(match[i]) and match[i][pointers[i]] < min:
                    min = match[i][pointers[i]]
            finger = min

        result = {k: v for k, v in reversed(sorted(result.items(), key=lambda item: item[0]))}
