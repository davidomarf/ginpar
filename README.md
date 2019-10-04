# Ginpar

Awkwardly named after _Generative Interactive Parametrisable Canvases_.

This is a light Python script that converts a list of P5.js projects into an
interactive website that includes forms to control the most important project
variables (defined by you) and adds utilities to make easier to replicate
previous results by forcing the use of seeds.

Current version may work for other libraries, but it's only meant for P5.js.

Following versions my guarantee support for different libraries.

## How to use

1. Download the content of this repository.
1. Clear the contents of `sketches/` and create your own.
1. For each script, you should add this (preferably at the beginning):
    ```js
    /* ## */
    const params = {
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
1. Make sure `config.py` is properly set up. Here you can specify the urls for
each library you'd need to use, and metadata for the website.
1. Run `python build.py`.
1. Enjoy your website created at `public/`.

## License

[MIT](./LICENSE)