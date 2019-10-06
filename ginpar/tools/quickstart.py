import os
import shutil
from pathlib import Path

from jinja2 import Environment, FileSystemLoader


_TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              'templates')

_THEMES_DIR = os.path.join(Path(os.path.dirname(os.path.abspath(__file__))).parent,
                              'themes')

_jinja_env = Environment(
    loader=FileSystemLoader(_TEMPLATES_DIR),
    trim_blocks=True,
)

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

def main():
    print("\n---\nInitializing the project with default values\n---\n")
    create_folder('sketches')
    copy_folder(_THEMES_DIR, 'themes')
    init_config()


if __name__ == '__main__':
    main()