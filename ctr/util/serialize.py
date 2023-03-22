from xml.etree.ElementTree import Element, SubElement, tostring, indent


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


class XmlSerialize:
    def __init__(self, rootName: str, **attributes):
        """A class utilized for writing to a XML document"""
        self.rootName: str = rootName
        # Create an empty xml document with custom root name
        self.document: Element = Element(self.rootName, attributes)

    def add(self, tag: str, elemText: str = None, **attributes) -> None:
        """Adds an element to the XML document"""
        element = SubElement(self.document, tag,
                             attributes)
        element.text = elemText

    def insert_from_attr(self, attributeDict: dict, tag, elementText: str = None, **attributes):
        """Inserts a sub-element into an element given its attributes match"""
        # TODO: Implement partial attribute matching
        allElements = [elem for elem in self.document.iter()]
        for element in allElements:
            # Match the attributes to the given dict
            if element.attrib == attributeDict:
                newSubElement = SubElement(element, tag, **attributes)
                newSubElement.text = elementText

    def insert_from_tag(self, tag, newTag, elementText: str = None, **attributes):
        """Inserts a sub-element into an element given its tag match"""
        allElements = [elem for elem in self.document.iter()]
        for elem in allElements:
            # Match the attributes to the tag name
            if elem.tag == tag:
                newSubElement = SubElement(elem, newTag, **attributes)
                newSubElement.text = elementText

    def serialize(self, encoding: str) -> str:
        """Serializes the XML Document into a string object"""
        # Prettify the document
        indent(self.document, level=0)

        # Remove dash from encoding for adding to xml header
        headerEncoding: str = encoding.replace("-", "").lower()

        return tostring(self.document, encoding=headerEncoding, method='xml').decode(headerEncoding)
