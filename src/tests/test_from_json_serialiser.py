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

    # To str
    def test_str_to_str(self):
        update_dict = { "str_attr": "some string" }
        self.thing.update_from_json_dictionary(update_dict)
        self.assertTrue(self.thing.str_attr == "some string")

    def test_int_to_str(self):
        update_dict = { "str_attr": 9000 }
        self.thing.update_from_json_dictionary(update_dict)
        self.assertTrue(self.thing.str_attr == "9000")

    def test_float_to_str(self):
        update_dict = { "str_attr": 9000.94 }
        self.thing.update_from_json_dictionary(update_dict)
        self.assertTrue(self.thing.str_attr == "9000.94")

    def test_bool_to_str_true(self):
        update_dict = { "str_attr": True }
        self.thing.update_from_json_dictionary(update_dict)
        self.assertTrue(self.thing.str_attr == "True")

    def test_bool_to_str_false(self):
        update_dict = { "str_attr": False }
        self.thing.update_from_json_dictionary(update_dict)
        self.assertTrue(self.thing.str_attr == "False")

    # To int
    def test_str_to_int(self):
        update_dict = { "int_attr": "45" }
        self.thing.update_from_json_dictionary(update_dict)
        self.assertTrue(self.thing.int_attr == 45)

    def test_int_to_int(self):
        update_dict = { "int_attr": 45 }
        self.thing.update_from_json_dictionary(update_dict)
        self.assertTrue(self.thing.int_attr == 45)

    def test_float_to_int(self):
        update_dict = { "int_attr": 45.76 }
        self.thing.update_from_json_dictionary(update_dict)
        self.assertTrue(self.thing.int_attr == int(45.76))

    def test_bool_to_int_true(self):
        update_dict = { "int_attr": True }
        self.thing.update_from_json_dictionary(update_dict)
        self.assertTrue(self.thing.int_attr == 1)

    def test_bool_to_int_false(self):
        update_dict = { "int_attr": False }
        self.thing.update_from_json_dictionary(update_dict)
        self.assertTrue(self.thing.int_attr == 0)

    # To float
    def test_str_to_float(self):
        update_dict = { "float_attr": "45.453" }
        self.thing.update_from_json_dictionary(update_dict)
        self.assertTrue(self.thing.float_attr == 45.453)

    def test_int_to_float(self):
        update_dict = { "float_attr": 543 }
        self.thing.update_from_json_dictionary(update_dict)
        self.assertTrue(self.thing.float_attr == 543.0)

    def test_float_to_float(self):
        update_dict = { "float_attr": 34.565 }
        self.thing.update_from_json_dictionary(update_dict)
        self.assertTrue(self.thing.float_attr == 34.565)

    def test_bool_to_float_true(self):
        update_dict = { "float_attr": True }
        self.thing.update_from_json_dictionary(update_dict)
        self.assertTrue(self.thing.float_attr == 1.0)

    def test_bool_to_float_false(self):
        update_dict = { "float_attr": False }
        self.thing.update_from_json_dictionary(update_dict)
        self.assertTrue(self.thing.float_attr == 0.0)

    # To bool
    def test_str_to_bool_false(self):
        self.thing.bool_attr = True
        for value in ["False", "0", "0.0", "0.00000000", "NONE", "none", "NO", "no"]:
            update_dict = { "bool_attr": value }
            self.thing.update_from_json_dictionary(update_dict)
            self.assertFalse(self.thing.bool_attr)

    def test_str_to_bool_true(self):
        self.thing.bool_attr = False
        for value in ["true", "TRUE", "0.1", "1.0", "1", "YES", "yes"]:
            update_dict = { "bool_attr": value }
            self.thing.update_from_json_dictionary(update_dict)
            self.assertTrue(self.thing.bool_attr)

    def test_int_to_bool(self):
        self.thing.bool_attr = True
        for value in [-2, -1, 0, 1, 2]:
            update_dict = { "bool_attr": value }
            self.thing.update_from_json_dictionary(update_dict)
            self.assertTrue(self.thing.bool_attr == bool(value))

    def test_float_to_bool(self):
        self.thing.bool_attr = True
        for value in [-2.2, -1.3, 0.0, 0.1, 1.3, 2.3]:
            update_dict = { "bool_attr": value }
            self.thing.update_from_json_dictionary(update_dict)
            self.assertTrue(self.thing.bool_attr == bool(value))

    def test_bool_to_bool_true(self):
        self.thing.bool_attr = False
        for value in [True, False]:
            update_dict = { "bool_attr": value }
            self.thing.update_from_json_dictionary(update_dict)
            self.assertTrue(self.thing.bool_attr == bool(value))

    # TODO: to datetime

    # TODO: to list

    # TODO: to set

    # TODO: to dict
