import json
import os
from jsonSchema.JSONSchema.newschema import schemacheck, reqcheck


def open_schema(name):
    # print("sadsssssssssssss:  ", name, flush=True)
    try:
        f = open(f'schema/{name}')
        data = json.loads(f.read())
    except FileNotFoundError:
        print("no file")
        flag = False
    except:
        print("Unexepected Error")
    finally:
        return data


def save_schema(data, name):
    try:
        f = open(f'schema/schema{name}.json', 'w+')
        f.write(data)
    except Exception as e:
        print("Unexpected Error")
    finally:
        f.close()


def schema_number():
    names = os.listdir('schema')
    number_files = len(names)
    return number_files

def schema_names():
    names = os.listdir('schema')
    return names

def get_mandatory_req_fields(data):
    mandatory = schemacheck("root", data)
    sp_req = reqcheck("root", data)
    return mandatory, sp_req