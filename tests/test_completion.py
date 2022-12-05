import os
import tempfile
from os import path

from easycli import Root

from bddcli import status, stderr, Application, Given, when, given


class Foo(Root):
    __help__ = 'Foo Help'
    __command__ = 'foo'
    __completion__ = True


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


# def test_bash_autocompletion_user():
#     app = Application('foo', 'tests.test_completion:Foo.quickstart')
#     with tempfile.TemporaryDirectory() as homedir:
#         os.mkdir(path.join(homedir, 'bin'))
#         with Given(app, ['completion'], environ={'HOME': homedir}):
#             assert status == 0
#
#             when(given + ['install', '-s'])
#             assert stderr == 'The -s/--system-wide flag can not be used ' \
#                 'within virtualenv\n'
#             assert status == 1


if __name__ == '__main__':
    Foo().main(['-h'])
