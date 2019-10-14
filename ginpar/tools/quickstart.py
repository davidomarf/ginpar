import os
import shutil
from pathlib import Path
import sys

from jinja2 import Environment, FileSystemLoader


_TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              'templates')

_THEMES_DIR = os.path.join(Path(os.path.dirname(os.path.abspath(__file__))).parent,
                              'themes')

_SKETCHES_DIR = os.path.join(Path(os.path.dirname(os.path.abspath(__file__))).parent,
                              'sketches')

_jinja_env = Environment(
    loader=FileSystemLoader(_TEMPLATES_DIR),
    trim_blocks=True,
)


def argv_to_flag_dict(argv):
    """Take an arguments vector and convert it into a dictionary"""
    possible_args = ["--force"]
    flags = {}
    for arg in possible_args:
        if arg in argv:
            flags[arg] = True
    return flags


def create_folder(folder):
    print(f'Creating `{folder}`:', end='\n\t')
    try:
        os.mkdir(folder)
    except FileExistsError:
        print(f'Failure. It already exists.')
    except:
        print(f'Failure.')
    else:
        print(f'Sucess')


def init_config():
    print('\nCreating `config.json` using template:', end = '\n\t')
    try:
        config = open('config.json', 'r')
    except:
        try:
            config = open('config.json', 'w+')
        except:
            print('Failure.')
        else:
            _template = _jinja_env.get_template('config.json.jinja2')
            config.write(_template.render())
            config.close()
            print('Success.')
    else:
        print("Failure. It already exists.")

def copy_folder(fr, to):
    print(f'\nCopying `{to}` from `{fr}`:', end = '\n\t')
    try:
        shutil.copytree(fr, to)
    except FileExistsError:
        print(f'Failure. It already exists.')
    else:
        print(f'Success.')

def try_remove(path):
    if os.path.isdir(path):
        print(f'`{path}` already exists. Attemping removal:', end = '\n\t')
        try:
            shutil.rmtree(path)
        except:
            print(f'Failure. Restart or delete manually.')
        else:
            print(f'Success.')
    elif os.path.isfile(path):
        print(f'`{path}` already exists. Attemping removal:', end = '\n\t')
        try:
            os.remove(path)
        except:
            print(f'Failure. Restart or delete manually.')
        else:
            print(f'Success.')
    else:
        print(f'`{path}` doesn\'t exist. Skipping.')

def main():
    flags = argv_to_flag_dict(sys.argv)
    
    if "--force" in flags:
        print("\n---\nForcing quickstart. This will replace existent directories and files.\n---\n")
        try_remove('sketches')
        try_remove('themes')
        try_remove('config.json')

    print("\n---\nInitializing the project with default values\n---\n")
    copy_folder(_THEMES_DIR, 'themes')
    copy_folder(_SKETCHES_DIR, 'sketches')
    init_config()


if __name__ == '__main__':
    main()