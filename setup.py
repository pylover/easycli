import re
from os.path import join, dirname

from setuptools import setup, find_packages


# reading package's version (same way sqlalchemy does)
with open(join(dirname(__file__), 'easycli', '__init__.py')) as f:
    version = re.match(".*__version__ = '(.*?)'", f.read(), re.S).group(1)


setup(
    name='easycli',
    version=version,
    author='Vahid Mardani',
    author_email='vahid.mardani@gmail.com',
    url='http://github.com/pylover/easycli',
    description='Easily define your Command line and sub-commands using '
        'argparse.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        'argcomplete'
    ],
    packages=find_packages(exclude=['tests']),
    license='MIT',
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development',
    ]
)
