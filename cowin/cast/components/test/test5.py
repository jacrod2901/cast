

class Test:

    def __init__(self):
        print('test Class Contructor Initiated')

    def square(self, a):
        return a * a


def driver(contextvar):
    test = Test()
    print('config_reveived', contextvar)
    print('Number Square', test.square(contextvar['A']))
