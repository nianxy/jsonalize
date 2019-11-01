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


class JSONObjectNotInitError(Exception):
    def __str__(self):
        return 'JSONObject.__init__() should be invoked!'


class _TypeValueNone:
    def __init__(self, tp):
        self.tp = tp


class _JSONTypeBase:
    def __init__(self, *args, **kwargs):
        pass

    def _to_map_value(self):
        return self

    def _from_json(self, value_dict):
        return value_dict


class JSONInt(int, _JSONTypeBase):
    def __new__(cls, *args, **kwargs):
        return int.__new__(JSONInt, *args, **kwargs)

    def __init__(self, *args, **kwargs):
        int.__init__(self)
        _JSONTypeBase.__init__(self)


if _IS_PYTHON_2:
    class JSONLong(long, _JSONTypeBase):
        def __new__(cls, *args, **kwargs):
            return long.__new__(JSONLong, *args, **kwargs)

        def __init__(self, *args, **kwargs):
            long.__init__(self)
            _JSONTypeBase.__init__(self)


class JSONFloat(float, _JSONTypeBase):
    def __new__(cls, *args, **kwargs):
        return float.__new__(JSONFloat, *args, **kwargs)

    def __init__(self, *args, **kwargs):
        float.__init__(self)
        _JSONTypeBase.__init__(self)


class JSONComplex(complex, _JSONTypeBase):
    def __new__(cls, *args, **kwargs):
        return complex.__new__(JSONComplex, *args, **kwargs)

    def __init__(self, *args, **kwargs):
        complex.__init__(self)
        _JSONTypeBase.__init__(self)

    def _to_map_value(self):
        return {'r': self.real, 'i': self.imag}

    def _from_json(self, value_dict):
        return complex(value_dict['r'], value_dict['i'])


class JSONBool(int, _JSONTypeBase):
    """
    注意，不要将JSONBool实例通过 is 关键字和 True 比较，这样的结果永远是 False。例：
    jbool = JSONBool(True)
    print(jbool is True) # False
    print(jbool == True) # True
    print(jbool.true()) # True
    print(jbool.true() is True) # True
    """
    def __new__(cls, *args, **kwargs):
        #b = bool.__new__(bool, *args, **kwargs)
        if len(args) == 0:
            b = 0
        else:
            b = 1 if args[0] >= 1 else 0
        return int.__new__(JSONBool, b)

    def __init__(self, *args, **kwargs):
        int.__init__(self)
        _JSONTypeBase.__init__(self)

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


class JSONString(str, _JSONTypeBase):
    def __init__(self, *args, **kwargs):
        str.__init__(self)
        _JSONTypeBase.__init__(self)


class _JSONIterable(_JSONTypeBase):
    def _to_map_value(self):
        return _JSONIterable._sub_iter_to_map_value(self)

    @staticmethod
    def _sub_iter_to_map_value(sub_iter):
        new_list = []
        for item in sub_iter:
            if isinstance(item, _JSONTypeBase):
                new_list.append(item._to_map_value())
            else:
                new_list.append(item)
        return new_list


class JSONList(list, _JSONIterable):
    def __init__(self, *args, **kwargs):
        list.__init__(self, *args, **kwargs)
        _JSONTypeBase.__init__(self)


class JSONSet(set, _JSONIterable):
    def __init__(self, *args, **kwargs):
        set.__init__(self, *args, **kwargs)
        _JSONTypeBase.__init__(self, *args, **kwargs)

    def _to_map_value(self):
        return list(_JSONIterable._to_map_value(self))


class JSONDict(dict, _JSONTypeBase):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        _JSONTypeBase.__init__(self, *args, **kwargs)

    def _to_map_value(self):
        return JSONDict._sub_dict_to_map_value(self)

    @staticmethod
    def _sub_dict_to_map_value(sub_dict):
        new_dict = {}
        for k, v in _iter_dict(sub_dict):
            if isinstance(v, _JSONTypeBase):
                new_dict[k] = v._to_map_value()
            else:
                new_dict[k] = v
        return new_dict


class _InnerDict(dict):
    pass


class JSONObject(_JSONTypeBase, object):
    __type_none_object = {}

    @staticmethod
    def NoneValue(class_type):
        ct = JSONObject.__type_none_object.get(class_type)
        if ct is None:
            ct = _TypeValueNone(class_type)
            JSONObject.__type_none_object[class_type] = ct
        return ct

    def __init__(self):
        _JSONTypeBase.__init__(self)
        object.__init__(self)
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
            object.__setattr__(self, key, value)
            return
        try:
            field_type = self._get_filed_type(key)
        except AttributeError:
            raise JSONObjectNotInitError()
        is_json_type = isinstance(value, _JSONTypeBase)
        if field_type is None:
            # 被赋值为None，保存字段类型
            if isinstance(value, _TypeValueNone):
                self._save_filed_type(key, value.tp)
                object.__setattr__(self, key, None)
                return
            # 如果不是JSON**类型，则使用父类的赋值方法
            if not is_json_type:
                object.__setattr__(self, key, value)
                return
            # 保存JSON**字段的类型
            field_type = type(value)
            self._save_filed_type(key, field_type)
        if value is None:
            self.__dict__[key] = None
        else:
            if issubclass(field_type, JSONObject):
                self.__dict__[key] = value
            else:
                self.__dict__[key] = field_type(value)

    def _save_filed_type(self, field, tp):
        self.__field_type[field] = tp

    def _get_filed_type(self, field):
        return self.__field_type.get(field)

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


JSONNoneInt = JSONObject.NoneValue(JSONInt)
JSONNoneFloat = JSONObject.NoneValue(JSONFloat)
JSONNoneComplex = JSONObject.NoneValue(JSONComplex)
JSONNoneBool = JSONObject.NoneValue(JSONBool)
JSONNoneString = JSONObject.NoneValue(JSONString)
JSONNoneList = JSONObject.NoneValue(JSONList)
JSONNoneSet = JSONObject.NoneValue(JSONSet)
JSONNoneDict = JSONObject.NoneValue(JSONDict)
if _IS_PYTHON_2:
    JSONNoneLong = JSONObject.NoneValue(JSONLong)

