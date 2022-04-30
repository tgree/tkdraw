class Document:
    def __init__(self):
        self.elems = []

    def elem_add(self, elem):
        print('%s added.' % elem)
        self.elems.append(elem)

    @staticmethod
    def elems_translated(elems, dv):
        print('%u elems translated by %s.' % (len(elems), dv))
