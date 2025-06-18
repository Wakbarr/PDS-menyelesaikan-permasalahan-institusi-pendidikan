# Proyek Akhir: Menyelesaikan Permasalahan Perusahaan Edutech

## Business Understanding

Jaya Jaya Edutech adalah perusahaan teknologi pendidikan inovatif yang menyediakan kursus online dan program gelar untuk mahasiswa di seluruh dunia. Berdiri sejak tahun 2010, perusahaan ini telah berkembang pesat dengan basis pengguna yang signifikan. Namun, Jaya Jaya Edutech menghadapi tantangan besar berupa tingkat dropout mahasiswa yang tinggi, yang berdampak negatif pada hasil pendidikan mahasiswa serta keberlanjutan bisnis perusahaan. Memahami faktor-faktor yang menyebabkan dropout dan memprediksi mahasiswa yang berisiko dapat membantu perusahaan menerapkan intervensi yang tepat untuk meningkatkan tingkat retensi.

## Permasalahan Bisnis

Proyek ini bertujuan untuk menyelesaikan beberapa permasalahan bisnis berikut:

1. **Mengidentifikasi Faktor Utama Penyebab Dropout Mahasiswa:** Menentukan variabel apa saja yang paling memengaruhi keputusan mahasiswa untuk berhenti dari program studi mereka.
2. **Membangun Model Prediktif untuk Status Mahasiswa:** Mengembangkan model machine learning yang dapat memprediksi apakah seorang mahasiswa akan lulus atau dropout berdasarkan profil dan kinerja akademik mereka.
3. **Memberikan Wawasan untuk Intervensi:** Menyediakan insight berbasis data kepada perusahaan untuk merancang strategi yang efektif dalam mengurangi tingkat dropout dan meningkatkan keberhasilan mahasiswa.

## Cakupan Proyek

Proyek ini mencakup aktivitas-aktivitas berikut:

- **Persiapan Data:** Membersihkan dan memproses data mahasiswa untuk menangani nilai yang hilang, mengkodekan variabel kategorikal, dan menskalakan fitur numerik.
- **Exploratory Data Analysis (EDA):** Menganalisis data untuk menemukan pola, korelasi, dan wawasan terkait dropout mahasiswa.
- **Feature Engineering:** Memilih dan mentransformasi fitur untuk meningkatkan performa model.
- **Pengembangan Model:** Melatih dan mengevaluasi beberapa model machine learning, termasuk Logistic Regression, Random Forest, dan Gradient Boosting, untuk memprediksi status mahasiswa.
- **Evaluasi Model:** Membandingkan performa model menggunakan metrik seperti akurasi, presisi, recall, dan AUC-ROC untuk memilih model terbaik.
- **Pembuatan Dashboard:** Mengembangkan dashboard interaktif untuk memvisualisasikan metrik kunci dan wawasan bagi pemangku kepentingan bisnis.
- **Pengembangan Prototipe:** Membuat aplikasi berbasis Streamlit yang memungkinkan pengguna memasukkan data mahasiswa dan mendapatkan prediksi status mereka (lulus atau dropout).
- **Deployment:** Menyimpan model yang telah dilatih dan mendeploy prototipe ke Streamlit Community Cloud untuk akses jarak jauh.

## Persiapan

### Sumber Data

Dataset yang digunakan dalam proyek ini adalah `data.csv`, yang berisi informasi tentang status mahasiswa, termasuk demografi (misalnya status perkawinan, kebangsaan), kualifikasi sebelumnya, dan kinerja akademik (misalnya jumlah unit kurikuler yang disetujui, nilai). Data ini digunakan untuk melatih model machine learning dan mengembangkan dashboard. Sumber data dapat diakses di:  
[https://github.com/dicodingacademy/a590-Belajar-Penerapan-Data-Science/tree/a590_proyek_akhir/a590_proyek_akhir](https://github.com/dicodingacademy/a590-Belajar-Penerapan-Data-Science/tree/a590_proyek_akhir/a590_proyek_akhir)

### Setup Environment

Untuk menjalankan proyek ini, ikuti langkah-langkah berikut:

1. **Instalasi Python dan Virtual Environment**
   - Pastikan Python 3.8 atau lebih tinggi telah terinstal di sistem Anda.
   - Buat virtual environment dengan perintah:
