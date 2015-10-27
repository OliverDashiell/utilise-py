from unittest import TestCase
from src.utilise.json_serialiser import JsonSerialiser

__author__ = 'James Stidard'


class Thing(JsonSerialiser):
    str_attr   = "string"
    int_attr   = 23
    bool_attr  = True
    float_attr = 23.54
    set_attr   = set()
    list_attr  = []
    dict_attr  = {}
    child_attr = None


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

    def test_child_thing_to_json(self):
        pass
