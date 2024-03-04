import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import plotly.graph_objects as go
import time

df_day = pd.read_csv("day_after.csv")
df_hour = pd.read_csv("hour_after.csv")

# Fungsi untuk menampilkan animasi selamat datang
def welcome_animation():
    st.image("https://storage.googleapis.com/flip-prod-mktg-strapi/media-library/sepeda_listrik_b94ecd50ea/sepeda_listrik_b94ecd50ea.jpg", use_column_width=True)
    st.write("Ini Adalah Dashboard Project Dicoding")
    st.write("Please wait...")
    progress_bar = st.progress(0)
    for i in range(100):
        time.sleep(0.001)
        progress_bar.progress(i + 1)

welcome_animation()

#Judul
st.title("Imam Nur Rizky Gusman Dashboard")

st.header("Analisis Bike Sharing Dataset")
st.write("""
Dataset ini berisi informasi tentang penyewaan sepeda berbagi yang dilakukan oleh pengguna dalam periode waktu tertentu. 
Dalam analisis ini, kita akan mengeksplorasi data untuk mendapatkan wawasan yang berguna.
""")

col1, col2 = st.columns(2)
with col1:
    st.header("Data Frame dari day.csv")
    st.write(df_day)

with col2:
    st.header("Data Frame dari hour.csv")
    st.write(df_hour)

#Pertanyaan Bisnis
st.markdown("""
### Pertanyaan Bisnis
- **Pada pukul berapa persewaan sepeda mengalami puncak tertinggi dan terendah?**
- **Apa musim dengan jumlah sewa sepeda tertinggi dan terendah?**
- **Berapa banyak pelanggan biasa dan pelanggan terdaftar? Bagaimana berbandingan keduanya?**
- **Manakah sewa yang lebih tinggi antara weekday dan weekend?**
- **Bagaimana hubungan rata-rata sewa dengan cuaca?**
""")

# Data1
one_df = df_hour.groupby(by="hours").agg({"count_cr": ["sum"]}).reset_index()
# Barchart with Plotly
fig = go.Figure()

# dataframe ke barchart
for i in range(len(one_df)):
    df_slice = one_df.iloc[:i+1]
    fig.add_trace(go.Bar(
        x=df_slice['hours'],
        y=df_slice[('count_cr', 'sum')],
        name='Total Sewa',
        marker_color='skyblue'
    ))

# tampilan layout
fig.update_layout(
    title='Jumlah Sewa Berdasarkan Waktu/jam',
    xaxis_title='Hours',
    yaxis_title='Jumlah Sewa',
    showlegend=False
)
st.plotly_chart(fig)
#komen
st.markdown("Waktu dengan jumlah sewa tertinggi adalah pada pukul 17.00 dengan jumlah sewa sebanyak 336,860 unit, sementara waktu dengan jumlah sewa terendah adalah pada pukul 04.00 dengan jumlah sewa sebanyak 4,428 unit.")

# Data2
two_df = df_hour.groupby(by="season", observed=False).count_cr.sum().sort_values(ascending=False).reset_index()

# barchart with Plotly
fig = go.Figure()

# dataframe ke barchart
for i in range(len(two_df)):
    df_slice = two_df.iloc[:i+1]
    fig.add_trace(go.Bar(
        x=df_slice['season'],
        y=df_slice['count_cr'],
        marker_color=['skyblue', 'lightgreen', 'salmon', 'orange'],
        name='Total Sewa'
    ))

# tampilan layout
fig.update_layout(
    title='Sewa Berdasarkan Musim',
    xaxis_title='Season',
    yaxis_title='count_cr/1000000',
    showlegend=False
)
st.plotly_chart(fig)
st.markdown("Diantara empat musim yang terjadi, musim gugur memiliki sewa yang tertinggi diikuti dengan musim panas, musim dingin, dan sewa terendah ada pada musim semi.")

# Data3
yearly_data = df_day.groupby(by="year").agg({"registered": "sum", "casual": "sum"})

# data for pie chart
sizes = yearly_data.sum()
labels = ['Registered', 'Casual']
colors = ['#FFA500', '#FFD700']  # Warna orange: orange dan gold
explode = (0.1, 0)

# list dataframes setiap frame
frames = []
for i in range(len(yearly_data)):
    year_data = yearly_data.iloc[:i+1]
    values = [year_data['registered'].iloc[-1], year_data['casual'].iloc[-1]]
    frames.append(go.Frame(data=[go.Pie(labels=labels, values=values, pull=[0.1, 0], marker=dict(colors=colors))]))

# pie chart withPlotly
fig = go.Figure(
    data=[go.Pie(labels=labels, values=sizes, pull=[0.1, 0], marker=dict(colors=colors))],
    layout=go.Layout(title='Persentase Sewa Berdasarkan Tahun')
)

# tampilan layout
fig.update_layout(
    updatemenus=[dict(
        type='buttons',
        showactive=False,
        buttons=[dict(label='Play', method='animate', args=[None, dict(frame=dict(duration=500, redraw=True), fromcurrent=True)])]
    )],
    showlegend=False
)
# animasi 
fig.frames = frames

st.plotly_chart(fig)
st.markdown("Jumlah total pengguna terdaftar sebesar 81.2% dan pengguna biasa sebesar 18.8%.")

# Data4
four_df = df_day.groupby('weekday_type', observed=False)['count_cr'].mean().reset_index().sort_values("count_cr")

# barchart with Plotly
fig = go.Figure()

# frame to barchart
for i in range(len(four_df)):
    df_slice = four_df.iloc[:i+1]
    fig.add_trace(go.Bar(
        x=df_slice['weekday_type'],
        y=df_slice['count_cr'],
        marker_color='skyblue'
    ))

# tampilan layout
fig.update_layout(
    title='Rata-rata Sewa Berdasarkan Tipe Hari',
    xaxis_title='Tipe Hari',
    yaxis_title='Rata-rata Sewa',
    showlegend=False
)
st.plotly_chart(fig)
st.markdown("Rata-rata sewa pada weekday cenderung lebih tinggi dibanding sewa pada weekend, tetapi perbedaan tersebut tidak signifikan.")

# Data5
five_df = df_hour.groupby('weather_situation', observed=False)['count_cr'].sum().reset_index().sort_values("count_cr")

# barchart with Plotly
fig = go.Figure()

# frame to barchart
for i in range(len(five_df)):
    df_slice = five_df.iloc[:i+1]
    fig.add_trace(go.Bar(
        x=df_slice['weather_situation'],
        y=df_slice['count_cr'],
        marker_color='skyblue'
    ))

# tampilan layout
fig.update_layout(
    title='Total Sewa Berdasarkan Situasi Cuaca',
    xaxis_title='Situasi Cuaca',
    yaxis_title='Total Sewa',
    showlegend=False
)
st.plotly_chart(fig)
st.markdown("Kecenderungan hubungan antara rata-rata sewa dengan cuaca dapat lebih terlihat secara logika dengan perbandingan jumlah rata-rata sewanya, semakin ekstrim cuaca, maka sewa cenderung semakin rendah.")

# clustering analysis
clustering_result = df_hour.groupby(by="weather_situation", observed=False).count_cr.nunique().sort_values(ascending=False)

# correlation
correlation_day = df_day['weathersit'].corr(df_day['count_cr'])
correlation_hour = df_hour['weathersit'].corr(df_hour['count_cr'])

# Show
st.header("Hasil Clustering Analysis dan Analisis Korelasi")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Hasil Clustering Analysis")
    st.write(clustering_result)

with col2:
    st.subheader("Analisis Korelasi")
    st.write("Rumus korelasi: $r = \\frac{\\sum (X_i - \\bar{X})(Y_i - \\bar{Y})}{\\sqrt{\\sum (X_i - \\bar{X})^2} \\sqrt{\\sum (Y_i - \\bar{Y})^2}}$")
    st.write("Korelasi data harian:", correlation_day)
    st.write("Korelasi data per-jam:", correlation_hour)
