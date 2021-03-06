from .tool import Tool


class NullTool(Tool):
    INSPECT_TITLE = 'NULL TOOL'

    def handle_app_activated(self):
        pass

    def handle_app_deactivated(self):
        pass

    def handle_tool_selected(self):
        self.icon_border.configure(outline='black')

    def handle_tool_deselected(self):
        self.icon_border.configure(outline='#CCCCCC')

    def handle_canvas_entered(self, p):
        pass

    def handle_canvas_exited(self):
        pass

    def handle_key_pressed(self, e):
        pass

    def handle_mouse_down(self, p):
        pass

    def handle_mouse_up(self, p):
        pass

    def handle_mouse_moved(self, p):
        pass

    def handle_elem_handles_changed(self, _elem, _handles):
        pass
