import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
hari = pd.read_csv("day.csv")
jam = pd.read_csv("hour.csv")

# Preprocessing hari.csv
hari['dteday'] = pd.to_datetime(hari['dteday'])
hari.drop(['instant', 'dteday', 'mnth', 'holiday', 'weekday', 'workingday', 'weathersit', 'temp', 'atemp', 'hum', 'windspeed', 'casual', 'registered'], axis=1, inplace=True)
hari.rename(columns={'yr': 'year', 'cnt': 'total'}, inplace=True)
hari.loc[hari['season'] == 1, 'season'] = 'Winter'
hari.loc[hari['season'] == 2, 'season'] = 'Spring'
hari.loc[hari['season'] == 3, 'season'] = 'Summer'
hari.loc[hari['season'] == 4, 'season'] = 'Fall'

# Preprocessing jam.csv
jam['dteday'] = pd.to_datetime(jam['dteday'])
jam.drop(['instant', 'dteday', 'season', 'yr', 'hr','holiday', 'weekday', 'weathersit', 'temp', 'atemp', 'hum', 'windspeed', 'casual', 'registered'], axis=1, inplace=True)
jam.rename(columns={'mnth': 'month', 'yr': 'year', 'cnt': 'total'}, inplace=True)

# Streamlit app layout
st.title("Dashboard Penyewaan Sepeda")

# Sidebar
st.sidebar.header("Pengaturan")
view_data = st.sidebar.checkbox("Lihat Data", False)

if view_data:
    st.subheader("Data Penyewaan Sepeda (hari)")
    st.write(hari.head())

    st.subheader("Data Penyewaan Sepeda (jam)")
    st.write(jam.head())

# Pengaruh musim per tahun
st.subheader('Pengaruh Musim per Tahun terhadap Jumlah Penyewaan Sepeda')
result_hari = hari.groupby(['year', 'season'])['total'].sum().reset_index()

plt.figure(figsize=(10, 6))
sns.barplot(data=result_hari, x='year', y='total', hue='season')
plt.title('Pengaruh Musim per Tahun terhadap Jumlah Penyewaan Sepeda')
plt.xlabel('Tahun')
plt.ylabel('Jumlah Penyewaan Sepeda')
plt.legend(title='Musim')
st.pyplot(plt)

# Penyewaan sepeda pada hari kerja vs hari libur
st.subheader('Total Penyewaan Sepeda pada Hari Kerja dan Hari Libur')
result_jam = jam.groupby(['month', 'workingday'])['total'].sum().reset_index()

plt.figure(figsize=(10, 6))
sns.barplot(data=result_jam, x='month', y='total', hue='workingday')
plt.title('Total Penyewaan Sepeda pada Hari Kerja dan Hari Libur')
plt.xlabel('Bulan')
plt.ylabel('Jumlah Penyewaan Sepeda')
plt.legend(title='Hari Kerja (1) vs Hari Libur (0)')
st.pyplot(plt)

# Visualisasi yang disimpan sebelumnya
st.subheader("Visualisasi yang Disimpan")
st.image("jumlah penyewa per musim.png", caption="Jumlah Penyewa Sepeda per Musim")
st.image("jumlah penyewa pada hari kerja.png", caption="Jumlah Penyewa Sepeda pada Hari Kerja dan Hari Libur")
