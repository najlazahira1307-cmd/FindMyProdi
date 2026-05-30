#  FindMyProdi

**FindMyProdi** adalah sistem rekomendasi program studi berbasis kata kunci yang dibangun menggunakan struktur data **Binary Search Tree (BST)** serta algoritma **Binary Search** dan **Regex Search**. Sistem ini membantu calon mahasiswa menemukan program studi yang sesuai dengan minat mereka hanya dengan memasukkan kata kunci tertentu.

Proyek ini merupakan implementasi langsung dari teori **perbandingan algoritma searching** dalam mata kuliah Struktur Data dan Algoritma.

---

## A. Struktur File

```text
FindMyProdi/
│
├── data_keywords.py
├── data_details.py
├── engine.py
├── app.py
└── README.md
```

---

## B. Penjelasan Komponen

### `data_keywords.py`

Menyimpan database seluruh kata kunci minat beserta daftar program studi yang relevan. File ini menjadi sumber data utama yang diproses oleh sistem untuk membangun struktur BST dan menjalankan proses pencarian.

### `data_details.py`

Menyimpan informasi lengkap setiap program studi, meliputi:

* Deskripsi program studi
* Prospek karier
* Skill yang dipelajari

Data ini ditampilkan ketika pengguna memilih detail program studi dari hasil pencarian.

### `engine.py`

Merupakan inti dari seluruh sistem. Modul ini bertanggung jawab untuk membangun BST seimbang, melakukan traversal data, serta menjalankan algoritma pencarian.

Komponen utama:

* **BSTNode** → Node penyusun Binary Search Tree
* **BinarySearchTree** → Implementasi struktur data BST
* **build_balanced_order()** → Menyusun urutan insert agar BST lebih seimbang
* **binary_search()** → Pencarian exact match dengan kompleksitas O(log n)
* **regex_search()** → Pencarian partial match dengan kompleksitas O(n)
* **search_prodi()** → Menjalankan kedua algoritma pencarian dan menggabungkan hasilnya

### `app.py`

Antarmuka pengguna berbasis **Streamlit** yang menghubungkan seluruh komponen sistem.

Fitur yang ditampilkan:

* Input kata kunci
* Hasil pencarian program studi
* Detail program studi
* Visualisasi BST interaktif menggunakan D3.js
* Analisis waktu eksekusi algoritma secara real-time

---

## C. Teknologi yang Digunakan

| Teknologi | Fungsi |
|-----------|---------|
| Python | Bahasa pemrograman utama |
| Streamlit | Framework antarmuka web |
| Binary Search Tree (BST) | Struktur data utama untuk penyimpanan keyword |
| Binary Search | Algoritma pencarian exact match |
| Regular Expression (Regex) | Algoritma pencarian partial match |
| D3.js | Visualisasi BST interaktif |
| HTML & CSS | Kustomisasi tampilan antarmuka |

## D. Cara Kerja Sistem

```text
KEYWORD_DATA
     │
     ▼
build_balanced_order()
(Menyusun urutan insert agar BST seimbang)
     │
     ▼
BST Insert
     │
     ▼
inorder()
     │
     ▼
SORTED_KEYWORDS
     │
     ├───────────────────────┐
     │                       │
     ▼                       ▼

Binary Search          Regex Search
O(log n)                 O(n)

Exact Match          Partial Match
     │                       │
     └───────────┬───────────┘
                 ▼
      Hasil Digabung & Deduplikasi
              menggunakan set()
                 ▼
           Final Results
                 ▼
              app.py
```

---

## E. Fitur Aplikasi

### Pencarian Kata Kunci

Pengguna dapat memasukkan kata kunci secara bebas atau memilih kata kunci yang tersedia melalui fitur chip.

### Hasil Pencarian Berwarna

* Merah → Hasil dari Binary Search
* Oranye → Hasil dari Regex Search

### Analisis Waktu Eksekusi

Menampilkan perbandingan waktu eksekusi Binary Search dan Regex Search secara real-time.

### Visualisasi BST Interaktif

Menampilkan struktur BST menggunakan D3.js dengan fitur:

* Zoom
* Pan
* Hover node

### Detail Program Studi

Informasi lengkap mengenai:

* Deskripsi program studi
* Prospek karier
* Skill yang dipelajari

### Alur Sistem Multi-Halaman

Aplikasi terdiri dari 8 halaman utama:

1. Splash Screen
2. Input Kata Kunci
3. Hasil Pencarian
4. Detail Program Studi
5. Visualisasi BST
6. Analisis Algoritma
7. Penutup
8. Sistem Keseluruhan

---

## F. Perbandingan Algoritma

| Aspek           | Binary Search                      | Regex Search                               |
| --------------- | ---------------------------------- | ------------------------------------------ |
| Kompleksitas    | O(log n)                           | O(n)                                       |
| Jenis Pencarian | Exact Match                        | Partial Match                              |
| Prasyarat       | Data harus terurut                 | Tidak memerlukan data terurut              |
| Kecepatan       | Lebih cepat pada dataset besar     | Lebih lambat karena memeriksa seluruh data |
| Kelebihan       | Presisi tinggi dan efisien         | Fleksibel terhadap input parsial           |
| Digunakan Saat  | Kata kunci sama persis dengan data | Kata kunci hanya sebagian dari data        |

---

## G. Instalasi dan Menjalankan Program

### Prasyarat

* Python 3.8 atau lebih baru

### 1. Install Dependencies

```bash
pip install streamlit matplotlib pyparsing
```

### 2. Jalankan Aplikasi

```bash
streamlit run app.py
```

---

## H. Tim Pengembang

| Nama         | NIM |
| ------------ | --- |
| Najla Zahira | 041 |
| Alin         | 068 |
| Moza         | 185 |

---

##  Lisensi

Proyek ini dibuat untuk keperluan akademik dan pembelajaran mengenai implementasi struktur data **Binary Search Tree (BST)** serta perbandingan algoritma pencarian **Binary Search** dan **Regex Search**.
