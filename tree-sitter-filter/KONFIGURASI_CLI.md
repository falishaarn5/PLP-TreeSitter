# Konfigurasi Tree-sitter CLI

## Tugas 5 - Langkah 1

Konfigurasi Tree-sitter CLI dibuat menggunakan:

tree-sitter init-config

Pada file ~/.config/tree-sitter/config.json,
parser-directories ditambahkan dengan folder induk proyek:

/home/falishaa/PLP-TreeSitter

Verifikasi dilakukan dari direktori home menggunakan:

tree-sitter parse ~/PLP-TreeSitter/tree-sitter-filter/contoh.filter

Hasil: parser berhasil mengenali grammar filter tanpa ERROR.
