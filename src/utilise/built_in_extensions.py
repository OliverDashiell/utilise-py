__author__ = 'James Stidard'


def public_vars(object_):
    return (name for name in vars(object_) if not name.startswith('_'))


def getattr_type(object_, attribute) -> type:
    return type( getattr(object_, attribute) )
