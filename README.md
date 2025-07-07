# Sales Performance Dashboard

Dashboard interaktif untuk analisis performa penjualan menggunakan Streamlit dan file CSV lokal (tanpa database server). Project ini dibuat berdasarkan tutorial dari [Towards Data Science: Building a Data Dashboard](https://towardsdatascience.com/building-a-data-dashboard-9441db646697/).

## 📊 Fitur Dashboard

### 🔍 Filter Data

- **Date Range Picker**: Filter data berdasarkan rentang tanggal
- **Category Dropdown**: Filter berdasarkan kategori produk

### 📈 Key Metrics

- **Total Revenue**: Total pendapatan dalam periode yang dipilih
- **Total Orders**: Jumlah pesanan unik
- **Average Order Value**: Rata-rata nilai per pesanan
- **Top Category**: Kategori produk dengan pendapatan tertinggi

### 📊 Visualisasi

1. **Revenue Over Time**: Grafik line chart pendapatan berdasarkan waktu
2. **Revenue by Category**: Bar chart pendapatan per kategori
3. **Top Products**: Horizontal bar chart 10 produk teratas

### 📋 Raw Data

- Tabel data mentah dengan pagination (maksimal 1000 baris)

## 🛠️ Teknologi yang Digunakan

- **Frontend**: Streamlit
- **Data Processing**: Pandas
- **Visualization**: Matplotlib
- **Data Generation**: Polars, NumPy

## 📋 Prerequisites

Sebelum menjalankan project, pastikan sudah menginstall:

1. **Python 3.8+**

## 🚀 Instalasi

### 1. Clone Repository

```bash
git clone <repository-url>
cd streamlit-sales-analytics-main
```

### 2. Install Dependencies

```bash
pip install streamlit pandas matplotlib psycopg2 polars numpy
```

### 3. Generate Data Dummy

```bash
python generate_data.py
```

File `sales_data.csv` akan otomatis dihasilkan dan digunakan sebagai sumber data dashboard.

## 🏃‍♂️ Cara Menjalankan

### **Local Development**

#### 1. Generate Data (Jika Belum Ada)

```bash
python generate_data.py
```

#### 2. Jalankan Dashboard

```bash
streamlit run app.py
```

#### 3. Akses Dashboard

Buka browser dan akses: `http://localhost:8501`

---

## 📁 Struktur Project

```
sales-dashboard/
├── app.py                 # File utama dashboard Streamlit
├── generate_data.py       # Script untuk generate data dummy
├── sales_data.csv         # File data dummy (dihasilkan otomatis)
├── README.md             # Dokumentasi project
└── requirements.txt      # Dependencies (opsional)
```

### Deployment Considerations

#### **Untuk Local Development:**

- ✅ **File CSV** digunakan sebagai sumber data utama
- ✅ **Semua fitur** berfungsi normal

#### **Untuk Cloud Deployment:**

- ⚠️ Pastikan file `sales_data.csv` tersedia di repository

### Customization

- **Data Source**: Ganti query SQL di fungsi-fungsi untuk menggunakan data real
- **Styling**: Edit CSS di bagian `st.markdown()` untuk mengubah tampilan
- **Charts**: Modifikasi fungsi `plot_data()` untuk mengubah jenis visualisasi

## 📊 Data Schema

### Tabel: sales_data

| Column        | Type          | Description                    |
| ------------- | ------------- | ------------------------------ |
| order_id      | integer       | ID pesanan unik                |
| order_date    | date          | Tanggal pesanan                |
| customer_id   | integer       | ID pelanggan                   |
| customer_name | varchar(255)  | Nama pelanggan                 |
| product_id    | integer       | ID produk                      |
| product_names | varchar(255)  | Nama produk                    |
| categories    | varchar(100)  | Kategori produk                |
| quantity      | integer       | Jumlah pesanan                 |
| price         | numeric(10,2) | Harga per unit                 |
| total         | numeric(10,2) | Total harga (quantity × price) |

## 📝 License

Project ini dibuat untuk tujuan pembelajaran berdasarkan tutorial dari Towards Data Science.

## 🙏 Acknowledgments

- [Towards Data Science](https://towardsdatascience.com/) untuk tutorial asli
- [Streamlit](https://streamlit.io/) untuk framework dashboard

## 📞 Support

Jika ada pertanyaan atau masalah, silakan buat issue di repository ini.

---

**Happy Dashboarding! 🎉**
