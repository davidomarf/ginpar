"""
    ginpar.build
    ~~~~~~~~~~~~

    Implements the generation of the static site.
"""
import os
import shutil
import yaml
import click

from jinja2 import Environment, FileSystemLoader

from ginpar.settings import read_config
import ginpar.generators as gg

from ginpar.utils.echo import echo, success
from ginpar.utils.strings import unkebab

import click

_SITE_FILE = "config.json"
_SITE = read_config(_SITE_FILE)
_THEME = _SITE["theme"]
_TEMPLATES_PATH = os.path.join("themes", _THEME, "templates")
_SKETCHES_PATH = _SITE["content_path"]
_jinja_env = Environment(loader=FileSystemLoader(_TEMPLATES_PATH), trim_blocks=True)
_jinja_env.filters["unkebab"] = unkebab


def build_link(sketch):
    title = sketch.split("/")[-1].split(".")[0]
    return f'<a href="./{title}"">{title}</a><br/>\n'


def build_index(sketches):
    content = ""
    for s in sketches:
        content += build_link(s)
    return content


def get_sketches(path):
    sketches = []
    # Create a list with all the directories inside path
    for r, d, _ in os.walk(path):
        for sketch in d:
            sketches.append(
                {
                    "name": sketch,
                    "script": os.path.join(r, sketch, "sketch.js"),
                    "data": os.path.join(r, sketch, "data.yaml"),
                }
            )

    return map(
        # Convert the data.yaml file into a dictionary
        convert_information,
        # Remove sketch if either `sketch.js` or `data.yaml` don't exist
        filter(
            lambda a: os.path.isfile(a["script"]) and os.path.isfile(a["data"]),
            sketches,
        ),
    )


def convert_information(sketch):
    path = sketch["data"]
    with open(path, "r") as stream:
        try:
            parsed_data = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    sketch["data"] = parsed_data
    return sketch


def create_publishing_directory(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.mkdir(path)


def copy_theme(path, theme_path):
    ## Copy the static/ folder of the theme
    shutil.copytree(
        os.path.join("themes", theme_path, "static"), os.path.join(path, "static")
    )


def render_index(path, sketches, site):
    ## Create an index to contain all the sketches
    _index_template = _jinja_env.get_template("index.html")
    index = open(os.path.join(path, "index.html"), "w")
    index.write(
        _index_template.render(sketches=map(lambda a: a["name"], sketches), site=site)
    )
    index.close()


def render_sketch_page(path, s, site):
    ## Create a directory with the sketch title
    os.mkdir(f"public/{s['name']}")

    ## Convert the form JSON into a dict
    form_dict = s["data"]

    ## Add name key to the dict elements
    form_dict = gg.add_name(form_dict)

    ## Create index.html
    _sketch_template = _jinja_env.get_template("sketch.html")
    sketch_index = open(f"public/{s['name']}/index.html", "w+")
    sketch_index.write(
        _sketch_template.render(
            sketch=unkebab(s["name"]), form=gg.sketch_index(form_dict), site=_SITE
        )
    )
    sketch_index.close()

    ## Create sketch.js
    sketch_path = f"public/{s['name']}/sketch.js"
    sketch = open(sketch_path, "w+")

    ## Copy all the content from original sketches/{title}.js to sketch.js
    sf = open(s["script"], "r")

    sketch.write(gg.makeValueGetter(form_dict))

    for x in sf.readlines():
        sketch.write(x)
    sf.close()
    sketch.close()


def build(path):
    create_publishing_directory(path)
    echo(f"Building in `{os.path.abspath(path)}`")

    copy_theme(path, _THEME)
    echo(f"Building using theme `{_THEME}`")

    ## Create a sketches array
    sketches = list(get_sketches(_SKETCHES_PATH))
    echo(f"Found {len(sketches)} sketch(es)")

    render_index(path, sketches, _SITE)
    echo("Building main page")

    echo("Building sketches:")
    for s in sketches:
        echo(f"  Building {s['name']}")
        render_sketch_page(path, s, _SITE)

    success("Success.")
