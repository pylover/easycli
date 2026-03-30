import os
import sys
from os import path

from .argument import Argument
from .command import SubCommand


class CompletionBase(SubCommand):
    def _print_venvrestart_guide(self, filename):
        print(f'Please source {filename} to apply changes')
        print('NOTE: if you\'re inside a virtual env, please deactivate first')

    def _find_rcfile(self, args):
        # user specified
        if args.rcfile:
            return args.rcfile

        # virtual env
        if 'VIRTUAL_ENV' in os.environ:
            rcfile = path.join(os.environ['VIRTUAL_ENV'], 'bin/postactivate')
            if not path.exists(rcfile):
                rcfile = path.join(os.environ['VIRTUAL_ENV'], 'bin/activate')

            return rcfile

        return path.join(os.environ['HOME'], '.bashrc')


class CompletionInstaller(CompletionBase):
    __command__ = 'install'
    __aliases__ = ['i']
    __help__ = 'Enables the autocompletion.'
    __arguments__ = [
        Argument(
            '-s', '--system-wide',
            action='store_true',
            help=f'Add the PYTHON_ARGCOMPLETE_OK into first 1024 bytes of the'
                 f'{sys.argv[0]}'
        ),
        Argument(
            '--rcfile',
            metavar='FILENAME',
            help='The rc/activation file to register completion function'
        )
    ]

    def _systemwide_install(self, filename, line):  # pragma: no cover
        filename = sys.argv[0]
        with open(filename) as f:
            content = f.read(1024)
            assert line not in content
            content += f.read()

        lines = content.splitlines()
        lines.insert(1, line)
        with open(filename, mode='w') as f:
            for l in lines:
                f.write(f'{l}\n')

    def _install(self, filename, line):
        with open(filename) as f:
            content = f.readlines()

        assert line not in content
        with open(filename, mode='a') as f:
            f.write(line)

        print(
            f'The line:\n\n    {line}\nwas added into '
            f'{path.abspath(filename)}'
        )

    def __call__(self, args):
        try:
            if args.system_wide:  # pragma: no cover
                if 'VIRTUAL_ENV' in os.environ:
                    print(
                        'The -s/--system-wide flag can not be used within '
                        'virtualenv',
                        file=sys.stderr
                    )
                    return 1

                line = '# PYTHON_ARGCOMPLETE_OK'
                filename = path.abspath(sys.argv[0])
                self._systemwide_install(filename, line)

            else:
                line = 'eval "$(register-python-argcomplete %s)"\n' % \
                    path.basename(sys.argv[0])
                filename = path.abspath(self._find_rcfile(args))
                self._install(filename, line)

        except AssertionError:
            print(
                'The autocompletion is already activated.\n'
                f'it means the line:\n\n    {line}\nwas found in file '
                f'{filename}',
                file=sys.stderr
            )
            return 1

        print(f'The line: {line} was added into: {filename}')
        self._print_venvrestart_guide(filename)


class CompletionUninstaller(CompletionBase):
    __command__ = 'uninstall'
    __aliases__ = ['u']
    __help__ = 'Disables the autocompletion.'
    __arguments__ = [
        Argument(
            '-s', '--system-wide',
            action='store_true',
            help=f'Remove the PYTHON_ARGCOMPLETE_OK from {sys.argv[0]}'
        ),
        Argument(
            '--rcfile',
            metavar='FILENAME',
            help='The rc/activation file to unregister completion function'
        )
    ]

    def _remove_line_from_file(self, filename, line):
        with open(filename) as f:
            lines = f.readlines()

        found = False
        with open(filename, mode='w') as f:
            for l in lines:
                if line != l:
                    f.write(l)
                else:
                    found = True

        assert found

    def __call__(self, args):
        try:
            if args.system_wide:  # pragma: no cover
                if 'VIRTUAL_ENV' in os.environ:
                    print(
                        'The -s/--system-wide flag can not be used within '
                        'virtualenv',
                        file=sys.stderr
                    )
                    return 1

                line = '# PYTHON_ARGCOMPLETE_OK'
                filename = path.abspath(sys.argv[0])

            else:
                line = 'eval "$(register-python-argcomplete %s)"\n' % \
                    path.basename(sys.argv[0])
                filename = path.abspath(self._find_rcfile(args))

            self._remove_line_from_file(filename, line)

        except AssertionError:
            print(
                f'The autocompletion is already deactivated.\n'
                f'it means the line:\n\n    {line}\nwas not found in '
                f'file {filename}',
                file=sys.stderr
            )
            return 1

        print(f'The line: {line} was removed from: {filename}')
        self._print_venvrestart_guide(filename)


class Completion(SubCommand):
    __command__ = 'completion'
    __help__ = 'Bash auto completion using argcomplete python package.'
    __arguments__ = [
        CompletionInstaller,
        CompletionUninstaller
    ]
