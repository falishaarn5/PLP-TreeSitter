import sys
from pathlib import Path
import tree_sitter_python as tspython
from tree_sitter import Language, Parser, Query, QueryCursor

PY = Language(tspython.language())
parser = Parser(PY)

Q_TODO = Query(PY, '((comment) @c (#match? @c "TODO|FIXME"))')
Q_FUNGSI = Query(PY, '(function_definition name: (identifier) @nama) @fungsi')

def cek_file(path):
    tree = parser.parse(path.read_bytes())

    # Fitur 1: komentar TODO/FIXME (sudah jadi)
    for node in QueryCursor(Q_TODO).captures(tree.root_node).get("c", []):
        print(f"{path}:{node.start_point[0] + 1}: {node.text.decode().strip()}")

    # Fitur 2 (TODO): fungsi yang lebih dari 30 baris
    for _, captures in QueryCursor(Q_FUNGSI).matches(tree.root_node):
        node_fungsi = captures["fungsi"][0]
        node_nama = captures["nama"][0]

        jumlah_baris = (
            node_fungsi.end_point[0]
            - node_fungsi.start_point[0]
            + 1
        )

        if jumlah_baris > 30:
            nama_fungsi = node_nama.text.decode(errors="replace")
            baris_awal = node_fungsi.start_point[0] + 1

            print(
                f"{path}:{baris_awal}: "
                f"Fungsi '{nama_fungsi}' terlalu panjang "
                f"({jumlah_baris} baris)"
            )
    # Fitur 3 (TODO): file yang pohonnya mengandung error

for path in Path(sys.argv[1]).rglob("*.py"):
    cek_file(path)