import math


L   = 22
W   = 2.25
D   = 1.63

l   = L / math.sqrt(2)
r   = W / math.sin(3 * math.pi / 8)
R   = 2*l - L - r
Qdx = W * math.cos(math.pi / 8)
Qdy = W * math.sin(math.pi / 8)

ARROW_VERTICES = [
    (0,                0),
    (0,                L),
    (R / math.sqrt(2), L - R / math.sqrt(2)),
    (D*(L-l) - Qdx,    D*l + Qdy),
    (D*(L-l) + Qdx,    D*l - Qdy),
    (l - R,            l),
    (l,                l),
]
ARROW_WIDTH  = max(v[0] for v in ARROW_VERTICES)
ARROW_HEIGHT = max(v[1] for v in ARROW_VERTICES)


def get_vertices(_R):
    x = _R.p0.x + (_R.width - ARROW_WIDTH) // 2
    y = _R.p0.y + (_R.height - ARROW_HEIGHT) // 2
    return [(x + vx, y + vy) for (vx, vy) in ARROW_VERTICES]
