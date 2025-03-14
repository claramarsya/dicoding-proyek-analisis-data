import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import calendar

# Load dataset
all_df = pd.read_csv("all_data.csv")

# Konversi kolom tanggal jika ada
if 'dteday' in all_df.columns:
    all_df['dteday'] = pd.to_datetime(all_df['dteday'])

# Tentukan rentang tanggal dari dataset
min_date = all_df['dteday'].min()
max_date = all_df['dteday'].max()

# Sidebar untuk filtering
date_range = st.sidebar.date_input("Pilih Rentang Waktu", [min_date, max_date], min_value=min_date, max_value=max_date)
season_filter = st.sidebar.multiselect("Pilih Musim", all_df['season'].unique())

# Filter data jika ada input dari user
filtered_df = all_df.copy()
if date_range and len(date_range) == 2:
    start_date, end_date = date_range
    filtered_df = filtered_df[(filtered_df['dteday'] >= pd.Timestamp(start_date)) & 
                              (filtered_df['dteday'] <= pd.Timestamp(end_date))]
if season_filter:
    filtered_df = filtered_df[filtered_df['season'].isin(season_filter)]

# Judul Dashboard
st.header("Dashboard Analisis Bike Sharing :sparkles:")
st.subheader('Statistik Penyewaan Sepeda')

# Menampilkan statistik data yang sudah difilter
col1, col2 = st.columns(2)

with col1:
    total_rentals = filtered_df["cnt"].sum()
    st.metric(label="Total Penyewaan", value=f"{total_rentals:,}")

with col2:
    avg_rentals = filtered_df["cnt"].mean()
    st.metric(label="Rata-rata Penyewaan per Hari", value=f"{avg_rentals:.2f}")

# Tren Penyewaan Sepeda
st.subheader("Tren Penyewaan Sepeda per Bulan")
day_df = filtered_df[filtered_df["source"] == "day"]
monthly_trend = day_df.groupby(['yr', 'mnth'])['cnt'].sum().reset_index()
monthly_trend['yr'] = monthly_trend['yr'].map({0: 2011, 1: 2012})
monthly_trend['mnth'] = monthly_trend['mnth'].apply(lambda x: calendar.month_abbr[x])
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(data=monthly_trend, x="mnth", y="cnt", hue="yr", marker="o", linewidth=2.5, ax=ax)
ax.set_title("Tren Penyewaan Sepeda per Bulan (2011 & 2012)")
ax.set_xlabel("Bulan")
ax.set_ylabel("Total Penyewaan Sepeda")
st.pyplot(fig)

# Waktu Paling Ramai dan Sepi
st.subheader("Waktu Paling Ramai dan Sepi dalam Sehari")
hourly_trend = filtered_df.groupby("hr")["cnt"].sum().reset_index()
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(x=hourly_trend["hr"], y=hourly_trend["cnt"], marker='o', color="#72BCD4", linewidth=2, ax=ax)
ax.set_title("Total Penyewaan Sepeda Berdasarkan Jam dalam Sehari")
ax.set_xlabel("Jam")
ax.set_ylabel("Total Penyewaan Sepeda")
plt.xticks(range(0, 24))
st.pyplot(fig)

# Pengaruh Faktor Cuaca terhadap Penyewaan Sepeda
st.subheader("Pengaruh Faktor Cuaca terhadap Penyewaan Sepeda")
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
sns.scatterplot(ax=axes[0], x=filtered_df["temp"], y=filtered_df["cnt"], alpha=0.5, color="#FF5733")
axes[0].set_title("Pengaruh Temperatur terhadap Penyewaan Sepeda")
axes[0].set_xlabel("Temp")
axes[0].set_ylabel("Jumlah Penyewaan Sepeda")
sns.scatterplot(ax=axes[1], x=filtered_df["hum"], y=filtered_df["cnt"], alpha=0.5, color="#3498DB")
axes[1].set_title("Pengaruh Kelembaban terhadap Penyewaan Sepeda")
axes[1].set_xlabel("Hum")
axes[1].set_ylabel("Jumlah Penyewaan Sepeda")
sns.scatterplot(ax=axes[2], x=filtered_df["windspeed"], y=filtered_df["cnt"], alpha=0.5, color="#2ECC71")
axes[2].set_title("Pengaruh Kecepatan Angin terhadap Penyewaan Sepeda")
axes[2].set_xlabel("Windspeed")
axes[2].set_ylabel("Jumlah Penyewaan Sepeda")
st.pyplot(fig)