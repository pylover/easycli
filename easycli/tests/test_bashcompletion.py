import os
import tempfile
from os import path

from easycli import Root, SubCommand, Argument

from bddcli import stdout, status, stderr, Application, Command, when, given



class Foo(Root):
    __help__ = 'Foo Help'
    __command__ = 'foo'
    __completion__ = True


def main():
    return Foo().main()


EXPECTED_HELP = '''usage: foo completion [-h] {install,uninstall} ...

optional arguments:
  -h, --help           show this help message and exit

Sub commands:
  {install,uninstall}
    install            Enables the autocompletion.
    uninstall          Disables the autocompletion.
'''


def test_bash_autocompletion_systemwide():
    app = Application('foo', 'easycli.tests.test_bashcompletion:main')
    with Command(app, 'Test bash autocompletion', arguments=['completion']):
        assert stdout == EXPECTED_HELP
        assert status == 0

        when('help', arguments=given + '-h')
        assert status == 0
        assert stderr == ''
        assert stdout == EXPECTED_HELP

        when('Install completion', arguments=given + 'install')
        when('Uninstall completion', arguments=given + 'uninstall')


def test_bash_autocompletion_virtualenv():
    app = Application('foo', 'easycli.tests.test_bashcompletion:main')
    with tempfile.TemporaryDirectory() as venvdir:
        os.mkdir(path.join(venvdir, 'bin'))
        with Command(
            app,
            'Bash autocompletion inside virtual environment',
            environ={'VIRTUAL_ENV': venvdir},
            arguments=['completion']
        ):
            assert stdout == EXPECTED_HELP
            assert status == 0

            when(
                'Install completion',
                arguments=given + ['install', '-s']
            )
            assert stderr == 'The -s/--system-wide flag can not be used ' \
                'within virtualenv\n'
            assert status == 1
#
#            when('Install completion', arguments=['completion', 'install'])
#            when('Uninstall completion', arguments=['completion', 'uninstall'])

