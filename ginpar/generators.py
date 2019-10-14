import os
import string
import json

from jinja2 import Environment, FileSystemLoader

def dict_to_attrs(d):
    attrs = []
    for k, v in d.items():
        attrs.append(f'{k}="{v}"')
    attrs = " ".join(attrs)
    return attrs

delimiters = '/* ##ginpar */'

_INPUT_TEMPLATES_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'templates')

# Get a list that contains the name of the templates
_INPUT_TEMPLATES_LIST = list(
    map(
        lambda e : e.split(".")[0],
        filter(
            lambda e : e.endswith(".html"),
            os.listdir(_INPUT_TEMPLATES_DIR))))

_jinja_env = Environment(
    loader=FileSystemLoader(_INPUT_TEMPLATES_DIR),
    trim_blocks=True,
)

_jinja_env.filters['getattrs'] = dict_to_attrs

def makeValueGetter(attrs):
    _TEMPLATE = _jinja_env.get_template("retrieve.js")
    
    return _TEMPLATE.render(attrs = attrs)

def sketch_to_dict(s):
    """Receives the content of a sketch file with a JSON object
    inside a pair of ginpar delimiters"""
    
    ## Work only with the substring between two delimiters
    params_string = s.split(delimiters)[1]

    ## Remove the part of the string before the assignment
    params = params_string.split("=")[1]

    ## Remove the whitespace at the ends
    params = params.strip()

    ## Remove the ` characters (first and last elements)
    params = params[1:-1]

    return json.loads(params)

def to_kebab(s):
    s = s.lower().split(" ")
    return '-'.join(s)


def input_tag(field):
    ## Obtain the html id
    id = to_kebab(field['name'])
    
    ## 
    attrs = []
    for k, v in field["attrs"].items():
        attrs.append(f'{k}="{v}"')
    attrs = " ".join(attrs)
    
    if id in _INPUT_TEMPLATES_LIST:
        _input_template = _jinja_env.get_template(id + '.html')
    else:
        _input_template = _jinja_env.get_template('input.html')
    
    # print(attrs)

    return (_input_template.render(
        id=id, name = field['name'], attrs = field["attrs"]))

def form_tag(fields):
    form = ["<form>"]
    for f in fields:
        form.append(input_tag(f))
    form.append('\n</form>')
    form = "\n".join(form)
    return form

def add_name(fields):
    """Adds a `name` using the `var` when no `name` was specified"""
    for field in fields:
        if 'name' not in field:
            field['name'] = " ".join(field['var'].split("_")).capitalize()
        field['id'] = to_kebab(field['name'])
    return fields

def sketch_index(sketch):
    return form_tag(sketch)
    