class Raw:
    def __init__(self, raw_string: str):
        self.raw_string = raw_string
    


seen = set()
repeats = False

coords = [(1, 0), (2, 0), (3, 0), (4, 0), (4, 1), (3, 1), (2, 1), (2, 2), (1, 2), (1, 3), (2, 3), (1, 3), (1, 2), (1, 1), (0, 1), (0, 2), (0, 3), (-1, 3), (-1, 4), (-2, 4)]

for coord in coords:
    if coord in seen:
        repeats = True
        break
    seen.add(coord)

print("Does the list contain repeating coordinates?", repeats)