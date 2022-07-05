from flask import Flask, render_template, redirect, request, jsonify
from schema_example import examples
import json

app = Flask(__name__)


@app.route('/')
def hello():
    return render_template("home.html")

@app.route('/error')
def error():
    return render_template("home.html")

@app.route('/get_input')
def get_input():
    return render_template("form.html")

@app.route('/create')
def create():
    options = ['int', 'float', 'array', 'object', 'string']
    return render_template("create.html", options = options)

@app.route('/get_json', methods=['POST'])
def get_json():
    if request.method == 'POST':
        text = request.form['schema_input']
        text = json.loads(text)
        text = jsonify(text)
        return text
    else:
        return redirect('/error')
    
@app.route('/get_input', methods=['POST'])
def inp():
    if request.method == 'POST':
        names = request.form.getlist('type-name')
        typess = request.form.getlist('types')
        for name, types in zip(names, typess):
            print(name, types, flush=True)
        return str(typess)
    else:
        return redirect('/error')

if __name__ == "__main__":
    app.run(port=4000, debug = True)