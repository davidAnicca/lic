from time import sleep
from flask import Flask, render_template, request
from model.GA.GA import GeneticSAW as GeneticAlgorithm
from model.GA.matri import create_lattice_diagram, create_visual
from view.forms.form_model import InputForm

app = Flask(__name__, template_folder="view/templates/", static_folder="static")

def inflate_matrix(G, P, M, A):
        generations = G
        population_size = P
        input_array = A
        mutation_rate = M

        best, score = GeneticAlgorithm.run(
            raw=input_array,
            population_size=population_size,
            generations=generations,
            mutation_rate=mutation_rate,
            rng_seed=42,
            tournament_k=1
        )

        visual = create_visual(input_array, best.ruld)
        return create_lattice_diagram(visual)
    
@app.route('/', methods=['GET', 'POST'])
def index():
    form = InputForm(request.form)
    if request.method == 'POST' and form.validate():
        result = inflate_matrix(form.G.data,
                                 form.P.data,
                                 form.M.data,
                                 form.A.data)
    else:
        result = None

    return render_template('index.html',
                           form=form, result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)