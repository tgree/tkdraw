#!/usr/bin/env python3
from .workspace import Workspace


def main():
    ws = Workspace()
    ws.mainloop()


def _main():
    main()


if __name__ == '__main__':
    _main()
