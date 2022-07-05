from flask import Flask, render_template, redirect, request, jsonify, session
from flask_session import Session
from utils import save_schema, open_schema, schema_number, schema_names, get_mandatory_req_fields
import json
# from constants import jsons, sp_req, mandatory
from json_schema_validator import output
from jsonSchema.JSONSchema.newschema import schemacheck, reqcheck

jsons = {}
data = {}

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route('/')
def hello():
    options = schema_names()
    return render_template("home.html", options = options)

@app.route('/error')
def error():
    return render_template("error.html")

@app.route('/data_input')
def get_input():
    data = session.get('schema')
    return render_template("form.html", data = data)

@app.route('/get_json', methods=['POST'])
def get_json():
    if request.method == 'POST':
        text = request.form['json_input']

        jsons = json.loads(text)
        num = schema_number()

        mandatory = session.get('mandatory')
        sp_req = session.get('sp_req')
        # print("dsaasdasdasdadas", sp_req, mandatory, flush=True)
        # print(data)
        input_data = {}
        input_data['root'] = jsons
        out = output([], input_data, sp_req, mandatory)
        session['out'] = out
        return redirect('/results')
    else:
        return redirect('/error')
    
@app.route('/get_input', methods=['POST'])
def get_inp():
    if request.method == 'POST':

        types = request.form['types']
        data = open_schema(str(types))
        mandatory = schemacheck("root", data)
        session['mandatory'] = mandatory
        sp_req = reqcheck("root", data)
        session['sp_req'] = sp_req
        session['schema'] = json.dumps(data, indent=4)
        # print("asdahelkkikkkerakrkaek", mandatory, session['sp_req'], flush=True)
        return redirect('/data_input')
    else:
        return redirect('/error')

@app.route('/get_data', methods=['POST'])
def temp():
    if request.method == 'POST':

        types = request.form['schema_input']
        # print("dasdasda", types, flush=True)
        data = json.loads(types)
        session['schema'] = json.dumps(data, indent=4)
        mandatory = schemacheck("root", data)
        session['mandatory'] = mandatory
        sp_req = reqcheck("root", data)
        session['sp_req'] = sp_req
        # print("asdahelkkikkkerakrkaek", mandatory, session['sp_req'], flush=True)
        return redirect('/data_input')
    else:
        return redirect('/error')

@app.route('/results')
def result():
    output = session.get('out')
    return render_template('result.html', output = output)


if __name__ == "__main__":
    app.run(port=4000, debug = True)