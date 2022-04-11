class Tool:
    def __init__(self, workspace):
        self.workspace = workspace

    def handle_app_activated(self):
        '''
        Called when the application becomes the frontmost app.
        '''
        raise NotImplementedError

    def handle_app_deactivated(self):
        '''
        Called when some other application becomes the frontmost app.
        '''
        raise NotImplementedError

    def handle_tool_selected(self):
        '''
        The user has selected the tool and it is now active.
        '''
        raise NotImplementedError

    def handle_tool_deselected(self):
        '''
        The tool is no longer active; the user has switched to some other tool.
        '''
        raise NotImplementedError

    def handle_canvas_entered(self):
        '''
        The mouse has entered the canvas.
        '''
        raise NotImplementedError

    def handle_canvas_exited(self):
        '''
        The mouse has left the canvas.
        '''
        raise NotImplementedError

    def handle_key_pressed(self, e):
        '''
        A key has been pressed.
        '''
        raise NotImplementedError

    def handle_mouse_down(self, x, y):
        '''
        Handle a mouse down at grid coordinate (x, y) in the canvas.  Note that
        these need to be converted to screen coordinates before drawing
        anything.
        '''
        raise NotImplementedError

    def handle_mouse_up(self, x, y):
        '''
        Handle a mouse up at grid coordinate (x, y) in the canvas.  Note that
        these need to be converted to screen coordinates before drawing
        anything.
        '''
        raise NotImplementedError

    def handle_mouse_moved(self, x, y):
        '''
        Handle a mouse moved event to coordinate (x, y) in the canvas.
        '''
        raise NotImplementedError
