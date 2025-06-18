
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
[Dataset](https://github.com/dicodingacademy/a590-Belajar-Penerapan-Data-Science/tree/a590_proyek_akhir/a590_proyek_akhir)

### Setup Environment

Untuk menjalankan proyek ini, ikuti langkah-langkah berikut:

1. **Instalasi Python dan Virtual Environment**
   - Pastikan Python 3.8 atau lebih tinggi telah terinstal di sistem Anda.
   - Buat virtual environment dengan perintah:
     ```
     python -m venv edutech_project
     ```
   - Aktifkan virtual environment:
     - Pada Windows:
       ```
       edutech_project\Scripts\activate
       ```
     - Pada macOS/Linux:
       ```
       source edutech_project/bin/activate
       ```

2. **Instalasi Dependensi**
   - Pastikan file `requirements.txt` tersedia di direktori proyek (berisi pustaka seperti pandas, scikit-learn, dll.).
   - Instal dependensi dengan perintah:
     ```
     pip install -r requirements.txt
     ```

3. **Konfigurasi Database (Opsional)**
   - Jika ingin mengunggah data ke Supabase, sediakan URL koneksi database dan simpan dalam file konfigurasi atau variabel lingkungan.
   - Contoh kode untuk menghubungkan ke Supabase:
     ```python
     from sqlalchemy import create_engine
     URL = "your_supabase_url"
     engine = create_engine(URL)
     ```

4. **Menjalankan Notebook**
   - Buka notebook `notebook.ipynb` dan jalankan sel-sel secara berurutan untuk melakukan analisis data, pelatihan model, dan penyimpanan model.

## Business Dashboard

Dashboard bisnis telah dikembangkan untuk memberikan wawasan kepada pemangku kepentingan perusahaan mengenai metrik kunci terkait status mahasiswa. Dashboard ini terintegrasi dalam aplikasi Streamlit dan mencakup:

- **Tinjauan Umum:**
  - Jumlah total mahasiswa.
  - Distribusi status mahasiswa (lulus, dropout, terdaftar).
  - Persentase mahasiswa yang dropout.
- **Analisis Faktor Kunci:**
  - Korelasi antara variabel demografis (misalnya status perkawinan) dan status mahasiswa.
  - Pengaruh kinerja akademik (misalnya unit kurikuler yang disetujui) terhadap kemungkinan dropout.
  - Visualisasi fitur-fitur paling berpengaruh.
- **Evaluasi Model:**
  - Metrik performa model machine learning (akurasi, precision, recall, AUC-ROC).
  - Confusion matrix untuk model terbaik.


**Link Dashboard:**  
[http://localhost:3000/dashboard/5-dashboard-wakbarr](http://localhost:3000/dashboard/5-dashboard-wakbarr)

  **Akses Dashboard:**  
Dashboard ini dapat diakses dengan kredensial berikut:  
- URL: `http://localhost:3000`  
- Username: `root@mail.com`  
- Password: `root123`

## Menjalankan Sistem Machine Learning

Prototype sistem machine learning telah dikembangkan menggunakan Streamlit dan dapat dijalankan baik secara online maupun lokal. Prototype ini memungkinkan pengguna untuk memasukkan data mahasiswa dan menerima prediksi apakah mahasiswa tersebut kemungkinan akan lulus atau dropout.

### 🔗 Akses Online (Prototype)
Klik link berikut untuk mencoba prototype yang telah dideploy:  
🌐 [Akses Prototype di Streamlit Cloud](https://pds-menyelesaikan-permasalahan-institusi-pendidikan-r6hex2iyxy.streamlit.app/)

### Menjalankan Secara Lokal
Untuk menjalankan prototype secara lokal, ikuti langkah-langkah berikut:

1. Pastikan virtual environment telah diaktifkan dan dependensi terinstal (lihat bagian **Persiapan**).
2. Pastikan model dan scaler telah disimpan di folder `saved_models` (hasil dari notebook: `best_model.pkl`, `scaler.pkl`, dan `class_names.pkl`).
3. Jalankan perintah berikut di terminal:
   ```
   streamlit run app.py
   ```
   Catatan: `app.py` adalah file script Streamlit yang berisi kode untuk menjalankan aplikasi.

Namun, untuk kemudahan akses, disarankan menggunakan versi online melalui link di atas.

## Conclusion

Proyek ini berhasil mengidentifikasi faktor-faktor utama yang memengaruhi keputusan mahasiswa untuk dropout, seperti nilai kualifikasi sebelumnya, jumlah unit kurikuler yang disetujui, dan status perkawinan. Model Logistic Regression dipilih sebagai model terbaik berdasarkan evaluasi performa, dengan akurasi pada test set sebesar 88.70% dan AUC 0.9267. Model ini menunjukkan stabilitas yang baik (CV_Accuracy 0.8759, CV_Std 0.0101) dan kemampuan membedakan kelas target yang kuat. Dengan model ini, perusahaan dapat memprediksi mahasiswa yang berisiko dropout dan mengambil tindakan pencegahan tepat waktu.

## Rekomendasi Action Items

Berdasarkan hasil analisis dan model prediktif, berikut adalah rekomendasi tindakan yang dapat diambil oleh Jaya Jaya Edutech untuk mengurangi tingkat dropout mahasiswa:

1. **Program Intervensi Dini:**  
   Gunakan model prediktif untuk mengidentifikasi mahasiswa berisiko tinggi dan tawarkan program dukungan khusus, seperti bimbingan belajar atau konseling akademik.
   
2. **Dukungan Akademik Tambahan:**  
   Sediakan sumber daya akademik tambahan (misalnya kelas pengayaan atau tutorial online) untuk mahasiswa yang kesulitan menyelesaikan unit kurikuler.

3. **Komunikasi Personalisasi:**  
   Kirim pesan atau notifikasi yang dipersonalisasi kepada mahasiswa berisiko, mengingatkan mereka tentang sumber daya yang tersedia dan mendorong mereka untuk mencari bantuan.

4. **Fleksibilitas untuk Mahasiswa dengan Tanggung Jawab Keluarga:**  
   Tawarkan jadwal yang lebih fleksibel atau dukungan penitipan anak untuk mahasiswa yang sudah menikah atau memiliki tanggung jawab keluarga, mengingat status perkawinan berpengaruh signifikan.

5. **Monitoring dan Feedback Berkala:**  
   Lakukan survei kepuasan mahasiswa secara rutin untuk memahami tantangan yang mereka hadapi dan tingkatkan pengalaman belajar berdasarkan umpan balik tersebut.

Dengan menerapkan rekomendasi ini, Jaya Jaya Edutech dapat meningkatkan retensi mahasiswa dan mendukung mereka untuk menyelesaikan program studi dengan sukses.
```
