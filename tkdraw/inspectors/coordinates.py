class CoordinatesInspector:
    def __init__(self, inspect_canvas, ncoords):
        self.inspect_canvas = inspect_canvas
        self.ncoords        = ncoords

        if ncoords > 1:
            inspect_canvas.iadd_header('COORDINATES')
            self.field_names = ['P%u:' % i for i in range(ncoords)]
        else:
            inspect_canvas.iadd_header('POSITION')
            self.field_names = ['P:']

        self.coord_text_elems = [
            inspect_canvas.iadd_field(n) for n in self.field_names]

    def set_coord(self, index, p):
        p_text = (' (%s, %s)' % (p.x, p.y)) if p is not None else ''
        self.coord_text_elems[index].set_text(
            '%s%s' % (self.field_names[index], p_text))
