import streamlit as st
from i18n import tr, set_language

def about_page():
    st.title(tr("About Us"))

    st.markdown(tr('This Project brought to you by:'))

    # --- Baris logo: rata tengah, responsif ---
    st.markdown(
        """
        <div style="
            display:flex;
            justify-content:center;      /* pusatkan horizontal */
            align-items:center;          /* rata-kan vertikal */
            gap: 32px;                   /* jarak antar logo */
            flex-wrap: wrap;             /* biar responsif di layar kecil */
            margin: 12px 0 28px 0;">
        <img src="https://raw.githubusercontent.com/mhmmdgoldy/stock_learning/main/gambar/UNY.png" width="160">
        <img src="https://raw.githubusercontent.com/mhmmdgoldy/stock_learning/main/gambar/Dikti.png" width="160">
        </div>
        """,
        unsafe_allow_html=True
    )

    # --- Teks di bawahnya: full center ---
    st.markdown(
        f"""
        <div style="text-align: center;">
            <h3>{tr('Department of Mathematics Education')}<br>{tr('Universitas Negeri Yogyakarta')}</h3>
            <p style="margin: 0;">Jl. Colombo No.1 Karangmalang Yogyakarta 55281</p>
            <p style="margin: 0;">Email: retnosubekti@uny.ac.id, muhammdgoldy@gmail.com</p>
            <p style="margin: 20px 0 0 0;">{tr('Build with Python Streamlit')}<br>Copyright © 2025 Tim Riset Website Departemen Pendidikan Matematika</p>
            <p style="margin: 8px 0 0 0;">Dr. Retno Subekti, S.Si., M.Sc.</p>
            <p style="margin: 0px 0 0 0;">Dr. Eminugroho Ratna Sari, S.Si., M.Sc.</p>
            <p style="margin: 0px 0 0 0;">Rizky Nur'aini, S.Stat., M.Stat.</p>
            <p style="margin: 0px 0 0 0;">Muhammad Goldy Wahyu Haryadi</p>
            <p style="margin: 0px 0 0 0;">Putri Kamilia</p>
        </div>
        """,
        unsafe_allow_html=True
    )