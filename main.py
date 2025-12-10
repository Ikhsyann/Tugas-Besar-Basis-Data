"""
Main Streamlit Dashboard Application
Mental Health & Social Media Usage Analysis
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from database import Database
from config import * # Mengimpor semua konfigurasi


# ================================================================
# 🚨 KRITIS: INITIALIZE AND CACHE DATABASE CONNECTION
# ================================================================

# Menggunakan st.cache_resource agar koneksi database dipertahankan dan tidak dibuat ulang
@st.cache_resource(ttl=DATA_CONFIG['cache_ttl'])
def init_db():
    """
    Menginisialisasi dan mengetes koneksi database.
    CATATAN KRITIS: Tidak boleh ada pemanggilan Streamlit element di sini.
    """
    db = Database(**DB_CONFIG)
    success, message = db.test_connection()
    
    # Hapus st.error, st.stop(), dan st.toast() dari sini.

    # Sekarang mengembalikan 3 nilai: objek DB, status, dan pesan.
    return db, success, message

# Panggil fungsi inisialisasi di awal script
db, success, message = init_db()

# Pindahkan penanganan UI/Error ke LUAR fungsi yang di-cache
if not success:
    # Dipanggil di luar init_db()
    st.error(f"{ERROR_MESSAGES['db_connection']} Detail: {message}")
    st.stop() # Hentikan aplikasi jika gagal koneksi
else:
    # Dipanggil di luar init_db()
    st.toast("✅ Koneksi database berhasil.", icon='💾') 

# Setelah ini, db dijamin berisi koneksi yang berhasil.
# db = init_db() # Ganti baris lama

# ================================================================
# HELPER FUNCTIONS
# ================================================================

@st.cache_data
def convert_df_to_csv(df):
    """Convert DataFrame to CSV for download (dosen pattern)"""
    return df.to_csv(index=False).encode('utf-8')

# ----------------------------------------------------------------
# CACHED DATA LOADERS (Untuk Halaman yang Sering Diakses)
# ----------------------------------------------------------------

@st.cache_data(ttl=DATA_CONFIG['cache_ttl'])
def load_home_data():
    """Memuat data untuk halaman Home."""
    stats = db.get_summary_statistics()
    df_responden = db.get_all_respondents()
    return stats, df_responden

@st.cache_data(ttl=DATA_CONFIG['cache_ttl'])
def load_usage_data():
    """Memuat data untuk halaman Ikhsyan."""
    # Menggunakan pd.read_sql untuk efisiensi
    usage_data = db.get_all_usage_data() 
    return usage_data

@st.cache_data(ttl=DATA_CONFIG['cache_ttl'])
def load_vera_data():
    """Memuat data untuk halaman Vera."""
    metrics_df, radar_df, favorit_df = db.get_gender_comparison_data()
    depression_df, detail_df = db.get_status_comparison_data()
    return metrics_df, radar_df, favorit_df, depression_df, detail_df

@st.cache_data(ttl=DATA_CONFIG['cache_ttl'])
def load_nabil_data():
    """Memuat data untuk halaman Nabil (Data Mentah)."""
    return db.get_master_dataframe()


# ================================================================
# PAGE: HOME / OVERVIEW
# ================================================================

def page_home():
    """Homepage with project overview and quick statistics"""
    
    st.title("🏠 Dashboard Overview")
    st.markdown("---")
    
    # Project Introduction
    st.markdown(TEXT_CONTENT['home_intro'])
    
    # Objectives
    st.markdown(TEXT_CONTENT['home_objective'])
    
    # Get summary statistics (sudah di-cache)
    stats, df_responden = load_home_data()
    
    st.markdown("---")
    st.subheader("📊 Quick Statistics")
    
    # Display metrics in columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="👥 Total Responden",
            value=stats['total_responden']
        )
    
    with col2:
        st.metric(
            label="📱 Total Platform",
            value=stats['total_platform']
        )
    
    with col3:
        st.metric(
            label="⏰ Avg Jam/Hari",
            value=f"{stats['avg_jam_penggunaan']:.1f}"
        )
    
    with col4:
        st.metric(
            label="🧠 Avg Mental Health",
            value=f"{stats['avg_mental_health']:.2f}/5"
        )
    
    # Quick visualizations
    if df_responden is not None and len(df_responden) > 0:
        col1, col2 = st.columns(2)
        
        with col1:
            # Gender distribution pie chart
            gender_counts = df_responden['jenis_kelamin'].value_counts()
            fig_gender = px.pie(
                values=gender_counts.values,
                names=gender_counts.index,
                title="Distribusi Gender",
                color_discrete_sequence=COLOR_PALETTE['platforms']
            )
            st.plotly_chart(fig_gender, use_container_width=True)
        
        with col2:
            # Age distribution histogram
            fig_age = px.histogram(
                df_responden,
                x='usia',
                nbins=CHART_CONFIG['histogram']['nbins'],
                title="Distribusi Usia Responden",
                color_discrete_sequence=[COLOR_PALETTE['primary']]
            )
            st.plotly_chart(fig_age, use_container_width=True)
    
    # Data source & disclaimer
    st.markdown("---")
    st.info(TEXT_CONTENT['data_source'])
    st.warning(TEXT_CONTENT['disclaimer'])

# ================================================================
# PAGE: DATA MENTAH (NABIL) 
# ================================================================

def page_data_mentah():
    """
    Data Mentah & Preprocessing - SUPER SINGKAT
    Jobdesk: NABIL
    Fitur: Filter, Search, Detail, Download
    """
    
    st.title("📊 Data Mentah & Preprocessing")
    st.markdown("**Jobdesk: Nabil**")
    st.markdown("---")
    
    # Load data menggunakan cached loader
    df = load_nabil_data()
    
    if df is None or df.empty:
        st.error("❌ Gagal memuat data")
        return
    
    df_filter = df.copy()
    
    # ============ FILTER ============
    st.subheader("🔍 Filter & Search")
    col1, col2, col3 = st.columns(3)
    
    # Filter Usia
    usia_col = 'usia' if 'usia' in df.columns else None
    if usia_col:
        usia_range = col1.slider("Usia:", int(df[usia_col].min()), int(df[usia_col].max()), 
                                   (int(df[usia_col].min()), int(df[usia_col].max())))
        df_filter = df_filter[(df_filter[usia_col] >= usia_range[0]) & (df_filter[usia_col] <= usia_range[1])]
    
    # Filter Gender
    gender_col = 'jenis_kelamin' if 'jenis_kelamin' in df.columns else None
    if gender_col:
        genders = df[gender_col].unique()
        selected_gender = col2.multiselect("Gender:", options=genders, default=genders)
        df_filter = df_filter[df_filter[gender_col].isin(selected_gender)]
    
    # Filter Status
    status_col = 'status_hubungan' if 'status_hubungan' in df.columns else None
    if status_col:
        statuses = df[status_col].unique()
        selected_status = col3.multiselect("Status:", options=statuses, default=statuses)
        df_filter = df_filter[df_filter[status_col].isin(selected_status)]
    
    # Search Box
    search = st.text_input("🔎 Cari Nama:", placeholder="Ketik nama...")
    if search:
        df_filter = df_filter[df_filter.apply(
            lambda row: search.lower() in str(row.get('nama', '')).lower(),
            axis=1
        )]
    
    # ============ DROPDOWN PILIH RESPONDEN ============
    st.subheader("👤 Pilih Responden")
    if 'nama' in df_filter.columns and len(df_filter) > 0:
        responden_list = df_filter['nama'].unique()
        selected_responden = st.selectbox("Nama Responden:", options=responden_list)
        
        # Detail Lengkap
        responden_data = df_filter[df_filter['nama'] == selected_responden].iloc[0]
        
        st.subheader(f"📋 Detail: {selected_responden}")
        
        # Tampilkan semua detail dalam 2 kolom
        cols = st.columns(2)
        for idx, (col_name, value) in enumerate(responden_data.items()):
            cols[idx % 2].write(f"**{col_name}:** {value}")
    else:
        st.warning("⚠️ Tidak ada data yang sesuai filter")
    
    # ============ DOWNLOAD ============
    st.markdown("---")
    st.subheader("📥 Download Data")
    
    csv = df_filter.to_csv(index=False)
    st.download_button(
        "⬇️ Download CSV",
        csv.encode('utf-8'),
        "data_responden_filtered.csv",
        "text/csv"
    )

# ================================================================
# PAGE: USAGE DASHBOARD (IKHSYAN) - DISEMUA DENGAN CACHE
# ================================================================

def page_usage_dashboard():
    """
    Platform Usage Analysis Dashboard
    Jobdesk: IKHSYAN
    Analisis 1 & 2 dari Visualisasi.md
    """
    
    st.title("📱 Usage Dashboard - Platform Analysis")
    st.markdown("**Jobdesk: Ikhsyan**")
    st.markdown("---")
    
    # Get data using cached function
    df_usage = load_usage_data() 
    
    if df_usage is None or df_usage.empty:
        st.error(ERROR_MESSAGES['no_data'])
        return
    
    # Rename columns to user-friendly names (dapat diambil dari COLUMN_DEFINITIONS)
    # Kita menggunakan nama kolom di DB di sini, bukan view_usage_with_details.
    df_usage = df_usage.rename(columns={
        'id_penggunaan': 'ID Penggunaan',
        'id_responden': 'ID Responden',
        'nama': 'Nama Responden',
        'id_platform': 'ID Platform',
        'nama_platform': 'Nama Platform',
        'jam_per_hari': 'Jam per Hari',
        'tujuan_penggunaan': 'Tujuan Penggunaan',
        'frekuensi_buka_per_hari': 'Frekuensi Buka'
    })
    
    # Display summary metrics
    st.subheader("📊 Summary Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_jam = df_usage['Jam per Hari'].sum()
        st.metric("Total Jam Penggunaan", f"{total_jam:.1f} jam")
    
    with col2:
        avg_jam = df_usage['Jam per Hari'].mean()
        st.metric("Rata-rata Jam/Hari", f"{avg_jam:.2f} jam")
    
    with col3:
        total_platform = df_usage['Nama Platform'].nunique()
        st.metric("Jumlah Platform", total_platform)
    
    with col4:
        total_users = df_usage['ID Responden'].nunique()
        st.metric("Total Users (Pengguna Medsos)", total_users)
    
    st.markdown("---")
    
    # Visualization 1: Bar Chart - Jam Penggunaan per Platform
    st.subheader("📊 Analisis 1: Jam Penggunaan Rata-Rata per Platform")
    
    platform_usage = df_usage.groupby('Nama Platform')['Jam per Hari'].mean().sort_values(ascending=False)
    
    fig_bar = px.bar(
        x=platform_usage.index,
        y=platform_usage.values,
        labels={'x': 'Platform', 'y': 'Rata-rata Jam per Hari'},
        title="Rata-rata Jam Penggunaan per Platform",
        color=platform_usage.values,
        color_continuous_scale='Blues'
    )
    fig_bar.update_layout(height=CHART_CONFIG['bar_chart']['height'])
    st.plotly_chart(fig_bar, use_container_width=True)
    
    # Visualisasi Lanjutan (Tetap sama)
    
    st.markdown("---")
    st.subheader("📋 Detail Data Penggunaan Platform") 
    all_columns = df_usage.columns.tolist()
    selected_columns = st.multiselect(
        "Pilih kolom yang ingin ditampilkan:",
        options=all_columns,
        default=['Nama Responden', 'Nama Platform', 'Jam per Hari', 'Tujuan Penggunaan', 'Frekuensi Buka']
    )
    
    if selected_columns:
        st.dataframe(df_usage[selected_columns], use_container_width=True)
        csv = convert_df_to_csv(df_usage[selected_columns])
        st.download_button(
            label="📥 Download Data as CSV",
            data=csv,
            file_name="usage_data.csv",
            mime="text/csv"
        )
    else:
        st.warning("Pilih minimal satu kolom untuk ditampilkan")


# ================================================================
# PAGE: MENTAL HEALTH DASHBOARD (AJI) 
# ================================================================

def page_mental_health():
    """
    Mental Health Analysis Dashboard
    Jobdesk: AJI
    """
    
    st.title("🧠 Mental Health Dashboard")
    st.markdown("**Jobdesk: Aji**")
    st.markdown("---")
    st.info("⚠️ Halaman ini masih dalam pengembangan oleh Aji")

# ================================================================
# PAGE: DEMOGRAPHIC EFFECTS (VERA) - KRITIS: FIX FUNGSI & DATA FLOW
# ================================================================

def page_demographic():

    st.title("👥 Demographic Effects Dashboard")
    st.markdown("**Jobdesk: Vera**")

    # TOMBOL DEBUG
    if st.button("🔄 Clear Cache & Reload Data"):
        st.cache_data.clear()
        st.rerun()
        
    st.markdown("---")
    
    # ----------------------------------------------------
    # A. GENDER COMPARISON
    # ----------------------------------------------------
    st.header("A. Gender Comparison (Laki-laki vs Perempuan)")
    
    # Load data yang sudah di-cache
    metrics_df, radar_df, favorit_df, depression_df, detail_df = load_vera_data()
    
    # Pengecekan data
    if metrics_df is None or metrics_df.empty or favorit_df is None:
        st.warning("Data Gender Comparison gagal dimuat. Cek koneksi atau Query SQL Anda.")
        return

    # Siapkan data untuk tampilan
    L = metrics_df[metrics_df['jenis_kelamin'] == 'Laki-laki'].iloc[0] if 'Laki-laki' in metrics_df['jenis_kelamin'].values else None
    P = metrics_df[metrics_df['jenis_kelamin'] == 'Perempuan'].iloc[0] if 'Perempuan' in metrics_df['jenis_kelamin'].values else None
    
    L_fav = favorit_df[favorit_df['jenis_kelamin'] == 'Laki-laki']['platform_favorit'].values[0] if 'Laki-laki' in favorit_df['jenis_kelamin'].values else 'N/A'
    P_fav = favorit_df[favorit_df['jenis_kelamin'] == 'Perempuan']['platform_favorit'].values[0] if 'Perempuan' in favorit_df['jenis_kelamin'].values else 'N/A'

    col1, col2, col3, col4 = st.columns(4)

    # 1. METRICS CARDS
    with col1:
        st.markdown("**Rata-rata Jam Penggunaan**")
        if L is not None: st.metric("Laki-laki (Jam)", f"{L['avg_jam_guna']:.2f}")
        if P is not None: st.metric("Perempuan (Jam)", f"{P['avg_jam_guna']:.2f}")

    with col2:
        st.markdown("**Rata-rata Depresi (Skala 1-5)**")
        if L is not None: st.metric("Laki-laki", f"{L['avg_depresi']:.2f}")
        if P is not None: st.metric("Perempuan", f"{P['avg_depresi']:.2f}")

    with col3:
        st.markdown("**Rata-rata Kecemasan (Skala 1-5)**")
        if L is not None: st.metric("Laki-laki", f"{L['avg_kecemasan']:.2f}")
        if P is not None: st.metric("Perempuan", f"{P['avg_kecemasan']:.2f}")
        
    with col4:
        st.markdown("**Platform Favorit**")
        st.metric("Laki-laki", L_fav) 
        st.metric("Perempuan", P_fav)
        
    st.markdown("---")
    
    # 2. RADAR CHART COMPARISON
    st.subheader("2. Radar Chart Comparison (Profil Kesehatan Mental)")
    
    # Pastikan radar_df tidak kosong
    if radar_df is not None and not radar_df.empty:
        radar_melted = radar_df.melt(id_vars='jenis_kelamin', 
                                     var_name='Aspek Mental', 
                                     value_name='Rata-rata Skor')
        
        # Mapping nama kolom dari SQL ke label Indonesia (menggunakan MENTAL_HEALTH_ATTRIBUTES)
        column_mapping = {
            'Fokus': MENTAL_HEALTH_ATTRIBUTES['gangguan_fokus'],
            'Gelisah': MENTAL_HEALTH_ATTRIBUTES['gelisah'],
            'Kecemasan': MENTAL_HEALTH_ATTRIBUTES['kecemasan'],
            'Konsentrasi': MENTAL_HEALTH_ATTRIBUTES['kesulitan_konsentrasi'],
            'Banding_Diri': MENTAL_HEALTH_ATTRIBUTES['perbandingan_diri'],
            'Validasi': MENTAL_HEALTH_ATTRIBUTES['mencari_validasi'],
            'Depresi': MENTAL_HEALTH_ATTRIBUTES['depresi'],
            'Sulit_Tidur': MENTAL_HEALTH_ATTRIBUTES['sulit_tidur']
        }
        
        # Terapkan mapping
        radar_melted['Aspek Mental'] = radar_melted['Aspek Mental'].map(column_mapping)
        
        fig_radar = px.line_polar(
            radar_melted.dropna(subset=['Aspek Mental']), # Hapus jika ada NaN setelah map
            r='Rata-rata Skor', 
            theta='Aspek Mental', 
            color='jenis_kelamin', 
            line_close=True,
            title='Perbandingan Profil Kesehatan Mental berdasarkan Gender'
        )
        fig_radar.update_traces(fill='toself')
        st.plotly_chart(fig_radar, use_container_width=True)
    else:
        st.info("⚠️ Data Radar Chart tidak tersedia.")


    st.markdown("---")
    st.markdown("---")
    
    # ----------------------------------------------------
    # B. STATUS RELATIONSHIP COMPARISON
    # ----------------------------------------------------
    st.header("B. Status Relationship Comparison")
    
    if depression_df is None or depression_df.empty:
        st.warning("Data Status Relationship gagal dimuat. Cek Query SQL untuk `get_status_comparison_data`.")
        return

    col_chart, col_table = st.columns([1, 1.5])

    # 1. DONUT CHART (Rata-rata Depresi per Status)
    with col_chart:
        fig_donut = px.pie(
            depression_df, 
            values='avg_depresi', 
            names='status_hubungan', 
            title='Rata-rata Skor Depresi berdasarkan Status Hubungan',
            hole=CHART_CONFIG['pie_chart']['hole'],
            color_discrete_sequence=COLOR_PALETTE['platforms']
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    # 2. TABEL DETAIL RATA-RATA MENTAL HEALTH
    with col_table:
        st.markdown("##### Detail Rata-rata Skor Kesehatan Mental (Skala 1-5)")
        # Menggunakan kolom dari SQL_DETAIL yang sudah ada di database.py
        styled_df = detail_df.rename(columns={
            'status_hubungan': 'Status Hubungan',
            'Depresi': 'Rata-rata Depresi',
            'Kecemasan': 'Rata-rata Kecemasan',
            'Gelisah': 'Rata-rata Gelisah',
            'Sulit_Tidur': 'Rata-rata Sulit Tidur',
            'Perbandingan_Diri': 'Rata-rata Perbandingan Diri'
        }).set_index('Status Hubungan').round(DATA_CONFIG['decimal_places'])
        
        st.dataframe(styled_df, use_container_width=True)
    
    st.markdown("---")
    st.success("✅ Dashboard Demographic Effects Selesai (Poin A & B berhasil diterapkan).")

# ================================================================
# PAGE: REGRESSION ANALYSIS (NAZWA - PART 1) 
# ================================================================

def page_regression():
    """
    Regression & Correlation Analysis
    Jobdesk: NAZWA (Part 1)
    """
    
    st.title("📈 Regression & Correlation Analysis")
    st.markdown("**Jobdesk: Nazwa (Part 1)**")
    st.markdown("---")
    
    st.info("⚠️ Halaman ini masih dalam pengembangan oleh Nazwa")


# ================================================================
# PAGE: CONCLUSION & INSIGHTS (NAZWA - PART 2) 
# ================================================================

def page_conclusion():
    """
    Conclusion & Key Insights
    Jobdesk: NAZWA (Part 2)
    """
    
    st.title("🎯 Conclusion & Key Insights")
    st.markdown("**Jobdesk: Nazwa (Part 2)**")
    st.markdown("---")
    
    st.info("⚠️ Halaman ini masih dalam pengembangan oleh Nazwa")


# ================================================================
# MAIN NAVIGATION
# ================================================================

def main():
    """Main application with navigation"""
    
    st.sidebar.title(PAGE_CONFIG['page_title'])
    st.sidebar.markdown(f"**{TEAM_INFO['project_name']}**")
    st.sidebar.markdown(f"*{TEAM_INFO['course']}*")
    st.sidebar.markdown("---")
    
    # Page navigation using radio buttons
    page = st.sidebar.radio(
        "Pilih Halaman:",
        options=list(PAGES.keys()),
        format_func=lambda x: PAGES[x]
    )
    
    # Route to appropriate page
    if page == "home":
        page_home()
    elif page == "data_mentah":
        page_data_mentah()
    elif page == "usage_dashboard":
        page_usage_dashboard()
    elif page == "mental_health":
        page_mental_health()
    elif page == "demographic":
        page_demographic()
    elif page == "regression":
        page_regression()
    elif page == "conclusion":
        page_conclusion()

if __name__ == "__main__":
    main()
