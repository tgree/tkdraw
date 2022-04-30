from enum import Enum

from .tool import Tool
from .. import geom
from .. import icons


ARROW_DV = {
    'Left'  : geom.Vec(-1,  0),
    'Right' : geom.Vec( 1,  0),
    'Up'    : geom.Vec( 0, -1),
    'Down'  : geom.Vec( 0,  1),
}


class State(Enum):
    IDLE              = 0
    DRAG_ELEM_STARTED = 1     # Clicked on an elem and dragging
    RECT_STARTED      = 2     # Clicked in open space and doing selection rect


class SelectionTool(Tool):
    def __init__(self, workspace, R, *args, **kwargs):
        super().__init__(workspace, R, *args, **kwargs)
        self.state            = State.IDLE
        self.nearest_elem     = None
        self.nearest_points   = []
        self.selected_elems   = set()
        self.selected_points  = []
        self.last_mouse_point = None
        self.drag_p0          = None
        self.drag_p1          = None

        self.select_rect        = None
        self.select_rect_elem   = None
        self.select_rect_elems  = set()
        self.select_rect_points = []

        workspace.tool_canvas.add_poly(icons.arrow.get_vertices(R),
                                       fill='black')

    def _add_handle_points(self, elems_set, points_list):
        R = geom.Rect.square(4)
        for se in elems_set:
            for h in se.handles:
                points_list.append(self.workspace.add_fine_rectangle(
                    h, R, fill='black'))

    def _remove_handle_points(self, points_list):
        for p in points_list:
            self.workspace.delete_canvas_elem(p)
        points_list.clear()

    def _add_selected_points(self):
        self._add_handle_points(self.selected_elems, self.selected_points)

    def _remove_selected_points(self):
        self._remove_handle_points(self.selected_points)

    def _update_selected_points(self):
        self._remove_selected_points()
        self._add_selected_points()

    def _add_select_rect_points(self):
        self._add_handle_points(self.select_rect_elems, self.select_rect_points)

    def _remove_select_rect_points(self):
        self._remove_handle_points(self.select_rect_points)

    def _add_nearest_points(self, p):
        if not self.workspace.doc.elems:
            return

        nearest_elem = None
        nearest_nn   = None
        for e in self.workspace.doc.elems:
            v  = geom.Vec(p.ex, p.ey)
            dv = e.nearest_point(v) - v
            nn = dv.norm_squared()
            if not nearest_elem or nn < nearest_nn:
                nearest_elem, nearest_nn = e, nn

        if nearest_nn >= 4:
            self._remove_nearest_points()
            self.nearest_elem = None
            return

        if nearest_elem == self.nearest_elem:
            return

        self._remove_nearest_points()
        self.nearest_elem = nearest_elem
        R = geom.Rect.square(6)
        for h in self.nearest_elem.handles:
            self.nearest_points.append(self.workspace.add_fine_rectangle(h, R))

    def _remove_nearest_points(self):
        self._remove_handle_points(self.nearest_points)

    def _translate_elems(self, elems, dv):
        if not dv:
            return

        for e in elems:
            e.translate(dv)

        self._update_selected_points()
        if self.nearest_elem:
            self._remove_nearest_points()
            self.nearest_elem = None
        if self.last_mouse_point:
            self._add_nearest_points(self.last_mouse_point)

    def _start_drag_elem(self, p):
        self.state   = State.DRAG_ELEM_STARTED
        self.drag_p0 = p
        self.drag_p1 = p

    def _start_selection_rect(self, p):
        assert self.state == State.IDLE
        assert not self.select_rect_elems
        assert not self.select_rect_points

        self.state            = State.RECT_STARTED
        self.select_rect      = geom.Rect(p, p)
        self.select_rect_elem = self.workspace.add_rectangle(
                self.select_rect, outline='gray')

    def _stop_selection_rect(self):
        assert self.state == State.RECT_STARTED
        self._remove_select_rect_points()
        self.workspace.delete_canvas_elem(self.select_rect_elem)
        self.select_rect_elems.clear()
        self.select_rect      = None
        self.select_rect_elem = None
        self.state            = State.IDLE

    def handle_app_activated(self):
        pass

    def handle_app_deactivated(self):
        if self.state == State.RECT_STARTED:
            self._remove_select_rect_points()
            self.select_rect_elems.clear()
            self.workspace.delete_canvas_elem(self.select_rect_elem)
            self.select_rect      = None
            self.select_rect_elem = None
            self.state            = State.IDLE

    def handle_tool_selected(self):
        self.icon_border.configure(outline='black')

    def handle_tool_deselected(self):
        assert self.state == State.IDLE

        self._remove_nearest_points()
        self.nearest_elem     = None
        self.last_mouse_point = None
        self._remove_selected_points()
        self.selected_elems.clear()
        self.icon_border.configure(outline='#CCCCCC')

    def handle_canvas_entered(self, p):
        self.handle_mouse_moved(p)

    def handle_canvas_exited(self):
        self._remove_nearest_points()
        self.nearest_elem     = None
        self.last_mouse_point = None

    def handle_key_pressed(self, e):
        dv = ARROW_DV.get(e.keysym)
        if dv is not None:
            self._translate_elems(self.selected_elems, dv)
            self.workspace.doc.elems_translated(self.selected_elems, dv)
        elif e.keysym == 'Escape':
            self.handle_esc_pressed()

    def handle_esc_pressed(self):
        if self.state == State.IDLE:
            self._remove_selected_points()
            self.selected_elems.clear()
        elif self.state == State.DRAG_ELEM_STARTED:
            dv = self.drag_p0 - self.drag_p1
            self._translate_elems(self.selected_elems, dv)
            self.drag_p0 = None
            self.drag_p1 = None
            self.state   = State.IDLE
        elif self.state == State.RECT_STARTED:
            self._stop_selection_rect()

    def handle_mouse_down(self, p):
        assert self.state == State.IDLE

        shift_click = (p.modifiers & 1)
        if shift_click:
            if not self.nearest_elem:
                self._start_selection_rect(p)
            elif self.nearest_elem in self.selected_elems:
                self.selected_elems.discard(self.nearest_elem)
            else:
                self.selected_elems.add(self.nearest_elem)
                self._start_drag_elem(p)
        else:
            if not self.nearest_elem:
                self.selected_elems.clear()
                self._start_selection_rect(p)
            elif self.nearest_elem not in self.selected_elems:
                self.selected_elems.clear()
                self.selected_elems.add(self.nearest_elem)
                self._start_drag_elem(p)
            else:
                self._start_drag_elem(p)

        self._update_selected_points()

    def handle_mouse_up(self, p):
        if self.state == State.DRAG_ELEM_STARTED:
            dv = self.drag_p1 - self.drag_p0
            if dv and self.selected_elems:
                self.workspace.doc.elems_translated(self.selected_elems, dv)
            self.state = State.IDLE
        elif self.state == State.RECT_STARTED:
            self.selected_elems.update(self.select_rect_elems)
            self._update_selected_points()
            self._stop_selection_rect()

    def handle_mouse_moved(self, p):
        self.last_mouse_point = p
        if self.state == State.IDLE:
            self._add_nearest_points(p)
        elif self.state == State.DRAG_ELEM_STARTED:
            self._translate_elems(self.selected_elems, p - self.drag_p1)
            self.drag_p1 = p
        elif self.state == State.RECT_STARTED:
            self.select_rect = geom.Rect(self.select_rect.p0, p)
            self.workspace.delete_canvas_elem(self.select_rect_elem)

            self.select_rect_elem = self.workspace.add_rectangle(
                    self.select_rect, outline='gray')

            self._remove_select_rect_points()
            self.select_rect_elems.clear()
            for e in self.workspace.doc.elems:
                if e.overlaps_rect(self.select_rect):
                    self.select_rect_elems.add(e)
            self._add_select_rect_points()
