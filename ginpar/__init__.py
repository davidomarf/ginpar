import os
import shutil

from jinja2 import Environment, FileSystemLoader

from ginpar.settings import read_config
import ginpar.generators as gg

_SITE_FILE = 'config.json'


def parse(path):
     return eval('f"""' + open(path).read() + '"""')

def build_sketch (sketch):
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

def main():
    _SITE = read_config(_SITE_FILE)

    _THEME = _SITE['theme']

    _TEMPLATES_PATH = os.path.join('themes', _THEME, 'templates')

    _jinja_env = Environment(
        loader=FileSystemLoader(_TEMPLATES_PATH),
        trim_blocks=True,
        )

    _jinja_env.filters['unkebab'] = unkebab

    ## Remove existent /public folder and create an empty one
    if os.path.exists("public"):
        shutil.rmtree('public')

    os.mkdir('public')

    ## Copy the static/ folder of the theme
    shutil.copytree(
        os.path.join('themes', _THEME, 'static'), 
         os.path.join('public', 'static'))

    ## Create a sketches array
    sketches_path = "./sketches"
    sketches = []

    for r, _, f in os.walk(sketches_path):
        for file in f:
            if file.endswith(".js"):
                sketches.append(os.path.join(r, file))

    ## Create an index to contain all the sketches
    _index_template = _jinja_env.get_template('index.html')

    index = open("public/index.html", "w")
    index.write(_index_template.render(sketches=sketches, site = _SITE))
    index.close()

    for s in sketches:
        ## Ignore the path and extension of the sketch
        title = s.split("/")[-1].split(".")[0]
        
        ## Create a directory with the sketch title
        os.mkdir(f'public/{title}')
        
        ## Convert the form JSON into a dict
        form_dict = gg.sketch_to_dict(open(s).read())
        
        ## Add name key to the dict elements
        form_dict = gg.add_name(form_dict)

        ## Create index.html
        _sketch_template = _jinja_env.get_template('sketch.html')
        sketch_index = open(f'public/{title}/index.html', "w+")
        sketch_index.write(_sketch_template.render(
            sketch = unkebab(title),
            form = gg.sketch_index(form_dict),
            site = _SITE))
        sketch_index.close()

        ## Create sketch.js
        sketch_path = f'public/{title}/sketch.js'
        sketch = open(sketch_path, "w+")

        ## Copy all the content from original sketches/{title}.js to sketch.js
        sf = open(s, 'r')

        sketch.write(gg.makeValueGetter(form_dict))

        for x in sf.readlines():
            sketch.write(x)
        sf.close()
        sketch.close()
