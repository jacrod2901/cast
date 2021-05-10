# 
class Test:
    def __init__(self, a):
        self.__a = a
        self.__b = self.__mainfunc()
        print('class is called')


    def __mainfunc(self):
        self__b =0
        print('mainfunc is initialised')
        return 1

    def testfunc2(self):
        return self.__b

    def testfunc3(self):
        self.__b = 0
        return self.__b + 3

obj = Test(2)
res = obj.testfunc2()
print(res)

res = obj.testfunc3()
print(res)





