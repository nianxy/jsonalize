from jsonalize.jsonalize import *


# Define a class
class MyData(JSONObject):
    def __init__(self):
        JSONObject.__init__(self)
        self.id = JSONString()
        self.name = JSONString()
        self.age = JSONInt()
        self.weight = JSONFloat()


# Create an object of MyData
my = MyData()
my.id = "20190101"
my.name = "Stanley"
my.age = 28
my.weight = 60

# jsonalize the object
json_str = my.to_json()
print(json_str)

# restore the object from json
my2 = JSONObject.from_json(MyData, json_str)
print(my2.to_json())