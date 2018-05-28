import herramientas
import ast
import subprocess


def pep_8(file):
    show = subprocess.call('pep8 --first ' + file,shell=True)
    print(show)


def mcc(file):
    show = subprocess.call('python -m mccabe ' + file, shell=True)
    print(show)


def run_check(file):
    print("Primer examen - LuisCheck")
    print("")
    code = herramientas.read_code(file)
    tree = compile(code, file, "exec", ast.PyCF_ONLY_AST)
    herramientas.test_everything(tree, code)
    print("")
    print("Segundo examen - Pep-8")
    print("")
    pep_8(file)
    print("")
    print("Tercer examen - Complejidad MCCABE")
    print("")
    mcc(file)


run_check("test.py")
