directions = ["R", "U", "L", "D"]
moves = {"R": (1, 0), "U": (0, 1), "L": (-1, 0), "D": (0, -1)}

corners = [
    "UUR",
    "UUL",
    "DDR",
    "DDL",
    "RRU",
    "RRD",
    "LLU",
    "LLD",
    "URU",
    "ULU",
    "DRD",
    "DLD",
    "RDR",
    "LUR",
    "LDL",
]


def rotate_char_clockwise(ch: str, k: int) -> str:
    i = directions.index(ch)
    return directions[(i + k) % 4]


def rotate_suffix_clockwise(suffix: str, k: int) -> str:
    if k % 4 == 0 or not suffix:
        return suffix
    return "".join(rotate_char_clockwise(ch, k) for ch in suffix)


def directions_to_steps(dirs: list):
    x, y = 0, 0
    xs = []
    ys = []
    for direction in dirs:
        dx, dy = directions[direction]
        x, y = dx + x, dy + y
        xs.append(x)
        ys.append(y)

    return xs, ys


def adjacent(a: tuple, b: tuple) -> bool:
    x1, y1 = a
    x2, y2 = b
    return (x1 == x2 and abs(y1 - y2) == 1) or (y1 == y2 and abs(x1 - x2) == 1)


def is_valid(ch, raw: str) -> bool:
    n = len(raw)
    if len(ch.ruld) != n or len(ch.xs) != n + 1 or len(ch.ys) != n + 1:
        return False

    x, y = ch.xs[0], ch.ys[0]
    seen = {(x, y)}
    for i, step in enumerate(ch.ruld):
        m = moves.get(step)
        if m is None:
            return False
        dx, dy = m
        x += dx
        y += dy
        if (x, y) in seen:
            return False
        if ch.xs[i + 1] != x or ch.ys[i + 1] != y:
            return False
        seen.add((x, y))
    return True


def fitness(ch, raw: str) -> int:
    if not is_valid(ch, raw):
        return 10**9

    n = len(raw)
    fit = 0
    for i in range(n):
        if raw[i] != "H":
            continue
        cx, cy = ch.xs[i], ch.ys[i]
        for j in range(n):
            if abs(i - j) <= 1 or raw[j] != "H":
                continue
            nx, ny = ch.xs[j], ch.ys[j]
            if adjacent((cx, cy), (nx, ny)):
                fit += 1
    return -fit // 2
