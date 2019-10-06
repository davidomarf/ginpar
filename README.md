# Ginpar ![PyPI](https://img.shields.io/pypi/v/ginpar)

Awkwardly named after _Generative Interactive Parametrisable Canvases_.

Generate a static site that indexes a list of P5.js sketches and turns each of
those into an interactive sketch.

- Sketches are inside a folder `sketches/`
- Will use the filename as the sketch name.
- Index of the site will contain a list of `a` tags for each `sketch`.
- Will read each sketch and create a page for each one:
  - A form will be created using a `params` object that specifies the type,
  range, step, and default values of the variables.
  - A fixed section will contain the canvas and will allow for easy saving,
  auto-naming using the seed, and scaling.

Current version may work for other libraries, but it's only meant for P5.js.

Following versions my guarantee support for different libraries.

## How to use

1. Install Ginpar.
  `pip install ginpar`
1. Initialize a new project
  `ginpar-init`
1. Modify `config.py` to reflect the metadata of the website.
1. Add your sketches to `sketches/`. Feel free to remove `example.js`.
1. For each script, you must define the `ginpar.params` object
  (preferably at the beginning).
  Read the [`ginpar.params` API][params-api]
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
    **Note that the `/* ##ginpar */` are the important thing to add!**
1. To convert this JSON into the original variables you had declared, add:
    ```js
    function jsonToVars(json){
      return Object.assign(...json.map(e => {return {[e.var]: e.attrs.value}}))
    }

    let {WIDTH, HEIGHT, STOP_ODDS} = jsonToVars(JSON.parse(paramsJSON))
    ```
    This will automatically assign the variables `WIDTH`, `HEIGHT`,
    and `STOP_ODDS` to the value they had on the `paramsJSON`.
1. In your `setup()` function, in your `createCanvas` instruction, add:
  `createCanvas(w, h).parent("artwork-container");`
1. Build your static site
  `ginpar`.
1. Enjoy your site created at `public/`.

## Dependencies

This project only uses [Jinja2][jinja] as template engine, however, some code
snippets were heavily inspired by [Pelican][pelican] source code.

## License

[MIT](./LICENSE)

[config-example]:config-example
[params-api]:params-api
[jinja]:https://jinja.palletsprojects.com/
[pelican]:https://getpelican.com