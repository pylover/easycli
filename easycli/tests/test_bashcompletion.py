from easycli import Root, SubCommand, Argument

from bddcli import stdout, status, stderr, Application, Command, when



class Foo(Root):
    __help__ = 'Foo Help'
    __command__ = 'foo'
    __completion__ = True


def main():
    Foo().main()


EXPECTED_HELP = '''usage: foo [-h] {completion} ...

Foo Help

optional arguments:
  -h, --help    show this help message and exit

Sub commands:
  {completion}
    completion  Bash auto completion using argcomplete python package.
'''


def test_subcommand():
    app = Application('foo', 'easycli.tests.test_bashcompletion:main')
    with Command(app, 'Subcommand application without any argument'):
        assert stdout == EXPECTED_HELP
        assert status == 0

        when('help', arguments=['-h'])
        assert status == 0
        assert stderr == ''
        assert stdout == EXPECTED_HELP

        when('Install completion', arguments=['completion', 'install'])
        when('Install completion', arguments=['completion', 'uninstall'])
