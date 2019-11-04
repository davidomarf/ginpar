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

obfuscate
~~~~~~~~~

*Boolean, Optional* [**False**]

When **True**, Ginpar will obfuscate the sketch source code before creating
the script file in the final build.

This option will use `Javascript Obfuscator`_

draft
~~~~~

*Boolean, Optional* [**False**]

When **True**, Ginpar will skip this sketch in the building proccess.


global_seed
~~~~~~~~~~~

*Boolean, Optional* [**True**]

When **True**, Ginpar will create a unique base 64 seed for each sketch
result, and allow the user to put that ID as an input field so it
automatically sets all the parameter values necessary to generate the same
result again.

.. Links

.. _Jinja: https://jinja.palletsprojects.com/en/2.10.x/
.. _`Javascript Obfuscator`: https://obfuscator.io
