import time

from easycli import Root, ProgressBar


DEFAULT_TCP_PORT = 8585
DEFAULT_HOST = 'WPP.local'


class Main(Root):
    __help__ = 'easycli example'
    __completion__ = True
    __arguments__ = [
    ]

    def __call__(self, args):
        length = 100
        with ProgressBar(length) as pb:
            for i in range(length):
                pb.increment()
                time.sleep(0.1)
        return


if __name__ == '__main__':
    Main().main()
