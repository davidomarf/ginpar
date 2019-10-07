# Ginpar ![PyPI](https://img.shields.io/pypi/v/ginpar)

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
  - [Preparing sketches](#preparing-sketches)
    - [Specifying parameters](#specifying-parameters)
    - [Assigning variables to corresponding values](#assigning-variables-to-corresponding-values)
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
1. Initialize
    ```sh
    $ ginpar-quickstart
    ```
1. Build
    ```sh
    $ ginpar
    ```

### Installing

For now the only way to get ginpar running is by installing the PyPi package:

```bash
$ pip install ginpar
```

### Initializing

Ginpar has a quickstart project that imports a theme with `jinja2` templates,
an example sketch, and an initial configuration file `config.py`:

```sh
$ ginpar-quickstart
```

### Preparing sketches

To use an existing sketch, you need to add some constants and functions with
tight restrictions.

We suggest to check some [examples][examples].

#### Specifying parameters

First you need to specify the parameters that will be controllable in the
sketch page. To do that, you must:

1. Declare a variable with a string containing **JSON valid syntax** that also
complies with [Ginpar API](#api).
1. Enclose the declaration with the delimiters `/* ##ginpar */`

```js
/* ##ginpar */
const paramsJSON = `[
  {
    "var": "WIDTH",
    "attrs": {
      "type": "number",
      "value": 2048,
      "min": 0,
      "max": 4096
    }
  },
  {
    "var": "HEIGHT",
    "attrs": {
      "type": "number",
      "value": 2560,
      "min": 0,
      "max": 5120
    }
  },
  {
    "var": "STOP_ODDS",
    "attrs": {
      "type": "range",
      "value": 0.8,
      "step": 0.001,
      "min": 0,
      "max": 1
    }
  }]`
/* ##ginpar */
```

It's necessary, as for the current version, to only include one declaration
between the delimiters. Ginpar relies on this to obtain the JSON string.

#### Assigning variables to corresponding values

This is optional, since Ginpar will automatically generate the JS script that
fetches the values of the form and assign it to the variables. 

However, following this step will allow you to keep using the sketch script
without needing to use Ginpar.

To do this, declare a new function that converts the `paramsJSON` string back
into variables:

```js
function jsonToVars(json){
  return Object.assign(...json.map(e => {return {[e.var]: e.attrs.value}}))
}
```

And re-write the declarations of the original variables like this:

```js
const {
  WIDTH,
  HEIGHT,
  // Any other constant you declared in paramsJSON
  STOP_ODDS } = jsonToVars(JSON.parse(paramsJSON))
```

Note that for this to work, the constant symbol (e.g. `WIDTH`) **must** be
equal to the value of `var` in the JSON array 
(e. g. `{"var": "WIDTH", "attrs": {...}}`).

## Building

To build, simply run:

```sh
ginpar
```

---

The building process consists of:

- Making a `public/` directory.
- Reading the `config.json` file (this consists of, among other things, the
author info, the Ginpar theme, and the website url).
- Copying the static content of the selected theme into `public/`
- Listing the contents of `sketches/`, and using the ones with `.js` 
extension to:
  - Make a directory `public/filename/` that contains a generated `index.html`
    and `sketch.js`.
  - Create a `public/index.html` file that adds `a` tags for every `filename`.

If you want to quickstart a project, read [initializing](#initializing).

## Deploying

For now, we've only deployed in Netlify. However, using any other server
to deliver static content should be easy.

### Netlify

How to deploy to Netlify

## Built With

* [Jinja2][jinja] - Templating language for Python.

## Versioning

We use [SemVer][semver] for versioning. For the versions
available, see the 
[tags on this repository](https://github.com/davidomarf/ginpar/tags). 

## Contributors

* **David Omar** - *Initial work* - 
[davidomarf](https://github.com/davidomarf)

See also the list of 
[contributors](https://github.com/davidomarf/ginpar/contributors)
who participated in this project.

## License

This project is licensed under the MIT License - see the 
[LICENSE.md](LICENSE) file for details

[semver]:semver.org
[examples]: examples
[config-example]:config-example
[params-api]:params-api
[jinja]:https://jinja.palletsprojects.com/
[pelican]:https://getpelican.com