"""File management for common Ginpar operations.

This module implements the default ways of managing file creation, deletion,
copying, and moving.
"""
import shutil
import os

from ginpar.utils.echo import echo, error, success, info


def check_existence(path):
    """Check if the received path exists as either a file or a directory.

    Parameters
    ----------
    path : str
        Can be a valid path or not.
    """
    return os.path.isfile(path) or os.path.isdir(path)


def create_file(file, content):
    """Attempt the creation of a new file with custom content.

    Parameters
    ----------
    file : str
        Name of the file to be created (path must be included).

    content : str
        Content to write into the file.
    """
    echo(f"> Creating `{file}`:")
    try:
        config = open(file, "r")
    except:
        try:
            config = open(file, "w+")
        except:
            error("Failure.")
        else:
            config.write(content)
            config.close()
            success("Success.")
    else:
        config.close()
        error("Failure. It already exists.")


def create_folder(folder, force=False):
    """Attempt (and optionally force) the creation of a new folder.

    Parameters
    ----------
    folder : str
        Name of the folder to be created (path must be included).

    force : bool
        Will remove an existing directory with the same name, if it exists.
    """
    echo(f"> Creating `{folder}`:")
    try:
        os.makedirs(folder)
    except FileExistsError:
        error("Failure. It already exists.")
    except:
        error("Failure.")
    else:
        success("Sucess")


def copy_folder(fr, to, force=False):
    """Attempt (and optionally force) the copy of a folder.

    Parameters
    ----------
    fr : str
        From. Path of the folder to be copied.

    to : str
        To. Path of the to be created.

    force : bool
        Will remove an existing directory with the same name of ``to``, if it exists.
    """
    echo(f"\n> Copying `{to}` from `{fr}`:")

    exists = check_existence(to)

    if exists and force:
        try_remove(to)

    try:
        shutil.copytree(fr, to)
    except FileExistsError:
        error(f"Failure. It already exists.")
    else:
        success(f"Success.")


def try_remove(path):
    """Attempt the removal of a path, either if it is a file or a directory.

    Parameters
    ----------
    path : str
        Must be an existing path.

    Notes
    -----
    To check for the existence of the path, previous to calling ``try_remove``, use
    `check_existence`_.
    """
    print(path)
    if os.path.isdir(path):
        echo(f"> `{path}` already exists. Attemping removal:")
        try:
            shutil.rmtree(path)
        except:
            error("Failure. Restart or delete manually.")
        else:
            success("Success.")
    elif os.path.isfile(path):
        echo(f"> `{path}` already exists. Attemping removal:")
        try:
            os.remove(path)
        except:
            error(f"Failure. Restart or delete manually.")
        else:
            success(f"Success.")
    else:
        echo(f"> `{path}` doesn't exist.")
        info("Skipping.")
