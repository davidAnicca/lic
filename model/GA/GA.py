# model/GA/main_engine.py
import random
from typing import Optional, List, Tuple
from .chromosome import Chromosome
from .utils import moves, is_valid, fitness

class GeneticSAW:
    @staticmethod
    def run(
        raw: str,
        population_size: int = 1000,
        generations: int = 10,
        mutation_rate: float = 0.3,
        tournament_k: int = 3,
        elitism: Optional[int] = None,
        rng_seed: Optional[int] = None,
        verbose: bool = False,
    ) -> Tuple[Chromosome, int]:
        """Rulează GA și întoarce (best_chromosome, best_fitness)."""
        if rng_seed is not None:
            random.seed(rng_seed)

        gene_len = len(raw)
        elitism = max(1, (elitism if elitism is not None else population_size // 200))

        # populatie inițială validă
        population: List[Chromosome] = []
        while len(population) < population_size:
            c = Chromosome()
            if c.generate(gene_len):
                population.append(c)

        # evoluție
        for g in range(generations):
            if verbose:
                print("generation:", g)

            fits = [fitness(c, raw) for c in population]
            elite_idxs = sorted(range(len(population)), key=lambda i: fits[i])[:elitism]
            new_population = [population[i] for i in elite_idxs]

            while len(new_population) < population_size:
                mom = GeneticSAW._tournament_select(population, fits, k=tournament_k)
                dad = GeneticSAW._tournament_select(population, fits, k=tournament_k)

                child = GeneticSAW._make_child(mom, dad, gene_len, raw)
                if not is_valid(child, raw):
                    child = GeneticSAW._make_child(mom, dad, gene_len, raw)

                try:
                    GeneticSAW._mutate(child, mutation_rate)
                    if not is_valid(child, raw):
                        child = GeneticSAW._make_child(mom, dad, gene_len, raw)
                except Exception:
                    child = GeneticSAW._make_child(mom, dad, gene_len, raw)

                new_population.append(child)

            population = new_population

        final_fits = [fitness(c, raw) for c in population]
        best_idx = min(range(len(population)), key=lambda i: final_fits[i])
        return population[best_idx], final_fits[best_idx]

    @staticmethod
    def _combine(mother: 'Chromosome', father: 'Chromosome', cross_point: int) -> Optional['Chromosome']:
        if len(mother.ruld) != len(father.ruld):
            return None
        if not (0 <= cross_point <= len(mother.ruld)):
            return None

        prefix_ruld = mother.ruld[:cross_point]
        suffix_ruld = father.ruld[cross_point:]
        ruld = prefix_ruld + suffix_ruld

        xs = mother.xs[:cross_point + 1]
        ys = mother.ys[:cross_point + 1]
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

        n = len(mother.xs)
        if len(xs) != n or len(ys) != n or len(ruld) != n - 1:
            return None

        child = Chromosome()
        child.cp(ruld, xs, ys)
        return child

    @staticmethod
    def _tournament_select(pop: List['Chromosome'], fits: List[int], k: int = 3) -> 'Chromosome':
        idxs = random.sample(range(len(pop)), k)
        best_idx = min(idxs, key=lambda i: fits[i])
        return pop[best_idx]

    @staticmethod
    def _mutate(ch: 'Chromosome', mutation_rate: float) -> None:
        if random.random() < mutation_rate and len(ch.ruld) > 1:
            position = random.randrange(1, len(ch.ruld))
            ch.change(position)
        if random.random() < mutation_rate:
            ch.diagonal()

    @staticmethod
    def _make_child(mom, dad, gene_len, raw, max_tries=10):
        for _ in range(max_tries):
            cp = random.randint(1, gene_len - 2)
            child = GeneticSAW._combine(mom, dad, cp)
            if child is not None and is_valid(child, raw):
                return child
        # fallback: generare random validă
        while True:
            child = Chromosome()
            if child.generate(gene_len) and is_valid(child, raw):
                return child