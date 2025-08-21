import datetime
import glob
import json
import os
import time
import matplotlib
from matplotlib.figure import Figure

from model.GA.chromosome import Chromosome
from model.GA.matri import create_lattice_diagram, create_visual


FILES_DIR = "static/results/"

def get_time_stamp():
    return time.time()

def cleanup_and_prepare():
    if not os.path.isdir(FILES_DIR):
        os.makedirs(FILES_DIR)
    else:
        for filename in glob.glob(os.path.join(FILES_DIR, '*')):
            os.remove(filename)

def save_image(fig: Figure, image_name) -> str:
    plotfile = os.path.join(FILES_DIR, f"{image_name}.png")
    fig.savefig(plotfile)
    return plotfile

def save_data(input_array, G, P, M, A, K, E, score, best: Chromosome, run_time):
    cleanup_and_prepare()
    file_name = get_time_stamp()

    visual = create_visual(input_array, best.ruld)

    figure = create_lattice_diagram(visual)
    image_path = save_image(figure, file_name)

    meta_filename = f"{file_name}.json"
    meta_data_files = os.path.join(FILES_DIR, meta_filename)

    payload = {
        "created-at": datetime.datetime.now().isoformat(timespec="seconds") + "Z",
        "result": {
            "score": score,
            "image_name": f'{file_name}.png',
        },
        "best-result": {
            "ruld": getattr(best, "ruld", ""),
            "xs": getattr(best, "xs", []),
            "ys": getattr(best, "ys", []),
            "valid": getattr(best, "valid", False),
        },
        "hyperparameters": {
            "generations": G,
            "population_size": P,
            "mutation_rate": M,
            "rng_seed": 42,
            "tournament_k": K,
            "elitism": E,
            "input_sequence": input_array,
        },
        "performance": {
            "runtime": run_time
        }
    }

    with open(meta_data_files, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=4)

    return image_path