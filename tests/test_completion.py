import os
import tempfile
from os import path

from easycli import Root, Argument

from bddcli import status, stderr, Application, Given, when, given


def _completer(prefix, **kw):
    # not need to test the argcomplete package. just testing easycli argument
    # wrapper
    return NotImplemented


class Foo(Root):
    __help__ = 'Foo Help'
    __command__ = 'foo'
    __completion__ = True
    __arguments__ = [
        Argument('-b', '--baz', completer=_completer)
    ]


def test_bash_autocompletion_completer():
    f = Foo()
    assert f.__arguments__[0].completer is _completer


def test_bash_autocompletion_virtualenv():
    app = Application('foo', 'tests.test_completion:Foo.quickstart')
    with tempfile.TemporaryDirectory() as venvdir:
        os.mkdir(path.join(venvdir, 'bin'))
        with Given(app, ['completion'], environ={'VIRTUAL_ENV': venvdir}):
            assert stderr == ''
            assert status == 0

            when(given + ['install', '-s'])
            assert stderr == 'The -s/--system-wide flag can not be used ' \
                'within virtualenv\n'
            assert status == 1
            when(['completion', 'install'])

            when(given + ['uninstall', '-s'])
            assert stderr == 'The -s/--system-wide flag can not be used ' \
                'within virtualenv\n'
            assert status == 1
            when(['completion', 'uninstall'])


if __name__ == '__main__':
    Foo().main(['-h'])
