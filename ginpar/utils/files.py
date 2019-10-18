import shutil
import os

from ginpar.utils.echo import echo, error, success, info


def create_folder(folder):
    echo(f"> Creating `{folder}`:")
    try:
        os.mkdir(folder)
    except FileExistsError:
        error("Failure. It already exists.")
    except:
        error("Failure.")
    else:
        success("Sucess")


def copy_folder(fr, to):
    echo(f"\n> Copying `{to}` from `{fr}`:")
    try:
        shutil.copytree(fr, to)
    except FileExistsError:
        error(f"Failure. It already exists.")
    else:
        success(f"Success.")


def try_remove(path):
    if os.path.isdir(path):
        echo(f"\n> `{path}` already exists. Attemping removal:")
        try:
            shutil.rmtree(path)
        except:
            error("Failure. Restart or delete manually.")
        else:
            success("Success.")
    elif os.path.isfile(path):
        echo(f"\n> `{path}` already exists. Attemping removal:")
        try:
            os.remove(path)
        except:
            error(f"Failure. Restart or delete manually.")
        else:
            success(f"Success.")
    else:
        info(f"> `{path}` doesn't exist. Skipping.")
