from collections import namedtuple

def get_name():
    name = namedtuple("name", ["first", "middle", "last"])
    return name("Richard", "Xavier", "Jones")

nameea = get_name()


normal = namedtuple("nome", ["u", "d", "t"])
nor = normal("uno", "dos", "tres")

nor = ("1", "2")

def isnamedtupleinstance(x):
    t = type(x)
    b = t.__bases__
    if len(b) != 1 or b[0] != tuple: return False
    f = getattr(t, '_fields', None)
    if not isinstance(f, tuple): return False
    return all(type(n)==str for n in f)

if isnamedtupleinstance(nor):
    print("Helloassd")


# If its a tuple
# Iterate over dictionaries rule
# Iterate over lists rule
# Not using type to compare types
# Comparing things to true
# pep 8
# mccabe





