Introduction
============

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
`Adapting existing sketches`_ and `Specifying the parameters`_.

**To be fully sure of how easy is to use Ginpar, check this** example_ 
**together with its** `source code`_. You can ignore ``requirements.txt``,
``runtime.txt``, ``netlify.toml``, ``README.md``, and ``.gitignore``.

Prerequisites
-------------

For now Ginpar only runs using Python >= 3.6.
Future versions will add compatibility with Python 2.

Installation
------------

The easiest way to install the latest version of Ginpar is using pip:

.. prompt:: bash

    pip install ginpar

To make sure it's installed and working, run:

.. prompt:: bash

    ginpar --version

Quickstart
----------

Ginpar has an example project ready for installation, it contains the default
project structure and a sketch example.

If you're new to static content generators, this may be the best way to start.

.. prompt:: bash

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

.. prompt:: bash

    cd quickstart
    ginpar serve

And the project will be live in `localhost:8080 <localhost:8080>`_

Now, you can start to modify the contents of ``config.yaml`` and 
``sketches/``.

Next, you should read `Creating new sketches`_, or `Serving & Building`_.

Initialization
--------------

Alternatively, if you want to start a new project without importing anything
extra, run:

.. prompt:: bash

    ginpar init

This will prompt you for the values to build your configuration file and then
create the project using those values.

With this command, you may configure things like the destination and source
directories (``public`` and ``sketches`` by default).

Check :ref:`cli:ginpar init` or run ``ginpar init --help`` for more
information.

Creating new sketches
---------------------

Ginpar has a handy command to start new projects with some configuration
already set:

.. prompt:: bash

    ginpar new [SKETCH]

This will create a new sketch inside your predefined source directory.
You must set the name of the sketch when running the command.

Check :ref:`cli:ginpar new` or run ``ginpar new --help`` for more information.

Now, you must be `specifying the parameters`_.

Adapting existing sketches
--------------------------

For Ginpar to build the interactive page, you'll need to add some modifications
to your sketch code.

Adding it to the list of sketches
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

First, make your sketch detectable by Ginpar:

#. Create a directory ``my-sketch/`` inside ``sketches/``.
#. Copy your existent sketch script inside ``my-sketch`` and rename it to
   ``sketch.js``.
#. Create a ``data.yaml`` file.

You should end with a structure like this::

    .
    └── sketches/
        └── my-sketch/
            ├── sketch.js
            └── data.yaml

Making your sketch compatible with Ginpar
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In your ``createCanvas`` instruction, add ``.parent("artwork-container")``.

Now, you must be `specifying the parameters`_.

Specifying the parameters
-------------------------

Each sketch is a directory that contains two files: ``sketch.js`` and
``data.yaml``. The ``data.yaml`` file is where the parameters specification
takes place.

To create a parameters list, add this to your data file:

.. code-block:: yaml

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

Once parsed, Ginpar will produce:

- A form containing each of the items in the ``parameters`` list:
    .. code-block:: HTML

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

- A JS code fragment to update each of the parameters using the form values:
    .. code-block:: JavaScript

      function updateVars() {
        MY_VARIABLE = document.getElementByID("my-variable").value;
        // More variable updates. One for each params element.
      }

If the type of the input is a ``number``, Ginpar will parse it before
assigning it to the variable.

----

To use this parameters inside your sketch, just use the same name you used as
key:

.. code-block:: JavaScript

  console.log(MY_VARIABLE)
  // ==> 30

Serving & Building
------------------

Ginpar has two different commands to build your site:

.. prompt:: bash

  ginpar build

Will build your site into the ``build_directory`` path, which by default is
``public``.

.. prompt:: bash

  ginpar serve

Will build your site and start a new server on ``localhost:8080``. 
You can specify the port with ``--port``.

Check :ref:`cli:ginpar serve` and :ref:`cli:ginpar build`, or run
``ginpar serve --help``, ``ginpar build --help`` to see the full list of
options and arguments available.

.. Links

.. _example: https://genp.netlify.com
.. _CLI: /cli
.. _data: /data
.. _config: /config
.. _source code: https://github.com/davidomarf/ginpar-quickstart
