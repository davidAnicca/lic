from .chromosome import Chromosome
from .utils import moves

from typing import Optional


def combine(
    mother: "Chromosome", father: "Chromosome", cross_point: int
) -> Optional["Chromosome"]:
    if len(mother.ruld) != len(father.ruld):
        return None
    if not (0 <= cross_point <= len(mother.ruld)):
        return None

    prefix_ruld = mother.ruld[:cross_point]
    suffix_ruld = father.ruld[cross_point:]
    ruld = prefix_ruld + suffix_ruld

    xs = mother.xs[: cross_point + 1]
    ys = mother.ys[: cross_point + 1]

    visited = set(zip(xs, ys))
    x, y = xs[-1], ys[-1]

    for step in suffix_ruld:
        dx, dy = moves[step]
        x += dx
        y += dy
        if (x, y) in visited:
            return None
        xs.append(x)
        ys.append(y)
        visited.add((x, y))

    child = Chromosome()
    child.cp(ruld, xs, ys)
    return child
