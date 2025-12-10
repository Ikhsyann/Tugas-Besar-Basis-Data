"""
Main Streamlit Dashboard Application
Mental Health & Social Media Usage Analysis
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
import warnings
warnings.filterwarnings('ignore')

# Import dari database dan config
from database import Database
from config import *

# ================================================================
# STREAMLIT PAGE CONFIGURATION
# ================================================================

st.set_page_config(
    page_title=PAGE_CONFIG['page_title'],
    page_icon=PAGE_CONFIG['page_icon'],
    layout=PAGE_CONFIG['layout'],
    initial_sidebar_state=PAGE_CONFIG['initial_sidebar_state']
)

# ================================================================
# LOAD DATA
# ================================================================

@st.cache_data
def load_data():
    """Load data dari database"""
    try:
        db = Database()
        db.connect()
        data = db.get_master_dataframe()
        db.disconnect()
        return data
    except Exception as e:
        st.error(f"❌ Error loading from database: {e}")
        return None

# Load data
try:
    df = load_data()
    if df is None or df.empty:
        st.error("❌ Gagal memuat data. Pastikan MySQL running dan database 'uas_basdat' sudah di-setup.")
        st.stop()
except Exception as e:
    st.error(f"❌ Error: {str(e)}")
    st.stop()

# Define constants
ALL_COLUMNS = list(df.columns)
ANALYSIS_MENUS = [
    "🏠 Home / Overview", 
    "🔎 Data Mentah",
    "💻 Usage Dashboard (Ikhsyan)", 
    "🧠 Mental Health Dashboard (Aji)", 
    "👥 Demographic Effects (Vera)",
    "📈 Regression & Conclusion (Nazwa)"
]


# ================================================================
# HELPER FUNCTIONS
# ================================================================

@st.cache_data
def convert_df_to_csv(df):
    """Convert DataFrame to CSV for download"""
    return df.to_csv(index=False).encode('utf-8')

# ================================================================
# PAGE: HOME / OVERVIEW
# ================================================================

def page_home():
    """Homepage with project overview and quick statistics"""
    
    st.title("🏠 Dashboard Overview")
    st.markdown("---")
    
    # Project Introduction
    st.markdown("""
    ### 📊 Analisis Hubungan Penggunaan Media Sosial Terhadap Kesehatan Mental
    
    Dashboard ini digunakan untuk menganalisis dampak penggunaan platform media sosial 
    terhadap kesehatan mental mahasiswa/i.
    """)
    
    st.markdown("---")
    st.subheader("📊 Quick Statistics")
    
    # Display metrics in columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="👥 Total Responden",
            value=len(df)
        )
    
    with col2:
        st.metric(
            label="📱 Columns",
            value=len(df.columns)
        )
    
    with col3:
        st.metric(
            label="⏰ Avg Jam/Hari",
            value=f"{df['jam_penggunaan'].mean():.1f}" if 'jam_penggunaan' in df.columns else "N/A"
        )
    
    with col4:
        st.metric(
            label="🧠 Avg Mental Health",
            value=f"{df['tingkat_stress'].mean():.2f}/5" if 'tingkat_stress' in df.columns else "N/A"
        )
    
    # Quick visualizations
    if df is not None and len(df) > 0:
        col1, col2 = st.columns(2)
        
        with col1:
            # Column data types summary
            st.write("**Data Shape:**", f"{df.shape[0]} rows × {df.shape[1]} columns")
            st.write("**Data Quality:**", f"{(1 - df.isnull().sum().sum() / (df.shape[0] * df.shape[1])) * 100:.1f}% complete")
        
        with col2:
            st.write("**Columns Sample:**")
            st.write(df.columns.tolist()[:5])
    
    # Data source & disclaimer
    st.markdown("---")
    st.info("📊 Data loaded dari MySQL Database (uas_basdat)")

# ================================================================
# PAGE: DATA MENTAH (NABIL) 
# ================================================================

def page_data_mentah():
    """
    Data Mentah & Preprocessing Dashboard
    Jobdesk: NABIL
    Menampilkan data mentah dengan filter, search, dan export
    """
    
    st.header("📊 Data Responden Master - Tampilan Komprehensif")
    
    # Tabs untuk berbagai view
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Tabel Data", "📈 Statistik", "🔍 Info Kolom", "📥 Export/Import"])
    
    # ============ TAB 1: TABEL DATA ============
    with tab1:
        st.subheader("Tabel Data Mentah Responden")
        
        # Controls Row 1: Search dan Filter Advanced
        col_search, col_page_size = st.columns([3, 1])
        
        search_term = col_search.text_input(
            "🔍 Cari Nama/ID/Platform:", 
            placeholder="Ketik nama responden atau ID..."
        )
        
        page_size = col_page_size.selectbox(
            "Baris per Halaman:", 
            options=[10, 25, 50, 100],
            index=1
        )
        
        # Controls Row 2: Kolom yang ditampilkan
        col_cols_select, col_sort = st.columns([3, 1])
        
        default_cols = ['id_respondent', 'nama', 'usia', 'jenis_kelamin', 'status_hubungan', 'jam_per_hari'] if 'id_respondent' in ALL_COLUMNS else ALL_COLUMNS[:6]
        selected_cols = col_cols_select.multiselect(
            "📌 Pilih Kolom yang Ditampilkan:",
            options=ALL_COLUMNS, 
            default=default_cols,
            help="Pilih kolom mana saja yang ingin ditampilkan di tabel"
        )
        
        sort_col = col_sort.selectbox(
            "Urutkan Berdasarkan:",
            options=selected_cols if selected_cols else ALL_COLUMNS,
            index=0 if selected_cols else 0
        )
        
        # Prepare Data
        df_display = df.copy()
        
        # Apply Search Filter
        if search_term:
            search_mask = df_display.apply(
                lambda row: (
                    search_term.lower() in str(row.get('nama', '')).lower() or 
                    search_term.lower() in str(row.get('id_respondent', '')).lower() or
                    (search_term.lower() in str(row.get('nama_platform', '')).lower() if 'nama_platform' in row else False)
                ),
                axis=1
            )
            df_display = df_display[search_mask]
        
        # Apply Sorting
        if sort_col and sort_col in df_display.columns:
            df_display = df_display.sort_values(by=sort_col, ascending=True)
        
        # Pagination Info
        total_rows = len(df_display)
        num_pages = (total_rows + page_size - 1) // page_size
        
        if total_rows > 0:
            col_info, col_page_selector = st.columns([2, 1])
            
            col_info.info(f"📊 **Total: {total_rows} baris** | Halaman: {num_pages}")
            
            current_page = col_page_selector.number_input(
                "Halaman:",
                min_value=1,
                max_value=max(1, num_pages),
                value=1
            )
            
            # Calculate pagination
            start_idx = (current_page - 1) * page_size
            end_idx = start_idx + page_size
            df_paginated = df_display.iloc[start_idx:end_idx]
            
            # Display Table
            if selected_cols:
                st.dataframe(
                    df_paginated[selected_cols],
                    use_container_width=True,
                    hide_index=True,
                    height=400
                )
            else:
                st.warning("❌ Mohon pilih setidaknya satu kolom untuk ditampilkan.")
        else:
            st.warning("❌ Tidak ada data yang cocok dengan kriteria filter/pencarian.")
        
        # Download Button
        st.markdown("---")
        col_csv, col_excel = st.columns(2)
        
        csv_data = df_display[selected_cols].to_csv(index=False) if selected_cols else ""
        col_csv.download_button(
            label="⬇️ Download as CSV",
            data=csv_data.encode('utf-8') if csv_data else b"",
            file_name='data_mentah_smmh_filtered.csv',
            mime='text/csv'
        )
        
        # Generate Excel file
        if selected_cols:
            excel_buffer = BytesIO()
            df_display[selected_cols].to_excel(excel_buffer, index=False, sheet_name='Data')
            excel_data = excel_buffer.getvalue()
        else:
            excel_data = b""
        
        col_excel.download_button(
            label="⬇️ Download as Excel",
            data=excel_data,
            file_name='data_mentah_smmh_filtered.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    
    # ============ TAB 2: STATISTIK DATA ============
    with tab2:
        st.subheader("📈 Statistik Deskriptif Data")
        
        col_stats1, col_stats2 = st.columns(2)
        
        with col_stats1:
            st.metric("📊 Total Baris", len(df))
            st.metric("👤 Responden Unik", df['id_respondent'].nunique() if 'id_respondent' in df.columns else len(df))
            st.metric("🏢 Platform Unik", df['nama_platform'].nunique() if 'nama_platform' in df.columns else 0)
            st.metric("👨 Male", len(df[df['jenis_kelamin'] == 'Male']) if 'jenis_kelamin' in df.columns else 0)
        
        with col_stats2:
            st.metric("📅 Total Kolom", len(df.columns))
            st.metric("📍 Gender Kategori", df['jenis_kelamin'].nunique() if 'jenis_kelamin' in df.columns else 0)
            st.metric("💑 Status Unik", df['status_hubungan'].nunique() if 'status_hubungan' in df.columns else 0)
            st.metric("👩 Female", len(df[df['jenis_kelamin'] == 'Female']) if 'jenis_kelamin' in df.columns else 0)
        
        st.markdown("---")
        
        # Numeric Columns Summary
        st.subheader("📉 Ringkasan Kolom Numerik")
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) > 0:
            stats_df = df[numeric_cols].describe().T
            st.dataframe(stats_df, use_container_width=True)
        else:
            st.info("Tidak ada kolom numerik untuk ditampilkan.")
    
    # ============ TAB 3: INFO KOLOM ============
    with tab3:
        st.subheader("ℹ️ Informasi Detail Setiap Kolom")
        
        col_select_info = st.selectbox("Pilih Kolom:", options=ALL_COLUMNS)
        
        if col_select_info:
            col_data = df[col_select_info]
            
            col_info1, col_info2 = st.columns(2)
            
            with col_info1:
                st.write(f"**Nama Kolom:** {col_select_info}")
                st.write(f"**Tipe Data:** {col_data.dtype}")
                st.write(f"**Total Nilai:** {len(col_data)}")
                st.write(f"**Nilai Unik:** {col_data.nunique()}")
            
            with col_info2:
                st.write(f"**Null/Missing:** {col_data.isna().sum()}")
                st.write(f"**Null %:** {(col_data.isna().sum() / len(col_data) * 100):.2f}%")
                
                if col_data.dtype in [np.int64, np.float64]:
                    st.write(f"**Min:** {col_data.min()}")
                    st.write(f"**Max:** {col_data.max()}")
            
            st.markdown("---")
            st.write("**Nilai Unik (Top 20):**")
            
            if col_data.dtype in [np.int64, np.float64]:
                st.bar_chart(col_data.value_counts().head(20))
            else:
                value_counts = col_data.value_counts().head(20)
                st.dataframe(value_counts, use_container_width=True)
    
    # ============ TAB 4: EXPORT/IMPORT ============
    with tab4:
        st.subheader("📥📤 Export & Import Data")
        
        col_exp1, col_exp2 = st.columns(2)
        
        with col_exp1:
            st.write("**📥 Export Data**")
            
            # Full Export CSV
            full_csv = df.to_csv(index=False)
            st.download_button(
                label="📋 Export All (CSV)",
                data=full_csv.encode('utf-8'),
                file_name='data_smmh_complete.csv',
                mime='text/csv'
            )
            
            # Excel Export
            try:
                full_excel_buffer = BytesIO()
                df.to_excel(full_excel_buffer, index=False, sheet_name='Data')
                st.download_button(
                    label="📊 Export All (Excel)",
                    data=full_excel_buffer.getvalue(),
                    file_name='data_smmh_complete.xlsx',
                    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )
            except:
                st.warning("Excel export tidak tersedia")
            
            # JSON Export
            full_json = df.to_json(orient='records', indent=2)
            st.download_button(
                label="📑 Export All (JSON)",
                data=full_json.encode('utf-8'),
                file_name='data_smmh_complete.json',
                mime='application/json'
            )
        
        with col_exp2:
            st.write("**📤 Import Data**")
            
            uploaded_file = st.file_uploader(
                "Upload CSV atau Excel file:",
                type=['csv', 'xlsx']
            )
            
            if uploaded_file is not None:
                try:
                    if uploaded_file.name.endswith('.csv'):
                        imported_df = pd.read_csv(uploaded_file)
                    else:
                        imported_df = pd.read_excel(uploaded_file)
                    
                    st.success(f"✅ File berhasil diupload! ({imported_df.shape[0]} baris, {imported_df.shape[1]} kolom)")
                    
                    st.write("**Preview Data:**")
                    st.dataframe(imported_df.head(), use_container_width=True)
                    
                    # Save imported data
                    if st.button("💾 Simpan Data Imported"):
                        imported_df.to_csv("data_clean/imported_data.csv", index=False)
                        st.success("✅ Data berhasil disimpan ke data_clean/imported_data.csv")
                
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")


# ================================================================
# PAGE: USAGE DASHBOARD (IKHSYAN) - ALREADY COMPLETE
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
    
    # Use master dataframe
    df_usage = df.copy()
    
    # Display summary metrics
    st.subheader("📊 Summary Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    jam_col = 'jam_penggunaan' if 'jam_penggunaan' in df_usage.columns else None
    platform_col = 'nama_platform' if 'nama_platform' in df_usage.columns else None
    
    with col1:
        total_jam = df_usage[jam_col].sum() if jam_col and jam_col in df_usage.columns else 0
        st.metric("Total Jam Penggunaan", f"{total_jam:.1f} jam")
    
    with col2:
        avg_jam = df_usage[jam_col].mean() if jam_col and jam_col in df_usage.columns else 0
        st.metric("Rata-rata Jam/Hari", f"{avg_jam:.2f} jam")
    
    with col3:
        total_platform = df_usage[platform_col].nunique() if platform_col and platform_col in df_usage.columns else 0
        st.metric("Jumlah Platform", total_platform)
    
    with col4:
        st.metric("Total Data Points", len(df_usage))
    
    st.markdown("---")
    
    # Visualization 1: Bar Chart - Jam Penggunaan per Platform
    st.subheader("📊 Analisis 1: Jam Penggunaan Rata-Rata per Platform")
    
    if jam_col and platform_col:
        platform_usage = df_usage.groupby(platform_col)[jam_col].mean().sort_values(ascending=False)
        
        fig_bar = px.bar(
            x=platform_usage.index,
            y=platform_usage.values,
            labels={'x': 'Platform', 'y': 'Rata-rata Jam per Hari'},
            title="Rata-rata Jam Penggunaan per Platform",
            color=platform_usage.values,
            color_continuous_scale='Blues'
        )
        fig_bar.update_layout(height=400)
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("⚠️ Data tidak tersedia untuk visualisasi ini")
    
    # Visualization 2: Pie Chart - Platform Paling Populer
    st.subheader("📊 Platform Paling Populer (by User Count)")
    
    if platform_col:
        platform_popularity = df_usage[platform_col].value_counts()
        
        fig_pie = px.pie(
            values=platform_popularity.values,
            names=platform_popularity.index,
            title="Distribusi Pengguna per Platform",
            color_discrete_sequence=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.info("⚠️ Data tidak tersedia")
    
    # Visualization 3: Bar Chart - Distribusi Data
    st.subheader("📊 Distribusi Data per Platform")
    
    if platform_col:
        platform_counts = df_usage[platform_col].value_counts().sort_values(ascending=False)
        
        fig_freq = px.bar(
            x=platform_counts.index,
            y=platform_counts.values,
            labels={'x': 'Platform', 'y': 'Jumlah Record'},
            title="Jumlah Data per Platform",
            color=platform_counts.values,
            color_continuous_scale='Greens'
        )
        fig_freq.update_layout(height=400)
        st.plotly_chart(fig_freq, use_container_width=True)
    else:
        st.info("⚠️ Data tidak tersedia")
    
    # Visualization 4: Box Plot - Distribusi Jam Penggunaan
    st.subheader("📊 Analisis 2: Distribusi Jam Penggunaan per Platform")
    
    if jam_col and platform_col:
        fig_box = px.box(
            df_usage,
            x=platform_col,
            y=jam_col,
            title="Box Plot: Distribusi Jam Penggunaan per Platform",
            color=platform_col,
            color_discrete_sequence=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
        )
        fig_box.update_layout(height=500)
        st.plotly_chart(fig_box, use_container_width=True)
    else:
        st.info("⚠️ Data tidak tersedia")
    
    # Visualization 5: Histogram - Sebaran Jam Penggunaan
    st.subheader("📊 Histogram: Sebaran Jam Penggunaan Harian")
    
    if jam_col:
        fig_hist = px.histogram(
            df_usage,
            x=jam_col,
            nbins=30,
            title="Distribusi Jam Penggunaan Harian (Semua Platform)",
            color_discrete_sequence=['#1f77b4']
        )
        fig_hist.update_layout(height=400)
        st.plotly_chart(fig_hist, use_container_width=True)
    else:
        st.info("⚠️ Data tidak tersedia")
    
    # Data Table with column selection (dosen pattern)
    st.markdown("---")
    st.subheader("📋 Detail Data Penggunaan Platform")
    
    # Multiselect untuk pilih kolom yang ditampilkan
    all_columns = df_usage.columns.tolist()
    default_cols = [col for col in ['nama', 'nama_platform', 'jam_penggunaan'] if col in all_columns]
    if not default_cols:
        default_cols = all_columns[:5] if len(all_columns) >= 5 else all_columns
    
    selected_columns = st.multiselect(
        "Pilih kolom yang ingin ditampilkan:",
        options=all_columns,
        default=default_cols
    )
    
    if selected_columns:
        st.dataframe(df_usage[selected_columns], use_container_width=True, hide_index=True)
        
        # Download CSV button
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
    
    TODO untuk Aji:
    1. Rata-rata kesehatan mental seluruh responden (bar chart)
    2. Heatmap korelasi antar atribut mental health
    3. Radar chart per responden (dropdown pilih responden)
    4. Tabel detail nilai kesehatan mental
    """
    
    st.title("🧠 Mental Health Dashboard")
    st.markdown("**Jobdesk: Aji**")
    st.markdown("---")
    
    # TODO: Ambil data mental health dari database
    # db = Database()
    # db.connect()
    # df_mental = db.get_all_mental_health_data()
    # db.disconnect()
    
    # TODO: Hitung rata-rata per atribut mental health
    
    # TODO: Buat bar chart rata-rata skor kesehatan mental
    
    # TODO: Buat heatmap korelasi antar atribut
    
    # TODO: Dropdown pilih responden untuk radar chart
    
    # TODO: Tampilkan radar chart profil mental health per responden
    
    # TODO: Tabel detail nilai kesehatan mental
    
    st.info("⚠️ Halaman ini masih dalam pengembangan oleh Aji")
    st.markdown("""
    **Yang harus dikerjakan:**
    1. Bar chart rata-rata kesehatan mental (semua responden)
    2. Heatmap korelasi antar atribut
    3. Dropdown pilih responden
    4. Radar chart per responden
    5. Tabel detail nilai
    
    **Atribut Mental Health:**
    - Gangguan Fokus
    - Gelisah
    - Kecemasan
    - Kesulitan Konsentrasi
    - Perbandingan Diri
    - Sentimen Posting
    - Mencari Validasi
    - Depresi
    - Fluktuasi Minat
    - Sulit Tidur
    """)

# ================================================================
# PAGE: DEMOGRAPHIC EFFECTS (VERA) 
# ================================================================

def page_demographic():
    """
    Demographic Effects Analysis
    Jobdesk: VERA
    
    TODO untuk Vera:
    1. Gender comparison (metrics + radar chart)
    2. Status relationship comparison (donut chart + tabel)
    3. Age group analysis
    """
    
    st.title("👥 Demographic Effects Dashboard")
    st.markdown("**Jobdesk: Vera**")
    st.markdown("---")
    
    # TODO: Ambil master dataframe dari database
    # db = Database()
    # db.connect()
    # df_master = db.get_master_dataframe()
    # db.disconnect()
    
    # TODO: Gender Comparison
    # - Split data by gender (Laki-laki vs Perempuan)
    # - Tampilkan metrics untuk masing-masing gender
    # - Buat radar chart comparison
    
    # TODO: Status Relationship Comparison
    # - Group by status hubungan
    # - Buat donut chart rata-rata depresi per status
    # - Tabel detail rata-rata mental health per status
    
    # TODO: Age Group Analysis (BONUS)
    # - Group by age ranges (17-20, 21-25, 26-30, 31-35, 36+)
    # - Comparison charts
    
    st.info("⚠️ Halaman ini masih dalam pengembangan oleh Vera")
    st.markdown("""
    **Yang harus dikerjakan:**
    
    **A. Gender Comparison:**
    1. Metrics cards (2 kolom: Laki-laki vs Perempuan)
       - Rata-rata jam penggunaan
       - Rata-rata depresi
       - Rata-rata kecemasan
       - Platform favorit
    2. Radar chart comparison (Male vs Female)
    
    **B. Status Relationship:**
    1. Donut chart rata-rata depresi per status
    2. Tabel detail rata-rata mental health per status
    """)

# ================================================================
# PAGE: REGRESSION ANALYSIS (NAZWA - PART 1) 
# ================================================================

def page_regression():
    """
    Regression & Correlation Analysis
    Jobdesk: NAZWA (Part 1)
    
    TODO untuk Nazwa:
    1. Scatter plot dengan regression line
    2. Multi-line regression per platform
    3. Correlation matrix
    """
    
    st.title("📈 Regression & Correlation Analysis")
    st.markdown("**Jobdesk: Nazwa (Part 1)**")
    st.markdown("---")
    
    # TODO: Ambil master dataframe
    # db = Database()
    # db.connect()
    # df_master = db.get_master_dataframe()
    # db.disconnect()
    
    # TODO: Scatter plot dengan trendline
    # - Selectbox pilih atribut mental health
    # - X-axis: Jam per Hari
    # - Y-axis: Atribut mental health yang dipilih
    # - Tambahkan trendline='ols'
    
    # TODO: Multi-line regression per platform
    # - Loop untuk setiap platform
    # - Tampilkan regression line untuk masing-masing
    
    # TODO: Correlation matrix
    # - Pilih kolom: Jam per Hari, Depresi, Kecemasan, Sulit Tidur, Gangguan Fokus
    # - Buat heatmap korelasi
    
    st.info("⚠️ Halaman ini masih dalam pengembangan oleh Nazwa")
    st.markdown("""
    **Yang harus dikerjakan:**
    
    1. **Scatter Plot with Regression:**
       - Selectbox pilih atribut (Depresi, Kecemasan, dll)
       - X: Jam Penggunaan
       - Y: Skor Mental Health
       - Tambah trendline OLS
    
    2. **Multi-line Regression per Platform:**
       - Loop setiap platform
       - Tampilkan regression line masing-masing
    
    3. **Correlation Matrix:**
       - Heatmap korelasi
       - Text annotation untuk nilai
    """)

# ================================================================
# PAGE: CONCLUSION & INSIGHTS (NAZWA - PART 2) 
# ================================================================

def page_conclusion():
    """
    Conclusion & Key Insights
    Jobdesk: NAZWA (Part 2)
    
    TODO untuk Nazwa:
    1. Tulis key findings dari analisis
    2. Tulis recommendations
    3. Gunakan template INSIGHT_CATEGORIES dari config.py
    """
    
    st.title("🎯 Conclusion & Key Insights")
    st.markdown("**Jobdesk: Nazwa (Part 2)**")
    st.markdown("---")
    
    # TODO: Tampilkan key findings
    # - Gunakan markdown dengan numbering
    # - Highlight angka-angka penting
    # - Jelaskan temuan dari semua analisis sebelumnya
    
    # TODO: Tampilkan recommendations
    # - Self-regulation tips
    # - Platform choice guidance
    # - Digital detox suggestions
    # - Awareness points
    
    # HINT: Bisa gunakan INSIGHT_CATEGORIES dari config.py sebagai template
    
    st.info("⚠️ Halaman ini masih dalam pengembangan oleh Nazwa")
    st.markdown("""
    **Yang harus dikerjakan:**
    
    1. **Key Findings (8-10 poin):**
       - Heavy users vs light users comparison
       - Platform dengan dampak tertinggi
       - Gender differences
       - Status hubungan effects
       - Outlier cases
       - Non-users vs users
    
    2. **Recommendations (5-7 poin):**
       - Self-regulation strategies
       - Platform choices
       - Digital detox tips
       - Warning signs
       - Professional help guidance
    
    **Template ada di config.py → INSIGHT_CATEGORIES**
    """)


# ================================================================
# MAIN NAVIGATION
# ================================================================

def main():
    """Main application with navigation"""
    
    # Page navigation using sidebar radio
    pages = {
        "home": "🏠 Home / Overview", 
        "data_mentah": "🔎 Data Mentah",
        "usage_dashboard": "💻 Usage Dashboard", 
        "mental_health": "🧠 Mental Health", 
        "demographic": "👥 Demographic Effects",
        "regression": "📈 Regression & Conclusion"
    }
    
    page = st.sidebar.radio(
        "Pilih Halaman:",
        options=list(pages.keys()),
        format_func=lambda x: pages[x]
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
