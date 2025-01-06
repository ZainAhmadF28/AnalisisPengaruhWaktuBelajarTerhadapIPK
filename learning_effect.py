import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
from sympy import symbols, integrate
import streamlit as st

# Fungsi pengaruh waktu belajar terhadap IPK dengan batasan logistik
def learning_effect(t):
    k = 0.5  # Parameter logistik
    t0 = 10  # Titik tengah logistik
    return 4 / (1 + np.exp(-k * (t - t0)))

# Fungsi untuk menghitung integral tentu
def calculate_integral(start_time, end_time):
    if start_time < 0 or end_time < 0:
        return "Waktu belajar tidak boleh negatif."
    if start_time > end_time:
        return "Batas awal tidak boleh lebih besar dari batas akhir."

    total_effect, _ = quad(learning_effect, start_time, end_time)
    return total_effect

# Fungsi untuk menghitung integral tak tentu
def calculate_indefinite_integral():
    t = symbols('t')
    k = 0.5
    t0 = 10
    f_t = 4 / (1 + symbols('e')**(-k * (t - t0)))
    F_t = integrate(f_t, t)
    return F_t

# Mulai aplikasi Streamlit
st.title("Analisis Pengaruh Waktu Belajar terhadap IPK")
st.markdown("Aplikasi ini membaca data waktu belajar dari file Excel atau input manual, menghitung pengaruh waktu belajar terhadap IPK menggunakan integral, dan menampilkan hasilnya secara visual.")

# Pilihan input data
input_option = st.radio("Pilih metode input data:", ("Upload File Excel", "Input Manual"))

data = pd.DataFrame()

if input_option == "Upload File Excel":
    # Upload file
    uploaded_file = st.file_uploader("Unggah file Excel dengan kolom 'Waktu Belajar', dan 'IPK'", type=["xlsx"])

    if uploaded_file:
        try:
            data = pd.read_excel(
                uploaded_file,
                dtype={"NPM": str, "Angkatan": str}
            )
        except ValueError:
            st.error("Terjadi kesalahan saat membaca file. Pastikan file memiliki format yang benar.")
            st.stop()

        if 'Angkatan' in data.columns:
            data['Angkatan'] = data['Angkatan'].astype(str)
        
        required_columns = ["Waktu Belajar", "IPK"]
        if not all(col in data.columns for col in required_columns):
            st.error("File tidak memiliki semua kolom yang dibutuhkan: 'Nama', 'NPM', 'Prodi', 'Waktu Belajar', dan 'IPK'.")
        else:
            st.subheader("Data Waktu Belajar dan IPK")
            st.dataframe(data)

elif input_option == "Input Manual":
    st.subheader("Input Data Waktu Belajar dan IPK")
    num_samples = st.number_input("Jumlah sampel mahasiswa yang akan diinput:", min_value=1, value=5, step=1)

    manual_data = []
    for i in range(num_samples):
        st.markdown(f"### Data Mahasiswa {i+1}")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            name = st.text_input(f"Nama - Mahasiswa {i+1}", key=f"name_{i}")
        with col2:
            npm = st.text_input(f"NPM - Mahasiswa {i+1}", key=f"npm_{i}")
        with col3:
            prodi = st.text_input(f"Prodi - Mahasiswa {i+1}", key=f"prodi_{i}")
        with col4:
            university = st.text_input(f"Universitas - Mahasiswa {i+1}", key=f"univ_{i}")

        col5, col6 = st.columns(2)
        with col5:
            time = st.number_input(f"Waktu belajar (jam) - Mahasiswa {i+1}", min_value=0.0, step=0.5, key=f"time_{i}")
        with col6:
            ipk = st.number_input(f"IPK - Mahasiswa {i+1}", min_value=0.0, max_value=4.0, step=0.01, key=f"ipk_{i}")
        
        manual_data.append({"Nama": name, "NPM": npm, "Prodi": prodi, "Universitas": university, "Waktu Belajar": time, "IPK": ipk})

    data = pd.DataFrame(manual_data)
    st.subheader("Data Waktu Belajar dan IPK")
    st.dataframe(data)

if not data.empty:
    start_time = data["Waktu Belajar"].min()
    end_time = data["Waktu Belajar"].max()
    
    total_effect = calculate_integral(start_time, end_time)
    indefinite_integral = calculate_indefinite_integral()

    st.subheader("Hasil Analisis")
    st.markdown("### Batas Waktu Belajar")
    st.latex(f"a = {start_time}, \\ b = {end_time}")

    st.markdown("### Total Pengaruh Waktu Belajar terhadap IPK (Integral Tentu)")
    if isinstance(total_effect, str):
        st.error(total_effect)
    else:
        st.latex(r"IPK = \int_{a}^{b} \left( \frac{4}{1+e^{-k(t-t_0)}} \right) \, dt")
        st.latex(f"IPK = {total_effect:.2f}")

    st.markdown("### Model Matematis Hubungan Waktu Belajar terhadap IPK (Integral Tak Tentu)")
    st.latex(r"F(t) = \int \left( \frac{4}{1+e^{-k(t-t_0)}} \right) \, dt")
    st.latex(f"F(t) = {indefinite_integral} + C")

    st.subheader("Visualisasi Hubungan Waktu Belajar dan IPK")
    fig, ax = plt.subplots(figsize=(12, 6))

    ax.scatter(data["Waktu Belajar"], data["IPK"], color='red', label="Data Aktual")

    time_values = np.linspace(start_time, end_time, 100)
    effect_values = learning_effect(time_values)
    ax.plot(time_values, effect_values, label="Model Fungsi Pengaruh", color="blue")

    ax.fill_between(time_values, 0, effect_values, alpha=0.2, label="Area (Integral Tentu)", color="cyan")

    ax.set_title("Pengaruh Waktu Belajar terhadap IPK")
    ax.set_xlabel("Waktu Belajar (jam)")
    ax.set_ylabel("IPK")
    ax.legend()
    ax.grid(True)

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
st.image("logoTI.png", caption="TI Universitas Indo Global Mandiri", width=150)