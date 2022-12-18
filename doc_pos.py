class DocPos:
    # my_map = {}

    # docId = ""
    # positionsList = []

    def __init__(self):
        # self.doc_id = doc_id
        self.my_map = {}
        self.positions = []
        pass

    # def add_doc(self, doc_id):
    #     self.docId = doc_id

    def new_doc_id(self, doc_Id, position):
        # positions = []
        self.positions.append(position)
        self.my_map[doc_Id] = self.positions

    def add_position(self, doc_id, position):
        # self.positionsList.append(position)
        positions = self.my_map[doc_id]
        positions.append(position)
