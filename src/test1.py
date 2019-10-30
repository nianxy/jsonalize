from jsonalize.jsonalize import *


class XXObj(JSONObject):
    def __init__(self):
        JSONObject.__init__(self)
        self.iv = JSONInt()
        self.sv = JSONString()


class MyClass(JSONObject):
    def __init__(self):
        JSONObject.__init__(self)
        self.bv = JSONBool(True)
        self.iv = JSONInt(10)
        self.lv = JSONLong(10)
        self.sv = JSONString('hello')
        self.lsv = JSONList()
        self.setv = JSONSet()
        self.ov = XXObj()
        self.ov.iv = 10
        self.ov.sv = 'where are you'


my = MyClass()
my.lsv.append(1)
my.lsv.append(2)
my.setv.add('a')
my.setv.add('b')
my.iv = None
#my.iv = 14

js = my.to_json()
print(js)

obj = JSONObject.from_json(MyClass, js)
print(obj.to_json())

print obj.bv
print obj.bv is True
print obj.bv == True
print obj.bv.true(), obj.bv.true() is True
