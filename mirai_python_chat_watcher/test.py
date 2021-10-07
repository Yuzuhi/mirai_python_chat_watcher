
def test(*args):
    if args:
        print(*args)
        for i in args:
            print(i)

def test1(**kwargs):
    for k,v, in kwargs.items():
        print(k)

class Test:

    def kk(self,ss):
        pass

test(1,2,3,4,5,a="ss")

print(callable(Test.kk))