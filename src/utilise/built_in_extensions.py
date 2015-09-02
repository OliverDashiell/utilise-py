__author__ = 'James Stidard'


def public_vars(object):
    return (name for name in vars(object) if not name.startswith('_'))


def getattr_type(object, attribute):
    return type( getattr(object, attribute) )
