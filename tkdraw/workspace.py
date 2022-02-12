import tkinter

from .canvas import Canvas


class Workspace:
    def __init__(self, geometry=None, title=None, alpha=None, tcl=None):
        if tcl is not None:
            self.root = tcl
            tcl.loadtk()
        else:
            self.root = tkinter.Tk()
        if title is not None:
            self.root.title(title)
        if alpha is not None:
            self.root.attributes('-alpha', alpha)
        if geometry is not None:
            self.set_geometry(*geometry)

    def set_geometry(self, x, y, width, height):
        self.root.geometry('%ux%u+%u+%u' % (width, height, x, y))

    def mainloop(self):
        self.root.mainloop()

    def add_canvas(self, width, height, column=0, row=0, sticky=None):
        return Canvas(self, width, height, column, row, sticky)

    def register_handler(self, event_type, handler):
        self.root.bind(event_type, lambda e: handler(self, e, e.x, e.y))

    def register_mouse_moved(self, handler):
        self.register_handler('<Motion>', handler)

    def register_mouse_down(self, handler):
        self.register_handler('<Button-1>', handler)

    def register_mouse_up(self, handler):
        self.register_handler('<ButtonRelease-1>', handler)
