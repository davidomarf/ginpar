Sketch data
===========

This is the API documentation for the data files of single sketches:
``data.yaml``.

Data files contain instructions to build the pages for individual sketches,
such as the sketch parameters, source code obfuscation, sketch hashing, etc.

All these values are converted into a Python dictionary and then associated
with the sketch. Ginpar will use this dictionary to render
``sketch templates``.

Check Jinja_ to learn how this templating works.

The following keys are the ones that:

- Ginpar uses to determine build flow, or
- Gart (the default theme) uses in its templates to render final pages.

The only indispensable key is ``params``. Every other key it's optional.

**If you want to use a configuration value for all your sketches, you may want
to read** :ref:`config:sketch_defaults`.

date
~~~~

**Date, Required** [**Date.today()**]

Used to sort the sketches in the index. The format is any valid date 
format, but the suggested is ``YYYY-MM-DD``: 2019-11-04.

The default value is th current day, however, this is only assigned when
you create the sketch using ``ginpar new [SKETCH]``.

params
~~~~~~

**List, Required**

This is the most important and the only required key for the data file.
In ``params``, you specify the sketch parameters and their attributes.

The key of every element **must match the variable name in your sketch.js**.

.. code-block:: YAML

    params:
        - YEAR:
            attrs:
                type: number
                value: 2019
                step: 1
        - RATIO:
            attrs:
                type: number
                value: 0.2
                step: 0.05
                min: 0
                max: 1

.. code-block:: JS

    console.log(NAME, YEAR, RATIO)
    // ==> "Ginpar", 2019, 0.2

For most of the variables, those attributes will suffice.

Ginpar will automatically remove low dashes and capitalize the parameter name,
however, you can also specify the name to display in the form:

.. code-block:: YAML

    params:
        - YEAR:
            name: Current year
            attrs:
                # ...

For a complete list of the fields you can specify for the ``params`` list,
check :ref:`params:Params API`.

global_seed
~~~~~~~~~~~

*Boolean, Optional* [**True**]

When **True**, Ginpar will add a button to generate new seeds, and will create
a file name for the saved image using ``{NAME}-{RANDOM_SEED}-{NOISE_SEED}``.

scripts
~~~~~~~

*List, Optional* [**site.scripts**]

By default, Ginpar will include all the scripts you specify in the
``config.yaml``. If you only wona to include a subset of these, you create
a list of the scripts to include.

.. code-block:: YAML

    # in config.yaml
    scripts:
        p5: https://my-p5-url
        d3: https://my-d3-url
        extra: https://extra
    
    # in data.yaml
    scripts:
        - p5
        - d3

The elements of `data.scripts` must exist as keys in your ``config.yaml`` file.

.. Links

.. _Jinja: https://jinja.palletsprojects.com/en/2.10.x/
.. _`Javascript Obfuscator`: https://obfuscator.io
