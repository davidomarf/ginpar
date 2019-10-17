import os
import shutil
import yaml

from jinja2 import Environment, FileSystemLoader

from ginpar.settings import read_config
import ginpar.generators as gg

_SITE_FILE = "config.json"


def parse(path):
    return eval('f"""' + open(path).read() + '"""')


def build_sketch(sketch):
    content = sketch
    return content


def build_link(sketch):
    title = sketch.split("/")[-1].split(".")[0]
    return f'<a href="./{title}"">{title}</a><br/>\n'


def build_index(sketches):
    content = ""
    for s in sketches:
        content += build_link(s)
    return content


def unkebab(s):
    return " ".join(s.split("-"))


def get_sketches_list(path):
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

    # Remove all the directories that don't contain both  a `sketch.js` and `data.yaml` file
    sketches[:] = filter(
        lambda a: os.path.isfile(a["script"]) and os.path.isfile(a["data"]), sketches
    )
    return sketches


def convert_information(sketch):
    path = sketch["data"]
    with open(path, "r") as stream:
        try:
            parsed_data = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    sketch["data"] = parsed_data
    return sketch


def main():
    _SITE = read_config(_SITE_FILE)

    _THEME = _SITE["theme"]

    _TEMPLATES_PATH = os.path.join("themes", _THEME, "templates")

    _jinja_env = Environment(loader=FileSystemLoader(_TEMPLATES_PATH), trim_blocks=True)

    _jinja_env.filters["unkebab"] = unkebab

    ## Remove existent /public folder and create an empty one
    if os.path.exists("public"):
        shutil.rmtree("public")

    os.mkdir("public")

    ## Copy the static/ folder of the theme
    shutil.copytree(
        os.path.join("themes", _THEME, "static"), os.path.join("public", "static")
    )

    ## Create a sketches array
    sketches_path = "./sketches"
    sketches = get_sketches_list(sketches_path)
    sketches[:] = map(convert_information, sketches)

    ## Create an index to contain all the sketches
    _index_template = _jinja_env.get_template("index.html")
    index = open("public/index.html", "w")
    index.write(
        _index_template.render(sketches=map(lambda a: a["name"], sketches), site=_SITE)
    )
    index.close()

    for s in sketches:
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
