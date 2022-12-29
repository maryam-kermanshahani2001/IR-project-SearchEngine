from inverted_index import DataPreprocess
from query_processor import QueryProcess


class SearchEngine:
    def __init__(self):
        self.data_preprocess = DataPreprocess()
        self.query_processor = QueryProcess()

    def execute(self, input_query):
        data_proc = DataPreprocess()
        postings_list = data_proc.execute()
        self.query_processor.execute(input_query, postings_list)


