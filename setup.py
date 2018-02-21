from setuptools import setup, find_packages

setup(
    name='kivydnd',
    version='0.5',
    description='Kivy Drag-n-Drop for Widgets',
    url='https://github.com/GreyGnome/KivyDnD',
    author='GreyGnome',
    author_email='mschwage@gmail.com',
    license='Apache License 2.0',
    packages=find_packages('kivydnd','examples'),
    package_data={
        '': ['*.md'],
        'examples': ['*'],
    },
)
