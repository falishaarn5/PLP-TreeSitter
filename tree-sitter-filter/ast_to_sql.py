
import tree_sitter_filter
from tree_sitter import Language, Parser

# Daftar kolom yang diperbolehkan dalam filter
ALLOWED_COLUMNS = {
    "status", "priority", "archived",
    "name", "a", "b", "c"
}

# Memeriksa nama kolom sebelum dimasukkan ke SQL
def validate_column(column):
    if column not in ALLOWED_COLUMNS:
        raise ValueError(f"Kolom tidak diizinkan: {column}")

    return column

# Menggunakan grammar filter yang sudah dibuat
FILTER_LANGUAGE = Language(tree_sitter_filter.language())
parser = Parser(FILTER_LANGUAGE)

# Contoh ekspresi DSL
source_code = 'name contains "admin"'

# Mengubah teks menjadi bytes
source_bytes = source_code.encode("utf-8")

# Melakukan parsing
tree = parser.parse(source_bytes)

# Menampilkan hasil AST
print("Input DSL:", source_code)
print("AST:", tree.root_node)

# Menampilkan child node dari root
print("\nChild node:")
for child in tree.root_node.named_children:
    print("Tipe:", child.type)
    print("Teks:", source_bytes[child.start_byte:child.end_byte].decode("utf-8"))


# Mengubah node comparison menjadi SQL terparameterisasi
def convert_comparison(node, source_bytes):
    # Mengambil node identifier dan nilai berdasarkan field
    left_node = node.child_by_field_name("left")
    right_node = node.child_by_field_name("right")

    # Mengambil teks asli dari AST
    column = source_bytes[left_node.start_byte:left_node.end_byte].decode("utf-8")
    column = validate_column(column)
    value_text = source_bytes[right_node.start_byte:right_node.end_byte].decode("utf-8")

    # Mengambil operator dari child anonim
    operator = next(
        source_bytes[child.start_byte:child.end_byte].decode("utf-8")
        for child in node.children
        if not child.is_named
    )

    # Mengubah nilai berdasarkan tipe node
    if right_node.type == "number":
        value = int(value_text)
    elif right_node.type == "boolean":
        value = value_text == "true"
    elif right_node.type == "string":
        value = value_text[1:-1]
    else:
        raise ValueError("Tipe nilai tidak dikenal")

    # Menghasilkan SQL dengan placeholder
    sql = f"{column} {operator} ?"

    return sql, [value]

# Mengubah node nilai AST menjadi nilai Python
def convert_value(node, source_bytes):
    text = source_bytes[node.start_byte:node.end_byte].decode("utf-8")

    if node.type == "number":
        return int(text)
    elif node.type == "boolean":
        return text == "true"
    elif node.type == "string":
        return text[1:-1]
    else:
        raise ValueError(f"Tipe nilai tidak dikenal: {node.type}")

# Mengonversi AST secara rekursif menjadi SQL
def convert_node(node, source_bytes):
    if node.has_error or node.is_missing:
        raise ValueError("Input DSL mengandung kesalahan sintaks")
    
    if node.type == "query":
        return convert_node(node.named_children[0], source_bytes)

    elif node.type == "comparison":
        return convert_comparison(node, source_bytes)

    elif node.type in ("and_expression", "or_expression"):
        left_node = node.child_by_field_name("left")
        right_node = node.child_by_field_name("right")

        # Mengonversi kedua sisi secara rekursif
        left_sql, left_params = convert_node(left_node, source_bytes)
        right_sql, right_params = convert_node(right_node, source_bytes)

        operator = "AND" if node.type == "and_expression" else "OR"

        sql = f"({left_sql} {operator} {right_sql})"
        params = left_params + right_params

        return sql, params

    elif node.type == "parenthesized":
        expression = node.child_by_field_name("expression")

        inner_sql, inner_params = convert_node(expression, source_bytes)

        return f"({inner_sql})", inner_params

    elif node.type == "not_expression":
        expression = node.child_by_field_name("expression")

        inner_sql, inner_params = convert_node(expression, source_bytes)

        return f"(NOT {inner_sql})", inner_params

    elif node.type == "in_expression":
        left_node = node.child_by_field_name("left")

        column = source_bytes[
            left_node.start_byte:left_node.end_byte
        ].decode("utf-8")
        column = validate_column(column)

        # Mengambil semua nilai dalam daftar IN
        value_nodes = [
            child for child in node.named_children
            if child.type in ("string", "number", "boolean")
        ]

        values = [
            convert_value(child, source_bytes)
            for child in value_nodes
        ]

        placeholders = ", ".join(["?"] * len(values))

        sql = f"{column} IN ({placeholders})"

        return sql, values

    elif node.type == "contains_expression":
        left_node = node.child_by_field_name("left")
        right_node = node.child_by_field_name("right")

        column = source_bytes[
            left_node.start_byte:left_node.end_byte
        ].decode("utf-8")
        column = validate_column(column)

        value = convert_value(right_node, source_bytes)

        sql = f"{column} LIKE ?"

        return sql, [f"%{value}%"]

    else:
        raise ValueError(f"Node belum didukung: {node.type}")


# Mengonversi seluruh AST menjadi SQL
sql, params = convert_node(tree.root_node, source_bytes)

print("\nHasil konversi:")
print("SQL WHERE:", sql)
print("Parameter:", params)


# Pengujian akhir konverter AST ke SQL
test_cases = [
    ('status = "open"', 'status = ?', ['open']),
    ('priority >= 2', 'priority >= ?', [2]),
    ('a = 1 and b = 2', '(a = ? AND b = ?)', [1, 2]),
    ('a = 1 or b = 2 and c = 3',
     '(a = ? OR (b = ? AND c = ?))', [1, 2, 3]),
    ('(a = 1 or b = 2) and c = 3',
     '(((a = ? OR b = ?)) AND c = ?)', [1, 2, 3]),
    ('not archived = true', '(NOT archived = ?)', [True]),
    ('status in ("open", "pending", "closed")',
     'status IN (?, ?, ?)', ['open', 'pending', 'closed']),
    ('name contains "admin"', 'name LIKE ?', ['%admin%']),
]

print("\n=== PENGUJIAN AKHIR ===")

for i, (dsl, expected_sql, expected_params) in enumerate(test_cases, 1):
    data = dsl.encode("utf-8")
    parsed_tree = parser.parse(data)

    # Pastikan AST tidak memiliki kesalahan sintaks
    if parsed_tree.root_node.has_error:
        print(f"Test {i}: GAGAL - AST mengandung ERROR")
        continue

    actual_sql, actual_params = convert_node(parsed_tree.root_node, data)

    if actual_sql == expected_sql and actual_params == expected_params:
        print(f"Test {i}: LULUS")
    else:
        print(f"Test {i}: GAGAL")
        print("  SQL aktual:", actual_sql)
        print("  Parameter aktual:", actual_params)
        print("  SQL diharapkan:", expected_sql)
        print("  Parameter diharapkan:", expected_params)

print("\n=== PENGUJIAN INPUT TIDAK VALID ===")

invalid_dsl = "priority >="
invalid_bytes = invalid_dsl.encode("utf-8")
invalid_tree = parser.parse(invalid_bytes)

try:
    convert_node(invalid_tree.root_node, invalid_bytes)
    print("GAGAL: Input tidak valid diterima")
except ValueError as error:
    print("LULUS: Input tidak valid ditolak")
    print("Pesan:", error)


print("\n=== PENGUJIAN VALIDASI KOLOM ===")

invalid_column_dsl = 'password = "secret"'
data = invalid_column_dsl.encode("utf-8")
parsed_tree = parser.parse(data)

try:
    convert_node(parsed_tree.root_node, data)
    print("GAGAL: Kolom tidak dikenal diterima")
except ValueError as error:
    print("LULUS: Kolom tidak dikenal ditolak")
    print("Pesan:", error)
