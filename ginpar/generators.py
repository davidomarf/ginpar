import os
import yaml

from jinja2 import Environment, FileSystemLoader


def dict_to_attrs(d):
    attrs = []
    for k, v in d.items():
        attrs.append(f'{k}="{v}"')
    attrs = " ".join(attrs)
    return attrs


_INPUT_TEMPLATES_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "templates"
)

# Get a list that contains the name of the templates
_INPUT_TEMPLATES_LIST = list(
    map(
        lambda e: e.split(".")[0],
        filter(lambda e: e.endswith(".html"), os.listdir(_INPUT_TEMPLATES_DIR)),
    )
)

_jinja_env = Environment(
    loader=FileSystemLoader(_INPUT_TEMPLATES_DIR), trim_blocks=True
)

_jinja_env.filters["getattrs"] = dict_to_attrs


def makeValueGetter(global_seed, attrs):
    _TEMPLATE = _jinja_env.get_template("retrieve.js")
    return _TEMPLATE.render(global_seed=global_seed, params=attrs)


def to_kebab(s):
    s = s.lower().split(" ")
    return "-".join(s)


def input_tag(field):
    ## Obtain the html id
    id = to_kebab(field["name"])

    ##
    attrs = []
    for k, v in field["attrs"].items():
        attrs.append(f'{k}="{v}"')
    attrs = " ".join(attrs)

    if id in _INPUT_TEMPLATES_LIST:
        _input_template = _jinja_env.get_template(id + ".html")
    else:
        _input_template = _jinja_env.get_template("input.html")

    # print(attrs)

    return _input_template.render(id=id, name=field["name"], attrs=field["attrs"])


def form_tag(fields):
    form = ["<form>"]
    for f in fields:
        form.append(input_tag(f))
    form.append("\n</form>")
    form = "\n".join(form)
    return form


def sketch_index(sketch):
    return form_tag(sketch)
