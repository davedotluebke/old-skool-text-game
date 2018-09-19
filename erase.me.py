print("Hello world")
class Foo():
    d1 = {"foo":1, "bar":2, "baz":3}

    def __init__(self):
        self.d1["x"] = 10

    def sillyfunction(self):
        print("this is silly")

class Bar(Foo): 
    d1 = dict(Foo.d1)
    
    def __init__(self):
        self.d1["y"] = 100
        self.d1 = dict(Bar.d1)
    def dummyfunction(self):
        print("I'm a dummy!")
    


f = Foo()
print("f.d1 = %s" % f.d1)
print("creating b...")
b = Bar()
b2 = Bar()

print("f.d1 = %s" % f.d1)
print("b.d1 = %s" % b.d1)
print("b2.d1 = %s" % b2.d1)

b2.d1["y"] = 3.14
print("f.d1 = %s" % f.d1)
print("b.d1 = %s" % b.d1)
print("b2.d1 = %s" % b2.d1)

