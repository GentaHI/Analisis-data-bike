import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
hour_df = pd.read_csv('edited_hour.csv', parse_dates=['date'])

# Set page title and description
st.set_page_config(page_title="Visualisasi Data Bike Sharing", page_icon=":bar_chart:", layout="wide")
st.title("Visualisasi Data Bike Sharing")
st.write("Dibuat dengan segenap hati.")

# Pertanyaan 1
st.subheader("Tingkat Peminjaman Sepeda 2011-2012")
monthly_bike_dl = hour_df.resample(rule='ME', on='date').agg({ # tidak menggunakan rule='M' karena rule untuk month end akan dingantikan dengan ME
    'casual': 'sum',
    'registered': 'sum',
    'total_users': 'sum'
})

total_users = monthly_bike_dl.total_users.sum()
st.metric("Total orders", value=total_users)
   
monthly_bike_dl.index = monthly_bike_dl.index.strftime('%b %Y')
monthly_bike_dl = monthly_bike_dl.reset_index()


fig, ax = plt.subplots(figsize=(16, 6))
ax.plot(
    monthly_bike_dl["date"],
    monthly_bike_dl["total_users"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=13)
ax.tick_params(axis='x', labelsize=13, rotation = 45) 
st.pyplot(fig)

# Pertanyaan 2
st.subheader("Rata - Rata peminjaman Sepeda")
fig, ax = plt.subplots(figsize=(19,6))
sns.pointplot(data=hour_df, x='hour', y='total_users', hue='weekday', ax=ax)

ax.set_title('Rata-rata Peminjaman Sepeda Setiap Jam', size=20)
ax.set_xlabel('Jam', size = 15)
ax.set_ylabel('Jumlah Peminjaman', size = 15)
ax.legend(title='Hari', loc='upper left')
st.pyplot(fig)

#Total peminjaman pengguna kasual setiap jamnya
fig, ax = plt.subplots(figsize=(19,6))
sns.pointplot(data=hour_df, x='hour', y='casual', hue='weekday', ax=ax)

ax.set_title('Rata-rata Peminjaman Sepeda User Kasual Setiap Jam', size=20)
ax.set_xlabel('Jam', size = 15)
ax.set_ylabel('Jumlah Peminjaman', size = 15)
ax.legend(title='Hari', loc='upper left')
st.pyplot(fig)

#Total peminjaman pengguna Teregistrasi setiap jamnya
fig, ax = plt.subplots(figsize=(19,6))
sns.pointplot(data=hour_df, x='hour', y='registered', hue='weekday', ax=ax)
#definisi nama
ax.set_title('Rata-rata Peminjaman Sepeda User Teregistrasi Setiap Jam', size=20)
ax.set_xlabel('Jam', size = 15)
ax.set_ylabel('Jumlah Peminjaman', size = 15)
ax.legend(title='Hari', loc='upper left')
st.pyplot(fig)

# pertanyaan 3
st.subheader("Rata - rata Peminjaman di hari libur dan hari kerja")
#Perbandingan barplot
fig, ax = plt.subplots(figsize=(10,5))
sns.barplot(data=hour_df, x='is_workingday', y='total_users',hue='is_workingday', legend=False, ax=ax)
#definisi nama
ax.set_title('Rata-rata Peminjaman Ketika Hari Kerja', size=20)
ax.set_ylabel(None)
ax.set_xlabel(None)
st.pyplot(fig)

# pertanyaan 4
fig, ax = plt.subplots(figsize=(14,6))
st.subheader("Rata - rata Peminjaman berdasarkan musim")
sns.barplot(data=hour_df, x='season', y='total_users', hue= 'suhu',
            palette=["#0368DB", "#49B6D7", "#98F5F9"], ax=ax)
st.pyplot(fig)
#definisi nama
ax.set_title('Rata-rata Peminjaman Sepeda Setiap Musim', size=20)
ax.set_ylabel("Jumlah Pengguna", size = 15)
ax.set_xlabel("Musim", size = 15)
ax.legend(title='Suhu', title_fontsize=15, loc='upper left', fontsize=14)
st.pyplot(fig)

# Display dataset
st.subheader("Dataset")
st.write(hour_df)
