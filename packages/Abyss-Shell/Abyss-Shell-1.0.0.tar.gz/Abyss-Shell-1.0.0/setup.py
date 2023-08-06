from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='Abyss-Shell',
  version='1.0.0',
  description='A very basic package to create shells/menus.',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Marlon Hernández',
  author_email='mmarlon.ssantiago@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='Shell', 
  packages=find_packages(),
  install_requires=['wheel','colorama','requests','pyfiglet','tqdm'] 
)