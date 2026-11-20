import tree_sitter_python as tspython
from tree_sitter import Language, Parser

parser = Parser(Language(tspython.language()))

kode = b"""
def hitung_luas_persegi(a):
    return a * a\n
"""

tree = parser.parse(kode)
print(tree.root_node)

for c in tree.root_node.children[0].children:
    print(c.type, "bernama" if c.is_named else "anonim")

parameters = tree.root_node.children[0].child_by_field_name("parameters")

for c in parameters.children:
    print(c.type, "bernama" if c.is_named else "anonim")