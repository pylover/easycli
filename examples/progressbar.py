from easycli import Root, SubCommand, Argument, ProgressBar


DEFAULT_TCP_PORT = 8585
DEFAULT_HOST = 'WPP.local'


class Main(Root):
    __help__ = 'easycli example'
    __completion__ = True
    __arguments__ = [
    ]

    def __call__(self, args):

        temp = 0
        length = 100

        with ProgressBar(length) as pb:
            for i in range(length):
                temp = temp + 1
                pb.increment()
        return


if __name__ == '__main__':
    Main()

