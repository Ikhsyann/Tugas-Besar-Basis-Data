"""
Main Streamlit Dashboard Application
Mental Health & Social Media Usage Analysis
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from database import Database
from config import *

# ================================================================
# STREAMLIT PAGE CONFIGURATION
# ================================================================

st.set_page_config(
    page_title=PAGE_CONFIG['page_title'],
    layout=PAGE_CONFIG['layout'],
    initial_sidebar_state=PAGE_CONFIG['initial_sidebar_state']
)

# ================================================================
# 🚨 KRITIS: INITIALIZE AND CACHE DATABASE CONNECTION
# ================================================================

@st.cache_resource(ttl=DATA_CONFIG['cache_ttl'])
def init_db():
    """
    Menginisialisasi dan mengetes koneksi database.
    CATATAN KRITIS: Tidak boleh ada pemanggilan Streamlit element di sini.
    """
    db = Database(
        host=DB_CONFIG['host'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        database=DB_CONFIG['database']
    )
    success, message = db.test_connection()
    return db, success, message

# Panggil fungsi inisialisasi di awal script
db, success, message = init_db()

# Pindahkan penanganan UI/Error ke LUAR fungsi yang di-cache
if not success:
    st.error(f"{ERROR_MESSAGES['db_connection']} Detail: {message}")
    st.stop()
else:
    st.toast("✅ Koneksi database berhasil.", icon='💾')

# ================================================================
# HELPER FUNCTIONS
# ================================================================

@st.cache_data
def convert_df_to_csv(df):
    """Convert DataFrame to CSV for download"""
    return df.to_csv(index=False).encode('utf-8')

# ----------------------------------------------------------------
# CACHED DATA LOADERS
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
    
    # Get summary statistics
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

# ================================================================
# PAGE: DATA MENTAH (NABIL)
# ================================================================

def page_data_mentah():
    """
    Data Mentah & Preprocessing
    """
    
    st.title("📊 Data Mentah & Preprocessing")
    st.markdown("---")
    
    # Load data
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
    
    # ============ INFO JUMLAH DATA TERFILTER ============
    st.info(f"📊 Menampilkan **{len(df_filter)}** dari **{len(df)}** responden")
    
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
# PAGE: USAGE DASHBOARD (IKHSYAN)
# ================================================================

def page_usage_dashboard():
    """
    Platform Usage Analysis Dashboard
    """
    
    st.title("📱 Usage Dashboard - Platform Analysis")
    st.markdown("---")
    
    # Get data
    df_usage = load_usage_data()
    
    if df_usage is None or df_usage.empty:
        st.error(ERROR_MESSAGES['no_data'])
        return
    
    # Rename columns
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
        st.metric("Total Users", total_users)
    
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
    
    # Visualization 2: Pie Chart - Platform Paling Populer
    st.subheader("📊 Platform Paling Populer (by User Count)")
    
    platform_counts = df_usage['Nama Platform'].value_counts()
    fig_pie = px.pie(
        values=platform_counts.values,
        names=platform_counts.index,
        title="Distribusi Platform Berdasarkan Jumlah Pengguna",
        color_discrete_sequence=COLOR_PALETTE['platforms']
    )
    st.plotly_chart(fig_pie, use_container_width=True)
    
    # Visualization 3: Box Plot
    st.subheader("📊 Analisis 2: Distribusi Jam Penggunaan per Platform")
    
    fig_box = px.box(
        df_usage,
        x='Nama Platform',
        y='Jam per Hari',
        title="Distribusi Jam Penggunaan per Platform (Box Plot)",
        color='Nama Platform',
        color_discrete_sequence=COLOR_PALETTE['platforms']
    )
    fig_box.update_layout(height=CHART_CONFIG['box_plot']['height'])
    st.plotly_chart(fig_box, use_container_width=True)
    
    # Data Table
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


def open_responden_modal(responden_id, df_responden, df_usage, df_mental):
    """Show respondent detail (regular function, not a decorator dialog)."""
    responden_data = df_responden[df_responden['id_responden'] == responden_id].iloc[0]
    usage_data = df_usage[df_usage['id_responden'] == responden_id]
    mental_data = df_mental[df_mental['id_responden'] == responden_id].iloc[0]
    show_responden_detail_modal(responden_data, usage_data, mental_data)


def page_mental_health():
    """
    Mental Health Analysis Dashboard
    """
    st.title("🧠 Dashboard Kesehatan Mental")
    # Fetch data using cached loaders (reusing existing connection)
    with st.spinner("Memuat data..."):
        df_responden = db.get_all_respondents()
        df_usage = db.get_all_usage_data()
        df_mental = db.get_all_mental_health_data()

    if df_responden is None or df_mental is None or df_usage is None:
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
    """
    Demographic Effects Dashboard
    """
    
    st.title("👥 Demographic Effects Dashboard")
    st.markdown("---")
    
    # Load data
    metrics_df, radar_df, favorit_df, depression_df, detail_df = load_vera_data()
    
    # === GENDER COMPARISON ===
    st.header("A. Gender Comparison (Laki-laki vs Perempuan)")
    
    # Validasi data
    if any(df is None or df.empty for df in [metrics_df, favorit_df]):
        st.warning("⚠️ Data Gender Comparison tidak lengkap.")
        return
    
    # Validasi kolom
    required_metrics_cols = {'jenis_kelamin', 'avg_jam_guna', 'avg_depresi', 'avg_kecemasan'}
    if not required_metrics_cols.issubset(metrics_df.columns):
        missing = required_metrics_cols - set(metrics_df.columns)
        st.error(f"❌ Kolom wajib tidak ditemukan: {missing}")
        return
    
    # Ambil data per gender
    L_row = metrics_df[metrics_df['jenis_kelamin'] == 'Laki-laki']
    P_row = metrics_df[metrics_df['jenis_kelamin'] == 'Perempuan']
    
    L = L_row.iloc[0] if not L_row.empty else None
    P = P_row.iloc[0] if not P_row.empty else None
    
    # Platform favorit
    def get_fav_platform(jk: str) -> str:
        if favorit_df is not None and 'jenis_kelamin' in favorit_df.columns and 'platform_favorit' in favorit_df.columns:
            match = favorit_df[favorit_df['jenis_kelamin'] == jk]
            if not match.empty:
                return str(match['platform_favorit'].iloc[0])
        return "N/A"
    
    L_fav = get_fav_platform('Laki-laki')
    P_fav = get_fav_platform('Perempuan')
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("**Rata-rata Jam Penggunaan**")
        if L is not None: st.metric("Laki-laki", f"{L['avg_jam_guna']:.2f} jam")
        if P is not None: st.metric("Perempuan", f"{P['avg_jam_guna']:.2f} jam")
    
    with col2:
        st.markdown("**Rata-rata Depresi**")
        if L is not None: st.metric("Laki-laki", f"{L['avg_depresi']:.2f}")
        if P is not None: st.metric("Perempuan", f"{P['avg_depresi']:.2f}")
    
    with col3:
        st.markdown("**Rata-rata Kecemasan**")
        if L is not None: st.metric("Laki-laki", f"{L['avg_kecemasan']:.2f}")
        if P is not None: st.metric("Perempuan", f"{P['avg_kecemasan']:.2f}")
    
    with col4:
        st.markdown("**Platform Favorit**")
        st.metric("Laki-laki", L_fav)
        st.metric("Perempuan", P_fav)
    
    st.markdown("---")
    
    # === RADAR CHART ===
    st.subheader("2. Radar Chart Comparison")
    
    if radar_df is not None and not radar_df.empty:
        if 'jenis_kelamin' not in radar_df.columns:
            st.error("❌ Kolom 'jenis_kelamin' tidak ditemukan di radar_df")
            return
        
        mental_cols = ['Fokus', 'Gelisah', 'Kecemasan', 'Konsentrasi', 'Banding_Diri', 'Validasi', 'Depresi', 'Sulit_Tidur']
        
        # Cek kolom yang hilang
        missing_radar_cols = [col for col in mental_cols if col not in radar_df.columns]
        if missing_radar_cols:
            st.warning(f"⚠️ Kolom tidak lengkap: {missing_radar_cols}")
            mental_cols = [col for col in mental_cols if col in radar_df.columns]
        
        if not mental_cols:
            st.error("❌ Tidak ada kolom aspek mental di radar_df")
            return
        
        # Mapping label
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
        
        # Apply mapping
        radar_melted['Aspek Mental'] = radar_melted['Aspek Mental'].map(COL_LABEL_MAP).fillna(radar_melted['Aspek Mental'])
        
        # Create radar chart
        fig_radar = px.line_polar(
            radar_melted,
            r='Rata-rata Skor',
            theta='Aspek Mental',
            color='jenis_kelamin',
            line_close=True,
            title='Perbandingan Profil Kesehatan Mental berdasarkan Gender',
            range_r=[1, 5]
        )
        fig_radar.update_traces(fill='toself')
        st.plotly_chart(fig_radar, use_container_width=True)
    else:
        st.info("⚠️ Data Radar Chart tidak tersedia")
    
    st.markdown("---")
    
    # === STATUS RELATIONSHIP COMPARISON ===
    st.header("B. Status Relationship Comparison")
    
    if depression_df is None or depression_df.empty:
        st.warning("Data Status Relationship tidak tersedia")
        return
    
    # Validasi kolom
    if not {'status_hubungan', 'avg_depresi'}.issubset(depression_df.columns):
        st.error("❌ Kolom tidak lengkap di depression_df")
        return
    
    col_chart, col_table = st.columns([1, 1.5])
    
    with col_chart:
        fig_donut = px.pie(
            depression_df,
            values='avg_depresi',
            names='status_hubungan',
            title='Rata-rata Skor Depresi per Status Hubungan',
            hole=CHART_CONFIG['pie_chart']['hole'],
            color_discrete_sequence=COLOR_PALETTE['platforms']
        )
        st.plotly_chart(fig_donut, use_container_width=True)
    
    with col_table:
        st.markdown("##### Detail Rata-rata Skor Kesehatan Mental")
        
        expected_detail_cols = {'status_hubungan', 'Depresi', 'Kecemasan', 'Gelisah', 'Sulit_Tidur', 'Perbandingan_Diri'}
        if not expected_detail_cols.issubset(detail_df.columns):
            missing = expected_detail_cols - set(detail_df.columns)
            st.warning(f"⚠️ Kolom tidak lengkap: {missing}")
            available_cols = list(expected_detail_cols & set(detail_df.columns))
            if available_cols:
                display_df = detail_df[available_cols]
            else:
                st.error("❌ Tidak ada kolom detail yang tersedia")
                return
        else:
            display_df = detail_df[list(expected_detail_cols)]
        
        # Rename
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

# ================================================================
# PAGE: REGRESSION ANALYSIS (NAZWA - PART 1)
# ================================================================

def page_regression():
    """
    Regression & Correlation Analysis
    """
    import numpy as np
    import statsmodels.api as sm
    import plotly.express as px

    st.title("📈 Regression & Correlation Analysis")
    st.markdown("---")

    # Load master dataframe (long format dari Nabil)
    df_raw = load_nabil_data()
    
    if df_raw is None or df_raw.empty:
        st.error("❌ Gagal memuat data dari database")
        return
    
    # Agregasi: Total jam penggunaan per responden
    df_usage_total = df_raw.groupby('id_responden').agg({
        'jam_per_hari': 'sum'  # Total jam semua platform
    }).reset_index()
    df_usage_total.rename(columns={'jam_per_hari': 'jam_penggunaan_total'}, inplace=True)
    
    # Pivot: Jam per platform (untuk multi-regression)
    df_platform = df_raw.pivot_table(
        index='id_responden',
        columns='nama_platform',
        values='jam_per_hari',
        aggfunc='sum',
        fill_value=0
    ).reset_index()
    
    # Mental health columns (ambil data unik per responden)
    mental_cols = ['gangguan_fokus', 'gelisah', 'kecemasan', 'kesulitan_konsentrasi',
                   'perbandingan_diri', 'sentimen_posting', 'mencari_validasi', 'depresi',
                   'fluktuasi_minat', 'sulit_tidur']
    
    df_mental = df_raw[['id_responden'] + mental_cols].drop_duplicates(subset='id_responden')
    
    # Hitung skor mental health (rata-rata dari semua indikator)
    df_mental['skor_mental_health'] = df_mental[mental_cols].mean(axis=1)
    
    # Merge semua data
    df_master = df_usage_total.merge(df_mental, on='id_responden')
    df_master = df_master.merge(df_platform, on='id_responden')

    
    # Preview data
    st.markdown("### 📋 Sample Data (Preview)")
    preview_cols = ['id_responden', 'jam_penggunaan_total', 'skor_mental_health']
    st.dataframe(df_master[preview_cols].head(10), use_container_width=True)
    
    st.info(f"✅ Data berhasil dimuat: {len(df_master)} responden")
    
    # ---------- SCATTER PLOT + REGRESSION LINE ----------
    st.markdown("---")
    st.subheader("📊 Scatter Plot + Regression Line")
    st.markdown("**X:** Total Jam Penggunaan (semua platform) | **Y:** Rata-rata Skor Mental Health")
    
    # Remove NaN
    df_plot = df_master[['jam_penggunaan_total', 'skor_mental_health']].dropna()
    
    if df_plot.empty:
        st.error("❌ Data kosong setelah filter NaN")
        return
    
    # Scatter + trendline
    fig = px.scatter(
        df_plot, 
        x='jam_penggunaan_total', 
        y='skor_mental_health',
        trendline="ols",
        labels={
            'jam_penggunaan_total': 'Total Jam Penggunaan (jam/hari)',
            'skor_mental_health': 'Skor Mental Health (rata-rata 1-5)'
        },
        title="Hubungan Jam Penggunaan vs Skor Mental Health"
    )
    fig.update_traces(marker=dict(size=8, opacity=0.6, color=COLOR_PALETTE['primary']))
    st.plotly_chart(fig, use_container_width=True)
    
    # Compute regression statistics
    X = df_plot['jam_penggunaan_total'].values
    Y = df_plot['skor_mental_health'].values
    X_sm = sm.add_constant(X)
    model = sm.OLS(Y, X_sm).fit()
    
    intercept = model.params[0]
    slope = model.params[1]
    r_sq = model.rsquared
    p_value = model.pvalues[1]
    corr = np.corrcoef(X, Y)[0, 1]
    
    # Display results
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Pearson r (Korelasi)", f"{corr:.3f}")
    with col2:
        st.metric("R² (Koefisien Determinasi)", f"{r_sq:.3f}")
    with col3:
        signif = "✅ Signifikan" if p_value < 0.05 else "⚠️ Tidak Signifikan"
        st.metric("P-value", f"{p_value:.4f}", delta=signif)
    
    st.markdown(f"**Persamaan Regresi:** Y = {intercept:.4f} + {slope:.4f} × X")
    
    # Interpretation
    if abs(corr) < 0.3:
        interpretation = "🟢 Hubungan **sangat lemah** / hampir tidak ada korelasi"
    elif abs(corr) < 0.5:
        interpretation = "🟡 Hubungan **lemah**"
    elif abs(corr) < 0.7:
        interpretation = "🟠 Hubungan **sedang**"
    else:
        interpretation = "🔴 Hubungan **kuat**"
    
    st.info(f"**Interpretasi:** {interpretation}")
    
    # ---------- MULTI-REGRESSION PER PLATFORM ----------
    st.markdown("---")
    st.subheader("📉 Analisis Regresi Per Platform")
    st.markdown("Regresi sederhana: **Skor Mental Health ~ Jam Platform**")
    
    # Get platform columns (dari pivot)
    platform_cols = [col for col in df_master.columns if col in PLATFORMS]
    
    if not platform_cols:
        st.warning("⚠️ Tidak ditemukan kolom platform. Skip multi-regression.")
        multi_results = []
    else:
        multi_results = []
        for platform in platform_cols:
            df_tmp = df_master[[platform, 'skor_mental_health']].dropna()
            
            if df_tmp.empty or df_tmp[platform].sum() == 0:
                continue  # Skip jika tidak ada data
            
            X_p = sm.add_constant(df_tmp[platform].values)
            Y_p = df_tmp['skor_mental_health'].values
            
            try:
                model_p = sm.OLS(Y_p, X_p).fit()
                slope_p = model_p.params[1]
                pval = model_p.pvalues[1]
                r2 = model_p.rsquared
                
                # Interpretasi
                if r2 > 0.5:
                    strength = "Kuat"
                elif r2 > 0.25:
                    strength = "Sedang"
                else:
                    strength = "Lemah"
                
                signif = "Signifikan" if pval < 0.05 else "Tidak Signifikan"
                
                multi_results.append({
                    "Platform": platform,
                    "Slope (β)": slope_p,
                    "P-value": pval,
                    "R²": r2,
                    "Kekuatan": strength,
                    "Signifikansi": signif
                })
            except Exception as e:
                continue
        
        if multi_results:
            df_multi = pd.DataFrame(multi_results).sort_values(by='R²', ascending=False)
            st.dataframe(
                df_multi.style.format({
                    'Slope (β)': '{:.4f}',
                    'P-value': '{:.4f}',
                    'R²': '{:.4f}'
                }).background_gradient(subset=['R²'], cmap='YlGn'),
                use_container_width=True
            )
            
            # Highlight top platform
            top_platform = df_multi.iloc[0]
            st.success(f"🏆 **Platform dengan pengaruh tertinggi:** {top_platform['Platform']} (R² = {top_platform['R²']:.3f})")
        else:
            st.warning("⚠️ Tidak ada hasil regresi yang dapat dihitung")
    
    # Save to session_state untuk halaman Conclusion
    st.session_state['regression_summary'] = {
        "global": {
            "slope": float(slope),
            "intercept": float(intercept),
            "r": float(corr),
            "R2": float(r_sq),
            "p_value": float(p_value)
        },
        "per_platform": multi_results
    }
    
    st.markdown("---")


def page_conclusion():
    """
    Conclusion & Key Insights
    """
    st.title("🎯 Conclusion & Key Insights")
    st.markdown("---")

    # Ambil hasil regresi dari session_state
    summary = st.session_state.get('regression_summary', None)

    if summary is None:
        st.warning("⚠️ **Hasil regresi belum tersedia.**")
        st.info("Jalankan halaman **Regression Analysis** terlebih dahulu untuk melihat insights.")
        return

    global_res = summary.get('global', {})
    per_platform = summary.get('per_platform', [])

    # Build insights
    insights = []

    # 1. Overall Relationship
    r = global_res.get('r', None)
    R2 = global_res.get('R2', None)
    slope = global_res.get('slope', None)
    p_value = global_res.get('p_value', None)
    
    if r is not None and R2 is not None:
        direction = "**positif**" if slope > 0 else "**negatif**"
        
        if abs(r) >= 0.7:
            strength = "**kuat**"
        elif abs(r) >= 0.5:
            strength = "**cukup kuat**"
        elif abs(r) >= 0.3:
            strength = "**sedang**"
        else:
            strength = "**lemah**"
        
        signif_text = "signifikan secara statistik" if p_value < 0.05 else "tidak signifikan secara statistik"
        
        insights.append(
            f"Terdapat hubungan {direction} antara total jam penggunaan media sosial dan skor kesehatan mental "
            f"(Pearson r = {r:.3f}, R² = {R2:.3f}). Kekuatan hubungan tergolong {strength} dan {signif_text} "
            f"(p-value = {p_value:.4f})."
        )

    # 2. Top Platform by R²
    if per_platform and len(per_platform) > 0:
        df_plat = pd.DataFrame(per_platform)
        top = df_plat.sort_values('R²', ascending=False).iloc[0]
        
        insights.append(
            f"Platform dengan pengaruh **terbesar** terhadap variasi skor kesehatan mental adalah "
            f"**{top['Platform']}** (R² = {top['R²']:.3f}). Interpretasi: pengaruhnya tergolong "
            f"**{top['Kekuatan'].lower()}** dan **{top['Signifikansi'].lower()}**."
        )
        
        # 3. Significant Platforms
        sigs = df_plat[df_plat['Signifikansi'] == 'Signifikan']
        if not sigs.empty:
            sig_list = ", ".join(sigs['Platform'].tolist())
            insights.append(
                f"Platform yang menunjukkan pengaruh **signifikan** (p < 0.05): **{sig_list}**. "
                f"Penggunaan platform ini perlu mendapat perhatian khusus dalam konteks kesehatan mental."
            )
        else:
            insights.append(
                "Tidak ada platform individual yang menunjukkan pengaruh signifikan secara statistik (p < 0.05) "
                "terhadap skor kesehatan mental."
            )

    # 4. Practical Recommendations
    if R2 is not None:
        if R2 > 0.25:
            insights.append(
                "Efek penggunaan media sosial terhadap kesehatan mental cukup jelas berdasarkan data ini (R² > 0.25). "
                "**Rekomendasi:** Pertimbangkan program pembatasan waktu screen time, kampanye literasi digital, "
                "dan edukasi tentang penggunaan media sosial yang sehat."
            )
        else:
            insights.append(
                "Efek penggunaan media sosial terhadap kesehatan mental relatif lemah menurut data ini (R² < 0.25). "
                "Ini menunjukkan bahwa faktor lain (genetik, lingkungan sosial, kondisi ekonomi, dll) "
                "kemungkinan memiliki peran yang lebih besar terhadap kesehatan mental."
            )

    # 5. General Advice
    insights.append(
        "**Saran praktis untuk pengguna media sosial:**\n"
        "- Batasi durasi penggunaan maksimal 3-4 jam per hari\n"
        "- Hindari scrolling media sosial sebelum tidur (minimal 1 jam sebelum)\n"
        "- Aktifkan fitur \"screen time reminder\" atau \"digital wellbeing\"\n"
        "- Lakukan \"digital detox\" secara berkala (1 hari per minggu tanpa medsos)\n"
        "- Konsultasi dengan profesional jika mengalami gejala gangguan mental yang persisten"
    )

    # Display Insights
    st.subheader("💡 Key Insights")
    
    for idx, insight in enumerate(insights, 1):
        with st.container(border=True):
            st.markdown(f"### {idx}. {insight}")
    
    # Download Option
    st.markdown("---")
    report_text = "\n\n".join([f"{i}. {txt}" for i, txt in enumerate(insights, 1)])
    report_text = f"CONCLUSION & KEY INSIGHTS\n{'='*50}\n\n{report_text}"
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.success("✅ **Insights berhasil** Anda dapat mengedit manual jika diperlukan.")
    with col2:
        st.download_button(
            "📥 Download (TXT)",
            report_text,
            "insights_regression.txt",
            "text/plain",
            use_container_width=True
        )
    
    # Additional Summary Table
    st.markdown("---")
    st.subheader("📊 Summary Statistics")
    
    summary_data = {
        "Metrik": ["Pearson Correlation (r)", "R² (Coefficient of Determination)", "P-value", "Slope (β)", "Intercept (α)"],
        "Nilai": [
            f"{r:.4f}" if r else "N/A",
            f"{R2:.4f}" if R2 else "N/A",
            f"{p_value:.4f}" if p_value else "N/A",
            f"{slope:.4f}" if slope else "N/A",
            f"{global_res.get('intercept', 'N/A'):.4f}"
        ],
        "Interpretasi": [
            "Kekuatan korelasi linier",
            "Proporsi variasi Y yang dijelaskan oleh X",
            "Signifikansi statistik (< 0.05 = signifikan)",
            "Perubahan Y untuk setiap peningkatan 1 unit X",
            "Nilai Y saat X = 0"
        ]
    }
    
    st.dataframe(pd.DataFrame(summary_data), use_container_width=True, hide_index=True)

# ================================================================
# MAIN NAVIGATION
# ================================================================

def main():
    """Main application with navigation"""
    
    st.sidebar.title(PAGE_CONFIG['page_title'])
    st.sidebar.markdown(f"**{TEAM_INFO['project_name']}**")
    st.sidebar.markdown("---")
    
    st.sidebar.success("Pilih Halaman:")
    if st.sidebar.checkbox("Home"):
        page_home()
    if st.sidebar.checkbox("Data Mentah"):
        page_data_mentah()
    if st.sidebar.checkbox("Usage Dashboard"):
        page_usage_dashboard()
    if st.sidebar.checkbox("Mental Health Dashboard"):
        page_mental_health()
    if st.sidebar.checkbox("Demographic Analysis"):
        page_demographic()
    if st.sidebar.checkbox("Regression Analysis"):
        page_regression()
    if st.sidebar.checkbox("Conclusion"):
        page_conclusion()

if __name__ == "__main__":
    main()
