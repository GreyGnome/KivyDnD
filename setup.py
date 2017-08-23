from setuptools import setup, find_packages

setup(name='kivydnd',
      version='0.2',
      description='Kivy Drag-n-Drop for Widgets',
      url='https://github.com/GreyGnome/KivyDnD',
      author='GreyGnome',
      author_email='notsureifneeded@gmail.com',
      license='Apache License 2.0',
      packages=find_packages(exclude=['examples'],))