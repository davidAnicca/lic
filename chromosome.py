import random
from utils import moves, directions, rotate_ruld_string, corners

class Chromosome:
    def __init__(self):
        # firstly, the chromosome is empty
        self.ruld = ''
        self.xs = []
        self.ys = []
        self.valid = False

    def cp(self, ruld: str, xs: list, ys: list):
        self.ruld = ruld
        self.xs = xs
        self.ys = ys
        self.valid = True

    def change(self, poz: int) -> None:
        n = len(self.ruld)
        if poz < 0 or poz >= n:
            return  # index invalid

        # copii defensive (evităm aliasing)
        original_ruld = self.ruld[:]          # list copy
        original_xs   = self.xs[:]            # list copy
        original_ys   = self.ys[:]            # list copy

        cur = original_ruld[poz]
        # încearcă toate direcțiile diferite de cea curentă
        for new_dir in (d for d in directions if d != cur):
            # dacă ai nevoie de o rotire a sufixului, aplic-o aici;
            # altfel lăsăm sufixul așa cum e:
            suffix = original_ruld[poz+1:]
            cand_ruld = original_ruld[:poz] + new_dir + suffix

            # Rebuild complet și verificare SAW din mers
            x = y = 0
            xs = [0]
            ys = [0]
            visited = {(0, 0)}
            valid = True

            for step in cand_ruld:
                dx, dy = moves[step]
                x += dx
                y += dy
                if (x, y) in visited:
                    valid = False
                    break
                xs.append(x)
                ys.append(y)
                visited.add((x, y))

            if valid:
                # acceptă candidatul și păstrează structura consistentă
                self.ruld = cand_ruld
                self.xs = xs
                self.ys = ys
                return

        # dacă nimic nu merge, revino la starea inițială (de fapt am păstrat-o deja)
        self.ruld = original_ruld
        self.xs = original_xs
        self.ys = original_ys
    

    def diagonal(self) -> None:
        n = len(self.ruld)
        if n < 3:
            return

        # corners ca set de stringuri e ok; facem pattern din subseq cu ''.join
        # exemplu: corners = {'UUR','UUL',...}

        for i in range(n - 2):
            subseq = self.ruld[i:i+3]            # ex: ['U','U','R']
            pattern = ''.join(subseq)
            if pattern in corners:
                # înlocuim tripleta (a,b,c) cu (a,c,b) — cum aveai tu
                a, b, c = subseq
                new_triplet = a+c+b

                # candidate ruld
                cand_ruld = self.ruld[:i] + new_triplet + self.ruld[i+3:]  # ← i+3:

                # reconstruim coordonatele de la început până la capăt, SAW din mers
                xs = [0]; ys = [0]; x = 0; y = 0
                visited = {(0, 0)}
                valid = True
                for step in cand_ruld:
                    dx, dy = moves[step]
                    x += dx; y += dy
                    if (x, y) in visited:
                        valid = False
                        break
                    xs.append(x); ys.append(y)
                    visited.add((x, y))

                if valid:
                    self.ruld = cand_ruld
                    self.xs = xs
                    self.ys = ys
                    return

        # dacă nu s-a putut aplica nicio diagonalizare validă, ieșim fără modificări
            
    def generate(self, string_len: int) -> bool:
        self.ruld = ''
        self.xs = [0]
        self.ys = [0]

        x = y = 0
        visited = {(0, 0)}

        # pasul 1 (forțat)
        d = 'R'
        dx, dy = moves[d]
        x += dx; y += dy
        self.ruld += d
        self.xs.append(x); self.ys.append(y)
        visited.add((x, y))

        # mai ai de făcut exact string_len - 2 pași
        for _ in range(string_len - 2):
            candidates = []
            for d in directions:
                dx, dy = moves[d]
                nx, ny = x + dx, y + dy
                if (nx, ny) not in visited:
                    candidates.append((d, nx, ny))

            if not candidates:
                self.ruld = ''; self.xs.clear(); self.ys.clear()
                return False

            d, x, y = random.choice(candidates)
            self.ruld += d
            self.xs.append(x); self.ys.append(y)
            visited.add((x, y))

        return True
    

    def check(self) -> bool:
        visited = set()
        for position in zip(self.xs, self.ys):
            if position in visited:
                return False
            visited.add(position)
        return True
    