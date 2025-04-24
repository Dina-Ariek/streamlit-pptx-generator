import pandas as pd
from data_prep import generate_ppt
import streamlit as st
from drive_utils import upload_file_to_drive, gdrive_auth

# Sample user credentials
USERNAME = "zahra@alva.digital"
PASSWORD = "password123"

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if 'pptx_file' not in st.session_state:
    st.session_state.pptx_file = None

if 'drive_service' not in st.session_state:
    st.session_state.drive_service = None

def show_login_page():
    """Menampilkan halaman login."""
    st.title("Welcome to Alva Analytics!")
    st.subheader("Masukkan kredensial untuk login.")

    email = st.text_input("Email")
    password = st.text_input("Password", type='password')

    if st.button("Login"):
        if email == USERNAME and password == PASSWORD:
            st.success("✅ Login berhasil!")
            st.session_state.logged_in = True
        else:
            st.error("❌ Kredensial salah, silakan coba lagi.")


def show_report_generation_form():
    """Menampilkan form untuk mengunggah data dan membuat laporan."""
    st.markdown("### 📊 Generate Laporan Bulanan")

    start_date = st.date_input("Pilih Tanggal Mulai", value=pd.to_datetime("2024-01-01"))
    end_date = st.date_input("Pilih Tanggal Akhir", value=pd.to_datetime("2025-01-31"))
    # version = st.selectbox("Pilih Versi", ["Strategist - V1", "Strategist - V2"])
    # channel = st.selectbox("Pilih Channel", ["All Channel", "Channel 1", "Channel 2"])
    username = st.selectbox("Pilih Username", ["Finvast", "fitbar", "emeronhaircare"])

    if st.button("Generate Report"):
        pptx_file = generate_ppt(username)  # Ini tipe BytesIO
        st.session_state.pptx_file = pptx_file

        # Simpan ke file lokal
        output_path = f"output/output.pptx"
        with open(output_path, "wb") as f:
            f.write(pptx_file.getbuffer())

        st.session_state.output_path = output_path  # Simpan path lokalnya
        st.success("✅ File PPT berhasil dibuat!")

        if "pptx_file" in st.session_state and st.session_state.pptx_file:
            st.subheader("📂 Preview PPT yang Digenerate")
            st.download_button(
                label="Download PPT",
                data=st.session_state.pptx_file,
                file_name="Generated_Presentation.pptx",
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
            )

            # Tombol upload ke Google Drive
            if st.button("Upload ke Google Drive"):
                if not st.session_state.drive_service:
                    st.session_state.drive_service = gdrive_auth()
                    drive = gdrive_auth()
                    local_path = 'output/output.pptx'  # Path file lokal kamu
                    filename = 'output/output.pptx'  # Nama file di Google Drive
                    folder_id = '1X2FUDVUN3s2wzVnj9w8daiDXMDYs7IDJ'
                    uploaded_link = upload_file_to_drive(drive, local_path, filename, folder_id)
                # uploaded_link = upload_file_to_drive(
                #     st.session_state.drive_service,
                #     st.session_state.output_path,
                #     "Generated_Presentation.pptx"  # Nama file di Drive
                # )

                if uploaded_link:
                    st.success("✅ File berhasil diupload ke Google Drive!")
                    st.markdown(f"📎 [Lihat file di Google Drive]({uploaded_link})", unsafe_allow_html=True)
                else:
                    st.error("❌ Gagal mengupload file ke Google Drive.")
            # if st.button("Simpan ke GDrive"):
            #     drive = gdrive_auth()
            #     local_path = 'output/output.pptx'  # Path file lokal kamu
            #     filename = 'output/output.pptx'  # Nama file di Google Drive
            #     folder_id = '1X2FUDVUN3s2wzVnj9w8daiDXMDYs7IDJ'
            #     file_url = upload_file_to_drive(drive, local_path, filename, folder_id)
            #     st.success(f"Berhasil upload ke Google Drive. Link file: {file_url}")


# Main app logic
if not st.session_state.logged_in:
    show_login_page()
else:
    show_report_generation_form()
