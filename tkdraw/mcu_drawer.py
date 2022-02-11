import argparse

import tkdraw


HILITED_RECT = None


def mouse_moved_handler(ws, x, y):
    global HILITED_RECT

    if HILITED_RECT is not None:
        if HILITED_RECT.contains(x, y):
            return
        HILITED_RECT.set_fill('')
        HILITED_RECT = None

    for e in ws.canvas.elems:
        if not isinstance(e, tkdraw.Rectangle):
            continue
        if e.contains(x, y):
            HILITED_RECT = e
            e.set_fill('white')
            return


def main(args):
    # Dimension and padding for the main square of the MCU.  Pad squares will
    # appear in the pad area.
    pad = 200
    l   = 25
    d   = 2*l*12 + l

    ws = tkdraw.Workspace(args.x_pos, args.y_pos,
                          d + 2*l + 2*pad, d + 2*l + 2*pad,
                          title=args.title, alpha=args.alpha)

    m = ws.add_rectangle(pad, pad, d, d)
    for i in range(12):
        # Top row
        r = ws.add_rectangle(m.x + l*(2*i + 1), m.y - l, l, l)
        ws.add_text(r.x, r.y + r.height, font=('Helvetica', 9), text='PA%u' % i,
                    anchor='sw', angle=90)

        # Left row.
        r = ws.add_rectangle(m.x - l, m.y + l*(2*i + 1), l, l)
        ws.add_text(r.x + r.width, r.y, font=('Helvetica', 9), text='PB%u' % i,
                    anchor='se')

        # Bottom row.
        r = ws.add_rectangle(m.x + l*(2*i + 1), m.y + m.height, l, l)
        ws.add_text(r.x, r.y, font=('Helvetica', 9), text='PD%u' % i,
                    anchor='se', angle=90)

        # Right row.
        r = ws.add_rectangle(m.x + m.width, m.y + l*(2*i + 1), l, l)
        ws.add_text(r.x + 1, r.y, font=('Helvetica', 9), text='PD%u' % i,
                    anchor='sw')

    ws.register_mouse_moved(mouse_moved_handler)
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
