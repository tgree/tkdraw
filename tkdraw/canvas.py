import tkinter


class Elem:
    def __init__(self, canvas, elem_id, x, y, width=None, height=None):
        self.canvas  = canvas
        self.elem_id = elem_id
        self.x       = x
        self.y       = y
        if width is not None:
            self.width = width
        if height is not None:
            self.height = height


class Rectangle(Elem):
    def __init__(self, canvas, x, y, width, height, **kwargs):
        elem_id = canvas.canvas.create_rectangle(
                (x, y, x + width, y + height), **kwargs)
        super().__init__(canvas, elem_id, x, y, width=width, height=height)

    def contains(self, x, y):
        return (self.x <= x <= self.x + self.width and
                self.y <= y <= self.y + self.height)

    def set_fill(self, fill):
        self.canvas.canvas.itemconfig(self.elem_id, fill=fill)


class Text(Elem):
    def __init__(self, canvas, x, y, **kwargs):
        elem_id = canvas.canvas.create_text((x, y), **kwargs)
        super().__init__(canvas, elem_id, x, y)


class Canvas:
    def __init__(self, workspace):
        self.workspace = workspace
        self.canvas = tkinter.Canvas(workspace.root, bd=0,
                                     highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)
        self.elems = []

    def add_rectangle(self, x, y, width, height, **kwargs):
        r = Rectangle(self, x, y, width, height, **kwargs)
        self.elems.append(r)
        return r

    def add_text(self, x, y, **kwargs):
        t = Text(self, x, y, **kwargs)
        self.elems.append(t)
        return t
