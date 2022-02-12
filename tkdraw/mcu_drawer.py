import argparse

import tkdraw


GRID_SIZE    = 12
HILITED_RECT = None
DRAG_RECT    = None
DRAG_DX      = None
DRAG_DY      = None
FONT         = ('Helvetica', 12)
FONT_PIN_NUM = ('Helvetica', 9)
MCU_PINS     = 48
RECT_FILL    = 'white'
HILITE_FILL  = 'lightgreen'
PIN_ELEMS    = []


def mouse_moved_handler(ws, x, y):
    global HILITED_RECT
    global PIN_ELEMS
    global DRAG_RECT

    if DRAG_RECT is not None:
        drag_mouse_moved_handler(ws, x, y)
        return

    closest  = PIN_ELEMS[-1]
    distance = closest.distance_squared(x, y)
    for e in reversed(PIN_ELEMS):
        d = e.distance_squared(x, y)
        if d < distance:
            distance = d
            closest  = e

    if HILITED_RECT is not None:
        if closest == HILITED_RECT:
            return
        HILITED_RECT.set_fill(RECT_FILL)
        HILITED_RECT = None

    HILITED_RECT = closest
    closest.set_fill(HILITE_FILL)
    return


def mouse_down_handler(ws, x, y):
    global HILITED_RECT
    global DRAG_RECT
    global DRAG_DX
    global DRAG_DY

    if HILITED_RECT is None or not HILITED_RECT.contains(x, y):
        return

    DRAG_RECT = HILITED_RECT
    DRAG_DX   = x - HILITED_RECT.x
    DRAG_DY   = y - HILITED_RECT.y



def mouse_up_handler(ws, x, y):
    global HILITED_RECT
    global DRAG_RECT

    DRAG_RECT = None


def drag_mouse_moved_handler(ws, x, y):
    assert DRAG_RECT is not None
    x = (x // GRID_SIZE) * GRID_SIZE
    y = (y // GRID_SIZE) * GRID_SIZE
    DRAG_RECT.move_to(x, y)


def main(args):
    global PIN_ELEMS

    # Dimension and padding for the main square of the MCU.  Pad squares will
    # appear in the pad area.
    pad  = 200
    pins = MCU_PINS // 4
    l    = GRID_SIZE
    pl   = l * 3 / 2
    d    = 2*l*pins + l

    ws = tkdraw.Workspace(args.x_pos, args.y_pos,
                          d + 2*l + 2*pad, d + 2*l + 2*pad,
                          title=args.title, alpha=args.alpha)

    m = ws.add_rectangle(pad, pad, d, d, fill=RECT_FILL)
    for i in range(pins):
        # Top row
        r = ws.add_rectangle(m.x + l*(2*i + 1), m.y - pl, l, pl, fill=RECT_FILL)
        ws.add_text(r.x + r.width / 2, r.y, font=FONT, text='PA%u' % i,
                    anchor='w', angle=90)
        ws.add_text(r.x + r.width / 2 + 1, r.y + r.height / 2,
                    font=FONT_PIN_NUM, text='%u' % (3*pins + pins - i),
                    anchor='c', angle=90)
        PIN_ELEMS.append(r)

        # Left row.
        r = ws.add_rectangle(m.x - pl, m.y + l*(2*i + 1), pl, l, fill=RECT_FILL)
        ws.add_text(r.x, r.y + r.height / 2, font=FONT, text='PB%u' % i,
                    anchor='e')
        ws.add_text(r.x + r.width / 2 + 1, r.y + r.height / 2 + 1,
                    font=FONT_PIN_NUM, text='%u' % (i + 1), anchor='c')
        PIN_ELEMS.append(r)

        # Bottom row.
        r = ws.add_rectangle(m.x + l*(2*i + 1), m.y + m.height, l, pl,
                             fill=RECT_FILL)
        ws.add_text(r.x + r.width / 2, r.y + r.height + 1, font=FONT,
                    text='PD%u' % i, anchor='e', angle=90)
        ws.add_text(r.x + r.width / 2 + 1, r.y + r.height / 2,
                    font=FONT_PIN_NUM, text='%u' % (pins + i + 1), anchor='c',
                    angle=90)
        PIN_ELEMS.append(r)

        # Right row.
        r = ws.add_rectangle(m.x + m.width, m.y + l*(2*i + 1), pl, l,
                             fill=RECT_FILL)
        ws.add_text(r.x + r.width + 1, r.y + r.height / 2, font=FONT,
                    text='PD%u' % i, anchor='w')
        ws.add_text(r.x + r.width / 2 + 1, r.y + r.height / 2 + 1,
                    font=FONT_PIN_NUM, text='%u' % (2*pins + pins - i),
                    anchor='c')
        PIN_ELEMS.append(r)

    ws.register_mouse_moved(mouse_moved_handler)
    ws.register_mouse_down(mouse_down_handler)
    ws.register_mouse_up(mouse_up_handler)
    ws.mainloop()


def _main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--alpha', type=float)
    parser.add_argument('--title')
    parser.add_argument('--x-pos', '-x', type=int, default=50)
    parser.add_argument('--y-pos', '-y', type=int, default=50)
    main(parser.parse_args())


if __name__ == '__main__':
    _main()
