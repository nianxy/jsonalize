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
        self.lsobjv = JSONList()
        self.lsobjv.append(XXObj())
        self.lsobjv.append(XXObj())
        self.mapv = JSONDict()
        self.mapv['a'] = 1
        self.mapv['b'] = 2
        self.mapv['c'] = XXObj()


class MyData(JSONObject):
    def __init__(self):
        JSONObject.__init__(self)
        self.id = JSONString()
        self.name = JSONString()
        self.age = JSONInt()
        self.weight = JSONFloat()


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

computer2 = JSONObject.from_json(Computer, json_str)
print(computer2.to_json())


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

school2 = JSONObject.from_json(School, json_str)
print(type(school2.students[0]), school2.students[0])
