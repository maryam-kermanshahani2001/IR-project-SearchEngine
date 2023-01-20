class DocPos:
    # my_map = {}

    # docId = ""
    # positionsList = []

    def __init__(self):
        # self.doc_id = doc_id
        self.my_map = {}
<<<<<<< Updated upstream:phase-1/doc_pos.py
        self.frequency = 0
        # self.positions = []
        # pass
=======
>>>>>>> Stashed changes:doc_pos.py

    # def add_doc(self, doc_id):
    #     self.docId = doc_id

<<<<<<< Updated upstream:phase-1/doc_pos.py
    def new_doc_id(self, doc_id, position):
        positions = [position]
        self.my_map[doc_id] = positions
        self.frequency += 1
=======
    def new_doc_id(self, doc_Id, position):
        positions = [position]
        self.my_map[doc_Id] = positions
>>>>>>> Stashed changes:doc_pos.py

    def add_position(self, doc_id, position):
        positions = self.my_map[doc_id]
        positions.append(position)
        self.frequency += 1

