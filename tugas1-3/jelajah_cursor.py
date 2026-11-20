import sys
import tree_sitter_python as tspython
from tree_sitter import Language, Parser

parser = Parser(Language(tspython.language()))


def jelajah_cursor(node):
    cursor = node.walk()
    kedalaman = 0

    while True:
        current = cursor.node

        if current.is_named:
            baris, kolom = current.start_point
            field = cursor.field_name
            label = f"{field}: " if field else ""

            print("  " * kedalaman + f"{label}{current.type} [{baris + 1}:{kolom}]")

        # Turun ke child pertama
        if cursor.goto_first_child():
            if current.is_named:
                kedalaman += 1
            continue

        # Berpindah ke sibling berikutnya
        if cursor.goto_next_sibling():
            continue

        # Naik ke parent sampai menemukan sibling
        while cursor.goto_parent():
            if cursor.node.is_named:
                kedalaman -= 1

            if cursor.goto_next_sibling():
                break
        else:
            break


with open(sys.argv[1], "rb") as f:
    tree = parser.parse(f.read())

jelajah_cursor(tree.root_node)