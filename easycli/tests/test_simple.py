from easycli import Root

from bddcli import stdout, status, stderr, Application, Command, when


class Foo(Root):
    __help__ = 'Foo Help'
    __command__ = 'foo'
    __completion__ = True

    def __call__(self, args):
        print('foo done')


def main():
    Foo().main()


EXPECTED_HELP = '''usage: foo [-h]

Foo Help

optional arguments:
  -h, --help  show this help message and exit
'''


EXPECTED_USAGE = '''usage: foo [-h]
foo: error: unrecognized arguments: --invalid
'''


def test_simple():
    app = Application('foo', 'easycli.tests.test_simple:main')
    with Command(app, 'Simple application without any argument'):
        assert stderr == ''
        assert stdout == 'foo done\n'
        assert status == 0

        when('help', arguments=['-h'])
        assert status == 0
        assert stderr == ''
        assert stdout == EXPECTED_HELP

        when('Invalid arguments', arguments=['--invalid'])
        assert status == 2
        assert stderr == EXPECTED_USAGE
        assert stdout == ''
