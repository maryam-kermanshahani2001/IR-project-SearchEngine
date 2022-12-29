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

    def execute(self, query, postings_list):
        processed_query_list = self.query_preprocess(query)
        if len(processed_query_list) == 1:
            print(processed_query_list[0])
            for term in postings_list:
                if term == processed_query_list[0]:
                    return postings_list[term].my_map

