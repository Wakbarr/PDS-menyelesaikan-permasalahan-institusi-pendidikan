# -*- coding: utf-8 -*-
"""notebook.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1jXiY5BaAz2rGojeywc7V-lsXNuZhQHDX

# Proyek Akhir: Menyelesaikan Permasalahan Perusahaan Edutech

- Nama: Akbar Widianto
- Email: wdntoakbar@gmail.com
- Id Dicoding: Wakbarr

## Persiapan

### Menyiapkan library yang dibutuhkan
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, roc_auc_score, roc_curve
from sklearn.impute import SimpleImputer
import warnings
warnings.filterwarnings('ignore')

"""### Menyiapkan data yang akan diguankan"""

# Yang benar:
df = pd.read_csv("data.csv", sep=';')
df.head(10)

"""Dataset ini merupakan kumpulan data komprehensif yang mencerminkan informasi akademik dan demografis mahasiswa dari Jaya Jaya Institut. Dataset ini dirancang untuk mendukung proses analisis dan pemodelan prediktif dalam upaya menentukan status akhir mahasiswa, apakah mereka akan dropout (mengundurkan diri), lulus, atau masih aktif dalam masa studinya.

## Data Understanding
"""

print(f"\n🔄 MEMPERSIAPKAN TARGET VARIABLE")
print("=" * 40)

# OPSI 1: Binary Classification (Dropout vs Non-Dropout)
# Gabungkan 'Graduate' dan 'Enrolled' sebagai 'Non-Dropout' (0)
# 'Dropout' tetap sebagai 'Dropout' (1)

df_binary = df.copy()
df_binary['Status_Binary'] = df_binary['Status'].map({
    'Graduate': 0,    # Non-Dropout
    'Enrolled': 0,    # Non-Dropout (masih berkuliah)
    'Dropout': 1      # Dropout
})

print("📊 BINARY CLASSIFICATION (Dropout vs Non-Dropout):")
binary_counts = df_binary['Status_Binary'].value_counts()
print(f"- Non-Dropout (Graduate + Enrolled): {binary_counts[0]:,} siswa ({binary_counts[0]/len(df)*100:.1f}%)")
print(f"- Dropout: {binary_counts[1]:,} siswa ({binary_counts[1]/len(df)*100:.1f}%)")

# OPSI 2: Multi-class Classification (3 kelas)
df_multi = df.copy()
label_encoder = LabelEncoder()
df_multi['Status_Encoded'] = label_encoder.fit_transform(df_multi['Status'])

print(f"\n📊 MULTI-CLASS CLASSIFICATION:")
status_mapping = dict(zip(label_encoder.classes_, label_encoder.transform(label_encoder.classes_)))
print(f"Status mapping: {status_mapping}")

# Pilih pendekatan (default: binary classification untuk prediksi dropout)
use_binary = True  # Set False untuk multi-class

if use_binary:
    df_processed = df_binary.copy()
    target_col = 'Status_Binary'
    print(f"\n✅ Menggunakan BINARY CLASSIFICATION")
    class_names = ['Non-Dropout', 'Dropout']
else:
    df_processed = df_multi.copy()
    target_col = 'Status_Encoded'
    print(f"\n✅ Menggunakan MULTI-CLASS CLASSIFICATION")
    class_names = list(label_encoder.classes_)


print("=" * 150)

"""Dalam proses analisis prediktif terhadap status mahasiswa di Jaya Jaya Institut, langkah awal yang dilakukan adalah menyiapkan target variable atau variabel sasaran yang akan diprediksi oleh model. Variabel ini berasal dari kolom Status pada dataset, yang menunjukkan kondisi akhir dari mahasiswa: apakah mereka telah lulus (Graduate), masih aktif (Enrolled), atau telah mengundurkan diri (Dropout). Untuk mempermudah pemodelan, dua pendekatan klasifikasi disiapkan, yaitu klasifikasi biner (binary classification) dan klasifikasi multi-kelas (multi-class classification).

Pada pendekatan pertama, yaitu klasifikasi biner, mahasiswa dikategorikan ke dalam dua kelas: Non-Dropout dan Dropout. Kategori Non-Dropout mencakup mahasiswa yang lulus maupun yang masih aktif kuliah, sementara Dropout mencakup mereka yang tidak menyelesaikan studi. Dalam proses ini, nilai Graduate dan Enrolled diubah menjadi 0 (Non-Dropout), sedangkan Dropout menjadi 1. Hasil pengelompokan ini menunjukkan bahwa sekitar 67.9% mahasiswa berada dalam kategori Non-Dropout, dan sisanya 32.1% berada pada kategori Dropout. Pendekatan ini cocok digunakan jika fokus utama analisis adalah untuk mendeteksi kemungkinan mahasiswa mengalami dropout.

Sementara itu, pendekatan kedua menerapkan klasifikasi multi-kelas, yang mempertahankan ketiga status asli mahasiswa tanpa penyederhanaan. Untuk keperluan pemrosesan model, nilai-nilai tersebut dikodekan ke dalam bentuk numerik menggunakan LabelEncoder, misalnya Enrolled dikodekan menjadi 0, Graduate menjadi 2, dan Dropout menjadi 1. Pendekatan ini memberikan fleksibilitas lebih apabila tujuan analisis adalah untuk memahami dan memprediksi semua kemungkinan status akhir mahasiswa, bukan hanya dropout.

Akhirnya, pengguna diberikan opsi untuk memilih pendekatan mana yang akan digunakan. Secara default, pendekatan biner digunakan, namun dapat dialihkan ke multi-kelas dengan mengatur nilai parameter use_binary ke False. Pilihan pendekatan ini akan menentukan struktur data dan label target yang digunakan pada proses pelatihan model selanjutnya.
"""

print(f"\n🔍 EXPLORATORY DATA ANALYSIS (EDA)")
print("=" * 50)

# Set style untuk plot
plt.style.use('default')
sns.set_palette("husl")

# 2.1 BASIC STATISTICS
print(f"\n📈 STATISTIK DESKRIPTIF")
print("-" * 30)

# Tampilkan statistik deskriptif untuk numerical columns
numerical_cols = df_processed.select_dtypes(include=[np.number]).columns.tolist()
# Remove target columns from numerical analysis
target_cols_to_remove = ['Status_Binary', 'Status_Encoded']
numerical_cols = [col for col in numerical_cols if col not in target_cols_to_remove]

print(f"Kolom numerik: {len(numerical_cols)} kolom")
if len(numerical_cols) > 0:
    print(df_processed[numerical_cols].describe().round(2))

# 2.2 TARGET VARIABLE ANALYSIS
print(f"\n🎯 ANALISIS TARGET VARIABLE")
print("-" * 30)

# Visualisasi distribusi target
plt.figure(figsize=(15, 5))

plt.subplot(1, 3, 1)
target_counts = df_processed[target_col].value_counts()
plt.pie(target_counts.values, labels=[class_names[i] for i in target_counts.index],
        autopct='%1.1f%%', startangle=90)
plt.title('Distribusi Target Variable')

plt.subplot(1, 3, 2)
target_counts_named = pd.Series(target_counts.values, index=[class_names[i] for i in target_counts.index])
target_counts_named.plot(kind='bar')
plt.title('Jumlah Siswa per Kategori')
plt.xticks(rotation=45)

plt.subplot(1, 3, 3)
target_pct = df_processed[target_col].value_counts(normalize=True) * 100
target_pct_named = pd.Series(target_pct.values, index=[class_names[i] for i in target_pct.index])
target_pct_named.plot(kind='bar')
plt.title('Persentase per Kategori')
plt.ylabel('Persentase (%)')
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()

# Print statistik target
print(f"Distribusi Target:")
for idx, count in target_counts.items():
    pct = (count/len(df_processed))*100
    print(f"  {class_names[idx]}: {count:,} siswa ({pct:.1f}%)")

# 2.3 MISSING VALUES ANALYSIS
print(f"\n❓ ANALISIS MISSING VALUES")
print("-" * 30)

missing_data = df_processed.isnull().sum()
missing_pct = (missing_data / len(df_processed)) * 100

if missing_data.sum() > 0:
    missing_df = pd.DataFrame({
        'Column': missing_data.index,
        'Missing_Count': missing_data.values,
        'Missing_Percentage': missing_pct.values
    }).sort_values('Missing_Count', ascending=False)

    print(missing_df[missing_df['Missing_Count'] > 0])

    # Visualisasi missing values
    if len(missing_df[missing_df['Missing_Count'] > 0]) > 0:
        plt.figure(figsize=(12, 6))
        sns.heatmap(df_processed.isnull(), cbar=True, yticklabels=False, cmap='viridis')
        plt.title('Missing Values Heatmap')
        plt.show()
else:
    print("✅ Tidak ada missing values dalam dataset")

# 2.4 NUMERICAL FEATURES ANALYSIS
print(f"\n📊 ANALISIS FITUR NUMERIK")
print("-" * 30)

# Top fitur numerik penting untuk dianalisis
important_numerical = ['Age_at_enrollment', 'Admission_grade',
                      'Curricular_units_1st_sem_grade', 'Curricular_units_2nd_sem_grade',
                      'Previous_qualification_grade', 'GDP', 'Unemployment_rate', 'Inflation_rate']

# Filter kolom yang ada di dataset
available_numerical = [col for col in important_numerical if col in df_processed.columns]
if len(available_numerical) == 0:
    available_numerical = numerical_cols[:4]  # Ambil 4 kolom numerik pertama

if len(available_numerical) >= 4:
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))

    for i, col in enumerate(available_numerical[:4]):
        row = i // 2
        col_idx = i % 2

        # Histogram
        axes[row, col_idx].hist(df_processed[col].dropna(), bins=30, alpha=0.7, edgecolor='black')
        axes[row, col_idx].set_title(f'Distribusi {col}')
        axes[row, col_idx].set_xlabel(col)
        axes[row, col_idx].set_ylabel('Frekuensi')

    plt.tight_layout()
    plt.show()

# Correlation dengan target untuk numerical features
if len(numerical_cols) > 0:
    print(f"\nKorelasi fitur numerik dengan Target:")
    correlations = {}
    for col in numerical_cols[:10]:  # Ambil 10 kolom pertama
        if col in df_processed.columns:
            corr = df_processed[col].corr(df_processed[target_col])
            if not np.isnan(corr):
                correlations[col] = corr

    if correlations:
        correlation_df = pd.DataFrame.from_dict(correlations, orient='index', columns=['Correlation'])
        correlation_df = correlation_df.sort_values('Correlation', key=abs, ascending=False)
        print(correlation_df.head(10).round(4))

# 2.5 CATEGORICAL FEATURES ANALYSIS
print(f"\n📝 ANALISIS FITUR KATEGORIKAL")
print("-" * 30)

categorical_cols = df_processed.select_dtypes(include=['object']).columns.tolist()
# Remove original Status column
if 'Status' in categorical_cols:
    categorical_cols.remove('Status')

print(f"Kolom kategorikal: {len(categorical_cols)} kolom")

# Analisis beberapa fitur kategorikal penting
important_categorical = ['Gender', 'Scholarship_holder', 'Debtor', 'Tuition_fees_up_to_date']
available_categorical = [col for col in important_categorical if col in df_processed.columns]
if len(available_categorical) == 0 and len(categorical_cols) > 0:
    available_categorical = categorical_cols[:4]  # Ambil 4 kolom kategorikal pertama

if len(available_categorical) > 0:
    fig_rows = min(2, (len(available_categorical) + 1) // 2)
    fig_cols = min(2, len(available_categorical))
    fig, axes = plt.subplots(fig_rows, fig_cols, figsize=(15, 5 * fig_rows))

    if fig_rows == 1 and fig_cols == 1:
        axes = [axes]
    elif fig_rows == 1 or fig_cols == 1:
        axes = axes.flatten()
    else:
        axes = axes.flatten()

    for i, col in enumerate(available_categorical[:4]):
        if col in df_processed.columns:
            # Countplot
            sns.countplot(data=df_processed, x=col, ax=axes[i])
            axes[i].set_title(f'Distribusi {col}')
            axes[i].tick_params(axis='x', rotation=45)

    plt.tight_layout()
    plt.show()

"""Secara keseluruhan, dataset ini mencakup 4424 entri (baris data) yang mewakili individu mahasiswa, serta 37 atribut (kolom) yang merekam berbagai aspek penting, mulai dari latar belakang pribadi hingga performa akademik. Setiap kolom memberikan wawasan spesifik yang berpotensi menjadi indikator terhadap keberhasilan studi mahasiswa.

## Data Preparation / Preprocessing

Pada tahap ini, dilakukan proses penting dalam data preprocessing atau prapemrosesan data sebelum model pelatihan dibuat. Tujuan utamanya adalah memastikan bahwa data dalam kondisi bersih, konsisten, dan siap digunakan oleh algoritma pembelajaran mesin. Proses ini mencakup penanganan nilai kosong (missing values), pengolahan variabel numerik dan kategorikal, pengkodean variabel kategorikal, pemisahan fitur dan target, standardisasi fitur numerik, serta pembagian data menjadi data latih dan data uji.
"""

# Handle missing values jika ada
if df_processed.isnull().sum().sum() > 0:
    print("Mengisi missing values...")
    # Untuk numerical columns
    numerical_cols_for_impute = df_processed.select_dtypes(include=[np.number]).columns
    numerical_cols_for_impute = [col for col in numerical_cols_for_impute if col not in [target_col]]

    if len(numerical_cols_for_impute) > 0:
        imputer_num = SimpleImputer(strategy='median')
        df_processed[numerical_cols_for_impute] = imputer_num.fit_transform(df_processed[numerical_cols_for_impute])

    # Untuk categorical columns
    categorical_cols_for_impute = df_processed.select_dtypes(include=['object']).columns
    categorical_cols_for_impute = [col for col in categorical_cols_for_impute if col != 'Status']

    if len(categorical_cols_for_impute) > 0:
        imputer_cat = SimpleImputer(strategy='most_frequent')
        df_processed[categorical_cols_for_impute] = imputer_cat.fit_transform(df_processed[categorical_cols_for_impute])

"""Langkah pertama adalah memeriksa dan mengisi nilai kosong dalam dataset. Untuk kolom numerik, digunakan strategi median, sedangkan untuk kolom kategorikal, nilai terbanyak (most frequent) digunakan. Pendekatan ini dipilih agar distribusi data tidak terlalu terdistorsi akibat nilai isian."""

# Encode categorical variables
categorical_cols_to_encode = df_processed.select_dtypes(include=['object']).columns.tolist()
if 'Status' in categorical_cols_to_encode:
    categorical_cols_to_encode.remove('Status')

if len(categorical_cols_to_encode) > 0:
    print(f"Encoding {len(categorical_cols_to_encode)} categorical columns...")
    df_encoded = pd.get_dummies(df_processed, columns=categorical_cols_to_encode, drop_first=True)
else:
    df_encoded = df_processed.copy()

"""Setelah nilai kosong ditangani, proses berikutnya adalah encoding atau pengkodean variabel kategorikal ke bentuk numerik agar bisa diproses oleh model. Semua kolom bertipe objek yang bukan kolom target (Status) dikodekan menggunakan metode one-hot encoding melalui fungsi pd.get_dummies(). Proses ini menghasilkan kolom baru yang merepresentasikan kategori dalam format biner (0 dan 1), menghindari ambiguitas dalam interpretasi nilai kategorikal oleh model."""

# Pisahkan features dan target
feature_cols = [col for col in df_encoded.columns if col not in ['Status', 'Status_Binary', 'Status_Encoded']]
X = df_encoded[feature_cols]
y = df_encoded[target_col]

print(f"✅ Features: {X.shape[1]} kolom")
print(f"✅ Target: {len(y.unique())} kelas unik")
print(f"✅ Target distribution: {dict(y.value_counts())}")

"""Selanjutnya, dipisahkan fitur prediktor (X) dari variabel target (y). Hanya kolom-kolom selain Status, Status_Binary, dan Status_Encoded yang digunakan sebagai fitur. Dalam kasus ini, terdapat total 36 fitur yang akan digunakan untuk memprediksi status mahasiswa. Target memiliki dua kelas unik, yaitu Non-Dropout dan Dropout, dengan distribusi yang tidak seimbang (sekitar 67.9% Non-Dropout dan 32.1% Dropout)."""

# Standardisasi numerical features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_scaled = pd.DataFrame(X_scaled, columns=X.columns)

print(f"✅ Semua features telah di-standardisasi")

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42, stratify=y
)

print(f"✅ Data split:")
print(f"   - Training: {X_train.shape[0]:,} samples")
print(f"   - Testing: {X_test.shape[0]:,} samples")

"""Kemudian dilakukan standardisasi pada fitur numerik menggunakan StandardScaler dari Scikit-Learn untuk memastikan semua fitur berada dalam skala yang seragam. Hal ini penting agar fitur dengan skala besar tidak mendominasi proses pelatihan model.

Langkah terakhir adalah pembagian data menjadi data latih dan data uji dengan rasio 80:20. Pembagian ini dilakukan secara stratified, yang artinya distribusi kelas pada data latih dan data uji akan mencerminkan distribusi asli dari keseluruhan data. Sebanyak 3.539 data digunakan untuk pelatihan dan 885 data untuk pengujian. Semua fitur pada kedua bagian data ini telah distandardisasi dan siap digunakan dalam proses pelatihan model klasifikasi selanjutnya.

## Modeling

## Gradient Boosting
Gradient Boosting adalah teknik pembelajaran ansambel yang membangun model prediksi secara bertahap dengan menambahkan pohon keputusan secara berurutan. Berbeda dengan Random Forest yang menggunakan pendekatan paralel, Gradient Boosting memperbaiki kesalahan prediksi dari model sebelumnya pada setiap iterasi. Tujuannya adalah meminimalkan loss function secara bertahap dengan menggunakan metode turunan gradien. Metode ini dikenal sangat akurat dan cocok untuk kompetisi data science karena kemampuannya menangkap pola non-linear dan interaksi antar fitur. Namun, Gradient Boosting cenderung lebih sensitif terhadap overfitting dan membutuhkan tuning parameter yang cermat, serta memerlukan waktu pelatihan yang lebih lama dibandingkan metode lainnya.
"""

# ====================================
#  GRADIENT BOOSTING TRAINING
# ====================================

print(f"\n🤖 TRAINING GRADIENT BOOSTING")
print("=" * 40)

# Training Gradient Boosting
gb_model = GradientBoostingClassifier(random_state=42)

print(f"\n🔄 Training Gradient Boosting...")

# Cross validation
gb_cv_scores = cross_val_score(gb_model, X_train, y_train, cv=5, scoring='accuracy')

# Fit model
gb_model.fit(X_train, y_train)

# Prediksi
gb_y_pred = gb_model.predict(X_test)
gb_y_pred_proba = gb_model.predict_proba(X_test)

if use_binary:
    gb_y_pred_proba = gb_y_pred_proba[:, 1]  # Probability of positive class

print(f"   ✅ CV Accuracy: {gb_cv_scores.mean():.4f} (±{gb_cv_scores.std():.4f})")
print(f"   ✅ Model trained successfully!")

"""## Logistic Regression
Logistic Regression merupakan algoritma klasifikasi statistik yang digunakan untuk memodelkan hubungan antara satu atau lebih variabel independen dengan variabel dependen biner. Berbeda dengan regresi linear, algoritma ini menggunakan fungsi sigmoid untuk mengubah output menjadi probabilitas dalam rentang 0 hingga 1, yang kemudian diklasifikasikan ke dalam dua kelas. Logistic Regression sangat cocok untuk kasus klasifikasi sederhana dan dapat diinterpretasikan dengan mudah karena koefisiennya menunjukkan pengaruh masing-masing fitur terhadap peluang kelas. Meskipun performanya tidak sekuat algoritma ansambel pada data kompleks, Logistic Regression sering digunakan sebagai baseline model karena kecepatan pelatihan dan kemudahan implementasinya.
"""

# ====================================
#  LOGISTIC REGRESSION TRAINING
# ====================================

print(f"\n🤖 TRAINING LOGISTIC REGRESSION")
print("=" * 40)

# Training Logistic Regression
lr_model = LogisticRegression(random_state=42, max_iter=1000)

print(f"\n🔄 Training Logistic Regression...")

# Cross validation
lr_cv_scores = cross_val_score(lr_model, X_train, y_train, cv=5, scoring='accuracy')

# Fit model
lr_model.fit(X_train, y_train)

# Prediksi
lr_y_pred = lr_model.predict(X_test)
lr_y_pred_proba = lr_model.predict_proba(X_test)

if use_binary:
    lr_y_pred_proba = lr_y_pred_proba[:, 1]  # Probability of positive class

print(f"   ✅ CV Accuracy: {lr_cv_scores.mean():.4f} (±{lr_cv_scores.std():.4f})")
print(f"   ✅ Model trained successfully!")

"""## Random forest
Random Forest adalah algoritma pembelajaran ansambel yang menggunakan pendekatan bagging (bootstrap aggregating) untuk membangun sejumlah pohon keputusan (decision trees) dari subset acak data pelatihan. Setiap pohon dibangun dari sampel data yang berbeda dan menggunakan subset fitur yang juga dipilih secara acak. Hasil prediksi akhir ditentukan melalui pemungutan suara mayoritas (majority voting) dari seluruh pohon. Kelebihan utama Random Forest adalah kemampuannya dalam menangani data yang kompleks dan besar tanpa overfitting secara signifikan. Selain itu, algoritma ini juga dapat memberikan estimasi pentingnya setiap fitur dalam prediksi. Namun, interpretasi model bisa menjadi sulit karena kompleksitas gabungan banyak pohon.
"""

# ====================================
#  RANDOM FOREST TRAINING
# ====================================

print(f"\n🤖 TRAINING RANDOM FOREST")
print("=" * 40)

# Training Random Forest
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)

print(f"\n🔄 Training Random Forest...")

# Cross validation
rf_cv_scores = cross_val_score(rf_model, X_train, y_train, cv=5, scoring='accuracy')

# Fit model
rf_model.fit(X_train, y_train)

# Prediksi
rf_y_pred = rf_model.predict(X_test)
rf_y_pred_proba = rf_model.predict_proba(X_test)

if use_binary:
    rf_y_pred_proba = rf_y_pred_proba[:, 1]  # Probability of positive class

print(f"   ✅ CV Accuracy: {rf_cv_scores.mean():.4f} (±{rf_cv_scores.std():.4f})")
print(f"   ✅ Model trained successfully!")

"""## Evaluation"""

# ====================================
#  EVALUASI GRADIENT BOOSTING
# ====================================

print(f"\n📊 EVALUASI GRADIENT BOOSTING")
print("=" * 40)

# Evaluasi Gradient Boosting
gb_accuracy = accuracy_score(y_test, gb_y_pred)
gb_auc = None

if use_binary:
    gb_auc = roc_auc_score(y_test, gb_y_pred_proba)

print(f"Test Accuracy: {gb_accuracy:.4f}")
if gb_auc:
    print(f"AUC Score: {gb_auc:.4f}")

print(f"\nClassification Report - Gradient Boosting:")
print(classification_report(y_test, gb_y_pred, target_names=class_names))

print(f"\nConfusion Matrix - Gradient Boosting:")
gb_cm = confusion_matrix(y_test, gb_y_pred)
print(gb_cm)

# Visualisasi Confusion Matrix
plt.figure(figsize=(8, 6))
sns.heatmap(gb_cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=class_names, yticklabels=class_names)
plt.title('Confusion Matrix - Gradient Boosting')
plt.ylabel('Actual')
plt.xlabel('Predicted')
plt.show()

# ====================================
#  EVALUASI LOGISTIC REGRESSION
# ====================================

print(f"\n📊 EVALUASI LOGISTIC REGRESSION")
print("=" * 40)

# Evaluasi Logistic Regression
lr_accuracy = accuracy_score(y_test, lr_y_pred)
lr_auc = None

if use_binary:
    lr_auc = roc_auc_score(y_test, lr_y_pred_proba)

print(f"Test Accuracy: {lr_accuracy:.4f}")
if lr_auc:
    print(f"AUC Score: {lr_auc:.4f}")

print(f"\nClassification Report - Logistic Regression:")
print(classification_report(y_test, lr_y_pred, target_names=class_names))

print(f"\nConfusion Matrix - Logistic Regression:")
lr_cm = confusion_matrix(y_test, lr_y_pred)
print(lr_cm)

# Visualisasi Confusion Matrix
plt.figure(figsize=(8, 6))
sns.heatmap(lr_cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=class_names, yticklabels=class_names)
plt.title('Confusion Matrix - Logistic Regression')
plt.ylabel('Actual')
plt.xlabel('Predicted')
plt.show()

# ====================================
#  EVALUASI RANDOM FOREST
# ====================================

print(f"\n📊 EVALUASI RANDOM FOREST")
print("=" * 40)

# Evaluasi Random Forest
rf_accuracy = accuracy_score(y_test, rf_y_pred)
rf_auc = None

if use_binary:
    rf_auc = roc_auc_score(y_test, rf_y_pred_proba)

print(f"Test Accuracy: {rf_accuracy:.4f}")
if rf_auc:
    print(f"AUC Score: {rf_auc:.4f}")

print(f"\nClassification Report - Random Forest:")
print(classification_report(y_test, rf_y_pred, target_names=class_names))

print(f"\nConfusion Matrix - Random Forest:")
rf_cm = confusion_matrix(y_test, rf_y_pred)
print(rf_cm)

# Visualisasi Confusion Matrix
plt.figure(figsize=(8, 6))
sns.heatmap(rf_cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=class_names, yticklabels=class_names)
plt.title('Confusion Matrix - Random Forest')
plt.ylabel('Actual')
plt.xlabel('Predicted')
plt.show()

# ====================================
# CELL 7: PERBANDINGAN SEMUA MODEL
# ====================================

print(f"\n📊 PERBANDINGAN SEMUA MODEL")
print("=" * 40)

# Kumpulkan semua hasil
models_results = {
    'Random Forest': {
        'cv_mean': rf_cv_scores.mean(),
        'cv_std': rf_cv_scores.std(),
        'test_accuracy': rf_accuracy,
        'auc': rf_auc
    },
    'Gradient Boosting': {
        'cv_mean': gb_cv_scores.mean(),
        'cv_std': gb_cv_scores.std(),
        'test_accuracy': gb_accuracy,
        'auc': gb_auc
    },
    'Logistic Regression': {
        'cv_mean': lr_cv_scores.mean(),
        'cv_std': lr_cv_scores.std(),
        'test_accuracy': lr_accuracy,
        'auc': lr_auc
    }
}

# Buat DataFrame hasil
results_df = pd.DataFrame({
    'Model': list(models_results.keys()),
    'CV_Accuracy': [models_results[model]['cv_mean'] for model in models_results.keys()],
    'CV_Std': [models_results[model]['cv_std'] for model in models_results.keys()],
    'Test_Accuracy': [models_results[model]['test_accuracy'] for model in models_results.keys()],
    'AUC': [models_results[model]['auc'] if models_results[model]['auc'] else 0 for model in models_results.keys()]
})

results_df = results_df.sort_values('Test_Accuracy', ascending=False)
print(results_df.round(4))

# Pilih model terbaik
best_model_name = results_df.iloc[0]['Model']
best_accuracy = results_df.iloc[0]['Test_Accuracy']
best_auc = results_df.iloc[0]['AUC'] if results_df.iloc[0]['AUC'] > 0 else None

print(f"\n🏆 MODEL TERBAIK: {best_model_name}")
print(f"   📈 Test Accuracy: {best_accuracy:.4f}")
if best_auc:
    print(f"   📈 AUC Score: {best_auc:.4f}")

# ROC Curve Comparison untuk binary classification
if use_binary:
    plt.figure(figsize=(10, 8))

    # Plot ROC curve untuk setiap model
    fpr_rf, tpr_rf, _ = roc_curve(y_test, rf_y_pred_proba)
    plt.plot(fpr_rf, tpr_rf, label=f'Random Forest (AUC = {rf_auc:.3f})')

    fpr_gb, tpr_gb, _ = roc_curve(y_test, gb_y_pred_proba)
    plt.plot(fpr_gb, tpr_gb, label=f'Gradient Boosting (AUC = {gb_auc:.3f})')

    fpr_lr, tpr_lr, _ = roc_curve(y_test, lr_y_pred_proba)
    plt.plot(fpr_lr, tpr_lr, label=f'Logistic Regression (AUC = {lr_auc:.3f})')

    plt.plot([0, 1], [0, 1], 'k--', label='Random')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curves Comparison')
    plt.legend()
    plt.grid(True)
    plt.show()

"""Berdasarkan hasil perbandingan model yang ditampilkan, telah dilakukan evaluasi terhadap tiga model machine learning yaitu Logistic Regression, Random Forest, dan Gradient Boosting. Dari ketiga model tersebut, Logistic Regression menunjukkan performa terbaik dengan CV_Accuracy sebesar 0.8759, CV_Std 0.0101, Test_Accuracy 0.8870, dan AUC 0.9267. Model Random Forest berada di posisi kedua dengan CV_Accuracy 0.8692, CV_Std 0.0136, Test_Accuracy 0.8859, dan AUC 0.9294. Sementara Gradient Boosting menempati posisi ketiga dengan CV_Accuracy 0.8748, CV_Std 0.0096, Test_Accuracy 0.8780, dan AUC 0.9307.

Meskipun perbedaan performa antar model relatif kecil, Logistic Regression dipilih sebagai model terbaik berdasarkan kombinasi metrics yang konsisten. Model ini memiliki tingkat akurasi yang stabil baik pada cross-validation maupun test set, dengan standar deviasi yang rendah menunjukkan konsistensi performa. Nilai AUC yang tinggi (0.9267) juga mengindikasikan kemampuan model yang baik dalam membedakan kelas target, menjadikannya pilihan optimal untuk implementasi lebih lanjut.

# Save Model
"""

# ====================================
# SAVE MODEL
# ====================================

import joblib
import os

# Buat folder
os.makedirs("saved_models", exist_ok=True)

# Simpan model terbaik (Logistic Regression)
joblib.dump(lr_model, "saved_models/best_model.pkl")
joblib.dump(scaler, "saved_models/scaler.pkl")
joblib.dump(class_names, "saved_models/class_names.pkl")

print("✅ Model tersimpan!")

"""# Pull data ke supabase"""

from sqlalchemy import create_engine
import pandas as pd

URL = "postgresql://postgres.oacodryygvswimfpnngq:luissayangyudha@aws-0-ap-southeast-1.pooler.supabase.com:5432/postgres"
engine = create_engine(
    URL,
    connect_args={
        "sslmode": "require",
        "sslcert": None,
        "sslkey": None,
        "sslrootcert": None
    }
)

# Upload data ke PostgreSQL (buat table baru)
df_processed.to_sql('education', engine, if_exists='replace', index=False)
print("✅ Table 'education' berhasil dibuat")

# Cek apakah table sudah ada
tables = pd.read_sql("SELECT tablename FROM pg_tables WHERE schemaname = 'public'", engine)
print("Tables yang ada:", tables['tablename'].tolist())

df_processed = pd.read_sql('education', engine)
df_processed.info()