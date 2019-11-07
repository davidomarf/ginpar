import os
import yaml

from jinja2 import Environment, FileSystemLoader


def dict_to_attrs(d):
    """Filter to convert a python dictionary into a HTML attributes.

    For each (key, value) pair inside the dict, a ``key=value`` string will
    be created.

    Parameters
    ----------
    d : dict
        Dictionary containing the key value attributes.

    Returns
    -------
    str
        String containing all the attributes of the dictionary separated with spaces.
    """

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
