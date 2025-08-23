import random
from .utils import moves, directions, corners
from model.GA import utils


class Chromosome:
    def __init__(self):
        self.ruld = ""
        self.xs = []
        self.ys = []
        self.valid = False

    def cp(self, ruld: str, xs: list, ys: list):
        self.ruld = ruld
        self.xs = xs
        self.ys = ys
        self.valid = True

    def change(self, poz: int) -> None:

        original_ruld = self.ruld[:]
        original_xs = self.xs[:]
        original_ys = self.ys[:]

        if self.change_with_rotation(poz) and utils.is_valid(self, self.ruld):
            return
        
        self.ruld = original_ruld
        self.xs = original_xs
        self.ys = original_ys
        
        n = len(self.ruld)
        if poz < 0 or poz >= n:
            return
        
        current_direction = original_ruld[poz]

        checked = []
        while len(checked) < 4:
            new_direction = random.choice(directions)
            if new_direction != current_direction:
                suffix = original_ruld[poz + 1 :]
                new_ruld = original_ruld[:poz] + new_direction + suffix
                x = y = 0
                xs = [0]
                ys = [0]
                visited = {(0, 0)}
                valid = True
                checked.append(new_direction)

                for step in new_ruld:
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
                    self.ruld = new_ruld
                    self.xs = xs
                    self.ys = ys
                    return

        self.ruld = original_ruld
        self.xs = original_xs
        self.ys = original_ys

    def diagonal(self) -> None:
        n = len(self.ruld)
        if n < 3:
            return

        for i in range(n - 2):
            subseq = self.ruld[i : i + 3]
            pattern = "".join(subseq)
            if pattern in corners:
                a, b, c = subseq
                new_triplet = a + c + b
                cand_ruld = self.ruld[:i] + new_triplet + self.ruld[i + 3 :]

                xs = [0]
                ys = [0]
                x = 0
                y = 0
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
                    self.ruld = cand_ruld
                    self.xs = xs
                    self.ys = ys
                    return

    def generate(self, string_len: int) -> bool:
        self.ruld = ""
        self.xs = [0]
        self.ys = [0]
        x = y = 0
        visited = {(0, 0)}
        first_direction = "R"
        dx, dy = moves[first_direction]
        x += dx
        y += dy
        self.ruld += first_direction
        self.xs.append(x)
        self.ys.append(y)
        visited.add((x, y))
        for _ in range(string_len - 1):
            candidates = []
            available_directions = directions[:]
            random.shuffle(available_directions)
            for direction in available_directions:
                dx, dy = moves[direction]
                nx, ny = x + dx, y + dy
                if (nx, ny) not in visited:
                    candidates.append((direction, nx, ny))

            if not candidates:
                self.ruld = ""
                self.xs.clear()
                self.ys.clear()
                return False

            direction, x, y = random.choice(candidates)
            self.ruld += direction
            self.xs.append(x)
            self.ys.append(y)
            visited.add((x, y))

        return True

    def _recompute_and_validate(self, ruld: str) -> tuple[bool, list[int], list[int]]:
        x = y = 0
        xs = [0]
        ys = [0]
        visited = {(0, 0)}
        for step in ruld:
            dx, dy = moves[step]
            x += dx
            y += dy
            if (x, y) in visited:
                return False, [], []
            xs.append(x)
            ys.append(y)
            visited.add((x, y))
        return True, xs, ys

    def change_with_rotation(self, poz: int) -> bool:
        n = len(self.ruld)
        if poz < 0 or poz >= n:
            return False

        original_ruld = self.ruld[:]
        original_xs   = self.xs[:]
        original_ys   = self.ys[:]

        cur = original_ruld[poz]

        candidates = [d for d in directions if d != cur]
        random.shuffle(candidates)  

        prefix = original_ruld[:poz]
        suffix = original_ruld[poz+1:]

        for cand in candidates:
            k = (directions.index(cand) - directions.index(cur)) % 4
            rotated_suffix = utils.rotate_suffix_clockwise(suffix, k)
            new_ruld = prefix + cand + rotated_suffix

            valid, xs, ys = self._recompute_and_validate(new_ruld)
            if valid:
                self.ruld, self.xs, self.ys = new_ruld, xs, ys
                return True

        self.ruld, self.xs, self.ys = original_ruld, original_xs, original_ys
        return False
