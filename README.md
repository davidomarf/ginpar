# Ginpar

[![PyPI](https://img.shields.io/pypi/v/ginpar)](https://pypi.org/project/ginpar/)
[![Build](https://github.com/davidomarf/ginpar/workflows/build/badge.svg)](https://github.com/davidomarf/ginpar/actions?workflow=build)
[![Documentation Status](https://readthedocs.org/projects/ginpar/badge/?version=stable)](https://ginpar.readthedocs.io/?badge=stable)

---

**Ginpar is, and will be unstable until we don't release a v1.0.0.**

---

Ginpar is a **static website generator** for interactive P5.js sketches,
awkwardly named after **Generative Interactive Parametrisable Canvases**.

Key features:

- Generate an individual page for each sketch in your project.
- Generate forms to control the parameters of the sketch on the go.
- Specify what parameters from the sketch you want to control.
- Generate an index page that links to every sketch.

Ginpar aims to generate portfolios for generative artists.

## Contents

- [How to use](#how-to-use)
  - [tl;dr](#tldr)
  - [Installing](#Installing)
  - [Initializing](#initializing)
  - [Quickstarting](#quickstarting)
  - [Creating sketch files](#creating-sketch-files)
    - [sketch.js](#sketchjs)
    - [data.yaml](#datayaml)
  - [Building](#building)
  - [Deploying](#Deploying)
    - [Netlify](#netlify)
- [Built with](#built-with)
- [Versioning](#Versioning)
- [Contributors](#Contributors)
- [License](#License)

## How to use

### tl;dr:

1. Install
   ```sh
   $ pip install ginpar
   ```
1. Initialize a new project
   ```sh
   $ ginpar init
   ```
1. Build
   ```sh
   $ ginpar build
   ```

Alternatively to `init`, you can use `quickstart` and import a working example
automatically.

Use `ginpar --help` to see a list of commands and options for each one.

### Installing

For now the only way to get ginpar running is by installing the PyPi package:

```bash
$ pip install ginpar
```

### Initializing

```sh
$ ginpar init
```

Ginpar will prompt you for the variables of your site, such as `name`,
`description`, `author`, etc.

This will create a new directory under the name you specified for `name`.

Available flags:

- `--quick, -q`: Skip the prompt and load the default values
- `--force, -f`: If there's a directory with the same name, remove it.

### Quickstarting

```sh
$ ginpar-quickstart
```

Ginpar includes a working example so you can modify its contents, and learn
how to set your own projects if current docs are not enough (they're not).

Available flags:

- `--force, -f`: If there's a directory with the same name, remove it.

### Creating sketch files

Every directory inside the `sketches/` folder will be considered a sketch if
it contains:

- `sketch.js`
- `data.yaml`

For example, for a sketch named `rectangle`, you'd need this file structure:

```
sketches/
  |- rectangle/
      |- sketch.js
      |- data.yaml
```

#### sketch.js

This is the script for the sketch. The only modifications you need to do to
be able to use ginpar are:

- Add a `.parent("artwork-container")` to the `createCanvas` instruction.

#### data.yaml

The `data.yaml` file will contain the list of variables that you'll be able to
control in the final sketch page.

The structure is this:

```yaml
---
# The name of the variable to control in your sketch.js file
- var: NUMBER_OF_POINTS 
  # Valid HTML input attributes, or ones that fit our API
  attrs: 
    type: number 
    value: 30
    step: 1
- var: SOME_RATIO
  # You can specify a custom name to display in the HTML form
  name: Minimum column height factor 
  attrs:
    type: range
    value: 0.1
    step: 0.01
    # These are all valid HTML attributes
    min: 0 
    max: 1
```

Ginpar will automatically produce the HTML forms, and the scripts to update the
script variables everytime the input values change.

You don't need to declare these values in your JS file, but you can do it. If
you decide to, **declare them with either `let` or `var`, not with `const`.**

### Building

To build, simply run:

```sh
ginpar build
```

### Deploying

For now, we've only deployed in Netlify. However, using any other server
to deliver static content should be easy.

### Netlify

You need to specify:

- the python version to run
  ```sh
  $ echo "3.7" > runtime.txt
  ```
- add `ginpar` as dependency
  ```sh
  $ echo "ginpar" > requirements.txt
  ```
- tell Netlify how to build
  ```sh
  $ echo -e "[build]\n  command = \"ginpar build\"\n  publish = \"public\"" > netlify.toml
  ```

Then just make a deployment and you'll be ready to go.

To see a site in production, check [gen.algorithms][algo]

## Built With

- [Jinja2][jinja] - Templating language.
- [Click][click] - CLI Tool composer.
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
[examples]: examples
[config-example]: config-example
[params-api]: params-api
[jinja]: https://jinja.palletsprojects.com/
[click]: https://click.palletsprojects.com/
[pelican]: https://getpelican.com
[algo]: https://github.com/davidomarf/gen.algorithms