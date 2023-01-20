# from preprocessor import DataPreprocess
#
#
# class QueryProcessor:
#     def __init__(self):
#         self.preprocessor = DataPreprocess()
#         self.query_freq_dictionary = {}
#
#     def execute(self, query):
#         query_freq = {}
#         tokenized_query = self.preprocessor.preprocess(query)
#
#         for t in tokenized_query:
#             query_freq[t] = query_freq.get(t, 0) + 1
#
#         self.query_freq_dictionary = query_freq
#
#     def find_similarity(self):
#
#
# if __name__ == '__main__':
#     q = "تحریم هسته ای"
#     query_processor = QueryProcessor()
#     query_processor.execute(q)
