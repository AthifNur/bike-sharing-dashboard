# dashboard.py (SUDAH DISESUAIKAN DENGAN main_data.csv KAMU)

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ==================================
# PAGE CONFIG
# ==================================
st.set_page_config(
    page_title="Bike Sharing Dashboard",
    page_icon="🚲",
    layout="wide"
)

# ==================================
# LOAD DATA
# ==================================
@st.cache_data
def load_data():
    path = os.path.join(os.path.dirname(__file__), "main_data.csv")
    df = pd.read_csv(path)
    return df

df = load_data()

# ==================================
# DATA PREP
# ==================================
# hanya ubah tahun
if df["yr"].max() == 1:
    df["yr"] = df["yr"].map({0: 2011, 1: 2012})

# ==================================
# SIDEBAR
# ==================================
st.sidebar.title("📌 Filter Dashboard")

selected_year = st.sidebar.multiselect(
    "Pilih Tahun",
    options=sorted(df["yr"].unique()),
    default=sorted(df["yr"].unique())
)

selected_season = st.sidebar.multiselect(
    "Pilih Musim",
    options=df["season"].unique(),
    default=df["season"].unique()
)

df_filtered = df[
    (df["yr"].isin(selected_year)) &
    (df["season"].isin(selected_season))
]

# ==================================
# HEADER
# ==================================
st.title("🚲 Bike Sharing Dashboard")
st.markdown("Analisis penyewaan sepeda berdasarkan musim, cuaca, dan tren waktu.")
st.caption("Dataset Bike Sharing Washington D.C (2011-2012)")
st.divider()

# ==================================
# KPI
# ==================================
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Rental", f"{df_filtered['cnt'].sum():,}")
col2.metric("Rata-rata Rental", f"{df_filtered['cnt'].mean():.0f}")
col3.metric("Max Rental", f"{df_filtered['cnt'].max():,}")
col4.metric("Jumlah Data", len(df_filtered))

st.divider()

# ==================================
# VISUALISASI 1
# ==================================
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Total Rental per Musim")

    season_data = df_filtered.groupby("season")["cnt"].sum().reset_index()

    fig1, ax1 = plt.subplots(figsize=(7,4))
    sns.barplot(data=season_data, x="season", y="cnt", palette="Set2", ax=ax1)
    ax1.set_xlabel("")
    ax1.set_ylabel("Total Rental")
    plt.tight_layout()
    st.pyplot(fig1)

with col2:
    st.subheader("📈 Trend Rental per Bulan")

    month_data = df_filtered.groupby("mnth")["cnt"].sum().reset_index()

    fig2, ax2 = plt.subplots(figsize=(7,4))
    sns.lineplot(data=month_data, x="mnth", y="cnt", marker="o", linewidth=3, ax=ax2)
    ax2.set_xlabel("Bulan")
    ax2.set_ylabel("Total Rental")
    plt.tight_layout()
    st.pyplot(fig2)

# ==================================
# VISUALISASI 2
# ==================================
col3, col4 = st.columns(2)

with col3:
    st.subheader("☁️ Rental Berdasarkan Cuaca")

    weather_data = df_filtered.groupby("humidity_category")["cnt"].mean().reset_index()

    fig3, ax3 = plt.subplots(figsize=(7,4))
    sns.barplot(data=weather_data, x="humidity_category", y="cnt", palette="coolwarm", ax=ax3)
    ax3.set_xlabel("")
    ax3.set_ylabel("Rata-rata Rental")
    plt.tight_layout()
    st.pyplot(fig3)

with col4:
    st.subheader("👥 Casual vs Registered")

    total_casual = df_filtered["casual"].sum()
    total_registered = df_filtered["registered"].sum()

    fig4, ax4 = plt.subplots(figsize=(7,4))
    ax4.pie(
        [total_casual, total_registered],
        labels=["Casual", "Registered"],
        autopct="%1.1f%%",
        startangle=90
    )
    plt.tight_layout()
    st.pyplot(fig4)

# ==================================
# DATA TABLE
# ==================================
st.subheader("📄 Preview Dataset")
st.dataframe(df_filtered, use_container_width=True)

# ==================================
# INSIGHT
# ==================================
st.subheader("💡 Insight")

st.success("""
✔ Musim Fall memiliki jumlah rental tertinggi.  
✔ Penyewaan meningkat di pertengahan tahun.  
✔ User Registered mendominasi penggunaan sepeda.  
✔ Kondisi kelembaban memengaruhi jumlah rental.
""")

# ==================================
# RECOMMENDATION
# ==================================
st.subheader("🎯 Recommendation")

st.info("""
1. Tambah unit sepeda saat musim ramai.  
2. Berikan promo di musim sepi.  
3. Fokus ubah casual user menjadi member.  
4. Optimalkan stok saat peak season.
""")

# ==================================
# FOOTER
# ==================================
st.markdown("---")
st.caption("Data Analysis Submission")