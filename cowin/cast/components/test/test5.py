

class Test:

    def __init__(self):
        print('test Class Contructor Initiated')

    def square(self, a):
        return a * a


def driver(contextvar):
    test = Test()
    print('config_reveived', contextvar['componentconfig'])
    print('Number Square', test.square(contextvar['componentconfig']['A']))
