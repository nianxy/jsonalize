from jsonalize.jsonalize import *


class MyData(JSONObject):
    def __init__(self):
        JSONObject.__init__(self)
        self.id = JSONNoneInt
        self.name = JSONNoneString
        self.attr = JSONObject.NoneValue(Attr)


class Attr(JSONObject):
    def __init__(self):
        JSONObject.__init__(self)
        self.value = JSONString()
        print("Attr object created")


my = MyData()
print(my.id is None, my.name is None, my.attr is None)

my.id = 10
my.name = "Stanley"
my.attr = Attr()
my.attr.value = "attr"
print(my.to_json())
