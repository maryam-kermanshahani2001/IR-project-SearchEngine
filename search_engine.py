from preprocess import DataPreprocess
from query_processor import QueryProcess


class SearchEngine:
    def __init__(self):
        self.data_preprocess = DataPreprocess()
        self.query_processor = QueryProcess()

    def execute(self, input_query):
        # the main function that for each input query runs the process
        self.data_preprocess.execute()

        # return result
