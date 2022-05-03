class TextEntryInspector:
    def __init__(self, workspace, elem=None):
        self.workspace = workspace
        self.elem      = elem

        workspace.inspect_canvas.iadd_header('TEXT')
        self.mentry = workspace.inspect_canvas.iadd_multiline_entry(nlines=6)

        if elem is not None:
            self.set_text(elem.text)

        self.mentry.bind('<<Modified>>', self._multiline_updated)
        self.mentry.bind('<KeyPress>', self._handle_key_pressed)

    def _handle_key_pressed(self, e):
        if e.keysym in ('Escape', 'Tab'):
            self.workspace.canvas.focus_set()
            return 'break'
        return None

    def focus_set(self):
        self.mentry.focus_set()

    def get_text(self):
        return self.mentry.get('1.0', 'end')[:-1]

    def set_text(self, text):
        self.mentry.replace('1.0', 'end', text)

    def _multiline_updated(self, _e):
        if self.elem is not None and self.mentry.edit_modified():
            self.mentry.edit_modified(False)
            self.elem.set_text(self.get_text())
