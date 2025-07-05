# Sales Performance Dashboard

Dashboard interaktif untuk analisis performa penjualan menggunakan Streamlit dan PostgreSQL. Project ini dibuat berdasarkan tutorial dari [Towards Data Science: Building a Data Dashboard](https://towardsdatascience.com/building-a-data-dashboard-9441db646697/).

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
- **Database**: PostgreSQL
- **Data Processing**: Pandas
- **Visualization**: Matplotlib
- **Data Generation**: Polars, NumPy

## 📋 Prerequisites

Sebelum menjalankan project, pastikan sudah menginstall:

1. **Python 3.8+**
2. **PostgreSQL** (untuk database)
3. **pgAdmin** (opsional, untuk manajemen database)

## 🚀 Instalasi

### 1. Clone Repository

```bash
git clone <repository-url>
cd sales-dashboard
```

### 2. Install Dependencies

```bash
pip install streamlit pandas matplotlib psycopg2 polars numpy
```

### 3. Setup Database PostgreSQL

#### A. Buat Database

```sql
CREATE DATABASE salesdb;
```

#### B. Buat Tabel

```sql
\c salesdb

CREATE TABLE IF NOT EXISTS public.sales_data
(
    order_id integer NOT NULL,
    order_date date,
    customer_id integer,
    customer_name character varying(255),
    product_id integer,
    product_names character varying(255),
    categories character varying(100),
    quantity integer,
    price numeric(10,2),
    total numeric(10,2)
);
```

#### C. Generate Data Dummy

```bash
python generate_data.py
```

#### D. Import Data ke Database

```sql
COPY sales_data FROM '/path/to/sales_data.csv' DELIMITER ',' CSV HEADER;
```

_Ganti `/path/to/sales_data.csv` dengan path file yang benar_

### 4. Konfigurasi Koneksi Database

Edit file `app.py` dan sesuaikan kredensial database:

```python
@st.cache_resource
def get_conn_pool():
    return psycopg2.pool.SimpleConnectionPool(
        1, 10,
        user="postgres",         # Ganti dengan user PostgreSQL kamu
        password="password",     # Ganti dengan password PostgreSQL kamu
        host="localhost",
        port="5432",
        database="salesdb"       # Ganti dengan nama database kamu
    )
```

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

### **🚀 Deployment ke Streamlit Cloud**

#### **Langkah 1: Push ke GitHub**

```bash
# Inisialisasi git repository (jika belum)
git init
git add .
git commit -m "Initial commit: Sales Dashboard"

# Buat repository baru di GitHub, lalu push
git remote add origin https://github.com/username/sales-dashboard.git
git branch -M main
git push -u origin main
```

#### **Langkah 2: Deploy di Streamlit Cloud**

1. **Buka [share.streamlit.io](https://share.streamlit.io)**
2. **Sign in dengan GitHub**
3. **Klik "New app"**
4. **Isi form:**
   - **Repository**: `username/sales-dashboard`
   - **Branch**: `main`
   - **Main file path**: `app.py`
5. **Klik "Deploy"**

#### **Langkah 3: Konfigurasi Database (Opsional)**

Untuk menggunakan database PostgreSQL di cloud:

- **Gunakan [Supabase](https://supabase.com)** (gratis tier)
- **Atau [Railway](https://railway.app)** (berbayar)
- **Update kredensial database** di `app.py`

#### **Langkah 4: Akses Dashboard**

Dashboard akan tersedia di: `https://your-app-name.streamlit.app`

---

### **🌐 Platform Deployment Lainnya**

#### **Heroku**

```bash
# Install Heroku CLI
# Buat Procfile
echo "web: streamlit run app.py --server.port=\$PORT --server.address=0.0.0.0" > Procfile

# Deploy
heroku create your-app-name
git push heroku main
```

#### **Railway**

1. **Connect GitHub repository**
2. **Add PostgreSQL service**
3. **Set environment variables**
4. **Deploy otomatis**

#### **DigitalOcean App Platform**

1. **Connect GitHub repository**
2. **Choose Python environment**
3. **Configure build settings**
4. **Deploy**

## 📁 Struktur Project

```
sales-dashboard/
├── app.py                 # File utama dashboard Streamlit
├── generate_data.py       # Script untuk generate data dummy
├── sales_data.csv         # File data dummy (dihasilkan otomatis)
├── README.md             # Dokumentasi project
└── requirements.txt      # Dependencies (opsional)
```

## 🔧 Konfigurasi

### Environment Variables (Opsional)

Buat file `.env` untuk menyimpan kredensial database:

```env
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=salesdb
```

### Deployment Considerations

#### **Untuk Local Development:**

- ✅ **PostgreSQL lokal** sudah cukup
- ✅ **File CSV** bisa digunakan sebagai alternatif
- ✅ **Semua fitur** berfungsi normal

#### **Untuk Cloud Deployment:**

- ⚠️ **Database cloud** diperlukan (Supabase, Railway, dll)
- ⚠️ **Environment variables** untuk kredensial database
- ⚠️ **CORS settings** jika diperlukan
- ✅ **Streamlit Cloud** mendukung PostgreSQL

#### **Alternatif Tanpa Database:**

Jika tidak ingin setup database di cloud, bisa modifikasi untuk menggunakan CSV:

```python
# Ganti fungsi database dengan pandas read_csv
@st.cache_data
def load_data():
    return pd.read_csv('sales_data.csv', parse_dates=['order_date'])
```

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

## 🐛 Troubleshooting

### Error: "relation 'sales_data' does not exist"

- Pastikan tabel sudah dibuat di database yang benar
- Cek nama database di konfigurasi koneksi
- Pastikan user memiliki akses ke database

### Error: "password authentication failed"

- Periksa username dan password PostgreSQL
- Pastikan user memiliki akses ke database

### Error: "could not connect to server"

- Pastikan service PostgreSQL berjalan
- Cek host dan port yang digunakan

## 🤝 Contributing

1. Fork repository
2. Buat branch baru (`git checkout -b feature/AmazingFeature`)
3. Commit perubahan (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buat Pull Request

## 📝 License

Project ini dibuat untuk tujuan pembelajaran berdasarkan tutorial dari Towards Data Science.

## 🙏 Acknowledgments

- [Towards Data Science](https://towardsdatascience.com/) untuk tutorial asli
- [Streamlit](https://streamlit.io/) untuk framework dashboard
- [PostgreSQL](https://www.postgresql.org/) untuk database

## 📞 Support

Jika ada pertanyaan atau masalah, silakan buat issue di repository ini.

---

**Happy Dashboarding! 🎉**
