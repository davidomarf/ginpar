Site configuration
==================

This is the API documentation for the configuration file of a Ginpar site:
``config.yaml``.

This file contains all the metadata for your site, such as your name, the name
of the site, the repository, social links, etc.

The following data fields are the ones used by Ginpar. However, you can design
a custom theme or template that makes uses of extra fields.

author
------

*String, optional* [**Not defined by default**]

The name of the author of the site. This will be used to set Copyright messages
and meta tags.

sitename
--------

*String, optional* [**Not defined by default**]

The name of the site. This will be used to set Copyright messages
and meta tags.

description
-----------

*String, optional* [**Not defined by default**]

The description of the site. This will be used as a meta tag, and will appear
in the index of the site.

url
---

*String, optional* [**Not defined by default**]

The URL you'll be using to redirect to the site's content.

theme
-----

*String, required* [**davidomarf/gart**]

If the theme you want to use is a GitHub repository, set this value to
``AUTHOR/REPO``.

If it's a git repository in a different server, add the ``.git`` address.

Alternatively, you can add a string that matches the name of one directory
inside the ``themes/`` folder for a locally designed theme.

The default value is ``davidomarf/ginpar``

content_path
------------

*String, required* [**sketches**]

The directory that contains the project sketches. This path is referenced
when you run :ref:`cli:ginpar build` and :ref:`cli:ginpar serve`.

build_path
----------

*String, required* [**public**]

The directory Ginpar will use to build the site.

scripts
-------

*List, Optional* [**Not defined by default**]

This is a list of scripts and the url to fetch them. You can later reference
the items of this list to include them in individual sketches.

The structure is this:

.. code-block:: yaml

    scripts:
        p5:
            "p5-url"
        extra:
            "extra-url"
        lib:
            "lib-url"

sketch_defaults
---------------

*Object, Optional* [**Not defined by default**]

Here you'll add the same content you'd otherwise manually add to every sketch
in your project.

For example, if you'd like all your sketches to **not allow a global_seed**,
you'd need to add this to your config.json file:

.. code-block:: YAML

    sketch_defaults:
        global_seed: False

Now, all your sketches will automatically have the value
``global_seed: False``. However, you can manually replace that value for a
single sketch.

For all the available values, check :ref:`data:Sketch data`.
