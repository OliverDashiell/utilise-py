from unittest import TestCase
from src.utilise.json_serialiser import JsonSerialiser
from src.utilise.built_in_extensions import *
import typing

__author__ = 'James Stidard'

JSS = typing.TypeVar( 'JSS', bound=JsonSerialiser )


class Thing(JsonSerialiser):
    str_attr   = "string"
    int_attr   = 23
    bool_attr  = True
    float_attr = 23.54
    set_attr   = set()
    list_attr  = []
    dict_attr  = {}
    child_attr = None

    def __init__(self,
                   str_attr: str='string',   int_attr: int=0,    bool_attr: bool=True,
                 float_attr: float=0,        set_attr: set=None, list_attr: list=None,
                  dict_attr: dict=None,    child_attr: JSS=None):
        self.str_attr   = str_attr
        self.int_attr   = int_attr
        self.bool_attr  = bool_attr
        self.float_attr = float_attr
        self.set_attr   = set_attr
        self.list_attr  = list_attr
        self.dict_attr  = dict_attr
        self.child_attr = child_attr

    @classmethod
    def surrogate_vars( cls ):
        return { 'str_attr', 'int_attr' }

    def test_method(self, a: int, b: int):
        return a + b + self.int_attr


class TestObjectSerialiser(TestCase):

    def setUp(self):
        self.thing = Thing()

    def test_str_to_json(self):
        self.thing.str_attr = "A String"
        json_thing          = self.thing.to_json_dictionary()
        self.assertTrue(json_thing['str_attr'] == "A String")

    def test_positive_int_to_json(self):
        self.thing.int_attr = 5
        json_thing          = self.thing.to_json_dictionary()
        self.assertTrue(json_thing['int_attr'] == 5)

    def test_negative_int_to_json(self):
        self.thing.int_attr = -502
        json_thing          = self.thing.to_json_dictionary()
        self.assertTrue(json_thing['int_attr'] == -502)

    def test_false_bool_to_json(self):
        self.thing.bool_attr = False
        json_thing           = self.thing.to_json_dictionary()
        self.assertTrue(json_thing['bool_attr'] == False)

    def test_true_bool_to_json(self):
        self.thing.bool_attr = True
        json_thing           = self.thing.to_json_dictionary()
        self.assertTrue(json_thing['bool_attr'] == True)

    def test_positive_float_to_json(self):
        self.thing.float_attr = 40.0
        json_thing            = self.thing.to_json_dictionary()
        self.assertTrue(json_thing['float_attr'] == 40.0)

    def test_negative_float_to_json(self):
        self.thing.float_attr = -40.4
        json_thing            = self.thing.to_json_dictionary()
        self.assertTrue(json_thing['float_attr'] == -40.4)

    def test_child_str_to_json(self):
        self.thing.child_attr = Thing(str_attr='hello')
        json_thing = self.thing.to_json_dictionary(depth=2)
        self.assertTrue(json_thing['child_attr']['str_attr'] == 'hello')

    def test_child_int_to_json(self):
        self.thing.child_attr = Thing(int_attr=3)
        json_thing = self.thing.to_json_dictionary(depth=2)
        self.assertTrue(json_thing['child_attr']['int_attr'] == 3)

    def test_child_surrogate_to_json(self):
        self.thing.child_attr    = Thing()
        surrogate_attributes     = Thing.surrogate_vars()
        non_surrogate_attributes = [attr for attr in public_vars(self.thing) if attr not in surrogate_attributes]

        json_thing = self.thing.to_json_dictionary()
        json_child = json_thing['child_attr']

        for surrogate_attr in surrogate_attributes:
            self.assertTrue(surrogate_attr in json_child)
        for non_surrogate_attr in non_surrogate_attributes:
            self.assertTrue(non_surrogate_attr not in json_child)

    def test_child_full_to_json(self):
        self.thing.child_attr    = Thing()

        json_thing = self.thing.to_json_dictionary(depth=2)
        json_child = json_thing['child_attr']

        for attr in json_child:
            self.assertTrue(attr in public_vars(self.thing))


