from jsonalize.jsonalize import *


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
