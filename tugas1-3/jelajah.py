import sys
import tree_sitter_python as tspython
from tree_sitter import Language, Parser

parser = Parser(Language(tspython.language()))

def jelajah(node, kedalaman=0, field=None):
    baris, kolom = node.start_point
    label = f"{field}: " if field else ""
    print("  " * kedalaman + f"{label}{node.type} [{baris + 1}:{kolom}]")
    # untuk setiap child yang bernama, panggil jelajah() lagi dengan kedalaman + 1 dan nama field-nya.
    for child in node.named_children:
        nama_field = None

        for i, semua_child in enumerate(node.children):
            if semua_child.id == child.id:
                nama_field = node.field_name_for_child(i)
                break

        jelajah(child, kedalaman + 1, nama_field)

with open(sys.argv[1], "rb") as f:
    tree = parser.parse(f.read())
jelajah(tree.root_node)