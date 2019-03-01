from easycli import Root, SubCommand, Argument

from bddcli import stdout, status, stderr, Application, Command, when


class Bar(SubCommand):
    __help__ = 'Bar help'
    __command__ = 'bar'
    __arguments__ = [
        Argument('-b', '--baz', action='store_true')
    ]

    def __call__(self, args):
        print('Bar done:', args.baz)


class Foo(Root):
    __help__ = 'Foo Help'
    __command__ = 'foo'
    __completion__ = True
    __arguments__ = [Bar]


def main():
    Foo().main()


EXPECTED_HELP = '''usage: foo [-h] {bar,completion} ...

Foo Help

optional arguments:
  -h, --help        show this help message and exit

Sub commands:
  {bar,completion}
    bar             Bar help
    completion      Bash auto completion using argcomplete python package.
'''


def test_subcommand():
    app = Application('foo', 'easycli.tests.test_subcommand:main')
    with Command(app, 'Subcommand application without any argument'):
        assert stdout == EXPECTED_HELP
        assert status == 0

        when('help', arguments=['-h'])
        assert status == 0
        assert stderr == ''
        assert stdout == EXPECTED_HELP

        when('Run Subcommand without any argument', arguments=['bar'])
        assert stderr == ''
        assert stdout == 'Bar done: False\n'
        assert status == 0

        when('Run Subcommand with argument', arguments=['bar', '--baz'])
        assert stderr == ''
        assert stdout == 'Bar done: True\n'
        assert status == 0
