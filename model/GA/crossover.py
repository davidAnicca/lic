from .chromosome import Chromosome

from typing import Optional

def combine(mother: 'Chromosome', father: 'Chromosome', cross_point: int) -> Optional['Chromosome']:
    # sanity: lungimi compatibile și cp în interval
    if len(mother.ruld) != len(father.ruld): 
        return None
    if not (0 <= cross_point <= len(mother.ruld)):
        return None

    # 1) ruld = prefix(mamă) + sufix(tată)
    prefix_ruld = mother.ruld[:cross_point]
    suffix_ruld = father.ruld[cross_point:]
    ruld = prefix_ruld + suffix_ruld

    # 2) prefixul coordonatelor: primele cross_point+1 poziții
    xs = mother.xs[:cross_point+1]
    ys = mother.ys[:cross_point+1]

    # 3) reconstruiește sufixul coordonatelor pas-cu-pas
    visited = set(zip(xs, ys))
    x, y = xs[-1], ys[-1]

    for step in suffix_ruld:
        dx, dy = moves[step]
        x += dx; y += dy
        if (x, y) in visited:   # self-avoid încalcat → copil invalid
            return None
        xs.append(x); ys.append(y)
        visited.add((x, y))

    # 4) construiește copilul
    child = Chromosome()
    child.cp(ruld, xs, ys)      # cp doar setează câmpurile
    return child                # SAW a fost verificat în bucla de mai sus
