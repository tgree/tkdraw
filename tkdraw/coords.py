'''
Utility methods for dealing with the grid in the canvas.  The canvas has fixed
padding around the four edges and the workspace ensures that when resizing the
window it can only go in multiples of the grid size.
'''
from . import geom


GRID_SPACING = 10
GRID_PAD     = (GRID_SPACING // 2)
GRID_PAD_DV  = geom.Vec(GRID_PAD, GRID_PAD)


def canvasx_floor(x):
    '''
    Given an X point in canvas coordinates, floor it to the nearest multiple of
    the grid spacing.
    '''
    return x - (x % GRID_SPACING)


def canvasy_floor(y):
    '''
    Given a Y point in canvas coordinates, floor it to the nearest multiple of
    the grid spacing.
    '''
    return y - (y % GRID_SPACING)


def canvasx_to_gridx_floor(x):
    '''
    Given an X point on the canvas in mouse coordinates, convert it to an
    integral grid coordinate.  The conversion rounds coordinates down, so
    yields the left edge of the grid rectangle containing the mouse.
    '''
    return (x - GRID_PAD) // GRID_SPACING


def canvasy_to_gridy_floor(y):
    '''
    Given a Y point on the canvas in mouse coordinates, convert it to an
    integral grid coordinate.  The conversion rounds coordinates down, so
    yields the top edge of the grid rectangle containing the mouse.
    '''
    return (y - GRID_PAD) // GRID_SPACING


def canvasx_to_gridx_float(x):
    '''
    Given an X point on the canvas in mouse coordinates, convert it to the
    equivalent point in grid coordinates, as a floating-point number that is
    not rounded to a grid point.
    '''
    return (x - GRID_PAD) / GRID_SPACING


def canvasy_to_gridy_float(y):
    '''
    Given a Y point on the canvas in mouse coordinates, convert it to the
    equivalent point in grid coordinates, as a floating-point number that is
    not rounded to a grid point.
    '''
    return (y - GRID_PAD) / GRID_SPACING


def canvasx_to_gridx_round(x):
    '''
    Given an X point on the canvas in mouse coordinates, convert it to an
    integral grid coordinate.  The conversion rounds to the nearest grid point.
    '''
    return round(canvasx_to_gridx_float(x))


def canvasy_to_gridy_round(y):
    '''
    Given a Y point on the canvas in mouse coordinates, convert it to an
    integral grid coordinate.  The conversion rounds to the nearest grid point.
    '''
    return round(canvasy_to_gridy_float(y))


def canvas_to_grid_floor(x, y):
    '''
    Given a point on the canvas in mouse coordinates, convert it to an integral
    grid coordinate.  The conversion rounds coordinates down, so yields the
    top-left point of the grid rectangle containing the mouse.

    Returns a tuple (x', y').
    '''
    return (canvasx_to_gridx_floor(x), canvasy_to_gridy_floor(y))


def canvas_to_grid_round(x, y):
    '''
    Given a point on the canvas in mouse coordinates, convert it to an integral
    grid coordinate.  The conversion rounds to the nearest grid point.

    Returns a tuple (x', y').
    '''
    return (canvasx_to_gridx_round(x), canvasy_to_gridy_round(y))


def gridx_to_canvasx(x):
    '''
    Given an X point in grid coordinates, convert it to a canvas mouse point.
    '''
    return x * GRID_SPACING + GRID_PAD


def gridy_to_canvasy(y):
    '''
    Given a Y point in grid coordinates, convert it to a canvas mouse point.
    '''
    return y * GRID_SPACING + GRID_PAD


def gridp_to_canvasp(p):
    '''
    Given a geom.Vec in grid coordinates, convert it to a canvas mouse point.
    '''
    return p * GRID_SPACING + GRID_PAD_DV


def grid_to_canvas(x, y):
    '''
    Given a point in grid coordinates, convert the point to canvas mouse
    coordinates.

    Returns a tuple (x', y').
    '''
    return (gridx_to_canvasx(x), gridy_to_canvasy(y))


def grid_to_canvas_delta(d):
    '''
    Convert a delta value in grid units to canvas units.
    '''
    return d * GRID_SPACING


def get_canvas_h_bands(w, h):
    '''
    Given the canvas width and height, returns a list of rectangles
    (x, y, w, h) in canvas coordinates that should be used to subdivide the
    black fill into horizontal bands, including the pad rectangle at the top.
    '''
    rs = [(0, 0, w, GRID_PAD)]
    for y in range(h // GRID_SPACING + 1):
        rs.append((0, gridy_to_canvasy(y) + 1, w, GRID_SPACING - 1))
    return rs


def get_canvas_v_bands(w, h):
    '''
    Given the canvas width and height, returns a list of rectangles
    (x, y, w, h) in canvas coordinates that should be used to subdivide the
    black fill into vertical bands, including the pad rectangle on the left.
    '''
    rs = [(0, 0, GRID_PAD, h)]
    for x in range(w // GRID_SPACING + 1):
        rs.append((gridx_to_canvasx(x) + 1, 0, GRID_SPACING - 1, h))
    return rs
