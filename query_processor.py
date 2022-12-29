

class QueryProcess:
    def __init__(self):
        pass

    @staticmethod
    def execute(query, postings_list):
        query_words_list = query.split(' ')
        if len(query_words_list) == 1:
            for term in postings_list:
                if term == query_words_list[0]:
                    return postings_list[term].my_map

