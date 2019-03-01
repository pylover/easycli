import os
import tempfile
from os import path

from easycli import Root, SubCommand, Argument

from bddcli import stdout, status, stderr, Application, Given, when, given



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

# TODO: remove
def test_bash_autocompletion_systemwide():
    app = Application('foo', 'easycli.tests.test_bashcompletion:main')
    with Given(app, ['completion']):
        assert stdout == EXPECTED_HELP
        assert status == 0

        when(given + '-h')
        assert status == 0
        assert stderr == ''
        assert stdout == EXPECTED_HELP

        when(given + 'install')
        when(given + 'uninstall')


def test_bash_autocompletion_virtualenv():
    app = Application('foo', 'easycli.tests.test_bashcompletion:main')
    with tempfile.TemporaryDirectory() as venvdir:
        os.mkdir(path.join(venvdir, 'bin'))
        with Given(app, ['completion'], environ={'VIRTUAL_ENV': venvdir}):
            assert stdout == EXPECTED_HELP
            assert status == 0

            when(given + ['install', '-s'])
            assert stderr == 'The -s/--system-wide flag can not be used ' \
                'within virtualenv\n'
            assert status == 1
#
#            when('Install completion', ['completion', 'install'])
#            when('Uninstall completion', ['completion', 'uninstall'])


def test_bash_autocompletion_user():
    app = Application('foo', 'easycli.tests.test_bashcompletion:main')
    with tempfile.TemporaryDirectory() as homedir:
        os.mkdir(path.join(homedir, 'bin'))
        with Given(app, ['completion'], environ={'HOME': homedir}):
            assert stdout == EXPECTED_HELP
            assert status == 0

            when(given + ['install', '-s'])
            assert stderr == 'The -s/--system-wide flag can not be used ' \
                'within virtualenv\n'
            assert status == 1

