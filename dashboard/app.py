import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

def date_range_for_df(start_date_range, end_date_range):
    df_output = bike_df[(bike_df["date"] >= str(start_date_range)) & 
                    (bike_df["date"] <= str(end_date_range))]
    return df_output

def borrowed_bike_day_df(df_input):
    # tidak menggunakan rule='M' karena rule untuk month end akan dingantikan dengan ME
    df_output = df_input.resample(rule='D', on='date').agg({ 
     'casual': 'sum',
     'registered': 'sum',
     'total_users': 'sum'
    })
    df_output = df_output.reset_index()
    return df_output

def overall_borrowed_bike_plot(df_input, set_x, mark, set_color, set_label):
    fig, ax = plt.subplots(figsize=(16, 6))
    date_format = mdates.DateFormatter('%d %b %Y')
    plt.gca().xaxis.set_major_formatter(date_format)
    ax.plot(df_input["date"], 
            df_input[set_x], 
            marker= mark, 
            linewidth=2, 
            color = set_color, 
            label=set_label
    )
    ax.tick_params(axis='y', labelsize=13)
    ax.tick_params(axis='x', labelsize=13, rotation = 45) 
    ax.legend(fontsize=15, loc="upper left")
    st.pyplot(fig)

def weather_status_plot(input_df, y_axis, title_str):
    # perbandingan barplot total user berdasarkan musim, dimana setiap musim dibagi sesuai dengan kategori suhu
    fig, ax = plt.subplots(figsize=(14,6))
    sns.barplot(data=input_df, x='season', y=y_axis, hue= 'suhu',
                palette=["#2166ac", "#f4a582", "#d6604d"], ax=ax)
    #definisi nama
    ax.set_title(title_str, size=20)
    ax.set_ylabel("Jumlah User", size = 15)
    ax.legend(title='Suhu', title_fontsize=15, loc='upper left', fontsize=14)
    st.pyplot(fig)

def day_status_info(input_df):
    processed_df = input_df.groupby('day_status')[[
        'casual', 
        'registered', 
        "total_users"
        ]].mean().reset_index()

    # Persiapan
    status_arr = processed_df['day_status']
    casual_arr = processed_df['casual']
    registered_arr = processed_df['registered']
    total_arr = processed_df['total_users']
    x_axis_len = np.arange(len(status_arr))
    return status_arr, casual_arr, registered_arr, total_arr, x_axis_len

def hours_bike_subplot(input_df, y_axis, title_input):
    fig, ax = plt.subplots(figsize=(19,6))
    sns.pointplot(data=input_df, 
                  x='hour', 
                  y= y_axis, 
                  hue='weekday', 
                  ax=ax)
    ax.set_title(title_input, size=20)
    ax.set_xlabel('Jam', size = 15)
    ax.set_ylabel('Jumlah Peminjaman', size = 15)
    ax.legend(fontsize=14, title='Hari', loc='upper left')
    st.pyplot(fig)

sns.set_theme(style="whitegrid", palette="bright")

# Load data
csv_url = "https://raw.githubusercontent.com/GentaHI/Analisis-data-bike/refs/heads/main/dashboard/edited_hour.csv"
bike_df = pd.read_csv(csv_url, parse_dates=['date'])

# Mengurut Ulang
bike_df.sort_values(by="borrow_id", inplace=True)
bike_df.reset_index(inplace=True)

# Definisi format pada kolom date menjadi pandas datetime 
bike_df["date"] = pd.to_datetime(bike_df['date'])

# Menggunakan widget tanggal sebagai interaktif dinamisnya
# dimana date terlama hingga terbaru nya merupakan batas tanggal yang akan ditampilkan
min_date = bike_df["date"].min()
max_date = bike_df["date"].max()

# Set page title and description 
st.set_page_config(page_title="Visualisasi Data Bike Sharing", page_icon=":bar_chart:", layout="wide")
st.title("Visualisasi Data Bike Sharing")

with st.sidebar:
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Tanggal Waktu Peminjaman',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    # Mengguakan input start_date dan end_date untuk memfilter DataFrame
    main_df = date_range_for_df(start_date, end_date)
    date_counter = str(start_date.strftime("%d %B %Y")) + " Hingga " + str(end_date.strftime("%d %B %Y"))

    # Berdasarkan Tahun saja
    column_1_button, column_2_button = st.columns(2)
    st.write("Rentang Tahun")
    if st.button('Selama tahun 2011'):
        main_df = date_range_for_df(
            start_date_range="2011-01-01", 
            end_date_range= "2011-12-31"
            )
        date_counter = "Tahun 2011"

    if st.button('Selama tahun 2012'):
        main_df = date_range_for_df(
            start_date_range="2012-01-01",
            end_date_range="2012-12-31"
        )
        date_counter = "Tahun 2012"

    if st.button('Selama 2011-2012'):
        main_df = date_range_for_df(
            start_date_range="2011-01-01", 
            end_date_range="2012-12-31"
        )
        date_counter = "Tahun 2011-2012"

# Modifikasi DataFrame
daily_bike_df = borrowed_bike_day_df(main_df)

# Pertanyaan 1
st.subheader("Tingkat Peminjaman Selama " + date_counter)
column_metric_1, column_metric_2, column_metric_3 = st.columns(3)

with column_metric_1:
    casual_users = str("{:,.0f}".format(daily_bike_df.casual.sum()).replace(',','.')) + " Unit"
    st.metric("Peminjam User Umum", value=casual_users, border=True)

with column_metric_2:
    registered_users = str("{:,.0f}".format(daily_bike_df.registered.sum()).replace(',','.')) + " Unit"
    st.metric("Peminjam User Teregistrasi", value=registered_users, border=True)

with column_metric_3:
    total_users = str("{:,.0f}".format(daily_bike_df.total_users.sum()).replace(',','.')) + " Unit"
    st.metric("Total Peminjaman", value=total_users, border=True)

# Menampilkan Plot
tab_date_freq_1, tab_date_freq_2, tab_date_freq_3, tab_date_freq_4 = st.tabs([
    "Perbandingan",
    "Total User",
    "User Umum",
    "user Terintegrasi"
])
# Dipisah menjadi 4 tab
with tab_date_freq_1:
    fig, ax = plt.subplots(figsize=(16, 6))
    date_format = mdates.DateFormatter('%d %b %Y')
    plt.gca().xaxis.set_major_formatter(date_format)
    ax.plot(
        daily_bike_df["date"], 
        daily_bike_df["total_users"], 
        marker='P', 
        linewidth=2, 
        color="#1710C8", 
        label='Total User'
    )
    ax.plot(
        daily_bike_df['date'], 
        daily_bike_df['casual'], 
        marker='o', 
        linewidth=2, 
        color="#94F36E", 
        label='User Umum'
    )
    ax.plot(
        daily_bike_df['date'], 
        daily_bike_df['registered'], 
        marker='s', 
        linewidth=2, 
        color="#F45252", 
        label='User Teregistrasi'
    )
    ax.tick_params(axis='y', labelsize=13)
    ax.tick_params(axis='x', labelsize=13, rotation = 45) 
    ax.legend(fontsize=15, loc="upper left")
    st.pyplot(fig)
with tab_date_freq_2:
    overall_borrowed_bike_plot(daily_bike_df, "total_users", "P", "#1710C8", "Total User")
with tab_date_freq_3:
    overall_borrowed_bike_plot(daily_bike_df, "casual", "o", "#94F36E", "User Umum")
with tab_date_freq_4:
    overall_borrowed_bike_plot(daily_bike_df, "registered", "s", "#F45252", "User Teregistrasi")

# Pertanyaan 2
st.subheader("Frekuensi Peminjaman berdasarkan Jam")
tab_freq_1, tab_freq_2, tab_freq_3 = st.tabs(["Total User Seluruhnya", "User Umum", "User Teregistrasi"])

with tab_freq_1:
    hours_bike_subplot(main_df, "total_users", "Total Peminjaman Sepeda Setiap Jam")
    hours_bike_subplot(main_df, "total_users", "Rata-rata Peminjaman Sepeda Setiap Jam")

with tab_freq_2:
    hours_bike_subplot(main_df, "casual", "Total Peminjaman Sepeda oleh User Umum Setiap Jam")
    hours_bike_subplot(main_df, "casual", "Rata-rata Peminjaman Sepeda oleh User Umum Setiap Jam")

with tab_freq_3:
    hours_bike_subplot(main_df, "registered", "Total Peminjaman Sepeda oleh User Teregistrasi Setiap Jam")
    hours_bike_subplot(main_df, "registered", "Rata-rata Peminjaman Sepeda oleh User Teregistrasi Setiap Jam")
    
# pertanyaan 3
st.subheader("Perbandingan Peminjam ketika Hari Libur dan Kerja")
statuses, casual, registered, total, x = day_status_info(main_df)
# Wrap x-axis label
wrapped_labels = [label.replace(' & ', '\n& ') for label in statuses]

# figure & sublot
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), sharey=True)

# subplot Kiri: Stacked bar
ax1.bar(x, casual, label='User Umum', color='#49B6D7')
ax1.bar(x, registered, bottom=casual, label='User Teregistrasi', color='#0368DB')
ax1.set_title('Komposisi Rata-Rata User per Kategori Hari')
ax1.set_ylabel('Rata-rata User')
ax1.legend()
ax1.set_xticks(x)
ax1.set_xticklabels(wrapped_labels)

# Subplot kanan: Total users
ax2.bar(x, total, color='#98F5F9')
ax2.set_title('Rata-Rata Total User per Kategori Hari')
ax2.set_ylabel('Rata-Rata Total User')
ax2.set_xticks(x)
ax2.set_xticklabels(wrapped_labels)

plt.tight_layout()

st.pyplot(fig)

# pertanyaan 4
st.subheader("Perbandingan Peminjaman Sepeda Terhadap Musim")
tab_season_1, tab_season_2, tab_season_3 = st.tabs(["Total User Seluruhnya", "User Umum", "User Teregistrasi"])

with tab_season_1:
    weather_status_plot(main_df, "total_users", "Rata-rata Total Peminjaman Sepeda Setiap Musim")

with tab_season_2:
    weather_status_plot(main_df, "casual", "Rata-rata Peminjaman Sepeda oleh User Umum Setiap Musim")

with tab_season_3:
    weather_status_plot(main_df, "registered", "Rata-rata Peminjaman Sepeda oleh User Teregistrasi Setiap Musim")