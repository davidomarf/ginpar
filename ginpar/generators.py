import os
import string
import json

delimiters = '/* ##ginpar */'

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

    div = f'''
    <label for="{id}">
        {field['name']}
    </label>
    <input {attrs}>'''

    return div

def form_tag(fields):
    form = ["<form>"]
    for f in fields:
        form.append(input_tag(f))
    form.append('\n</form>')
    form = "\n".join(form)
    return form

def sketch_index(sketch):
    form_data = sketch_to_dict(sketch)
    return form_tag(form_data)
    