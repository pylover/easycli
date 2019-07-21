# easycli

[![PyPI](http://img.shields.io/pypi/v/easycli.svg)](https://pypi.python.org/pypi/easycli)
[![Build Status](https://travis-ci.org/pylover/easycli.svg?branch=master)](https://travis-ci.org/pylover/easycli)
[![Coverage Status](https://coveralls.io/repos/github/pylover/easycli/badge.svg?branch=master)](https://coveralls.io/github/pylover/easycli?branch=master)

Command line interface for python application on top of the argparse 
including sub-parsers.

## Installation

```bash
pip install easycli
```


## Quickstart

`quickstart.py`

```python
from easycli import Root, SubCommand, Argument


__version__ = '0.1.0'
DEFAULT_TCP_PORT = 8585
DEFAULT_HOST = 'WPP.local'


class SubCommand1(SubCommand):
    __command__ = 'sub-command1'
    __aliases__ = ['s1', 'sc1']
    __arguments__ = [
        Argument(
            '-V', '--version',
            action='store_true',
            help='Show programmer\'s version'
        ),
        Argument(
            '-p', '--port',
            type=int,
            default=DEFAULT_TCP_PORT,
            help=f'TCP port, default: {DEFAULT_TCP_PORT}'
        ),
        Argument(
            '-H', '--host',
            default=DEFAULT_HOST,
            help=f'Hostname, default: {DEFAULT_HOST}'
        )

    ]

    def __call__(self, args):
        print('Sub command 1, args:', args)


class Example(Root):
    __help__ = 'easycli example'
    __completion__ = True
    __arguments__ = [
        Argument('-V', '--version', action='store_true', help='Show version'),
        SubCommand1,
    ]

    def __call__(self, args):
        if args.version:
            print(__version__)
            return

        return super().__call__(args)



if __name__ == '__main__':
    Example().main()
```


```bash
$ python quickstart.py
usage: quickstart.py [-h] [-V] {sub-command1,completion} ...

easycli example

optional arguments:
  -h, --help            show this help message and exit
  -V, --version         Show version

Sub commands:
  {sub-command1,completion}
    sub-command1
    completion          Bash auto completion using argcomplete python package.
```


### Bash Auto Completion

```bash
$ python quickstart.py completion
usage: quickstart.py completion [-h] {install,uninstall} ...

optional arguments:
  -h, --help           show this help message and exit

Sub commands:
  {install,uninstall}
    install            Enables the autocompletion.
    uninstall          Disables the autocompletion.
```

### ProgressBar

```python
from easycli import ProgressBar 


steps = 100
with ProgressBar(steps) as pb:
    for i in range(steps):
        # Do what you want here
        pb.increment()
```

See [examples/progressbar.py](examples/progressbar.py)

![](examples/media/example_progressbar.gif)
