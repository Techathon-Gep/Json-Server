def validateNode(node, child):
  print(f"Node: {node}\nChild: {child}\n", end="="*100+"\n")
  if type(child) is list:
    if node in sp_req.keys():
      if "minItems" in sp_req[node].keys() and len(child) < sp_req[node]["minItems"]:
        error.append(f"Length of the node: '{node}' is less.")
      elif "maxItems" in sp_req[node].keys() and len(child) > sp_req[node]["maxItems"]:
        error.append(f"Length of the node: '{node}' is more.")
    for i in range(0, len(child)):
      validateNode(node, child[i])
  elif type(child) is dict:
    if node in mandatory.keys():
      for i in mandatory[node]:
        if i not in child.keys():
          error.append(f"Mandatory Node '{i}' is not present in {node}")
    for i in child.keys():
      validateNode(i, child[i])
  else:
    if node in sp_req.keys():
      if child is None:
        error.append(f"Child: '{child}' of node: '{node}' cannot be a NULL.")
      elif type(sp_req[node]) is list:
        if child not in sp_req[node]:
          error.append(f"Child: '{child}' of node: '{node}' value is not the required one.")
      elif type(sp_req[node]) is dict:
        if ("maxlen" or "minlen") in sp_req[node].keys():
          if type(child) is not str:
            error.append(f"Child: '{child}' of node: '{node}' should be a string")
          elif "maxlen" in sp_req[node].keys() and len(child) > sp_req[node]["maxlen"]:
            error.append(f"Child: '{child}' of node: '{node}' exceeded the maximum length.")
          elif "minlen" in sp_req[node].keys() and len(child) < sp_req[node]["minlen"]:
            error.append(f"Child: '{child}' of node: '{node}' is shorter in length.")
        elif ("max" or "min") in sp_req[node].keys():
          if type(child) is not int:
            error.append(f"Child: '{child}' of node: '{node}' should be an integer")
          elif "max" in sp_req[node].keys() and child > sp_req[node]["max"]:
            error.append(f"Child: '{child}' of node: '{node}' crosses the upper limit.")
          elif "min" in sp_req[node].keys() and child < sp_req[node]["min"]:
            error.append(f"Child: '{child}' of node: '{node}' not able to cross the lower limit.")
      elif type(child) is not sp_req[node]:
        error.append(f"Value of '{node}' should be an '{sp_req[node]}'")
