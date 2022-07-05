from constants import sp_req, mandatory

def schemacheck(name,node):
    if node["type"] == "object":
        mandatory[name] = node["required"]
        for key,value in node.items():
            if key == "properties":
                for key2,value2 in node["properties"].items():
                    schemacheck(key2,value2)
    elif node["type"] == "array":
        for key,value in node.items():
            if key == "items":
                schemacheck(name,value[0])
    return mandatory

def reqcheck(name,node):
    if "enum" in node.keys():
        temp = {}
        if name not in sp_req.keys():
            temp["enum"] = node["enum"]
        else:
            temp = sp_req[name]
            temp["enum"] = node["enum"]
        sp_req[name] = temp
    if node["type"] == "object":
        for key,value in node.items():
            if key == "properties":
                for key2,value2 in node["properties"].items():
                    reqcheck(key2,value2)
    elif node["type"] == "array":
        if "maxItems" in node.keys():
            temp = {}
            if name not in sp_req.keys():
                temp["maxItems"] = node["maxItems"]
            else:
                temp = sp_req[name]
                temp["maxItems"] = node["maxItems"]
            sp_req[name] = temp
        if "minItems" in node.keys():
            temp = {}
            if name not in sp_req.keys():
                temp["minItems"] = node["minItems"]
            else:
                temp = sp_req[name]
                temp["minItems"] = node["minItems"]
            sp_req[name] = temp
        for key,value in node.items():
            if key == "items":
                for i in range(len(value)):
                    reqcheck(name,value[i])
    elif node["type"] in ["number","integer"]:
        if "maximum" in node.keys():
            temp = {}
            if name not in sp_req.keys():
                temp["maximum"] = node["maximum"]
            else:
                temp = sp_req[name]
                temp["maximum"] = node["maximum"]
            sp_req[name] = temp
        if "minimum" in node.keys():
            temp = {}
            if name not in sp_req.keys():
                temp["minimum"] = node["minimum"]
            else:
                temp = sp_req[name]
                temp["minimum"] = node["minimum"]
            sp_req[name] = temp
    elif node["type"] == "string":
        if "maxLength" in node.keys():
            temp = {}
            if name not in sp_req.keys():
                temp["maxLength"] = node["maxLength"]
            else:
                temp = sp_req[name]
                temp["maxLength"] = node["maxLength"]
            sp_req[name] = temp
        if "minLength" in node.keys():
            temp = {}
            if name not in sp_req.keys():
                temp["minLength"] = node["minLength"]
            else:
                temp = sp_req[name]
                temp["minLength"] = node["minLength"]
            sp_req[name] = temp
    return sp_req




# schemacheck("root",b)
# reqcheck("root",b)
# print(f" mandatory : {mandatory}")
# print(f" special req : {sp_req}")

# schemacheck("root",c)
# reqcheck("root",c)
# print(f" mandatory : {mandatory}")
# print(f" special req : {sp_req}")
