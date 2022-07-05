from flask import Flask, render_template, redirect, request, jsonify
from utils import save_schema, open_schema, schema_number, schema_names, get_mandatory_req_fields
import json


app = Flask(__name__)


@app.route('/')
def hello():
    options = schema_names()
    return render_template("home.html", options = options)

@app.route('/error')
def error():
    return render_template("error.html")

@app.route('/get_input')
def get_input():
    return render_template("form.html")

@app.route('/get_json', methods=['POST'])
def get_json():
    if request.method == 'POST':
        text = request.form['schema_input']
        text = json.loads(text)
        num = schema_number()
        save_schema(json.dumps(text, indent=4), num + 1)
        man, sq = get_mandatory_req_fields(text)
        return redirect('/get_input')
    else:
        return redirect('/error')
    
@app.route('/get_input', methods=['POST'])
def get_inp():
    if request.method == 'POST':
        # names = request.form.getlist('type-name')
        # for name, types in zip(names, typess):
        #     print(name, types, flush=True)

        types = request.form['types']
        data = open_schema(str(types))
        man, sq = get_mandatory_req_fields(data)
        return redirect('/get_input')
    else:
        return redirect('/error')

if __name__ == "__main__":
    app.run(port=4000, debug = True)