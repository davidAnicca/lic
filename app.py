from flask import Flask, render_template
import numpy
import matri
import base64

app = Flask(__name__)

state = 'H'
road = []

def inflate_matrix():
    image_buffer = matri.create_lattice_diagram(road)
    image_base64 = base64.b64encode(image_buffer.getvalue()).decode('utf-8')
    return image_base64

@app.route('/')
def home():
    return render_template('play.html')

@app.route('/toggle', methods=['POST'])
def toggle():
    global state
    state = 'P' if state == 'H' else 'H'
    return state 

@app.route('/up', methods=['POST'])
def up():
    global road, state
    road.append("U" + state)
    return inflate_matrix()

@app.route('/down', methods=['POST'])
def down():
    global road, state
    road.append("D" + state)
    return inflate_matrix()

@app.route('/left', methods=['POST'])
def left():
    global road, state
    road.append("L" + state)
    return inflate_matrix()

@app.route('/right', methods=['POST'])
def right():
    global road, state
    road.append("R" + state)
    return inflate_matrix()

if __name__ == '__main__':
    state = 'H' 
    road = []
    app.run(host='0.0.0.0', port=5000)


    

