import sys
import tokenize
import string_utils
import _ast


def read_code(filename):
    if (2, 5) < sys.version_info < (3, 0):
        with open(filename, 'rU') as f:
            return f.read()
    elif (3, 0) <= sys.version_info < (4, 0):
        """Read the source code."""
        try:
            with open(filename, 'rb') as f:
                (encoding, _) = tokenize.detect_encoding(f.readline)
        except (LookupError, SyntaxError, UnicodeError):
            # Fall back if file encoding is improperly declared
            with open(filename, encoding='latin-1') as f:
                return f.read()
        with open(filename, 'r', encoding=encoding) as f:
            return f.read()


def snake_case(function_name):
    if not string_utils.is_snake_case(function_name):
        return is_lowercase_word(function_name)
    return True


def is_lowercase_word(word):
    if not has_upper_case(word):
        return True
    print("No puede tener letras en mayuscula")
    return False


def has_upper_case(word):
    copy_word = (word + ".")[:-1]
    for original_letter, copy_letter in zip(word, copy_word):
        if copy_letter == original_letter.upper():
            return True
    return False


#  https://stackoverflow.com/questions/2166818/python-how-to-check-if-an-object-is-an-instance-of-a-namedtuple
def is_named_tuple_instance(x):
    t = type(x)
    b = t.__bases__
    if len(b) != 1 or b[0] != tuple:
        return False
    f = getattr(t, '_fields', None)
    if not isinstance(f, tuple):
        return False
    return all(type(n) == str for n in f)



def get_for_loops2(tree_code: "_ast.Module", code: "str"):
    for_loops = {}
    element_number = 0
    for element in tree_code.body:
        if not isinstance(element, _ast.For):
            if hasattr(element, 'body'):
                for inside_element in element.body:
                    if isinstance(inside_element, _ast.For):
                        for_loops[get_line_code(code, inside_element.lineno - 1)] = [inside_element.lineno,
                                                                                     element_number]
        else:
            for_loops[get_line_code(code, element.lineno - 1)] = [element.lineno, element_number]
        element_number += 1
    return for_loops


def get_for_loops(tree_code, code, wanted_structure=_ast.For, element_number=0, assign=False, return_structures=[]):
    #return_structures = []
    for element in tree_code.body:
        if assign:
            if hasattr(element, 'body'):
                get_for_loops(element, code, wanted_structure, element_number, assign, return_structures)
            elif isinstance(element, _ast.Assign) and isinstance(element.value, wanted_structure):
                return_structures.append([element, get_line_code(code, element.lineno - 1), element_number])
                element_number -= 1
        else:
            if not isinstance(element, wanted_structure):
                if hasattr(element, 'body'):
                    get_for_loops(element, code, wanted_structure, element_number - 2, assign=False, return_structures=return_structures)
                    # return_dict.update(get_for_loops(element, code, wanted_structure, element_number - 2))
            else:
                return_structures.append([element, get_line_code(code, element.lineno - 1), element_number])
                # return_dict[get_line_code(code, element.lineno - 1)] = [element.lineno, element_number]
                for inside_for in element.body:
                    if isinstance(inside_for, wanted_structure):
                        return_structures.append([inside_for, get_line_code(code, inside_for.lineno - 1), element_number])
                        get_for_loops(inside_for, code, wanted_structure, element_number, assign=False, return_structures=return_structures)
        element_number += 1
    return return_structures


def get_line_code(code: "str", line: "int"):
    return code.split("\n")[line]


def get_iterators(for_loops: "dict"):
    for x in for_loops:
        x.append(get_iterator(x[1]))
    return


def get_iterator(for_loop: "str"):
    index_in = for_loop.find("in")
    iterator = for_loop[index_in+2:].replace(" ", "").replace(":", "")
    if len(iterator) >= 5:
        if iterator[0:5] == "range":
            return "range"
    return iterator


def is_a_dict_ok(loop, tree_code, code):
    if hasattr(loop[0].iter, "id"):
        vamos_ver = get_for_loops(tree_code, code, wanted_structure=_ast.Dict, element_number=0, assign=True, return_structures=[])
        vamos_ver = clean_list(vamos_ver, True)
        if len(vamos_ver) == 0:
            vamos_ver = get_for_loops(tree_code, code, wanted_structure=_ast.Dict, element_number=0, assign=True,
                                      return_structures=[])
        for x in vamos_ver:
            if isinstance(x[0].value, _ast.Dict):
                if x[0].targets[0].id == loop[0].iter.id:
                    print("No esta utilizan items() para iterar en este diccionario: " + x[1] +
                          " en linea: " + str(x[0].lineno))


def assign_involves_list(tree, code, attributes):
    master_element = attributes[0]
    for element in master_element.body:
        if hasattr(element, 'body'):
            assign_involves_list(tree, code, [element])
        else:
            if isinstance(element, _ast.Assign):
                if isinstance(element.targets[0], _ast.Subscript):
                    vamos_ver = get_for_loops(tree, code, _ast.List, 0, True)
                    vamos_ver = clean_list(vamos_ver, True)
                    for x in vamos_ver:
                        if x not in new_vamos_ver:
                            new_vamos_ver.append(x)
                    for x in new_vamos_ver:
                        x[1] = x[1].replace(" ", "")
                        nombre = x[1][0:x[1].find("=")]
                        if attributes[-1] == element.targets[0].value.value.id == nombre:
                            print("Advertencia! En la linea: " + str(element.lineno) +
                                  " se esta iterando una lista sin enumerate(). Codigo: " + get_line_code(code,
                                                                                                      element.lineno - 1))
                elif isinstance(element.value, _ast.Subscript):
                    vamos_ver = get_for_loops(tree, code, _ast.List, 0, True)
                    vamos_ver = clean_list(vamos_ver, True)
                    new_vamos_ver = []
                    for x in vamos_ver:
                        if x not in new_vamos_ver:
                            new_vamos_ver.append(x)
                    for x in new_vamos_ver:
                        x[1] = x[1].replace(" ", "")
                        nombre = x[1][0:x[1].find("=")]
                        if attributes[-1] == element.value.value.id == nombre:
                            print("Advertencia! En la linea: " + str(element.lineno) +
                                  " se esta iterando una lista sin enumerate(). Codigo: " + get_line_code(code,
                                                                                                  element.lineno - 1))


def clean_list(lista, assign=False):
    new_lista = []
    for x in lista:
        if x != []:
            if not isinstance(x[0], list):
                new_lista.append([x[0], x[1]])
            else:
                for element in x:
                    new_lista.append(element)
    newnew = []
    for x in new_lista:
        if x != []:
            newnew.append(x)
    if assign:
        return newnew[:-1]
    return newnew


def test_everything(tree_code, master_code):
    get_for_tuples(tree_code, master_code)
    for_loops = get_for_loops(tree_code, master_code)
    for_loops = clean_list(for_loops)
    get_iterators(for_loops)
    for loop in for_loops:
        is_a_dict_ok(loop, tree_code, master_code)
    for loop in for_loops:
        assign_involves_list(tree_code, master_code, loop)
    ifs = get_for_loops(tree_code, master_code, wanted_structure=_ast.If, element_number=0, assign=False,
                        return_structures=[])
    for x in ifs:
        if x[1].find("True") != -1:
            print("Advertencia, no se deberia usar True en un if, linea: " + str(x[0].lineno) + " expression: "
                  + x[1])
        elif x[1].find("False") != -1:
            print("Advertencia, no se deberia usar False en un if, linea: " + str(x[0].lineno) + " expression: "
                  + x[1])
    for x in ifs:
        if x[1].find("type") != -1:
            print("Advertencia, no se deberia usar type para comparar tipos, linea: " + str(x[0].lineno) + " expression: "
                  + x[1] + " Es mejor usar isinstance")
    for element in tree_code.body:
        if isinstance(element, _ast.FunctionDef):
            if not snake_case(element.name):
                print(element.name + " no esta en snakecase")


def get_for_tuples(tree_code: "_ast.Module", code: "str"):
    for element in tree_code.body:
        if hasattr(element, 'body'):
            get_for_tuples(element, code)
        else:
            if isinstance(element, _ast.Assign) and isinstance(element.value, _ast.Tuple):
                print("Tupla sin namedtuple linea: " + str(element.lineno) + " Codigo: " +
                              get_line_code(code, element.lineno - 1))



