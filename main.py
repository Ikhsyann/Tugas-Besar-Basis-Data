"""
Main Streamlit Dashboard Application
Kesehatan Mental  & Social Media Usage Analysis
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
# mental health helpers are defined in this file below for clarity

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
    "🧠 Kesehatan Mental  Dashboard (Aji)", 
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
    
    st.title("Dashboard Lihat-lihat")
    st.markdown("---")
    
    # Project Introduction
    st.markdown("""
    ###  Analisis Hubungan Penggunaan Media Sosial Terhadap Kesehatan Mental
    """) 
    #Dashboard ini digunakan untuk menganalisis dampak penggunaan platform media sosial terhadap kesehatan mental orang-orang.
    
    st.markdown("---")
    st.subheader("Statistik Singkat")
    
    # Display metrics in columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Responden",
            value=len(df)
        )
    
    with col2:
        st.metric(
            label="Kolom",
            value=len(df.columns)
        )
    
    with col3:
        st.metric(
            label="Rata-rata Jam/Hari",
            value=f"{df['jam_penggunaan'].mean():.1f}" if 'jam_penggunaan' in df.columns else "N/A"
        )
    
    with col4:
        st.metric(
            label="Rata-rata Kesehatan Mental",
            value=f"{df['tingkat_stress'].mean():.2f}/5" if 'tingkat_stress' in df.columns else "N/A"
        )
    
    # Quick visualizations
    if df is not None and len(df) > 0:
        col1, col2 = st.columns(2)
        
        with col1:
            # Column data types summary
            st.write("**Bentuk Data:**", f"{df.shape[0]} rows × {df.shape[1]} kolomh")
            st.write("**Kualitas Data:**", f"{(1 - df.isnull().sum().sum() / (df.shape[0] * df.shape[1])) * 100:.1f}% Terisi")
        
        with col2:
            st.write("**Columns Sample:**")
            st.write(df.columns.tolist()[:5]) #masih belum dapat asal kode nya dari mana
    
    # Data source & disclaimer
    st.markdown("---")
    st.info("Data diambil dari _uas_basdat_")

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
            help="Pilih kolom mana saja yang ingin di" \
            "tampilkan di tabel"
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
# PAGE: Kesehatan Mental  DASHBOARD (AJI) 
# ================================================================

def create_avg_mental_health_barchart(df_mental):
    """
    Create bar chart showing average mental health scores across all respondents
    
    Args:
        df_mental: DataFrame with mental health data
        
    Returns:
        Plotly figure object
    """
    # Calculate average for each mental health attribute
    mental_cols = list(MENTAL_HEALTH_ATTRIBUTES.keys())
    averages = df_mental[mental_cols].mean()
    
    # Create DataFrame for plotting
    chart_data = pd.DataFrame({
        'Atribut': [MENTAL_HEALTH_ATTRIBUTES[col] for col in mental_cols],
        'Rata-rata Nilai': averages.values
    })
    
    # Create bar chart
    fig = go.Figure(data=[
        go.Bar(
            x=chart_data['Atribut'],
            y=chart_data['Rata-rata Nilai'],
            marker_color=COLOR_PALETTE['primary'],
            text=chart_data['Rata-rata Nilai'].round(2),
            textposition='outside',
            textfont=dict(size=12),
            hovertemplate='<b>%{x}</b><br>Rata-rata: %{y:.2f}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title={
            'text': '',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18, 'weight': 'bold'}
        },
        xaxis_title='Atribut Kesehatan Mental',
        yaxis_title='Nilai Rata-Rata',
        yaxis=dict(range=[0, 5.5]),
        height=CHART_CONFIG['bar_chart']['height'],
        template='plotly_white',
        showlegend=False,
        margin=dict(t=80, b=100, l=60, r=40)
    )
    
    fig.update_xaxes(tickangle=-45)
    
    return fig


def create_radar_chart(mental_data, responden_name):
    """
    Create radar chart for individual respondent's mental health scores
    
    Args:
        mental_data: Series containing mental health scores for one respondent
        responden_name: Name of the respondent
        
    Returns:
        Plotly figure object
    """
    mental_cols = list(MENTAL_HEALTH_ATTRIBUTES.keys())
    
    # Prepare data for radar chart
    categories = [MENTAL_HEALTH_ATTRIBUTES[col] for col in mental_cols]
    values = [mental_data[col] for col in mental_cols]
    
    # Close the radar chart by appending first value
    categories_closed = categories + [categories[0]]
    values_closed = values + [values[0]]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values_closed,
        theta=categories_closed,
        fill='toself',
        fillcolor='rgba(31, 119, 180, 0.3)',
        line=dict(color=COLOR_PALETTE['primary'], width=2),
        marker=dict(size=8, color=COLOR_PALETTE['primary']),
        name=responden_name,
        hovertemplate='<b>%{theta}</b><br>Nilai: %{r}<extra></extra>'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5],
                tickfont=dict(size=10),
                tickmode='linear',
                tick0=0,
                dtick=1
            ),
            angularaxis=dict(
                tickfont=dict(size=11)
            )
        ),
        title={
            'text': f'Profil Kesehatan Mental: {responden_name}',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 16, 'weight': 'bold'}
        },
        showlegend=False,
        height=500,
        margin=dict(t=80, b=40, l=80, r=80)
    )
    
    return fig


def show_responden_detail_modal(responden_data, usage_data, mental_data):
    """
    Show modal with respondent detail including usage table and radar chart
    
    Args:
        responden_data: Series with respondent basic info
        usage_data: DataFrame with usage data for this respondent
        mental_data: Series with mental health data for this respondent
    """
    
    st.markdown("---")
    # Display usage data table
    st.markdown("### 📱 Data Penggunaan Media Sosial")
    
    if not usage_data.empty:
        # Format table
        display_usage = usage_data[['nama_platform', 'jam_per_hari', 'tujuan_penggunaan', 'frekuensi_buka_per_hari']].copy()
        display_usage.columns = ['Platform', 'Jam/Hari', 'Tujuan', 'Frekuensi (x/hari)']
        
        # Calculate total
        total_jam = usage_data['jam_per_hari'].sum()
        
        st.dataframe(
            display_usage,
            use_container_width=True,
            hide_index=True
        )
        
        st.info(f"**Total Jam Penggunaan:** {total_jam:.1f} jam/hari")
    else:
        st.warning("Tidak ada data penggunaan media sosial untuk responden ini.")
    
    st.markdown("---")
    
    # Display mental health radar chart
    st.markdown("### 🧠 Profil Kesehatan Mental")
    
    # Show radar chart
    radar_fig = create_radar_chart(mental_data, responden_data['nama'])
    st.plotly_chart(radar_fig, use_container_width=True)
    
    # Show detailed mental health values in expandable section
    with st.expander("📋 Lihat Nilai Detail Kesehatan Mental"):
        mental_cols = list(MENTAL_HEALTH_ATTRIBUTES.keys())
        
        # Create 2 columns for better layout
        col1, col2 = st.columns(2)
        
        for idx, col in enumerate(mental_cols):
            target_col = col1 if idx % 2 == 0 else col2
            with target_col:
                value = mental_data[col]
                # Color coding based on severity
                if value <= 2:
                    color = "🟢"
                elif value <= 3:
                    color = "🟡"
                elif value <= 4:
                    color = "🟠"
                else:
                    color = "🔴"
                
                st.markdown(f"{color} **{MENTAL_HEALTH_ATTRIBUTES[col]}:** {value}")
@st.cache_data
def _cached_empty():
    return None


def open_responden_modal(responden_id, df_responden, df_usage, df_mental):
    """Show respondent detail (regular function, not a decorator dialog).

    We intentionally do not use experimental decorator dialogs so the
    function can be called directly from a button and render inline.
    """
    responden_data = df_responden[df_responden['id_responden'] == responden_id].iloc[0]
    usage_data = df_usage[df_usage['id_responden'] == responden_id]
    mental_data = df_mental[df_mental['id_responden'] == responden_id].iloc[0]
    show_responden_detail_modal(responden_data, usage_data, mental_data)


def page_mental_health():
    """Single entrypoint for the Kesehatan Mental page.

    This function replaces the previous `render_mental_health_dashboard`
    and is the only `page_mental_health()` definition used by navigation.
    """
    st.title("Dashboard Kesehatan Mental 🧠")

    # Connect to database and fetch required tables
    db = Database()
    try:
        db.connect()
        with st.spinner("Memuat data..."):
            df_responden = db.get_all_respondents()
            df_usage = db.get_all_usage_data()
            df_mental = db.get_all_mental_health_data()
    except Exception as e:
        st.error(f"❌ Gagal memuat data dari database: {e}")
        try:
            db.disconnect()
        except Exception:
            pass
        return
    finally:
        # Ensure connection is closed if still open
        try:
            db.disconnect()
        except Exception:
            pass

    if df_responden is None or df_mental is None:
        st.error("❌ Data tidak tersedia atau gagal diambil dari database.")
        return

    st.markdown("---")

    # Section 1: Average Bar Chart
    st.markdown("## 📊 Rata-Rata Nilai Kesehatan Mental")
    avg_chart = create_avg_mental_health_barchart(df_mental)
    st.plotly_chart(avg_chart, use_container_width=True)

    st.markdown("---")

    # Section 2: Daftar Responden (grid)
    st.markdown("## 👥 Daftar Responden")
    st.markdown("**Klik 'Lihat Detail' untuk membuka detail responden**")

    num_cols = 3
    cols = st.columns(num_cols)

    for idx, (_, responden) in enumerate(df_responden.iterrows()):
        col = cols[idx % num_cols]
        with col:
            with st.container(border=True):
                st.markdown(f"### {responden['nama']}")
                st.markdown(f"**Usia:** {responden.get('usia', 'N/A')} tahun")
                st.markdown(f"**Gender:** {responden.get('jenis_kelamin', 'N/A')}")
                st.markdown(f"**Status:** {responden.get('status_hubungan', 'N/A')}")

                if st.button("📋 Lihat Detail", key=f"btn_responden_{responden['id_responden']}"):
                    open_responden_modal(
                        responden['id_responden'],
                        df_responden,
                        df_usage,
                        df_mental
                    )

    st.markdown("---")

    # Additional statistics
    st.markdown("## 📈 Statistik Tambahan")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_responden = len(df_responden)
        st.metric("Total Responden", total_responden)

    with col2:
        mental_cols = list(MENTAL_HEALTH_ATTRIBUTES.keys())
        overall_avg = df_mental[mental_cols].values.mean()
        st.metric("Rata-rata Keseluruhan", f"{overall_avg:.2f}")

    with col3:
        avg_values = df_mental[mental_cols].mean()
        max_attr = avg_values.idxmax()
        st.metric(
            "Atribut Tertinggi",
            MENTAL_HEALTH_ATTRIBUTES[max_attr],
            delta=f"{avg_values[max_attr]:.2f}",
            delta_color="inverse"
        )

    with col4:
        min_attr = avg_values.idxmin()
        st.metric(
            "Atribut Terendah",
            MENTAL_HEALTH_ATTRIBUTES[min_attr],
            delta=f"{avg_values[min_attr]:.2f}",
            delta_color="normal"
        )

# ================================================================
# PAGE: DEMOGRAPHIC EFFECTS (VERA) 
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
    
    # === VALIDASI UTAMA: SEMUA DATA HARUS ADA ===
    if any(df is None or df.empty for df in [metrics_df, favorit_df]):
        st.warning("⚠️ Data Gender Comparison tidak lengkap. Periksa query di `get_gender_comparison_data()`.")
        return

    # === VALIDASI KOLOM WAJIB DI METRICS_DF ===
    required_metrics_cols = {'jenis_kelamin', 'avg_jam_guna', 'avg_depresi', 'avg_kecemasan'}
    if not required_metrics_cols.issubset(metrics_df.columns):
        missing = required_metrics_cols - set(metrics_df.columns)
        st.error(f"❌ Kolom wajib tidak ditemukan di `metrics_df`: {missing}.")
        st.write("Kolom yang tersedia:", list(metrics_df.columns))
        return

    # === AMBIL DATA LAKI-LAKI & PEREMPUAN DENGAN AMAN ===
    L_row = metrics_df[metrics_df['jenis_kelamin'] == 'Laki-laki']
    P_row = metrics_df[metrics_df['jenis_kelamin'] == 'Perempuan']
    
    L = L_row.iloc[0] if not L_row.empty else None
    P = P_row.iloc[0] if not P_row.empty else None

    # === PLATFORM FAVORIT (dengan validasi) ===
    def get_fav_platform(jk: str) -> str:
        if favorit_df is not None and 'jenis_kelamin' in favorit_df.columns and 'platform_favorit' in favorit_df.columns:
            match = favorit_df[favorit_df['jenis_kelamin'] == jk]
            if not match.empty:
                return str(match['platform_favorit'].iloc[0])
        return "N/A"

    L_fav = get_fav_platform('Laki-laki')
    P_fav = get_fav_platform('Perempuan')

    col1, col2, col3, col4 = st.columns(4)

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
    
    # 2. RADAR CHART COMPARISON — FIXED MAPPING
    st.subheader("2. Radar Chart Comparison (Profil Kesehatan Mental)")
    
    if radar_df is not None and not radar_df.empty:
        # Pastikan kolom 'jenis_kelamin' ada
        if 'jenis_kelamin' not in radar_df.columns:
            st.error("❌ Kolom 'jenis_kelamin' tidak ditemukan di radar_df.")
            return

        # Daftar kolom mental health dari query SQL_RADAR (sesuai database.py)
        mental_cols = ['Fokus', 'Gelisah', 'Kecemasan', 'Konsentrasi', 'Banding_Diri', 'Validasi', 'Depresi', 'Sulit_Tidur']
        
        # Cek apakah semua kolom ada
        missing_radar_cols = [col for col in mental_cols if col not in radar_df.columns]
        if missing_radar_cols:
            st.warning(f"⚠️ Kolom radar tidak lengkap. Missing: {missing_radar_cols}")
            # Gunakan hanya kolom yang tersedia
            mental_cols = [col for col in mental_cols if col in radar_df.columns]

        if not mental_cols:
            st.error("❌ Tidak ada kolom data mental health yang valid untuk radar chart.")
            return

        # Buat mapping dari nama kolom ke label deskriptif
        # Sesuaikan dengan teks yang ingin ditampilkan (bisa ambil dari config jika mau)
        COL_LABEL_MAP = {
            'Fokus': 'Gangguan Fokus',
            'Gelisah': 'Perasaan Gelisah',
            'Kecemasan': 'Tingkat Kecemasan',
            'Konsentrasi': 'Kesulitan Konsentrasi',
            'Banding_Diri': 'Perbandingan Diri',
            'Validasi': 'Mencari Validasi',
            'Depresi': 'Gejala Depresi',
            'Sulit_Tidur': 'Kesulitan Tidur'
        }

        # Melt dataframe
        radar_melted = radar_df.melt(
            id_vars='jenis_kelamin',
            value_vars=mental_cols,
            var_name='Aspek Mental',
            value_name='Rata-rata Skor'
        )

        # Terapkan mapping label
        radar_melted['Aspek Mental'] = radar_melted['Aspek Mental'].map(COL_LABEL_MAP).fillna(radar_melted['Aspek Mental'])

        # Buat radar chart
        fig_radar = px.line_polar(
            radar_melted,
            r='Rata-rata Skor', 
            theta='Aspek Mental', 
            color='jenis_kelamin', 
            line_close=True,
            title='Perbandingan Profil Kesehatan Mental berdasarkan Gender',
            range_r=[1, 5]  # Skala 1-5
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

    # Validasi kolom untuk donut chart
    if not {'status_hubungan', 'avg_depresi'}.issubset(depression_df.columns):
        st.error("❌ Kolom 'status_hubungan' atau 'avg_depresi' tidak ditemukan di depression_df.")
        st.write("Kolom tersedia:", list(depression_df.columns))
        return

    col_chart, col_table = st.columns([1, 1.5])

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

    with col_table:
        st.markdown("##### Detail Rata-rata Skor Kesehatan Mental (Skala 1-5)")
        # Validasi kolom detail_df
        expected_detail_cols = {'status_hubungan', 'Depresi', 'Kecemasan', 'Gelisah', 'Sulit_Tidur', 'Perbandingan_Diri'}
        if not expected_detail_cols.issubset(detail_df.columns):
            missing = expected_detail_cols - set(detail_df.columns)
            st.warning(f"⚠️ Kolom detail tidak lengkap. Missing: {missing}")
            # Tampilkan hanya kolom yang ada
            available_cols = list(expected_detail_cols & set(detail_df.columns))
            if 'status_hubungan' in detail_df.columns:
                available_cols = ['status_hubungan'] + [c for c in available_cols if c != 'status_hubungan']
                display_df = detail_df[available_cols]
            else:
                display_df = detail_df
        else:
            display_df = detail_df

        # Rename untuk tampilan
        rename_map = {
            'status_hubungan': 'Status Hubungan',
            'Depresi': 'Rata-rata Depresi',
            'Kecemasan': 'Rata-rata Kecemasan',
            'Gelisah': 'Rata-rata Gelisah',
            'Sulit_Tidur': 'Rata-rata Sulit Tidur',
            'Perbandingan_Diri': 'Rata-rata Perbandingan Diri'
        }
        styled_df = display_df.rename(columns=rename_map)
        if 'Status Hubungan' in styled_df.columns:
            styled_df = styled_df.set_index('Status Hubungan')
        st.dataframe(styled_df.round(DATA_CONFIG['decimal_places']), use_container_width=True)
    
    st.markdown("---")
    st.success("✅ Dashboard Demographic Effects Selesai (Poin A & B berhasil diterapkan).")

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
    # - Selectbox pilih atribut Kesehatan Mental 
    # - X-axis: Jam per Hari
    # - Y-axis: Atribut Kesehatan Mental  yang dipilih
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
       - Y: Skor Kesehatan Mental 
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
    
    st.sidebar.success("Pilih Halaman:")

    if st.sidebar.checkbox("🏠 Home / Overview"):
        page_home()

    if st.sidebar.checkbox("📊 Data Mentah"):
        page_data_mentah()

    if st.sidebar.checkbox("💻 Usage Dashboard"):
        page_usage_dashboard()

    if st.sidebar.checkbox("🧠 Kesehatan Mental"):
        page_mental_health()

    if st.sidebar.checkbox("👥 Demographic Effects"):
        page_demographic()

    if st.sidebar.checkbox("📈 Regression & Conclusion"):
        page_regression()

if __name__ == "__main__":
    main()
