import tkinter

from .canvas import Canvas


class Workspace:
    def __init__(self, x, y, width, height, title=None, alpha=None):
        self.root = tkinter.Tk()
        if title is not None:
            self.root.title(title)
        self.root.geometry('%ux%u+%u+%u' % (width, height, x, y))
        if alpha is not None:
            self.root.attributes('-alpha', alpha)

        self.canvas = Canvas(self)

    def mainloop(self):
        self.root.mainloop()

    def add_rectangle(self, *args, **kwargs):
        return self.canvas.add_rectangle(*args, **kwargs)

    def add_text(self, *args, **kwargs):
        return self.canvas.add_text(*args, **kwargs)

    def _mouse_moved(self, event):
        self._mouse_moved_handler(self, event.x, event.y)

    def register_mouse_moved(self, handler):
        self._mouse_moved_handler = handler
        self.root.bind('<Motion>', self._mouse_moved)
