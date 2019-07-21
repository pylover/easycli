#! /usr/bin/env python3

from easycli import Root, SubCommand, Argument


__version__ = '0.1.0'
DEFAULT_TCP_PORT = 8585
DEFAULT_HOST = 'WPP.local'


class SubCommand1(SubCommand):
    __command__ = 'sub-command1'
    __aliases__ = ['sc', 'su', 's']
    __arguments__ = [
        Argument(
            '-V', '--version',
            action='store_true',
            help='Show programmer\'s version'
        ),
        Argument(
            '-p', '--port',
            type=int,
            default=DEFAULT_TCP_PORT,
            help=f'TCP port, default: {DEFAULT_TCP_PORT}'
        ),
        Argument(
            '-H', '--host',
            default=DEFAULT_HOST,
            help=f'Hostname, default: {DEFAULT_HOST}'
        )

    ]

    def __call__(self, args):
        print('Sub command 1, args:', args)


class Example(Root):
    __help__ = 'easycli example'
    __completion__ = True
    __arguments__ = [
        Argument('-V', '--version', action='store_true', help='Show version'),
        SubCommand1,
    ]

    def __call__(self, args):
        if args.version:
            print(__version__)
            return

        return super().__call__(args)



if __name__ == '__main__':
    Example().main()

