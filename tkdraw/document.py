class Document:
    def __init__(self):
        self.elems = []

    def elem_add(self, elem):
        print('%s added.' % elem)
        self.elems.append(elem)
