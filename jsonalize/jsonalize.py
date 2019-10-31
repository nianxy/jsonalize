# coding=utf-8
import sys
import json

_IS_PYTHON_2 = sys.version_info < (3,)


def _iter_dict(d):
    if _IS_PYTHON_2:
        return d.iteritems()
    else:
        return d.items()


class InvalidJSONClassError(Exception):
    def __str__(self):
        return 'Invalid JSON object class'


class JSONTypeBase(object):
    def _to_map_value(self):
        return self

    def _from_json(self, value_dict):
        return value_dict


class JSONInt(JSONTypeBase, int):
    def __new__(cls, *args, **kwargs):
        return int.__new__(JSONInt, *args, **kwargs)


if _IS_PYTHON_2:
    class JSONLong(JSONTypeBase, long):
        def __new__(cls, *args, **kwargs):
            return long.__new__(JSONLong, *args, **kwargs)


class JSONFloat(JSONTypeBase, float):
    def __new__(cls, *args, **kwargs):
        return float.__new__(JSONFloat, *args, **kwargs)


class JSONComplex(JSONTypeBase, complex):
    def __new__(cls, *args, **kwargs):
        return complex.__new__(JSONComplex, *args, **kwargs)

    def _to_map_value(self):
        return {'r': self.real, 'i': self.imag}

    def _from_json(self, value_dict):
        return complex(value_dict['r'], value_dict['i'])


class JSONBool(JSONTypeBase, int):
    """
    注意，不要将JSONBool实例通过 is 关键字和 True 比较，这样的结果永远是 False。例：
    jbool = JSONBool(True)
    print(jbool is True) # False
    print(jbool == True) # True
    print(jbool.true()) # True
    print(jbool.true() is True) # True
    """
    def __new__(cls, *args, **kwargs):
        b = bool.__new__(bool, *args, **kwargs)
        return int.__new__(JSONBool, b)

    def __str__(self):
        return ['False', 'True'][self]

    def _to_map_value(self):
        return [False, True][self]

    def true(self):
        return self == 1

    def false(self):
        return self == 0

    def equals(self, other):
        return self == other


class JSONString(JSONTypeBase, str):
    pass


class _JSONIterable(JSONTypeBase):
    def _to_map_value(self):
        return _JSONIterable._sub_iter_to_map_value(self)

    @staticmethod
    def _sub_iter_to_map_value(sub_iter):
        new_list = []
        for item in sub_iter:
            if isinstance(item, JSONTypeBase):
                new_list.append(item._to_map_value())
            else:
                new_list.append(item)
        return new_list


class JSONList(_JSONIterable, list):
    pass


class JSONSet(_JSONIterable, set):
    def _to_map_value(self):
        return list(_JSONIterable._to_map_value(self))


class JSONDict(JSONTypeBase, dict):
    def _to_map_value(self):
        return JSONDict._sub_dict_to_map_value(self)

    @staticmethod
    def _sub_dict_to_map_value(sub_dict):
        new_dict = {}
        for k, v in _iter_dict(sub_dict):
            if isinstance(v, JSONTypeBase):
                new_dict[k] = v._to_map_value()
            else:
                new_dict[k] = v
        return new_dict


class _InnerDict(dict):
    pass


class JSONObject(JSONTypeBase):
    def __init__(self):
        JSONTypeBase.__init__(self)
        self.__field_type = _InnerDict()

    def __setattr__(self, key, value):
        """
        为字段赋值，分为几种情况：
        1. self.__field_type中不存在类型记录，value is not instance of JSONTypeBase
           直接调用父类的__setattr__()
        2. self.__field_type中不存在类型记录，value is instance of JSONTypeBase
           将类型记录在self.__field_type中，并根据以下两条为key赋值
        3. self.__field_type中存在类型记录，value is not None
           创建新的value对象，赋值给key
        4. self.__field_type中存在类型记录，value is None
           将key赋值为None
        :param key: 字段名称
        :param value: 字段值
        :return: 无
        """
        if isinstance(value, _InnerDict):
            JSONTypeBase.__setattr__(self, key, value)
            return
        field_type = self.__field_type.get(key)
        is_json_type = isinstance(value, JSONTypeBase)
        if field_type is None:
            if not is_json_type:
                JSONTypeBase.__setattr__(self, key, value)
                return
            field_type = type(value)
            self.__field_type[key] = field_type
        if value is None:
            self.__dict__[key] = None
        else:
            if issubclass(field_type, JSONObject):
                self.__dict__[key] = value
            else:
                self.__dict__[key] = field_type(value)

    def _to_map_value(self):
        value_dict = {}
        for k, v in _iter_dict(self.__field_type):
            nv = self.__dict__.get(k)
            if nv is None:
                value_dict[k] = None
            else:
                value_dict[k] = nv._to_map_value()
        return value_dict

    def _from_json(self, value_dict):
        for k, v in _iter_dict(self.__field_type):
            json_value = value_dict.get(k)
            if json_value is None:
                self.__setattr__(k, None)
            else:
                rv = self.__dict__.get(k)
                self.__setattr__(k, rv._from_json(json_value))

        return self

    def to_json(self):
        return json.dumps(self._to_map_value())

    @staticmethod
    def from_json(cls, json_str):
        if not issubclass(cls, JSONObject):
            raise InvalidJSONClassError()
        try:
            value_dict = json.loads(json_str)
        except ValueError as e:
            raise e

        return cls()._from_json(value_dict)



