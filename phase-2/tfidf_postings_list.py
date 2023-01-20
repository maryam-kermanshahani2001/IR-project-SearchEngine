class TfIdfPostingsList:
    # TfIdfPostingsList = * idf, my_map = {docid: tf} *
    # main_dict = {'token' =   * idf, my_map = {docid: tf} *  }
    # maryam: 3:doc1: 5,doc2, doc3
    def __init__(self):
        self.my_map = {}
        self.idf = 0

    def new_doc_id(self, doc_id):
        self.idf += 1
        self.my_map[doc_id] = 1

    def add_tf(self, doc_id):
        self.my_map[doc_id] = self.my_map[doc_id] + 1
