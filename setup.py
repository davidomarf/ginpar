import setuptools

version = '1.0.0'

requires = ['jinja2 >= 2.7', 'pyyaml', 'click', 'livereload']

setup_requires = ['wheel']

entry_points = {
    'console_scripts': [
        'ginpar = ginpar.cli:cli',
    ]
}

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='ginpar',
    version=version,
    url='https://github.com/davidomarf/ginpar',
    author='David Omar Flores Chávez',
    author_email='david@davidomar.com',
    description='A static content generator for interactive and parametrisable p5.js canvases.',
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=requires,
    entry_points=entry_points,
    classifiers=[
         'Programming Language :: Python :: 3',
         'License :: OSI Approved :: MIT License',
         'Operating System :: OS Independent',
    ],
)