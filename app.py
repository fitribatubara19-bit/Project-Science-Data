import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# =========================
# 🎨 CONFIG & STYLE
# =========================
st.set_page_config(page_title="Dashboard Analisis dan Visualisasi Data GLU", layout="wide")

st.markdown("""
<style>
.header-box {
    background: linear-gradient(90deg, #00c6ff, #0072ff);
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 20px;
    color: white;
}
.header-title {
    font-size: 32px;
    font-weight: bold;
}
.header-sub {
    font-size: 16px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header-box">
    <div class="header-title">📊 Analisis dan Visualisasi Data</div>
    <div class="header-sub">Nama Mahasiswa: ALSIAN OMAS</div>
    <div class="header-sub">NIM: 050913872</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<style>
.title {
    font-size:36px;
    font-weight:700;
    color:#1f4e79;
}
.subtitle {
    font-size:16px;
    color:gray;
}
.kpi {
    background:#f5f7fa;
    padding:15px;
    border-radius:12px;
    text-align:center;
    box-shadow: 2px 2px 8px rgba(0,0,0,0.05);
}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="title">📊 Dashboard Analisis GLU</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Statistik Deskriptif & Visualisasi Data Kadar Gula Darah</p>', unsafe_allow_html=True)

# =========================
# 📂 SIDEBAR
# =========================
st.sidebar.header("⚙️ Pengaturan")
file = st.sidebar.file_uploader("Upload File Excel", type=["xlsx"])

# =========================
# 📊 MAIN
# =========================
if file:

    df = pd.read_excel(file)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    # Cari kolom GLU
    glu_col = None
    for col in df.columns:
        if col.strip().lower() == "glu":
            glu_col = col

    if glu_col:

        glu = pd.to_numeric(df[glu_col], errors='coerce').dropna()

        # =========================
        # 📌 KPI
        # =========================
        st.subheader("📌 Statistik Utama")

        c1, c2, c3, c4 = st.columns(4)

        c1.markdown(f'<div class="kpi">Mean<br><b>{round(glu.mean(),2)}</b></div>', unsafe_allow_html=True)
        c2.markdown(f'<div class="kpi">Median<br><b>{round(glu.median(),2)}</b></div>', unsafe_allow_html=True)
        c3.markdown(f'<div class="kpi">Std Dev<br><b>{round(glu.std(),2)}</b></div>', unsafe_allow_html=True)
        c4.markdown(f'<div class="kpi">Range<br><b>{glu.max()-glu.min()}</b></div>', unsafe_allow_html=True)

        # =========================
        # 📈 DISTRIBUSI
        # =========================
        st.subheader("📈 Distribusi")

        skew = stats.skew(glu)
        kurt = stats.kurtosis(glu)

        colA, colB = st.columns(2)
        colA.metric("Skewness", round(skew,4))
        colB.metric("Kurtosis", round(kurt,4))

        # =========================
        # 📊 VISUALISASI
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
        # 🧠 KESIMPULAN OTOMATIS
        # =========================
        st.subheader("🧠 Kesimpulan Analisis")

        # Interpretasi otomatis
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

        mean = round(glu.mean(),2)
        median = round(glu.median(),2)
        mode = glu.mode()[0]
        std = round(glu.std(),2)

        st.success(f"""
        Berdasarkan hasil analisis, data kadar gula darah (GLU) memiliki rata-rata sebesar **{mean}**, 
        median **{median}**, dan modus **{mode}**, yang menunjukkan bahwa pusat data relatif stabil.
        Nilai standar deviasi sebesar **{std}** menunjukkan bahwa tingkat penyebaran data tergolong sedang.
        Dari visualisasi boxplot, terlihat adanya kemungkinan **outlier**, yang menunjukkan adanya nilai ekstrem.
        Distribusi data bersifat **{skew_text}**, dan berdasarkan kurtosis, distribusi bersifat **{kurt_text}**.
        Secara keseluruhan, data GLU memiliki distribusi yang cukup stabil dengan sedikit penyimpangan pada nilai tertentu.
        """)

        # =========================
        # 🔍 DATA
        # =========================
        st.subheader("🔍 Data")
        st.dataframe(df)

    else:
        st.error("Kolom GLU tidak ditemukan!")

else:
    st.info("⬅️ Silakan upload file Excel di sidebar")