from setuptools import setup, find_packages
from codecs import open
from os import path

with open(path.join('.', 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='kivydnd',
    version='0.5.0',
    description='Kivy Drag-n-Drop for Widgets',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/GreyGnome/KivyDnD',
    author='GreyGnome',
    author_email='mschwage@gmail.com',
    license='Apache License 2.0',
    keywords='kivy drag-n-drop',
    packages=find_packages(exclude=[]),
    data_files=[('share/kivydnd-examples',
        [
            'examples/dndexample1.py',
            'examples/dndexample2.py',
            'examples/dndexample3.py',
            'examples/dndexample_copy_draggable.py',
            'examples/dndexample_drop_groups.py',
            'examples/dndexample_relative_layout.py',
            'examples/example_base_classes.py',
            'examples/example_base_classes.pyc',
        ]
    )],
)
#   packages=['kivydnd'],
