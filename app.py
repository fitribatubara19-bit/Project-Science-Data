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
# KESIMPULAN
# =========================
st.subheader("🧠 Kesimpulan")

if skew > 0:
    skew_text = "miring ke kanan (positif)"
elif skew < 0:
    skew_text = "miring ke kiri (negatif)"
else:
    skew_text = "simetris"

if kurt > 0:
    kurt_text = "lebih runcing (leptokurtic)"
else:
    kurt_text = "lebih datar (platykurtic)"

st.success(f"""
 Berdasarkan hasil analisis, data kadar gula darah (GLU) memiliki rata-rata sebesar **{mean}**, median **{median}**, dan modus **{mode}**, yang menunjukkan bahwa pusat data relatif stabil.
 Nilai standar deviasi sebesar **{std}** menunjukkan bahwa tingkat penyebaran data tergolong sedang.
 Dari visualisasi boxplot, terlihat adanya kemungkinan **outlier**, yang menunjukkan adanya nilai ekstrem.
 Distribusi data bersifat **{skew_text}**, dan berdasarkan kurtosis, distribusi bersifat **{kurt_text}**.
 Secara keseluruhan, data GLU memiliki distribusi yang cukup stabil dengan sedikit penyimpangan pada nilai tertentu.""")

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
