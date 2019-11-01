import test
import math
from jsonalize.jsonalize import *


def compare_float(f1, f2, precision=0.0000001):
    return math.fabs(f1-f2)<precision


def compare_complex(c1, c2, precision=0.0000001):
    return compare_float(c1.real, c2.real, precision) and\
           compare_float(c1.imag, c2.imag, precision)


class TestDataType:
    def test_int(self):
        # Test data types
        assert type(JSONInt()) == JSONInt
        assert type(JSONInt(1)) == JSONInt

        assert JSONInt() == 0
        assert JSONInt(1) == 1
        assert JSONInt(10) == JSONInt(10)
        assert JSONInt(10) != 11
        assert JSONInt(100) + 100 == 200
        assert JSONInt(1000) + JSONInt(1000) == JSONInt(2000)
        assert JSONInt(100) * 10 == 1000
        assert JSONInt(100) / 5 == 20
        assert JSONInt(100) - 5 == 95

    if test.IS_PYTHON_2:
        def test_long(self):
            # Test data types
            assert type(JSONLong()) == JSONLong
            assert type(JSONLong(1)) == JSONLong

            assert JSONLong() == 0
            assert JSONLong(1) == 1
            assert JSONLong(10) == JSONLong(10)
            assert JSONLong(10) != 11
            assert JSONLong(100) + 100 == 200
            assert JSONLong(1000) + JSONLong(1000) == JSONLong(2000)
            assert JSONLong(100) * 10 == 1000
            assert JSONLong(100) / 5 == 20
            assert JSONLong(100) - 5 == 95

    def test_float(self):
        # Test data types
        assert type(JSONFloat()) == JSONFloat
        assert type(JSONFloat(1.0)) == JSONFloat

        assert compare_float(JSONFloat(), 0)
        assert compare_float(JSONFloat(1.0), 1.0)
        assert compare_float(JSONFloat(1.0)+10, 11.0)
        assert compare_float(JSONFloat(100.0)-10, 90.0)
        assert compare_float(JSONFloat(1.0)*10, 10.0)
        assert compare_float(JSONFloat(1.0)/10, 0.1)

    def test_complex(self):
        # Test data types
        assert type(JSONComplex()) == JSONComplex
        assert type(JSONComplex(1.0)) == JSONComplex
        assert type(JSONComplex(1.0, 2.0)) == JSONComplex

        assert compare_complex(JSONComplex(), 0+0j)
        assert compare_complex(JSONComplex(1.0), 1+0j)
        assert compare_complex(JSONComplex(1.0, 2.0), 1+2j)
        assert compare_complex(JSONComplex(1.0, 2.0), 1+2j)
        assert compare_complex(JSONComplex(1.0, -2.0), 1-2j)
        assert compare_complex(JSONComplex(1.0, -2.0) + (2+3j), 3+1j)

    def test_string(self):
        # Test data types
        assert type(JSONString()) == JSONString
        assert type(JSONString("abc")) == JSONString

        assert JSONString() == ""
        assert JSONString("abc") == "abc"
        assert JSONString("abc") + "def" == "abcdef"

    def test_bool(self):
        # Test data types
        assert type(JSONBool()) == JSONBool
        assert type(JSONBool(True)) == JSONBool

        assert JSONBool() == False
        assert JSONBool(True) == True
        assert JSONBool(True) is not True
        assert JSONBool(True).true()
        assert JSONBool(True).true() is True
        assert not JSONBool(False).true()
        assert JSONBool(False).false()
        assert JSONBool(False).false() is True
        assert JSONBool(0).false()
        assert JSONBool(1).true()
        assert JSONBool(2).true()
        assert JSONBool(False) == 0
        assert JSONBool(True) == 1
        assert JSONBool(2) == 1

    def test_list(self):
        # Test data types
        assert type(JSONList()) == JSONList
        assert type(JSONList([1,2])) == JSONList
        a = JSONList([1,2])
        a.append(3)
        assert type(a) == JSONList

        assert len(JSONList()) == 0
        assert len(JSONList([1, 2, 3])) == 3
        a = JSONList([1, 2, 3])
        a.append(4)
        assert len(a) == 4

    def test_set(self):
        # Test data types
        assert type(JSONSet()) == JSONSet
        assert type(JSONSet([1,2])) == JSONSet
        a = JSONSet([1,2])
        a.add(3)
        assert type(a) == JSONSet

        assert len(JSONSet()) == 0
        assert len(JSONSet([1,2,3])) == 3
        a = JSONSet([1, 2, 3])
        a.add(3)
        assert len(a) == 3
        a.add(4)
        assert len(a) == 4

    def test_dict(self):
        # Test data types
        assert type(JSONDict()) == JSONDict
        d = JSONDict()
        d['a'] = 1
        assert type(d) == JSONDict

        assert len(JSONDict()) == 0
        d = JSONDict()
        d['a'] = 1
        d['b'] = 2
        assert len(d) == 2
        del(d['a'])
        assert len(d) == 1

