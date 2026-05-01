import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Dashboard Analisis GLU", layout="wide")

# =========================
# HEADER
# =========================
st.markdown("""
<div style="background: linear-gradient(90deg,#00c6ff,#0072ff); padding:20px; border-radius:15px; color:white;">
<h2>📊 Analisis dan Visualisasi Data</h2>
<p>Nama Mahasiswa: ALSIAN OMAS</p>
<p>NIM: 050913872</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# =========================
# LOAD DATA OTOMATIS
# =========================
file_path = "Data Tugas Tuton STDA4101-2025.2.xlsx"

try:
    df = pd.read_excel(file_path)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
except:
    st.error("❌ File data_tuton.xlsx tidak ditemukan di folder project")
    st.stop()

# =========================
# CEK KOLOM
# =========================
glu_col = None
for col in df.columns:
    if col.strip().lower() == "glu":
        glu_col = col
        break

if glu_col is None:
    st.error("❌ Kolom GLU tidak ditemukan!")
    st.write("Kolom tersedia:", df.columns)
    st.stop()

# =========================
# AMBIL DATA GLU
# =========================
glu = pd.to_numeric(df[glu_col], errors='coerce').dropna()

if glu.empty:
    st.error("❌ Data GLU kosong atau tidak valid")
    st.stop()

# =========================
# KPI
# =========================
st.subheader("📊 Statistik Utama")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Mean", round(glu.mean(),2))
c2.metric("Median", round(glu.median(),2))
c3.metric("Std Dev", round(glu.std(),2))
c4.metric("Range", glu.max() - glu.min())

# =========================
# DISTRIBUSI
# =========================
st.subheader("📈 Distribusi")

skew = stats.skew(glu)
kurt = stats.kurtosis(glu)

colA, colB = st.columns(2)
colA.metric("Skewness", round(skew,4))
colB.metric("Kurtosis", round(kurt,4))

# =========================
# VISUAL
# =========================
col1, col2 = st.columns(2)

with col1:
    st.subheader("📦 Boxplot")
    fig1, ax1 = plt.subplots()
    sns.boxplot(x=glu, ax=ax1)
    st.pyplot(fig1)

with col2:
    st.subheader("📊 Histogram")
    fig2, ax2 = plt.subplots()
    sns.histplot(glu, kde=True, ax=ax2)
    st.pyplot(fig2)

# =========================
# KESIMPULAN ANALISIS DETAIL
# =========================
st.subheader("🧠 Kesimpulan Analisis")

mean = round(glu.mean(), 2)
median = round(glu.median(), 2)
mode = glu.mode()[0]
std = round(glu.std(), 2)
min_val = glu.min()
max_val = glu.max()

# Interpretasi skewness
if skew > 0:
    skew_text = "miring ke kanan (positif), yang menunjukkan bahwa terdapat beberapa nilai tinggi yang menarik distribusi ke arah kanan"
elif skew < 0:
    skew_text = "miring ke kiri (negatif), yang menunjukkan adanya nilai rendah yang menarik distribusi ke arah kiri"
else:
    skew_text = "simetris, yang menunjukkan distribusi data seimbang di sekitar rata-rata"

# Interpretasi kurtosis
if kurt > 0:
    kurt_text = "lebih runcing (leptokurtic), yang berarti data memiliki puncak yang tinggi dan kemungkinan terdapat outlier"
else:
    kurt_text = "lebih datar (platykurtic), yang menunjukkan data tersebar lebih merata tanpa puncak yang tajam"

st.success(f"""
Berdasarkan hasil analisis statistik deskriptif terhadap data kadar gula darah (GLU), diperoleh nilai rata-rata (mean) sebesar **{mean}**, median sebesar **{median}**, dan modus sebesar **{mode}**. 
Hal ini menunjukkan bahwa pusat distribusi data relatif berada di sekitar nilai tersebut, dengan kemungkinan distribusi yang cukup stabil.

Nilai standar deviasi sebesar **{std}** menunjukkan bahwa tingkat penyebaran data berada pada kategori sedang, artinya data tidak terlalu menyebar jauh dari rata-rata, namun tetap terdapat variasi antar pengamatan.
Nilai minimum yang tercatat adalah **{min_val}** dan maksimum **{max_val}**, yang menunjukkan rentang data yang cukup luas.

Berdasarkan nilai skewness, distribusi data bersifat **{skew_text}**. 
Sementara itu, nilai kurtosis menunjukkan bahwa distribusi data bersifat **{kurt_text}**.

📊 **Interpretasi Visualisasi Boxplot:**
Berdasarkan grafik boxplot, dapat diamati beberapa komponen penting:
- Garis di dalam kotak menunjukkan **median**, yaitu nilai tengah dari data.
- Batas bawah dan atas kotak menunjukkan **kuartil pertama (Q1)** dan **kuartil ketiga (Q3)**, yang mencakup 50% data utama.
- Panjang kotak mencerminkan **interquartile range (IQR)**, yaitu ukuran penyebaran data utama.
- Garis yang memanjang ke atas dan bawah (whisker) menunjukkan jangkauan data tanpa outlier.
- Titik-titik di luar whisker menunjukkan adanya **outlier**, yaitu nilai ekstrem yang jauh dari distribusi utama.

Jika terlihat adanya titik di luar whisker, maka dapat disimpulkan bahwa terdapat **data ekstrem** yang dapat mempengaruhi nilai rata-rata dan distribusi keseluruhan.

📌 **Kesimpulan Akhir:**
Secara keseluruhan, data kadar gula darah (GLU) menunjukkan distribusi yang cukup stabil dengan penyebaran moderat. 
Namun, adanya kemiringan distribusi dan kemungkinan outlier menunjukkan bahwa terdapat beberapa nilai yang menyimpang dari pola umum, sehingga perlu perhatian lebih lanjut dalam analisis atau pengambilan keputusan berbasis data ini.
""")

# =========================
# DATA
# =========================
st.subheader("📋 Data")

st.dataframe(df, use_container_width=True)

# =========================
# DOWNLOAD
# =========================
st.download_button(
    "⬇️ Download Data",
    df.to_csv(index=False),
    "data.csv"
)
