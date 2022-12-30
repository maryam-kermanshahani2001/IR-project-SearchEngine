from inverted_index import InvertedIndex
from query_processor import QueryProcess


class SearchEngine:
    def __init__(self):
        self.data_preprocess = InvertedIndex()
        self.query_processor = QueryProcess()

    def execute(self, input_query):
        postings_list = self.data_preprocess.execute()
        docs = self.query_processor.execute(input_query, postings_list)
        print(docs)


se = SearchEngine()
se.execute('"گرامیداشت کرونا"')
