import test
import pytest
from jsonalize.jsonalize import *


def _remove_space_from_str(s):
    return s.replace(" ", "")


class TestDataTypeJSON:
    def test_int(self):
        class A(JSONObject):
            def __init__(self):
                JSONObject.__init__(self)
                self.v = JSONInt()

        obj = A()
        obj.v = 10

        json_str = obj.to_json()
        test_json_str = '{"v":10}'

        assert _remove_space_from_str(json_str) == test_json_str

    if test.IS_PYTHON_2:
        def test_long(self):
            class A(JSONObject):
                def __init__(self):
                    JSONObject.__init__(self)
                    self.v = JSONLong()

            obj = A()
            obj.v = 10

            json_str = obj.to_json()
            test_json_str = '{"v":10}'

            assert _remove_space_from_str(json_str) == test_json_str

    def test_float(self):
        class A(JSONObject):
            def __init__(self):
                JSONObject.__init__(self)
                self.v = JSONFloat()

        obj = A()
        obj.v = 10.0

        json_str = obj.to_json()
        test_json_str = '{"v":10.0}'

        assert _remove_space_from_str(json_str) == test_json_str

    def test_complex(self):
        class A(JSONObject):
            def __init__(self):
                JSONObject.__init__(self)
                self.v = JSONComplex()

        obj = A()
        obj.v = 1+2j

        json_str = obj.to_json()
        test_json_str = ['{"v":{"r":1.0,"i":2.0}}','{"v":{"i":2.0,"r":1.0}}']

        assert _remove_space_from_str(json_str) in test_json_str

    def test_bool(self):
        class A(JSONObject):
            def __init__(self):
                JSONObject.__init__(self)
                self.v = JSONBool()

        obj = A()
        obj.v = True

        json_str = obj.to_json()
        test_json_str = '{"v":true}'

        assert _remove_space_from_str(json_str) == test_json_str

    def test_string(self):
        class A(JSONObject):
            def __init__(self):
                JSONObject.__init__(self)
                self.v = JSONString()

        obj = A()
        obj.v = "jsonalize"

        json_str = obj.to_json()
        test_json_str = '{"v":"jsonalize"}'

        assert _remove_space_from_str(json_str) == test_json_str

    def test_list(self):
        class A(JSONObject):
            def __init__(self):
                JSONObject.__init__(self)
                self.v = JSONList()

        obj = A()
        obj.v = [1,2]

        json_str = obj.to_json()
        test_json_str = '{"v":[1,2]}'

        assert _remove_space_from_str(json_str) == test_json_str

    def test_set(self):
        class A(JSONObject):
            def __init__(self):
                JSONObject.__init__(self)
                self.v = JSONSet()

        obj = A()
        obj.v = set([1,2])

        json_str = obj.to_json()
        test_json_str = ['{"v":[1,2]}','{"v":[2,1]}']

        assert _remove_space_from_str(json_str) in test_json_str

    def test_dict(self):
        class A(JSONObject):
            def __init__(self):
                JSONObject.__init__(self)
                self.v = JSONDict()

        obj = A()
        obj.v = {"v1":1}

        json_str = obj.to_json()
        test_json_str = '{"v":{"v1":1}}'

        assert _remove_space_from_str(json_str) in test_json_str

    def test_object(self):
        class A(JSONObject):
            def __init__(self):
                JSONObject.__init__(self)
                self.v = B()

        class B(JSONObject):
            def __init__(self):
                JSONObject.__init__(self)
                self.v = JSONInt()

        obj = A()
        obj.v.v = 1

        json_str = obj.to_json()
        test_json_str = '{"v":{"v":1}}'

        assert _remove_space_from_str(json_str) in test_json_str

