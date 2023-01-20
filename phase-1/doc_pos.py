class DocPos:
    # my_map = {}

    # docId = ""
    # positionsList = []

    def __init__(self):
        # self.doc_id = doc_id
        self.my_map = {}
        self.frequency = 0
        # self.positions = []
        # pass

    # def add_doc(self, doc_id):
    #     self.docId = doc_id

    def new_doc_id(self, doc_id, position):
        positions = [position]
        self.my_map[doc_id] = positions
        self.frequency += 1

    def add_position(self, doc_id, position):
        positions = self.my_map[doc_id]
        positions.append(position)
        self.frequency += 1

