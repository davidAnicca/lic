from time import sleep
from flask import Flask, render_template, request
from main_engine import genetic_saw
import matri
from model.form_model import InputForm
from utils import create_visual

app = Flask(__name__)

state = 'H'
road = []

def inflate_matrix(G, P, M, A):
        generations = G
        population_size = P
        input_array = A
        mutation_rate = M

        best, score = genetic_saw(
            raw=input_array,
            population_size=population_size,
            generations=generations,
            mutation_rate=mutation_rate,
            rng_seed=42,
            tournament_k=1
        )

        visual = create_visual(input_array, best.ruld)
        print(f'visual form of result: {visual}')

        print("Best score:", score)
        print("ruld:", best.ruld)
        print("xs:", best.xs)
        print("ys:", best.ys)
        sleep(5)
        print(generations, population_size)
        return matri.create_lattice_diagram(visual)
    

# @app.route('/toggle', methods=['POST'])
# def toggle():
#     global state
#     state = 'P' if state == 'H' else 'H'
#     return state 

# @app.route('/up', methods=['POST'])
# def up():
#     global road, state
#     road.append("U" + state)
#     return inflate_matrix()

# @app.route('/down', methods=['POST'])
# def down():
#     global road, state
#     road.append("D" + state)
#     return inflate_matrix()

# @app.route('/left', methods=['POST'])
# def left():
#     global road, state
#     road.append("L" + state)
#     return inflate_matrix()

# @app.route('/right', methods=['POST'])
# def right():
#     global road, state
#     road.append("R" + state)
#     return inflate_matrix()

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
    state = 'H' 
    road = []
    app.run(host='0.0.0.0', port=5000)


    

