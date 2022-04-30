class Document:
    def __init__(self):
        self.elems = []

    def elem_add(self, elem):
        print('%s added.' % elem)
        self.elems.append(elem)

    def elems_delete(self, elems):
        print('%u elems deleted.' % len(elems))
        for e in elems:
            self.elems.remove(e)

    @staticmethod
    def elems_translated(elems, dv):
        print('%u elems translated by %s.' % (len(elems), dv))

    @staticmethod
    def elem_handle_dragged(elem, index, h0, h1):
        print('%s handle %u dragged from %s to %s.' % (elem, index, h0, h1))
