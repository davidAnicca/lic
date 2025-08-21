import datetime
import glob
import io
import json
import os
import time
import zipfile
from flask import Flask, current_app, render_template, request, send_file
from controller import validator
from model.GA.GA import GeneticSAW as GeneticAlgorithm
from model.GA.matri import create_lattice_diagram, create_visual
from model.persistence import persistence
from view.forms.form_model import InputForm

app = Flask(__name__, template_folder="view/templates/", static_folder="static")
app.config.from_file("config/ga_thresholds.json", load=json.load)


def run(G, P, M, A, K, E):
    generations = G
    population_size = P
    input_array = A
    mutation_rate = M
    seed = 42

    start_time = time.time()

    best, score = GeneticAlgorithm.run(
        raw=input_array,
        population_size=population_size,
        generations=generations,
        mutation_rate=mutation_rate,
        rng_seed=seed,
        tournament_k=K,
        elitism=E,
    )

    stop_time = time.time()
    elapsed = int(stop_time - start_time)
    mins, secs = divmod(elapsed, 60)
    elapsed_str = f"{mins} mins {secs} secs"

    metadata = {
        "RULD string": best.ruld,
        "Generations": G,
        "Population Size": P,
        "Mutation rate": M,
        "Elitism": E,
        "Tournament K ": K,
        "Sequence": A,
        "Lowest found energy": score,
        "Runtime": elapsed_str,
        "Random used seed": seed,
    }

    return (
        metadata,
        persistence.save_data(input_array, G, P, M, A, K, E, score, best, elapsed_str),
    )


def inflate_err(errs, form):
    image_path = None
    meta = None
    ts = None
    return render_template(
        "index.html", form=form, result=image_path, meta=meta, default_zipname=ts, error=errs
    )


@app.route("/", methods=["GET", "POST"])
def index():
    bounds = current_app.config["GA_BOUNDS"]
    form = InputForm(request.form)
    image_path = None
    meta = None
    ts = None
    if request.method == "POST" and form.validate():
        errs = validator.validate(
            form.G.data, form.P.data, form.M.data, form.K.data, form.E.data, form.A.data, bounds
        )
        if len(errs):
            return inflate_err(errs, form)
        meta, image_path = run(
            form.G.data, form.P.data, form.M.data, form.A.data, form.K.data, form.E.data
        )
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return render_template(
        "index.html", form=form, result=image_path, meta=meta, default_zipname=ts, error=None
    )


@app.route("/download-zip", methods=["POST"])
def download_zip():
    # numele cerut de user
    name = request.form.get("zipname", "").strip()
    if not name:
        # fallback la timestamp
        name = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    if not name.endswith(".zip"):
        name += ".zip"

    # construim arhiva în memorie
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in glob.glob(os.path.join(persistence.FILES_DIR, "*")):
            if os.path.isfile(path):
                zf.write(path, arcname=os.path.basename(path))
    buf.seek(0)

    return send_file(
        buf, as_attachment=True, download_name=name, mimetype="application/zip"
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
