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
1. Create `config.toml` to indicate the metadata of the website. You can copy
   [this config.toml example][config-example].
1. Create `sketches/` and add all your P5.js sketches.
1. For each script, you must define the `ginpar.params` object
  (preferably at the beginning).
  Read the [`ginpar.params` API][params-api]
    ```js
    /* ## */
    const ginpar.params = {
    height: {
        value: 500,
        type: "number",
        range: [0, 4096]
    },
    my-variable: {
        value: .8,
        type: "slide",
        range: [0, 1],
        step: .05
        // ...
    },
    //   ...
    };
    /* ## */
    ```
    **Note that the `/* ## */` are the important thing to add!**
    
1. Run `python build.py`.
1. Enjoy your website created at `public/`.

## License

[MIT](./LICENSE)

[config-example]:config-example
[params-api]:params-api