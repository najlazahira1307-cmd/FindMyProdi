import re # mengimport modul regular expression
import time # digunakan untuk mengukur waktu eksekusi setiap algoritma pencarian dalam satu milidetik

from data_keywords import KEYWORD_DATA # import variabel KEYWORD_DATA dari file data_keywords.py
from data_details import DETAIL_PRODI # import variabel DETAIL_PRODI dari file data_details.py


class BSTNode: # untuk mendefinikan class untuk satu node dalam pohon BST
    def __init__(self, data): # konstruktor untuk menginisialisasi node dengan data dan pointer ke anak kiri dan kanan
        self.data = data # menyimpan isi data node
        self.left = None # pointer ke anak kiri
        self.right = None # pointer ke anak kanan


class BinarySearchTree: # mendefinikan class untuk seluruh struktur pohon BST
    def __init__(self): # constuctor BST yang dipanggil saat BinarySearchTree() dibuat
        self.root = None # menyimppan referensi ke node paling atas 

    def insert(self, data): # method untuk menyisipkan data baru ke pohon 
        self.root = self._insert(self.root, data) # memanggil method bantu _insert untuk menyisipkan data ke dalam pohon, dimulai dari root

    def _insert(self, node, data): # method bantu untuk menyisipkan data ke dalam pohon
        if node is None: # kondisi dasar rekursi 
            return BSTNode(data)

        if data["keyword"] < node.data["keyword"]:
            node.left = self._insert(node.left, data) # keputusan untuk menyisipkan data ke anak kiri jika keyword lebih kecil dari node saat ini
        else:
            node.right = self._insert(node.right, data) # keputusan untuk menyisipkan data ke anak kanan jika keyword lebih besar atau sama dengan node saat ini

        return node # mengembalikan node yang telah diperbarui setelah penyisipan, ini memastikan pohon tetap terhubung setelah rekursi selesai
    
    def inorder(self): # method untuk melakukan traversal inorder pada pohon, yang menghasilkan daftar data yang diurutkan berdasarkan keyword
        result = [] # membuat list kosong untuk menyimpan hasil traversal
        self._inorder(self.root, result) # memanggil method bantu _inorder untuk melakukan traversal mulai dari root dan menyimpan hasilnya dalam list result
        return result # mengembalikan daftar hasil traversal inorder, yang berisi data dari setiap node dalam urutan yang diurutkan berdasarkan keyword
    
    def _inorder(self, node, result): # method bantu untuk melakukan traversal inorder secara rekursif, yang mengunjungi node kiri, kemudian node saat ini, dan akhirnya node kanan
        if node: # kondisi berhenti rekursi, jika node adalah None (sudah mencapai daun pohon), tidak lakukan apapun dan kembali
            self._inorder(node.left, result) # kunjungi kiri dulu
            result.append(node.data) # setelah mengunjungi kiri, tambahkan data node saat ini ke hasil
            self._inorder(node.right, result) # kemudian kunjungi kanan

def build_balanced_order(data): # fungsi untuk menyusun ulang data agar BST yang terbentuk seimbang (balanced), mencegah BST menjadi condong ke satu sisi (skewed)
    sorted_data = sorted(data, key=lambda x: x["keyword"]) # urutkan seluruh data berdasarkan keyword secara alfabetis, sebagai persiapan sebelum diambil titik tengahnya
    result = [] # list kosong untuk menyimpan data yang sudah disusun ulang dengan urutan sisipan optimal
    def add_middle(items): # fungsi rekursif di dalam build_balanced_order untuk mengambil elemen tengah terlebih dahulu, lalu rekursif ke kiri dan kanan
        if not items: # kondisi dasar rekursi: jika list sudah kosong, hentikan rekursi
            return
        mid = len(items) // 2 # hitung indeks tengah dari list saat ini menggunakan pembagian bulat
        result.append(items[mid]) # masukkan elemen tengah ke result terlebih dahulu, sehingga ia menjadi node yang disisipkan lebih awal ke BST
        add_middle(items[:mid]) # rekursif ke bagian kiri (semua elemen sebelum tengah) untuk mencari dan menyisipkan titik tengah bagian kiri
        add_middle(items[mid + 1:]) # rekursif ke bagian kanan (semua elemen setelah tengah) untuk mencari dan menyisipkan titik tengah bagian kanan
    add_middle(sorted_data) # panggil add_middle dengan seluruh data yang sudah diurutkan untuk memulai proses penyusunan ulang dari level paling atas
    return result # kembalikan list result yang berisi data dengan urutan sisipan optimal agar BST terbentuk seimbang
    
bst = BinarySearchTree() # membuat instance dari BinarySearchTree untuk menyimpan data keyword dalam struktur pohon BST


BALANCED_KEYWORDS = build_balanced_order(KEYWORD_DATA) # panggil build_balanced_order dengan KEYWORD_DATA sebagai input, hasilnya adalah list keyword yang sudah disusun ulang dengan urutan sisipan seimbang, lalu simpan ke variabel BALANCED_KEYWORDS

for item in BALANCED_KEYWORDS: # loop setiap item dalam BALANCED_KEYWORDS satu per satu untuk disisipkan ke dalam pohon BST
        bst.insert(item) # sisipkan item saat ini ke dalam pohon BST menggunakan method insert, sehingga pohon terbentuk secara seimbang karena urutan sisipannya sudah diatur oleh build_balanced_order

SORTED_KEYWORDS = bst.inorder() # menjalankan in order tarversal dan simpan hasilnya sebagai list terurut. list ini kemudian di pakai oleh binary_search


def binary_search(keyword): # melakukan pencarian keyword menggunakan algoritma binary search pada list SORTED_KEYWORDS yang sudah diurutkan berdasarkan keyword    

    low = 0 # menetapkan indeks awal untuk pencarian
    high = len(SORTED_KEYWORDS) - 1 # dan ini untuk indeks akhir untuk pencarian

    results = [] # list kosong yang akan diisi nama nama prodi yang cocok

    while low <= high: # loop terus selama indeks awal tidak melebihi indeks akhir, yang berarti masih ada elemen yang bisa diperiksa
        mid = (low + high) // 2 # menghitung indeks tengah dari rentang saat ini, yang digunakan untuk membagi daftar menjadi dua bagian
        mid_keyword = SORTED_KEYWORDS[mid]["keyword"] # mengambil keyword dari elemen tengah untuk dibandingkan dengan keyword yang dicari

        if keyword == mid_keyword: # jika keyword ditemukan tepat ditengah 
            left = mid # mulai dari posisi tengah, bergerak ke kiri selama keyword masih sama 
            while left >= 0 and SORTED_KEYWORDS[left]["keyword"] == keyword:
                results.extend(SORTED_KEYWORDS[left]["prodi"]) # jika keyword cocok, tambahkan semua prodinya ke result 
                left -= 1

            right = mid + 1 # setelah selesai bergerak ke kiri, mulai dari posisi tengah + 1, bergerak ke kanan selama keyword masih sama
            while right < len(SORTED_KEYWORDS) and SORTED_KEYWORDS[right]["keyword"] == keyword:
                results.extend(SORTED_KEYWORDS[right]["prodi"]) # jika keyword cocok, tambahkan semua prodinya ke result
                right += 1

            break

        elif keyword < mid_keyword: # jika keyword yang dicari lebih kecil dari keyword tengah, berarti keyword yang dicari berada di bagian kiri daftar, sehingga kita mempersempit pencarian dengan mengubah indeks akhir menjadi mid - 1
            high = mid - 1

        else:
            low = mid + 1 # jika lebih besar dari tengah, buang separuh kiri, pindahkan low ke mid + 1, lalu area pencarian berkurang setengah.

    return list(set(results)) # disini set() digunakan untuk menghapus duplikat. jika satu prodi muncul dari beberapa keyword yang cocok, tetap hitung satu kali.


def regex_search(keyword): # mendefinisikan fungsi regex, untuk menemukan partial match

    pattern = re.compile(re.escape(keyword), re.IGNORECASE) # membuat pola regex dari keyword 
    # re escape untuk mengubah karakter khusus jadi literal 
    # re compile untuk mengkompilasi pola sekali di awal 
    # re ignorecase untuk membuat pencarian tidak peka terhadap huruf besar kecil, sehingga "Teknik" dan "teknik" dianggap sama
    results = [] # list kosong untuk menampung nama prodi yang cocok 

    for item in KEYWORD_DATA: # loop seluruh data keyword dari awal hingga akhir 
        if pattern.search(item["keyword"]): # mencari apakah pola ada dimana saja dalam string keyword. misal pattern "dig" akan cocok dengan "digital"
            results.extend(item["prodi"])
    return list(set(results)) # hapus duplikat dengan set 


def get_prodi_detail(nama_prodi): # untuk mengambil detail satu prodi dari dictionary DETAIL_PRODI
    return DETAIL_PRODI.get(nama_prodi)


def search_prodi(keyword): # fungsi utama untuk melakukan pencarian prodi berdasarkan keyword yang diberikan, menggunakan kedua metode pencarian (binary search dan regex search) dan mengukur waktu eksekusinya

    keyword = keyword.lower().strip() # normalisasi keyword sebelum diproses 
    # lower untuk huruf jadi kecil semua 
    # strip untuk menghapus spasi di awal dan akhir 

    # jalankan binary searh sambil ukur waktunya 
    start_binary = time.perf_counter()
    binary_results = binary_search(keyword)
    binary_time = (time.perf_counter() - start_binary) * 1000

    # jalankan regex search sambil ukur waktunya
    start_regex = time.perf_counter()
    regex_results = regex_search(keyword)
    regex_time = (time.perf_counter() - start_regex) * 1000

    final_results = [] # list hasil akhir berisi dict deatil prodi
    used = set() # set untuk melacak prodi mana yang sudah dimasukkan, mencegah duplikat

    for nama in regex_results: # loop hasil dari regex search, untuk setiap nama prodi yang cocok, ambil detailnya dan tambahkan ke final results jika belum pernah ditambahkan sebelumnya
        detail = get_prodi_detail(nama) # ambil detail lengkap prodi 
        if detail and nama not in used: # detail berati pastikan prdi memang ada di database detail, dan namanot in used untuk memastikan prodi belum pernah ditambahkan sebelumnya
            detail["prodi"] = nama
            final_results.append(detail)
            used.add(nama)

    # kembalikan satu dict besar berisi semua informasi yang dibutuhkan app.py 
    return {
        "keyword": keyword,

        "binary_results": binary_results,
        "regex_results": regex_results,

        "binary_time": binary_time,
        "regex_time": regex_time,

        "results": final_results
    }