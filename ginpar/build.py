"""Build command for Ginpar projects.

This module implements the building command for the ginpar static content
generator.

`build` will read the configuration file in search for `build_path` and
`source_path`. If not defined, `build` will use `"public"` and
`"sketches`, respectively.

Examples
--------

To build your project according to your specifications in `config.yaml`::

    ginpar build

To build targeting a custom path `_site/`::

    ginpar build --path="_site"

Notes
-----

You cannot specify the content path. It is either ``config.content_path`` or
``"sketches"``.
"""

import os
import shutil

import yaml
import click
from jinja2 import Environment, FileSystemLoader

import ginpar.generators as gg
from ginpar.utils.echo import echo, success
from ginpar.utils.strings import unkebab
from ginpar.utils.git import clone_repo, delete_git_files

import click


def get_sketches(content_path):
    """Obtain the list of **valid** sketches inside `path`.

    Valid sketches are directories containing at least two files:
    `sketch.js` and `data.yaml`.

    This function will create a list of sketch objects containing
    `name`, `script`, and `data`.

    Parameters
    ----------
    content_path : str
        The path containing the sketches to fetch.

    Returns
    -------
    list
        Individual elements contain `{"name", "script", "data"}`.
    """

    sketches = []

    # Create a list with all the directories inside path
    for r, d, _ in os.walk(content_path):
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
    """Convert the `["data"]` field of a sketch into a Python dictionary.

    Parameters
    ----------
    sketch : dict
        It contains the sketch information. Must contain `["data"]`, and
        `["data"]` must be a YAML-valid string.


    Returns
    -------
    dictionary
        `sketch` but with the updated `["data"]` field.
    """

    path = sketch["data"]
    with open(path, "r") as stream:
        try:
            parsed_data = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    sketch["data"] = parsed_data
    return sketch


def create_publishing_directory(build_path):
    """Remove existing directories with the same name, and create again.

    Parameters
    ----------
    build_path : str
        Path of the build.
    """

    if os.path.exists(build_path):
        shutil.rmtree(build_path)
    os.mkdir(build_path)


def copy_theme(build_path, theme):
    """Copy the theme static content into the build static directory.

    Parameters
    ----------
    build_path : str
        Path of the build.

    theme : str
        Name of the theme to install.
    """

    ## Copy the static/ folder of the theme
    shutil.copytree(
        os.path.join("themes", theme, "static"), os.path.join(build_path, "static")
    )


def render_index(build_path, sketches, site, page_template):
    """Render the index using the list of sketches and site configuration

    The index is rendered using a Jinja2 template inside the theme `templates/`
    directory.

    The index template must receive `sketches`, containing a list of the sketches
    names; and `site`, containing the site configuration from ``config.yaml``.

    Parameters
    ----------
    build_path : str
        Path of the build.

    sketches : list
        Contains all the sketches in the project. Must contain at leas `["name"]`.
    
    site : dict
        Contains the site information, such as `sitename` and `author`.

    page_template : Jinja2.Template
        Jinja2 template to render the sketch.
    """

    # Open the index in the build path for writing
    index = open(os.path.join(build_path, "index.html"), "w")

    # Write the contents of the rendered template into the index file
    index.write(
        page_template.render(sketches=map(lambda a: a["name"], sketches), site=site)
    )
    index.close()


def render_sketch_page(build_path, sketch, site, page_template):
    """Render a sketch page

    This generates the page for a single sketch. This will convert the
    `sketch["data"]` into a form that will control the variables of the
    script.

    When `sketch["data"]` doesn't define fields that may be used at the moment
    of the form generation, Ginpar will instead look up for those fields in
    `site["sketch_defaults"]`. 

    When both `sketch["data"]` and `site["sketch_defaults"]` don't define those
    fields, Ginpar will use the default values. 

    `Ginpar default values for sketch data <https://ginpar.readthedocs.io/en/latest/data.html>`_

    Parameters
    ----------

    build_path : str
        Path of the build.

    sketch : dict
        Sketch information. Must contain `["data"]` and `["name"]`

    site : dict
        Site configuration.
        
    page_template : Jinja2.Template
        Jinja2 template to render the sketch.
    """
    ## Create a directory with the sketch title
    os.mkdir(os.path.join(build_path, sketch["name"]))

    ## Convert the form JSON into a dict
    form_dict = sketch["data"]

    ## Add name key to the dict elements
    form_dict = gg.add_name(form_dict)

    ## Create index.html
    sketch_index = open(f"public/{sketch['name']}/index.html", "w+")
    sketch_index.write(
        page_template.render(
            sketch=unkebab(sketch["name"]), form=gg.sketch_index(form_dict), site=site
        )
    )
    sketch_index.close()

    ## Create sketch.js
    sketch_path = f"public/{sketch['name']}/sketch.js"
    sketch_script = open(sketch_path, "w+")

    ## Copy all the content from original sketches/{title}.js to sketch.js
    sf = open(sketch["script"], "r")

    sketch_script.write(gg.makeValueGetter(form_dict))

    for x in sf.readlines():
        sketch_script.write(x)
    sf.close()
    sketch_script.close()


def read_config(path):
    """Create a dictionary out of the YAML file received

    Paremeters
    ----------
    path : str
        Path of the YAML file.
    """
    with open(path, "r") as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    return config


def build(path):
    """Main function of the module. This is what `ginpar build` calls.

    Parameters
    ----------
    build_path : str
        Path of the build.
    """

    _SITE_FILE = "config.yaml"
    _SITE = read_config(_SITE_FILE)
    _THEME = _SITE["theme"].split("/")[1]
    _THEME_PATH = os.path.join("themes", _THEME)
    _TEMPLATES_PATH = os.path.join(_THEME_PATH, "templates")
    _SKETCHES_PATH = _SITE["content_path"]
    _jinja_env = Environment(loader=FileSystemLoader(_TEMPLATES_PATH), trim_blocks=True)
    _jinja_env.filters["unkebab"] = unkebab

    if not os.path.isdir(_THEME_PATH):
        clone_repo(_SITE["theme"], _THEME_PATH)
        delete_git_files(_THEME_PATH)

    create_publishing_directory(path)
    echo(f"Building in `{os.path.abspath(path)}`")

    copy_theme(path, _THEME)
    echo(f"Building using theme `{_THEME}`")

    ## Create the sketches list
    sketches = list(get_sketches(_SKETCHES_PATH))
    echo(f"Found {len(sketches)} sketch(es)")

    render_index(path, sketches, _SITE, _jinja_env.get_template("index.html"))
    echo("Building main page")

    echo("Building sketches:")
    for sketch in sketches:
        echo(f"  Building {sketch['name']}")
        render_sketch_page(path, sketch, _SITE, _jinja_env.get_template("sketch.html"))

    success("Success.")
