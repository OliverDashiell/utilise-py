__author__ = 'James Stidard'

import re
from datetime import datetime
from src.utilise.built_in_extensions import *


def bool_from_json(x):
    if type(x) is str \
    and (x.lower() in ["none", "no", "0", "false"] or re.match('^0\.0*$', x)):
        return False
    return bool(x)


class JsonSerialiser:

    def update_from_json_dictionary(self, dictionary):
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
                if  object_type  is str \
                and (update_type is int or update_type is float or update_type is bool):
                    update_value = str(update_value)

                elif object_type is int \
                and  (update_type is str or update_type is float):
                    update_value = int(update_value)

                elif object_type is float \
                and  update_type is str:
                    update_value = float(update_value)

                elif object_type is bool:
                    update_value = bool_from_json(update_value)

                elif object_type is datetime \
                and  update_type is str:
                    update_value = datetime.strptime(update_value + " +0000", "%Y/%m/%d %H:%M:%S %z")

                elif object_type is JsonSerialiser \
                and  update_type is dict:
                    child = getattr(self, attribute)
                    child.update_from_json_dictionary(update_value)

                elif (object_type is list or object_type is set) \
                and  update_type is list:
                    children = getattr(self, attribute, [])
                    [child.update_from_json_dictionary(update_value) for child in children
                     if child is JsonSerialiser]

            setattr(self, attribute, update_value)
