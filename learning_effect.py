import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
from sympy import symbols, integrate
import streamlit as st

# Fungsi pengaruh waktu belajar terhadap IPK
def learning_effect(t):
    return 0.05 * t ** 2 - 0.3 * t + 2

# Fungsi untuk menghitung integral tentu
def calculate_integral(start_time, end_time):
    total_effect, _ = quad(learning_effect, start_time, end_time)
    return total_effect

# Fungsi untuk menghitung integral tak tentu
def calculate_indefinite_integral():
    t = symbols('t')
    f_t = 0.05 * t**2 - 0.3 * t + 2
    F_t = integrate(f_t, t)
    return F_t

# Mulai aplikasi Streamlit

st.write('''<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">

<style>

    body {

        font-family: 'Roboto', sans-serif;

    }

    .reportview-container {

        background: #f0f2f6;

    }

    .stButton>button {

        background-color: #FF4B4B;

        color: white;

        border-radius: 10px;

        padding: 10px;

        font-size: 16px;

    }

    .stTextInput>div>input {

        border: 2px solid #FF4B4B;

        border-radius: 5px;

    }

    .stMarkdown {

        font-size: 18px;

        color: #333;

    }

    .stDataFrame {

        border: 1px solid #FF4B4B;

        border-radius: 5px;

    }

</style>''', unsafe_allow_html=True)

# Mulai aplikasi Streamlit
st.title("Analisis Pengaruh Waktu Belajar terhadap IPK")
st.markdown("Aplikasi ini membaca data waktu belajar dari file Excel atau input manual, menghitung pengaruh waktu belajar terhadap IPK menggunakan integral, dan menampilkan hasilnya secara visual.")

# Pilihan input data
input_option = st.radio("Pilih metode input data:", ("Upload File Excel", "Input Manual"))

data = pd.DataFrame()

if input_option == "Upload File Excel":
    # Upload file
    uploaded_file = st.file_uploader("Unggah file Excel dengan kolom 'Waktu Belajar' dan 'IPK'", type=["xlsx"])

    if uploaded_file:
        # Baca data
        data = pd.read_excel(uploaded_file)
        
        # Validasi kolom
        if "Waktu Belajar" not in data.columns or "IPK" not in data.columns:
            st.error("Kolom 'Waktu Belajar' atau 'IPK' tidak ditemukan dalam file.")
        else:
            st.subheader("Data Waktu Belajar dan IPK")
            st.dataframe(data)

elif input_option == "Input Manual":
    st.subheader("Input Data Waktu Belajar dan IPK")
    num_samples = st.number_input("Jumlah sampel mahasiswa yang akan diinput:", min_value=1, value=5, step=1)

    manual_data = []
    for i in range(num_samples):
        col1, col2 = st.columns(2)
        with col1:
            time = st.number_input(f"Waktu belajar (jam) - Mahasiswa {i+1}", min_value=0.0, step=0.5, key=f"time_{i}")
        with col2:
            ipk = st.number_input(f"IPK - Mahasiswa {i+1}", min_value=0.0, max_value=4.0, step=0.01, key=f"ipk_{i}")
        manual_data.append({"Waktu Belajar": time, "IPK": ipk})

    data = pd.DataFrame(manual_data)
    st.subheader("Data Waktu Belajar dan IPK")
    st.dataframe(data)

if not data.empty:
    # Batas waktu belajar
    start_time = data["Waktu Belajar"].min()
    end_time = data["Waktu Belajar"].max()
    
    # Hitung integral
    total_effect = calculate_integral(start_time, end_time)
    indefinite_integral = calculate_indefinite_integral()

    # Tampilkan hasil analisis dalam format rumus
    st.subheader("Hasil Analisis")
    st.markdown("### Batas Waktu Belajar")
    st.latex(f"a = {start_time}, \\ b = {end_time}")

    st.markdown("### Total Pengaruh Waktu Belajar terhadap IPK (Integral Tentu)")
    st.latex(r"IPK = \int_{a}^{b} \left( 0.05t^2 - 0.3t + 2 \right) \, dt")
    st.latex(f"IPK = {total_effect:.2f}")

    st.markdown("### Model Matematis Hubungan Waktu Belajar terhadap IPK (Integral Tak Tentu)")
    st.latex(r"F(t) = \int \left( 0.05t^2 - 0.3t + 2 \right) \, dt")
    st.latex(f"F(t) = {indefinite_integral} + C")

    # Visualisasi
    st.subheader("Visualisasi Hubungan Waktu Belajar dan IPK")
    fig, ax = plt.subplots(figsize=(12, 6))

    # Plot data aktual
    ax.scatter(data["Waktu Belajar"], data["IPK"], color='red', label="Data Aktual")

    # Plot fungsi model
    time_values = np.linspace(start_time, end_time, 100)
    effect_values = learning_effect(time_values)
    ax.plot(time_values, effect_values, label="Model Fungsi Pengaruh", color="blue")

    # Tambahkan area integral
    ax.fill_between(time_values, 0, effect_values, alpha=0.2, label="Area (Integral Tentu)", color="cyan")

    ax.set_title("Pengaruh Waktu Belajar terhadap IPK")
    ax.set_xlabel("Waktu Belajar (jam)")
    ax.set_ylabel("IPK")
    ax.legend()
    ax.grid(True)

    # Tampilkan grafik
    st.pyplot(fig)

# Tambahkan bagian kredit pemilik aplikasi
st.markdown("---")  # Garis pemisah
st.subheader("Author dan Publisher")
st.write("Aplikasi ini dibuat oleh:")
st.write("- Zain Ahmad Fahrezi")
st.write("- Sayyida Naila Alia")
st.write("- Nyimas Nayla Deswitha")
st.write("- Septa Ayu Kirana")
st.write("- Sindi Aprianti")
st.write("Fakultas Ilmu Komputer dan Sains")
st.write("Universitas Indo Global Mandiri")
st.image("uigm.png", caption="Universitas Indo Global Mandiri", width=150)
