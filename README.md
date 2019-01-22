# easycli

Command line interface for python application on top of the argparse 
including sub-parsers.

## Quickstart

`quickstart.py`

```python
from easycli import Root, SubCommand, Argument


DEFAULT_TCP_PORT = 8585
DEFAULT_HOST = 'WPP.local'


class SubCommand1(SubCommand):
    __command__ = 'sub-command1'
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


class Main(Root):
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
    Main()

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

