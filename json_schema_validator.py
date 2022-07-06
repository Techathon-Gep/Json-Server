# json = {"StudentInfo": [{"name": "John","age": 25,"city": "US"},{"name": "Jh","age": 125,"city": 123,"gender": "F"},{"name": None,"age": "12","city": "US","gender": "T"}]}
# mandatory = {"StudentInfo": ["name", "gender"]}
# sp_req = {"name": {"maxLength": 8, "minLength": 3}, "age": {"max": 100, "min": 0}, "gender": ["F", "M", "N"], "city": str, 'StudentInfo': {'minItems': 3}}

from constants import jsons, sp_req, mandatory
import sys

def validateNode(error, sp_req, mandatory, node, child):
  # print(sp_req, mandatory, flush=True)
  # print(f"Node: {node}\nChild: {child}\n", end="="*100+"\n", flush=True)

  if type(child) is list:
    if node in sp_req.keys():
      if "minItems" in sp_req[node].keys() and len(child) < sp_req[node]["minItems"]:
        error.append(f"Length of the node: '{node}' is less.")
      elif "maxItems" in sp_req[node].keys() and len(child) > sp_req[node]["maxItems"]:
        error.append(f"Length of the node: '{node}' is more.")
    for i in range(0, len(child)):
      validateNode(error, sp_req, mandatory, node, child[i])
  elif type(child) is dict:
    if node in mandatory.keys():
      for i in mandatory[node]:
        if i not in child.keys():
          error.append(f"Mandatory Node '{i}' is not present in {node}")
    for i in child.keys():
      validateNode(error, sp_req, mandatory, i, child[i])
  else:
    if node in sp_req.keys():
      if child is None:
        error.append(f"Child: '{child}' of node: '{node}' cannot be a NULL.")
      elif type(sp_req[node]) is list:
        if child not in sp_req[node]:
          error.append(f"Child: '{child}' of node: '{node}' value is not the required one.")
      elif type(sp_req[node]) is dict:
        if 'type' in sp_req[node] and type(child) is not sp_req[node]['type']:
          error.append(f"Value of '{node}' should be an '{sp_req[node]}'")
        elif ("maxLength" or "minLength") in sp_req[node].keys():
          if type(child) is not str:
            error.append(f"Child: '{child}' of node: '{node}' should be a string")
          elif "maxLength" in sp_req[node].keys() and len(child) > sp_req[node]["maxLength"]:
            error.append(f"Child: '{child}' of node: '{node}' exceeded the maximum length.")
          elif "minLength" in sp_req[node].keys() and len(child) < sp_req[node]["minLength"]:
            error.append(f"Child: '{child}' of node: '{node}' is shorter in length.")
        elif ("maximum" or "minimum") in sp_req[node].keys():
          if type(child) is not int:
            error.append(f"Child: '{child}' of node: '{node}' should be an integer")
          elif "maximum" in sp_req[node].keys() and child > sp_req[node]["maximum"]:
            error.append(f"Child: '{child}' of node: '{node}' crosses the upper limit.")
          elif "minimum" in sp_req[node].keys() and child < sp_req[node]["minimum"]:
            error.append(f"Child: '{child}' of node: '{node}' not able to cross the lower limit.")
        elif "enum" in sp_req[node].keys():
          if child not in sp_req[node]["enum"]:
            error.append(f"Child: '{child}' of node: '{node}' value is not the required one.")


def output(error, jsons, sp_req, mandatory):
    # print(sp_req, mandatory, flush=True)
    # print("isnsdiasidasidasidaids",jsons, flush=True)
    for key in jsons.keys():
        validateNode(error, sp_req, mandatory, key, jsons[key])
    # print(error, "sdaasdasdasdadadasdas")
    if len(error) > 0:
        return error
    else:
        return ["No error found json data validated"]