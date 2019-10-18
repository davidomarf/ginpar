import shutil
import os

from ginpar.utils.echo import echo, error, success, info

def check_existence(path):
    return os.path.isfile(path) or os.path.isdir(path)

def create_file(file, content):
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


def create_folder(folder, force = False):
    echo(f"> Creating `{folder}`:")
    try:
        os.makedirs(folder)
    except FileExistsError:
        error("Failure. It already exists.")
    except:
        error("Failure.")
    else:
        success("Sucess")


def copy_folder(fr, to, force = False):
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
