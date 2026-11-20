import tree_sitter_python as tspython
from tree_sitter import Language, Parser

parser = Parser(Language(tspython.language()))

kode = b"""
class Persegi:
	def hitung_luas(self, sisi):
		return sisi * sisi\n
"""

tree = parser.parse(kode)
print(tree.root_node)