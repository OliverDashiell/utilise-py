import re
import time
import datetime
import json
from typing import Optional
from utilise.built_in_extensions import *

__author__ = 'James Stidard'


def parse_unix_time(value):
    return datetime.datetime.fromtimestamp(int(value))


def to_unix_time(value):
    return time.mktime(value.timetuple()) * 1000


def bool_from_json(value):
    if type(value) is str \
    and (value.lower( ) in ["none", "no", "0", "false"] or re.match('^0\.0*$', value)):
        return False
    return bool(value)


class JsonSerialiser:

    # # TODO: find better way to mark and find surrogate properties
    # @classmethod
    # def surrogate_vars( cls ) -> set:
    #     return set()
    #
    # def to_json_dictionary(self, depth: int=1, surrogate: bool=False, meta: bool=False) -> dict:
    #     depth     -= 1
    #     result     = { '_type': self.__class__.__name__ } if meta else {}
    #     attributes = self.surrogate_vars() if surrogate else public_vars(self)
    #
    #     for attribute in attributes:
    #         value             = getattr(self, attribute)
    #         result[attribute] = JsonSerialiser._json_value(value, depth, surrogate)
    #
    #     return result
    #
    # @staticmethod
    # def _json_value(value, depth: int=1, surrogate: bool=False):
    #     type_ = type(value)
    #
    #     if not value and type_ is not bool:
    #         return None
    #
    #     elif type_ is datetime:
    #         return to_unix_time(value)
    #
    #     elif isinstance(value, JsonSerialiser) and depth == 0:
    #         return value.to_json_dictionary(depth, True)
    #
    #     elif isinstance(value, JsonSerialiser) and depth >= 1:
    #         return value.to_json_dictionary(depth, surrogate)
    #
    #     elif type_ is list or type_ is set:
    #         return [JsonSerialiser._json_value(item, depth, surrogate) for item in value]
    #
    #     elif type_ is str or type_ is int or type_ is float or type_ is bool:
    #         return value

    def update_from_json_dictionary(self, dictionary: dict):
        for attribute in public_vars(self.__class__):
            # If it doesn't exist in update dict then skip
            if attribute not in dictionary: continue

            object_type  = getattr_type(self, attribute)
            update_value = dictionary[attribute]
            update_type  = type(update_value)

            # Update to no value
            if update_value is None:
                setattr(self, attribute, None)
                continue

            if object_type is not update_type:
                if   object_type is str \
                and (update_type is int or update_type is float or update_type is bool):
                    update_value = str(update_value)

                elif object_type is str \
                and  update_type is dict:
                    update_value = json.dumps(update_value)

                elif object_type is int \
                and (update_type is str or update_type is float):
                    update_value = int(update_value)

                elif object_type is float \
                and  update_type is str:
                    update_value = float(update_value)

                elif object_type is bool:
                    update_value = bool_from_json(update_value)

                elif object_type is datetime \
                and (update_type is str or update_type is int):
                    update_value = parse_unix_time(update_value)

                elif object_type is JsonSerialiser \
                and  update_type is dict:
                    child = getattr(self, attribute)
                    child.update_from_json_dictionary(update_value)

                elif (object_type is list or object_type is set) \
                and   update_type is list:
                    children = getattr(self, attribute, [])
                    [child.update_from_json_dictionary(update_value) for child in children if child is JsonSerialiser]

            setattr(self, attribute, update_value)
