"""String filters to convert between cases.

The list of filters in here are added to the Jinja2 environment, so they may
come handy when designing a custom theme.
"""


def unkebab(s):
    """Replace dashes with spaces.

    Parameters
    ----------
    s : str
        String that may contain "-" characters.
    """
    return " ".join(s.split("-"))


def space_to_kebab(s):
    """Replace spaces with dashes.

    Parameters
    ----------
    s : str
        String that may contain " " characters.
    """
    return "-".join(s.split(" "))


def camel_to_space(s):
    """Replace low dashes with spaces.

    Parameters
    ----------
    s : str
        String that may contain "_" characters.
    """
    return " ".join(s.split("_"))
