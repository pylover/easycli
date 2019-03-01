import os
import tempfile
from os import path

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


def test_bash_autocompletion_systemwide():
    app = Application('foo', 'easycli.tests.test_bashcompletion:main')
    with Command(app, 'Test bash autocompletion'):
        assert stdout == EXPECTED_HELP
        assert status == 0

        when('help', arguments=['-h'])
        assert status == 0
        assert stderr == ''
        assert stdout == EXPECTED_HELP

        when('Install completion', arguments=['completion', 'install'])
        when('Un.nstall completion', arguments=['completion', 'uninstall'])


def test_bash_autocompletion_virtualenv():
    app = Application('foo', 'easycli.tests.test_bashcompletion:main')
    with tempfile.TemporaryDirectory() as venvdir:
        os.mkdir(path.join(venvdir, 'bin'))
        with Command(
            app,
            'Bash autocompletion inside virtual environment',
            environ={'VIRTUAL_ENV': venvdir}
        ):
            assert stdout == EXPECTED_HELP
            assert status == 0

            when('help', arguments=['-h'])
            assert status == 0
            assert stderr == ''
            assert stdout == EXPECTED_HELP

            when('Install completion', arguments=['completion', 'install'])
            when('Uninstall completion', arguments=['completion', 'uninstall'])

