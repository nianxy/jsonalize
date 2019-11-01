# coding=utf-8
import test
import pytest
from jsonalize.jsonalize import *


class TestJSON:
    def test_all_types(self):
        class A(JSONObject):
            def __init__(self):
                JSONObject.__init__(self)
                self.intv = JSONInt()
                self.floatv = JSONFloat()
                self.complexv = JSONComplex()
                self.boolv = JSONBool()
                self.strv = JSONString()
                self.listv = JSONList()
                self.setv = JSONSet()
                self.dictv = JSONDict()
                self.objv = B()
                self.nonev = JSONObject()
                if test.IS_PYTHON_2:
                    self.longv = JSONLong()

        class B(JSONObject):
            def __init__(self):
                JSONObject.__init__(self)
                self.v = JSONInt()

        def assert_attr_types(obj):
            assert isinstance(obj.intv, int)
            assert isinstance(obj.floatv, float)
            assert isinstance(obj.complexv, complex)
            # JSONBOOL is not an instance of bool, because bool is not inheritable
            assert isinstance(obj.boolv, int)
            assert isinstance(obj.strv, str)
            assert isinstance(obj.listv, list)
            assert isinstance(obj.setv, set)
            assert isinstance(obj.dictv, dict)
            assert isinstance(obj.objv, JSONObject)
            if test.IS_PYTHON_2:
                assert isinstance(obj.longv, long)

        obj = A()

        # test object attr types
        assert_attr_types(obj)

        obj.intv = 100
        obj.floatv = 10.0
        obj.complexv = 1+2j
        obj.boolv = True
        obj.strv = "hello"
        obj.listv = [1,2]
        obj.listv.append(3)
        obj.setv = set([1,2])
        obj.setv.add(2)
        obj.setv.add(3)
        obj.dictv = {'a':1}
        obj.dictv['b'] = 2
        obj.objv.v = 10
        obj.nonev = None
        if test.IS_PYTHON_2:
            obj.longv = long(10)

        # test types again
        assert_attr_types(obj)

        # convert to json string
        json_str = obj.to_json()

        # restore the object from json string
        json_obj = JSONObject.from_json(A, json_str)

        # test the new object attr types
        assert_attr_types(json_obj)

        # test the new object and the old
        assert json_obj.intv == obj.intv
        assert test.compare_float(json_obj.floatv, obj.floatv)
        assert test.compare_complex(json_obj.complexv, obj.complexv)
        assert json_obj.boolv == obj.boolv
        assert json_obj.strv == obj.strv
        assert json_obj.listv == obj.listv
        assert json_obj.setv == obj.setv
        assert json_obj.dictv['a'] == obj.dictv['a']
        assert json_obj.dictv['b'] == obj.dictv['b']
        assert json_obj.objv.v == obj.objv.v
        assert json_obj.nonev is None
        if test.IS_PYTHON_2:
            assert json_obj.longv == obj.longv

    def test_field_mismatch(self):
        class A(JSONObject):
            def __init__(self):
                JSONObject.__init__(self)
                self.v1 = JSONInt()
                self.v2 = JSONString()
                self.v3 = JSONBool()

        json_str = '{"v1":1, "v2":"jsonalize", "v4":10}'
        json_obj = JSONObject.from_json(A, json_str)

        assert json_obj.v1 == 1
        assert json_obj.v2 == "jsonalize"
        assert json_obj.v3 is None

        json_str = '{"v1":"v", "v2":"jsonalize", "v4":10}'
        with pytest.raises(ValueError):
            json_obj = JSONObject.from_json(A, json_str)
