from .tool import Tool


class NullTool(Tool):
    def handle_app_activated(self):
        pass

    def handle_app_deactivated(self):
        pass

    def handle_tool_selected(self):
        self.icon_border.configure(outline='black')

    def handle_tool_deselected(self):
        self.icon_border.configure(outline='#CCCCCC')

    def handle_canvas_entered(self):
        pass

    def handle_canvas_exited(self):
        pass

    def handle_key_pressed(self, e):
        pass

    def handle_mouse_down(self, x, y):
        pass

    def handle_mouse_up(self, x, y):
        pass

    def handle_mouse_moved(self, x, y):
        pass
