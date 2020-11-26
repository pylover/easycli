import os
import sys
from os import path

from .argument import Argument
from .command import SubCommand


def print_venv_restart_help():
    venv = path.basename(os.environ['VIRTUAL_ENV'])
    print('\nPlease run this to apply changes auto completion:\n')
    print(f'    deactivate && workon {venv}\n')


class CompletionInstaller(SubCommand):
    __command__ = 'install'
    __help__ = 'Enables the autocompletion.'
    __arguments__ = [
        Argument(
            '-s', '--system-wide',
            action='store_true',
            help=f'Add the PYTHON_ARGCOMPLETE_OK into first 1024 bytes of the'
                 f'{sys.argv[0]}'
        )
    ]

    def __call__(self, args):
        if 'VIRTUAL_ENV' in os.environ:
            if args.system_wide:
                print(
                    'The -s/--system-wide flag can not be used within '
                    'virtualenv',
                    file=sys.stderr
                )
                return 1

            self.install_virtualenv()

        elif args.system_wide:  # pragma: no cover
            self.install_systemwide()

        else:
            self.install_user()

    def install_virtualenv(self):
        sourcefile = path.join(os.environ['VIRTUAL_ENV'], 'bin/postactivate')
        result = self.install_file(sourcefile)
        if not result:
            print_venv_restart_help()

        return result

    def install_user(self):
        sourcefile = path.join(os.environ['HOME'], '.bashrc')
        return self.install_file(sourcefile)

    def install_file(self, filename):
        line = 'eval "$(register-python-argcomplete %s)"\n' % \
            path.basename(sys.argv[0])

        with open(filename) as f:
            content = f.readlines()

        if line in content:
            print(
                'The autocompletion is already activated.\n'
                f'it means the line:\n\n    {line}\nwas found in file '
                f'{path.abspath(filename)}',
                file=sys.stderr
            )
            return 1

        with open(filename, mode='a') as f:
            f.write(line)

        print(
            f'The line:\n\n    {line}\nwas added into '
            f'{path.abspath(filename)}'
        )

    def install_systemwide(self):  # pragma: no cover
        line = '# PYTHON_ARGCOMPLETE_OK'
        filename = sys.argv[0]
        with open(filename) as f:

            content = f.read(1024)
            if line in content:
                print(
                    'The autocompletion is already activated.\n'
                    f'it means the line:\n\n    '
                    f'{line}\nwas found in file {path.abspath(filename)}',
                    file=sys.stderr
                )
                return 1

            content += f.read()

        lines = content.splitlines()
        lines.insert(1, line)
        with open(filename, mode='w') as f:
            for l in lines:
                f.write(f'{l}\n')

        print(f'The line: {line} was added into: {path.abspath(filename)}')


class CompletionUninstaller(SubCommand):
    __command__ = 'uninstall'
    __help__ = 'Disables the autocompletion.'
    __arguments__ = [
        Argument(
            '-s', '--system-wide',
            action='store_true',
            help=f'Remove the PYTHON_ARGCOMPLETE_OK from {sys.argv[0]}'
        )
    ]

    def __call__(self, args):
        if 'VIRTUAL_ENV' in os.environ:
            if args.system_wide:
                print(
                    'The -s/--system-wide flag can not be used within '
                    'virtualenv',
                    file=sys.stderr
                )
                return 1
            self.uninstall_from_virtualenv()

        elif args.system_wide:
            self.uninstall_systemwide()

        else:
            self.uninstall_from_user()

    def uninstall_from_virtualenv(self):
        sourcefile = path.join(os.environ['VIRTUAL_ENV'], 'bin/postactivate')
        result = self.uninstall_from_file(sourcefile)
        if not result:
            print_venv_restart_help()

        return result

    def uninstall_from_user(self):
        sourcefile = path.join(os.environ['HOME'], '.bashrc')
        return self.uninstall_from_file(sourcefile)

    def uninstall_from_file(self, filename):
        line = \
            f'eval "$(register-python-argcomplete ' \
            f'{path.basename(sys.argv[0])})"\n'

        return self.remove_line_from_file(filename, line)

    def uninstall_systemwide(self):
        line = '# PYTHON_ARGCOMPLETE_OK\n'
        filename = sys.argv[0]
        self.remove_line_from_file(filename, line)

    def remove_line_from_file(self, filename, line):
        with open(filename) as f:
            lines = f.readlines()

        found = False
        with open(filename, mode='w') as f:
            for l in lines:
                if line != l:
                    f.write(l)
                else:
                    found = True

        if found:
            print(
                f'The line:\n\n    '
                f'{line}\nwas removed from {path.abspath(filename)}'
            )
        else:
            print(
                f'The autocompletion is already deactivated.\n'
                f'it means the line:\n\n'
                f'    {line}\nwas not found in file {path.abspath(filename)}',
                file=sys.stderr
            )
            return 1


class Completion(SubCommand):
    __command__ = 'completion'
    __help__ = 'Bash auto completion using argcomplete python package.'
    __arguments__ = [
        CompletionInstaller,
        CompletionUninstaller
    ]
