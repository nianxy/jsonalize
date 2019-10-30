# Introduction

This library supports two-way data binding between JSON and Python class.

# Turorial

Here is a simple example to use jsonalize:

```python
from jsonalize import *


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

```

This example should output the following message:
```
{"age": 28, "id": "20190101", "weight": 60.0, "name": "Stanley"}
{"age": 28, "id": "20190101", "weight": 60.0, "name": "Stanley"}
```

### Key points from this tutorial
- A serializable class should inherit the `JSONObject` class
- Don't forget to invoke the `__init__` method in your class
- The serializable class attributes should be set as `JSON**` types


# List of supported JSON types

- JSONInt
- JSONLong
- JSONFloat
- JSONComplex
- JSONBool
- JSONString
- JSONList
- JSONSet
- JSONDict
- JSONObject

Most of the types can be initialized with an initial value, for example:
```python
a_string = JSONString("hello jsonalize")
```

### Remarks for JSONBool

You can't test the value of a JSONBool object with the `is` keyword, because `is` will compare the instance id of two objects, but an object of JSONBool is never an instance of `True` or `False`. 

You can do the test as follows:
```Python
a_bool = JSONBool(True)
print(a_bool is True, a_bool == True)
# False, True
print(a_bool.true(), a_bool.true() is True, a_bool.equals(True))
# True, True, True

```


# A more complex example
You can have an object of JSONObject in another JSONObject class:
```python
class Monitor(JSONObject):
    def __init__(self):
        JSONObject.__init__(self)
        self.size = JSONFloat()
        self.power = JSONFloat()
        self.color = JSONString()
        
        
class Computer(JSONObject):
    def __init__(self):
        JSONObject.__init__(self)
        self.brand = JSONString()
        self.monitor = Monitor()
        
        
computer = Computer()
computer.brand = "Lenovo"
computer.monitor.size = 23.0
computer.monitor.power = 25.0

json_str = computer.to_json()
print(json_str)
#{"brand": "Lenovo", "monitor": {"color": "", "power": 25.0, "size": 23.0}}

computer2 = JSONObject.from_json(Computer, json_str)
print(computer2.to_json())
#{"brand": "Lenovo", "monitor": {"color": "", "power": 25.0, "size": 23.0}}
```

# A list of JSONObject objects?
Look at the following example:
```python
class Student(JSONObject):
    def __init__(self):
        JSONObject.__init__(self)
        self.id = JSONString()
        self.name = JSONString()
        
        
class School(JSONObject):
    def __init__(self):
        JSONObject.__init__(self)
        self.address = JSONString()
        self.students = JSONList()
        
        
stu1 = Student()
stu1.id = "20190202"
stu1.name = "Stanley"

stu2 = Student()
stu2.id = "20190203"
stu2.name = "Cyrus"

school = School()
school.address = "Central Street No.23"
school.students.append(stu1)
school.students.append(stu2)

json_str = school.to_json()
print(json_str)
#{"students": [{"id": "20190202", "name": "Stanley"}, {"id": "20190203", "name": "Cyrus"}], "address": "Central Street No.23"}

school2 = JSONObject.from_json(School, json_str)
print(type(school2.students[0]), school2.students[0])
#(<type 'dict'>, {u'id': u'20190202', u'name': u'Stanley'})

```

As you can see here, the deserializing of the School object is incorrect. Because any type of object could be appended to school.students, so `jsonalize` don't know what to restore when deserializing.

This problem is currently not resolved, maybe I can add a type mapping structure in the future.
