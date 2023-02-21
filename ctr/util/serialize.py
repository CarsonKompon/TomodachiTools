import json

class JsonSerialize:
    
    string: str = ""

    def __init__(self, data: str = ""):
        self.string = data.strip()
    
    def add(self, key, var, wrapVarInQuotes=False):
        if self.string == "":
            self.string = "{"
        
        match self.string[-1]:
            case "}":
                self.string = self.string[:-1] + ","
            case "{":
                pass
            case ",":
                pass
            case " ":
                pass
            case _:
                self.string += ","

        if wrapVarInQuotes:
            self.string += f"\"{key}\": \"{var_to_json(var)}\""
        else:
            self.string += f"\"{key}\": {var_to_json(var)}"
        
        self.string += "}"

    def serialize(self):
        if self.string[-1] != "}":
            self.string += "}"
        return self.string

def format_line(key, var, wrapVarInQuotes=False):
    if wrapVarInQuotes:
        return f"\"{key}\": \"{var_to_json(var)}\""
    return f"\"{key}\": {var_to_json(var)}"

def var_to_json(var):
    if type(var) is dict:
        return dict_to_json(var)
    elif isinstance(var, list) or isinstance(var, tuple):
        return list_to_json(var)
    elif isinstance(var, str):
        return str_to_json(var)
    elif type(var) is bytes:
        return str_to_json(var.decode("utf-8"))
    elif type(var) is int:
        return int_to_json(var)
    elif type(var) is float:
        return float_to_json(var)
    elif type(var) is bool:
        return bool_to_json(var)
    elif var is None:
        return null_to_json(var)
    else:
        return str(var)

def dict_to_json(var):
    if len(var) == 0:
        return "{}"
    else:
        return "{" + ", ".join(f'"{key}": {var_to_json(value)}' for key, value in var.items()) + "}"

def list_to_json(var):
    if len(var) == 0:
        return "[]"
    else:
        return "[" + ", ".join(var_to_json(value) for value in var) + "]"

def str_to_json(var):
    return '"{}"'.format(var)

def int_to_json(var):
    return str(var)

def float_to_json(var):
    return str(var)

def bool_to_json(var):
    if var:
        return "true"
    return "false"

def null_to_json(_):
    return "null"