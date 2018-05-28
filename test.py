import mccabe
import ast
import herramientas
import string_utils
from collections import namedtuple
import _ast


def first_Sfun():
    print("This is a test")
    print("This is another test")
    name = namedtuple("name", ["first", "middle", "last"])
    hola = name("RUN", "RUN", "RUN")
    exiii = ("1", "2")


def second_fun():
    a = [1,2,3]
    b = 2
    for x in range(a):
        for y in range(100):
            pass
        c = a[2]
        print(x)
    print("This is another test")

for x in range(2):
    pass


code = herramientas.read_code("test.py")
tree = compile(code, "test.py", "exec", ast.PyCF_ONLY_AST)
a = herramientas.get_for_loops(tree, code)
b = herramientas.get_for_loops2
#herramientas.test_everything(tree, code)
#print(string_utils.is_snake_case("hello"))



#  Que sea una palabra sola en minuscula




