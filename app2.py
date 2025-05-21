import streamlit as st
import pandas as pd
import calendar
from generate_report.report_generator_basic import generate_ppt_basic
from generate_report.report_generator import generate_ppt
from dotenv import load_dotenv
load_dotenv()

# Sample user credentials

USERNAME = "user1"
PASSWORD = "password123"

# Inisialisasi session state
if 'pptx_file' not in st.session_state:
    st.session_state.pptx_file = None
if 'output_path' not in st.session_state:
    st.session_state.output_path = None
if 'drive_service' not in st.session_state:
    st.session_state.drive_service = None
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False


# ====================
def select_month_ui(df):
    df['month'] = df['month'].astype(str)
    years = sorted(df['month'].str[:4].astype(int).unique())
    months = list(calendar.month_name)[1:]

    col1, col2 = st.columns(2)
    with col1:
        selected_year = st.selectbox("Pilih tahun", years, index=len(years) - 1)
    with col2:
        selected_month = st.selectbox("Pilih bulan", months, index=pd.Timestamp.today().month - 1)
    return selected_year, selected_month
#===================
# UI
# ====================
def show_login_page():
    st.title("Welcome to Alva Analytics!")
    st.subheader("Masukkan kredensial untuk login.")

    userid = st.text_input("UserID")
    password = st.text_input("Password", type='password')

    if st.button("Login"):
        if userid == USERNAME and password == PASSWORD:
            st.success("✅ Login berhasil!")
            st.session_state.logged_in = True
        else:
            st.error("❌ Kredensial salah, silakan coba lagi.")


def show_form():
    st.title("📊 PPTX Report Generator")
    st.markdown("Masukkan parameter laporan di bawah:")

    username = st.selectbox("Pilih Username", ["FinVast", "Tesla", "emeronhaircare"])

    # Step 1: Pilih bulan & tahun terlebih dahulu
    df = pd.read_excel("data/rawdata_post-sample.xlsx", parse_dates=["post_date"])
    df['month'] = df['post_date'].dt.to_period("M").astype(str)

    selected_year, selected_month = select_month_ui(df)
    month_number = list(calendar.month_name).index(selected_month)
    selected_period = f"{selected_year}-{month_number:02}"

    # Step 2: Tampilkan pemilihan versi hanya setelah bulan-tahun dipilih
    # st.markdown("### Pilih versi laporan:")
    version = st.selectbox("Pilih Versi Laporan", ["", "Basic", "Analytic"], index=0)

    if version == "":
        st.info("⬆️ Silakan pilih versi untuk melanjutkan.")
        return  # hentikan render berikutnya sampai versi dipilih

    # Step 3: Jika versi Basic, tampilkan file uploader
    external_df = None
    if version == "Basic":
        uploaded_file = st.file_uploader("📁 Upload data Media External (.xlsx)", type=["xlsx"])
        if uploaded_file is not None:
            try:
                external_df = pd.read_excel(uploaded_file)
                st.success("✅ Data berhasil diupload!")
                st.dataframe(external_df.head())
            except Exception as e:
                st.error(f"❌ Gagal membaca file: {e}")
    # Step 4: Tombol generate
    if st.button("🚀 Generate PPT"):
        if version == "Basic":
            pptx_file = generate_ppt_basic(username, selected_period, external_df)
        else:
            pptx_file = generate_ppt(username, selected_period)

        st.session_state.pptx_file = pptx_file

        output_path = "output/output.pptx"
        with open(output_path, "wb") as f:
            f.write(pptx_file.getbuffer())
        st.session_state.output_path = output_path

        st.success("✅ PPT berhasil digenerate!")
        st.download_button("⬇️ Download PPT", data=pptx_file, file_name="report.pptx",
                           mime="application/vnd.openxmlformats-officedocument.presentationml.presentation")

    # if st.session_state.pptx_file:
    #     if st.button("☁️ Upload ke Google Drive"):
    #         if not st.session_state.drive_service:
    #             st.session_state.drive_service = gdrive_auth()
    #         uploaded_link = upload_file_to_drive(
    #             st.session_state.drive_service,
    #             st.session_state.output_path,
    #             "Laporan_Sosmed.pptx"
    #         )
    #         if uploaded_link:
    #             st.success("✅ File berhasil diupload!")s
    #             st.markdown(f"[📎 Lihat di Google Drive]({uploaded_link})", unsafe_allow_html=True)
    #         else:
    #             st.error("❌ Upload gagal.")


# ====================
# Main App
# ====================
if not st.session_state.logged_in:
    show_login_page()
else:
    show_form()
