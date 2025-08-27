import re

def validate(G, P, M, K, E, input_hp, bounds: dict):
    errs = []
    if not (bounds["G_MIN"] <= G <= bounds["G_MAX"]):
        errs.append(
            f"Generations number {G} is outside [{bounds['G_MIN']}, {bounds['G_MAX']}]"
        )

    if not (bounds["P_MIN"] <= P <= bounds["P_MAX"]):
        errs.append(
            f"Population size {P} is outside [{bounds['P_MIN']}, {bounds['P_MAX']}]"
        )

    if not (0 < M < 1):
        errs.append(f"Mutation rate {M} must be strictly between 0 and 1")
    if not (bounds["MU_MIN"] <= M <= bounds["MU_MAX"]):
        errs.append(f"Mutation {M} outside [{bounds['MU_MIN']}, {bounds['MU_MAX']}]")

    if E < bounds["E_MIN"] or E >= P:
        errs.append(f"Elitism {E} invalid: must be >= {bounds['E_MIN']} and < {P}")

    if K < bounds["K_MIN"] or K >= P:
        errs.append(
            f"Tournament size {K} invalid: must be >= {bounds['K_MIN']} and < {P}"
        )

    import re

    if not isinstance(input_hp, str) or not re.fullmatch(r"[HP]+", input_hp):
        errs.append("Input sequence must be non-empty string of H/P")

    return errs
