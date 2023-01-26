from inverted_index import InvertedIndex
from query_processor import QueryProcess


class SearchEngine:
    def __init__(self):
        self.data_preprocess = InvertedIndex()
        self.query_processor = QueryProcess()

    def execute(self, input_query):
        main_dict, contents, urls = self.data_preprocess.execute()
        docs = self.query_processor.execute(input_query, main_dict)
        for doc in docs[:10]:
            print(urls[doc])
            print(contents[doc])


se = SearchEngine()
# se.execute('تحریم های آمریکا علیه ایران')  # [2388, 2788, 6845, 6926, 6929, 6942, 6945, 6959, 6963, 6996]
# se.execute('تحریم های آمریکا ! ایران')  # [] #[6256, 6878, 6938, 7261, 7268, 7328, 7491, 7615, 7627, 8063]
# se.execute('" باشگاه های فوتسال آسیا "')

# se.execute('" باشگاه های فوتسال"')
se.execute('"شکست سنگین"')

# se.execute(' باشگاه های فوتسال آسیا ')
# se.execute('" مسابقات فوتبال "')
# se.execute(' مسابقات  فوتبال ')
# se.execute(' اورشلیم ! صهیونیست ') # []
# se.execute('" مسابقات "')

