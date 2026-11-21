# CLI Pendeteksi TODO, Fungsi Panjang dan Syntax Error

## Deskripsi

Program `cek.py` merupakan aplikasi Command Line Interface (CLI) berbasis Python yang menggunakan Tree-sitter untuk menganalisis struktur kode sumber Python melalui Abstract Syntax Tree (AST).

Program ini memiliki tiga fitur utama:

1. Mendeteksi komentar yang mengandung `TODO` atau `FIXME` menggunakan Tree-sitter Query dan `#match?`.
2. Mendeteksi fungsi dengan panjang lebih dari 30 baris menggunakan `QueryCursor.matches()`.
3. Mendeteksi kesalahan sintaks menggunakan `root_node.has_error` dan penelusuran AST secara rekursif.

## Cara Memasang Dependensi

Pastikan Python sudah terpasang, kemudian jalankan:

```bash
python -m pip install tree-sitter tree-sitter-python
```

## Cara Menjalankan

Masuk ke direktori `cek`, kemudian jalankan:

```bash
python cek.py uji/
```

Untuk memeriksa folder proyek Python lainnya:

```bash
python cek.py /lokasi/folder/proyek
```

Program akan mencari seluruh file berekstensi `.py` secara rekursif.

## Contoh Output

```text
uji/contoh_error.py:5: Ditemukan kesalahan sintaks Python
uji/contoh_panjang.py:1: Fungsi 'fungsi_panjang' terlalu panjang (36 baris)
uji/contoh_todo.py:1: # TODO: Tambahkan validasi input
uji/contoh_todo.py:6: # FIXME: Perbaiki penanganan nama kosong
```

## Pengujian pada Repository Nyata

Repository yang digunakan adalah [PyPA sampleproject](https://github.com/pypa/sampleproject).

Repository diunduh menggunakan:

```bash
git clone https://github.com/pypa/sampleproject.git /tmp/plp-sampleproject
```

Pengujian dilakukan menggunakan:

```bash
python cek.py /tmp/plp-sampleproject
```

Program tidak menghasilkan laporan temuan pada repository tersebut.

### Verifikasi Manual

Dua file diperiksa secara manual:

| File | Hasil Pemeriksaan |
|---|---|
| `src/sample/simple.py` | Fungsi `add_one()` terdiri dari 2 baris, tanpa TODO/FIXME atau kesalahan sintaks. |
| `tests/test_simple.py` | Fungsi `test_add_one()` terdiri dari 2 baris, tanpa TODO/FIXME atau kesalahan sintaks. |

Hasil pemeriksaan manual pada kedua file sesuai dengan hasil program.