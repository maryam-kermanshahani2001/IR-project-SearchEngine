import re
from preprocess import DataPreprocess


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
        if not_query_word != '':
            self.process_not_query(not_query_word, postings_list)

        return containing_list


