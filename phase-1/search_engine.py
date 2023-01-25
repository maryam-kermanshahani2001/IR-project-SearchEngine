from inverted_index import InvertedIndex
from query_processor import QueryProcess


class SearchEngine:
    def __init__(self):
        self.data_preprocess = InvertedIndex()
        self.query_processor = QueryProcess()

    def execute(self, input_query):
        # main_dict = self.data_preprocess.execute()
        # docs = self.query_processor.execute(input_query, postings_list)
        # # docs = self.query_processor.execute(input_query, main_dict, )
        # print(docs[:10])
        postings_list = self.data_preprocess.execute()
        docs = self.query_processor.phrase_query_search(postings_list, input_query)
        print(docs)
        print(docs[:10])


se = SearchEngine()
# se.execute('تحریم های آمریکا علیه ایران')  # [0, 2, 3, 5, 8]
# se.execute('تحریم های آمریکا ! ایران')  # []
# se.execute('" باشگاه های فوتسال آسیا "')

# se.execute('" باشگاه های فوتسال"')
se.execute('"شکست سنگین"')

# se.execute(' باشگاه های فوتسال آسیا ')
# se.execute('" مسابقات فوتبال "')
# se.execute(' مسابقات  فوتبال ')
# se.execute('" اورشلیم صهیونیست "')
# se.execute('" مسابقات "')

