# Ginpar

[![PyPI](https://img.shields.io/pypi/v/ginpar)](https://pypi.org/project/ginpar/)
[![Build](https://github.com/davidomarf/ginpar/workflows/build/badge.svg)](https://github.com/davidomarf/ginpar/actions?workflow=build)
[![Documentation Status](https://readthedocs.org/projects/ginpar/badge/?version=stable)](https://ginpar.readthedocs.io/en/stable/?badge=stable)


---

**Ginpar is, and will be unstable until we don't release a v1.0.0.**

---

Ginpar is a **static content generator** for interactive P5.js sketches,
awkwardly named after **Generative Interactive Parametrisable Canvases**.

By separating the primary development and the parametric experimentation,
it allows you to stop thinking about code once your pieces have reached an
acceptable level of complexity, freeing you to experiment in a GUI for the
browser.

Features:

- Simple API to define the controllable variables in your sketch.
- Easy to adapt existing sketches.
- Easy replicability of each final result.
- Index page to list all your sketches.

Check [ginpar-quickstar.netlify.com](https://ginpar-quickstart.netlify.com/) to
see how a site generated with Ginpar looks like.

The following Introduction is part of the [Ginpar Documentation][ginpar-docs] and
may be read at [Introduction][docs-intro]

## Table of contents

- [Introduction](#introduction)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
    - [Quickstart](#quickstart)
    - [Initialization](#initialization)
    - [Creating new sketches](#creating-new-sketches)
    - [Adapting existing sketches](#adapting-existing-sketches)
    - [Specifying the parameters](#specifying-the-parameters)
    - [Serving & Building](#serving-&-building)
- [Build with](#built-with)
- [Versioning](#versioning)
- [Contributors](#contributors)
- [License](#license)

## Introduction

This is a quick introductory documentation for the Ginpar static content
generator.

Ginpar works similarly to other engines such as Jekyll, Hugo, or Pelican, but
with a narrower and deeper set of functionalities, since it's very specific in
its task.

The two main objectives of Ginpar are:

- Allowing artists to stop thinking about code when experimenting with the
  parameters that control the results of the artwork, achieving a **quicker
  feedback loop.**

- Making interactive websites to share the artist's work, letting users play
  with the same GUI.


The basic structure of a Ginpar project consists of a ``config.yaml`` file,
and a ``sketches`` directory.

It's easy to adapt your existing sketches to work with Ginpar. In fact, the
only **necessary** step is to add ``.parent("artwork-container")`` to the
``createCanvas()`` call.

But to fully take advantage of Ginpar ---that is, the interactive sketch with
custom parameters---, you need to create a ``data.yaml`` file. Check 
[Adapting existing sketches](#adapting-existing-sketches) and 
[Specifying the parameters](#specifying-the-parameters).

**To be fully sure of how easy is to use Ginpar, check this
[example][ginpar-quickstart] together with its 
[source code][quickstart-repo].** 
You can ignore ``requirements.txt``, ``runtime.txt``, ``netlify.toml``,
``README.md``, and ``.gitignore``.

### Prerequisites

For now Ginpar only runs using Python >= 3.6.
Future versions will add compatibility with Python 2.

### Installation

The easiest way to install the latest version of Ginpar is using pip:

    pip install ginpar

To make sure it's installed and working, run:

    ginpar --version

### Quickstart

Ginpar has an example project ready for installation, it contains the default
project structure and a sketch example.

If you're new to static content generators, this may be the best way to start.

    ginpar quickstart

This will create the following directory structure::

    .
    ├── config.yaml
    └── sketches/
        ├── circles/
        │   ├── sketch.js
        │   └── data.yaml
        └── ...

To build the project and start a server, run:

    cd quickstart
    ginpar serve

And the project will be live in [localhost:8080](localhost:8080)

Now, you can start to modify the contents of ``config.yaml`` and 
``sketches/``.

Next, you should read [Creating new sketches](#creating-new-sketches),
or [Serving & Building](#serving-building).

### Initialization

Alternatively, if you want to start a new project without importing anything
extra, run:

    ginpar init

This will prompt you for the values to build your configuration file and then
create the project using those values.

With this command, you may configure things like the destination and source
directories (``public`` and ``sketches`` by default).

Check [ginpar init][ginpar-init] or run ``ginpar init --help`` for more
information.

### Creating new sketches

Ginpar has a handy command to start new projects with some configuration
already set:

    ginpar new [SKETCH]

This will create a new sketch inside your predefined source directory.
You can set the name when running the command, but it's optional.

Check [cli:ginpar new][ginpar-new] or run ``ginpar new --help`` for more
information.

Now, you must be [specifying the parameters](#specifying-the-parameters).

### Adapting existing sketches

For Ginpar to build the interactive page, you'll need to add some modifications
to your sketch code.

#### Adding it to the list of sketches

First, make your sketch detectable for Ginpar:

1. Create a directory ``my-sketch/`` inside ``sketches/``.
1. Copy your existent sketch script inside ``my-sketch`` and rename it to
   ``sketch.js``.
1. Create a ``data.yaml`` file.

You should end with a structure like this::

    .
    └── sketches/
        └── my-sketch/
            ├── sketch.js
            └── data.yaml

#### Making your sketch compatible with Ginpar

In your ``createCanvas`` instruction, add ``.parent("artwork-container")``.

Now, you must be [specifying the parameters](#specifying-the-parameters).

### Specifying the parameters

Each sketch is a directory that contains two files: ``sketch.js`` and
``data.yaml``. The ``data.yaml`` file is where the parameters specification
takes place.

To create a parameters list, add this to your data file:

 ```yaml
---
date: 2019-11-04
# ... other data
# ...

# Key that contains a list of parameters
params:

  # The name of the parameter must be the key of the element
  # It must match a variable in your sketch.js file
  - MY_VARIABLE:

      # Ginpar parameters definition keys. All optional.
      # For a full list check the API
      randomizable: True
      name: My displayed variable name

      # HTML valid attributes
      attrs:
        type: number
        value: 30
        step: 1
        min: 0
        max: 100
```

Once parsed, Ginpar will produce:

- A form containing each of the items in the ``parameters`` list:
    ```html
      <form>
        <div class="form-field">
            <label for="my-variable">
                My displayed variable name
            </label>
            <input name="my-variable"
                    id="my-variable"
                    type="number"
                    value="30"
                    step="1">
          </div>
        <!-- More form-fields. One for each params element. --->
      </form>
    ```
    
- A JS code fragment to update each of the parameters using the form values:
    ```JS

      function updateVars() {
        MY_VARIABLE = document.getElementByID("my-variable").value;
        // More variable updates. One for each params element.
      }
    ```

If the type of the input is a ``number``, Ginpar will parse it before
assigning it to the variable.

---

To use this parameters inside your sketch, just use the same name you used as
key:

```js
console.log(MY_VARIABLE)
// ==> 30
```

### Serving & Building

Ginpar has two different commands to build your site:

  ginpar build

Will build your site into the ``build_directory`` path, which by default is
``public``.

  ginpar serve

Will start a new server on ``localhost:8000`` and open your default web
browser. You can specify the port with ``--port``.

Check [ginpar serve][ginpar-serve] and [ginpar build][ginpar-build], or run
``ginpar serve --help``, ``ginpar build --help`` to see the full list of
options and arguments available.

---

## Built With

- [Jinja2][jinja] - Templating language.
- [Click][click] - CLI Tool composer.
- [PyYAML][pyyaml] - YAML framework.
- [Livereload][livereload] - Hot reloading server.

## Versioning

We use [SemVer][semver] for versioning. For the versions
available, see the
[tags on this repository](https://github.com/davidomarf/ginpar/tags).

## Contributors

- **David Omar** - _Initial work_ -
  [davidomarf](https://github.com/davidomarf)

See also the list of
[contributors](https://github.com/davidomarf/ginpar/contributors)
who participated in this project.

## License

This project is licensed under the MIT License - see the
[LICENSE.md](LICENSE) file for details

[semver]: semver.org
[jinja]: https://jinja.palletsprojects.com/
[click]: https://click.palletsprojects.com/
[pelican]: https://getpelican.com
[algo]: https://github.com/davidomarf/gen.algorithms
[ginpar-docs]: https://ginpar.readthedocs.io
[docs-intro]: https://ginpar.readthedocs.io/en/latest/intro.html
[ginpar-serve]: https://ginpar.readthedocs.io/en/latest/cli.html#ginpar-serve
[ginpar-build]: https://ginpar.readthedocs.io/en/latest/cli.html#ginpar-build
[ginpar-init]: https://ginpar.readthedocs.io/en/latest/cli.html#ginpar-init
[ginpar-new]: https://ginpar.readthedocs.io/en/latest/cli.html#ginpar-new
[pyyaml]:https://pyyaml.org
[livereload]: https://github.com/lepture/python-livereload
[ginpar-quickstart]: https://ginpar-quickstart.netlify.com/
[quickstart-repo]:https://github.com/davidomarf/ginpar-quickstart