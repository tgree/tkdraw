from .tool import Tool
from ..elems import TextElem
from ..inspectors import CoordinatesInspector


class TextTool(Tool):
    INSPECT_TITLE = 'TEXT TOOL'

    def __init__(self, workspace, R, *args, **kwargs):
        super().__init__(workspace, R, *args, **kwargs)
        self.icon_text = workspace.tool_canvas.add_text(
                R.p0 + (R.p1 - R.p0) / 2, text='T')

        self.coordinates_inspector = None

    def handle_app_activated(self):
        pass

    def handle_app_deactivated(self):
        pass

    def handle_tool_selected(self):
        self.icon_border.configure(outline='black')

        ic = self.workspace.inspect_canvas
        self.coordinates_inspector = CoordinatesInspector(ic, 1)

    def handle_tool_deselected(self):
        self.icon_border.configure(outline='#CCCCCC')

    def handle_canvas_entered(self, p):
        pass

    def handle_canvas_exited(self):
        pass

    def handle_key_pressed(self, e):
        pass

    def handle_mouse_down(self, p):
        e = TextElem(self.workspace, p, 'Terry\nis\nCOOOOOL')
        self.workspace.doc.elem_add(e)

    def handle_mouse_up(self, p):
        pass

    def handle_mouse_moved(self, p):
        self.coordinates_inspector.set_coord(0, p)

    def handle_elem_handles_changed(self, _elem, _handles):
        pass
