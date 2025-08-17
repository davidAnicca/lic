import random
from typing import Optional, List, Tuple
from chromosome import Chromosome
from utils import *

# --- Crossover (1-punct) cu validare ---
def combine(mother: 'Chromosome', father: 'Chromosome', cross_point: int) -> Optional['Chromosome']:
    # sanity (opțional, dar util în dev)
    if len(mother.ruld) != len(father.ruld):
        return None
    if not (0 <= cross_point <= len(mother.ruld)):
        return None

    # 1) prefixul direcțiilor vine din mamă; sufixul din tată
    prefix_ruld = mother.ruld[:cross_point]
    suffix_ruld = father.ruld[cross_point:]
    ruld = prefix_ruld + suffix_ruld

    # 2) prefixul coordonatelor: primele (cross_point+1) poziții
    #    (pozițiile sunt cu una mai multe decât pașii)
    xs = mother.xs[:cross_point + 1]
    ys = mother.ys[:cross_point + 1]

    # 3) reconstruiește sufixul coordonatelor pas-cu-pas din ultima poziție a prefixului
    visited = set(zip(xs, ys))
    x, y = xs[-1], ys[-1]

    for step in suffix_ruld:
        dx, dy = moves[step]
        x += dx
        y += dy
        if (x, y) in visited:       # auto-evitare încălcată → copil invalid
            return None
        xs.append(x)
        ys.append(y)
        visited.add((x, y))

    # 4) (opțional) verificări de lungime/coerență
    #    len(ruld) = n-1, len(xs)=len(ys)=n. Folosim n dedus din mamă.
    n = len(mother.xs)
    if len(xs) != n or len(ys) != n or len(ruld) != n - 1:
        return None

    # 5) construiește copilul
    child = Chromosome()
    child.cp(ruld, xs, ys)  # cp doar setează câmpurile; SAW a fost verificat deja
    return child

# --- Selecție: turneu de mărime k ---
def tournament_select(pop: List['Chromosome'], fits: List[int], k: int = 3) -> 'Chromosome':
    idxs = random.sample(range(len(pop)), k)
    best_idx = max(idxs, key=lambda i: fits[i])
    return pop[best_idx]

# --- Mutații cu probabilitate dată ---
def mutate(ch: 'Chromosome', mutation_rate: float) -> None:
    # schimbare pe o poziție internă (evită 0)
    if random.random() < mutation_rate and len(ch.ruld) > 1:
        position = random.randrange(1, len(ch.ruld)-1)
        ch.change(position)   # asigură-te că suportă poz==1..n-1
    if random.random() < mutation_rate:
        ch.diagonal()         # asigură-te că păstrează lungimea și reconstruiește xs/ys

# --- Reproducere: încearcă să creezi un copil valid; dacă eșuează, regenerează ---
def make_child(mom, dad, gene_len, raw, max_tries=10):
    for _ in range(max_tries):
        cp = random.randint(1, gene_len-1)
        child = combine(mom, dad, cp)      # combine reconstruiește xs/ys din ruld
        if child is not None and is_valid(child, raw):
            return child
    # fallback: regenerează până iese valid
    while True:
        child = Chromosome()
        if child.generate(gene_len) and is_valid(child, raw):
            return child

# --- GA principal ---
def genetic_saw(
    raw: str,
    population_size: int = 1000,
    generations: int = 10,
    mutation_rate: float = 0.3,
    tournament_k: int = 3,
    elitism: int = 5,
    rng_seed: Optional[int] = None
) -> Tuple['Chromosome', int]:
    """
    Returnează cel mai bun cromozom și scorul lui.
    """
    if rng_seed is not None:
        random.seed(rng_seed)

    gene_len = len(raw)  # lungimea inputului pentru generate()

    # 1) Inițializare
    population: List[Chromosome] = []
    while len(population) < population_size:
        c = Chromosome()
        if c.generate(gene_len):
            population.append(c)

    # 2) Evoluție
    for g in range(generations):
        print("generation : ", g)
        fits = [fitness(c, raw) for c in population]

        # Elitism: păstrăm cei mai buni 'elitism'
        elite_idxs = sorted(range(len(population)), key=lambda i: fits[i])[:elitism]
        new_population = [population[i] for i in elite_idxs]

        # Reproducere până completăm populația
        while len(new_population) < population_size:
            mom = tournament_select(population, fits, k=tournament_k)
            dad = tournament_select(population, fits, k=tournament_k)

            child = make_child(mom, dad, gene_len, raw)

            # sanity înainte de mutații
            if not is_valid(child, raw):
            # n-ar trebui să se întâmple; defensive
                child = make_child(mom, dad, gene_len, raw)

            try:
                mutate(child, mutation_rate)
                # dacă mutația a încălcat invarianta, refă copilul
                if not is_valid(child, raw):
                    child = make_child(mom, dad, gene_len, raw)
            except Exception as e:
                # log util, dar NU păstra acest copil
                print("MUTATE_ERR:", repr(e))
                child = make_child(mom, dad, gene_len, raw)

            new_population.append(child)

        population = new_population

    # 3) Rezultat
    final_fits = [fitness(c, raw) for c in population]
    best_idx = min(range(len(population)), key=lambda i: final_fits[i])
    return population[best_idx], final_fits[best_idx]

# ---- Exemplu de rulare cu valorile date ----
if __name__ == "__main__":
    generations = 100
    population_size = 10000
    input_array = "HPPHPPPHPPHPPPPHHHHHPPP"
    mutation_rate = 0.2

    best, score = genetic_saw(
        raw=input_array,
        population_size=population_size,
        generations=generations,
        mutation_rate=mutation_rate,
        rng_seed=42,           # reproducibil
    )

    visual = create_visual(input_array, best.ruld)
    print(visual)

    print("Best score:", score)
    # dacă Chromosome are o reprezentare utilă, poți printa direct 'best'
    # altfel:
    print("ruld:", best.ruld)
    print("xs:", best.xs)
    print("ys:", best.ys)
