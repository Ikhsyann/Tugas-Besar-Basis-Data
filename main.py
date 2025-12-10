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
    page_title=PAGE_CONFIG['title'],
    page_icon=PAGE_CONFIG['icon'],
    layout=PAGE_CONFIG['layout'],
    initial_sidebar_state=PAGE_CONFIG['sidebar_state']
)

# ================================================================
# HELPER FUNCTIONS
# ================================================================

@st.cache_data
def convert_df_to_csv(df):
    """Convert DataFrame to CSV for download (dosen pattern)"""
    return df.to_csv(index=False).encode('utf-8')

def show_database_status():
    """Show database connection status in sidebar"""
    db = Database()
    success, message = db.test_connection()
    
    if success:
        st.sidebar.success(f"✅ {message}")
    else:
        st.sidebar.error(f"❌ {message}")
    
    db.disconnect()

def show_team_info():
    """Display team member information"""
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 👥 Tim Pengembang")
    
    for member, info in TEAM_INFO.items():
        with st.sidebar.expander(f"{info['icon']} {member}"):
            st.markdown(f"**Jobdesk:** {info['jobdesk']}")
            if 'tasks' in info:
                st.markdown("**Tasks:**")
                for task in info['tasks']:
                    st.markdown(f"- {task}")

# ================================================================
# PAGE: HOME / OVERVIEW
# ================================================================

def page_home():
    """Homepage with project overview and quick statistics"""
    
    st.title("🏠 Dashboard Overview")
    st.markdown("---")
    
    # Project Introduction
    st.markdown(TEXT_CONTENT['intro'])
    
    # Objectives
    st.subheader("🎯 Objektif Penelitian")
    for i, obj in enumerate(TEXT_CONTENT['objectives'], 1):
        st.markdown(f"{i}. {obj}")
    
    # Get summary statistics
    db = Database()
    db.connect()
    stats = db.get_summary_statistics()
    df_responden = db.get_all_respondents()
    db.disconnect()
    
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
                color_discrete_sequence=COLOR_PALETTE['gender']
            )
            st.plotly_chart(fig_gender, use_container_width=True)
        
        with col2:
            # Age distribution histogram
            fig_age = px.histogram(
                df_responden,
                x='usia',
                nbins=20,
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
    Data Mentah & Preprocessing Dashboard
    Jobdesk: NABIL
    
    TODO untuk Nabil:
    1. Tampilkan tabel data responden dengan filter
    2. Tambahkan search box untuk cari nama
    3. Tambahkan dropdown untuk pilih responden spesifik
    4. Tampilkan detail lengkap responden yang dipilih
    5. Tambahkan fitur download CSV
    """
    
    st.title("📊 Data Mentah & Preprocessing")
    st.markdown("**Jobdesk: Nabil**")
    st.markdown("---")
    
    # TODO: Ambil data dari database
    # db = Database()
    # db.connect()
    # data = db.view_all_respondents()
    # db.disconnect()
    
    # TODO: Buat DataFrame dari data
    
    # TODO: Tampilkan metrics (Total Responden, Gender Distribution, Age Range)
    
    # TODO: Buat sidebar filter (usia, gender, status hubungan)
    
    # TODO: Tampilkan tabel dengan multiselect kolom
    
    # TODO: Tambahkan search box
    
    # TODO: Tambahkan dropdown pilih responden
    
    # TODO: Tampilkan detail responden yang dipilih
    
    # TODO: Tambahkan download CSV button
    
    st.info("⚠️ Halaman ini masih dalam pengembangan oleh Nabil")
    st.markdown("""
    **Yang harus dikerjakan:**
    1. Filter data responden (usia, gender, status)
    2. Search box untuk cari nama
    3. Dropdown pilih responden
    4. Tampilkan detail lengkap
    5. Download CSV
    """)

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
    
    # Get data using cursor pattern (dosen style)
    db = Database()
    db.connect()
    usage_data = db.view_usage_with_details()
    db.disconnect()
    
    # Convert to DataFrame with proper column names
    df_usage = pd.DataFrame(usage_data, columns=COLUMN_DEFINITIONS['usage_with_details'])
    
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
        total_users = df_usage['Nama Responden'].nunique()
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
    fig_bar.update_layout(height=CHART_CONFIG['height'])
    st.plotly_chart(fig_bar, use_container_width=True)
    
    # Visualization 2: Pie Chart - Platform Paling Populer
    st.subheader("📊 Platform Paling Populer (by User Count)")
    
    platform_popularity = df_usage['Nama Platform'].value_counts()
    
    fig_pie = px.pie(
        values=platform_popularity.values,
        names=platform_popularity.index,
        title="Distribusi Pengguna per Platform",
        color_discrete_sequence=COLOR_PALETTE['platforms']
    )
    st.plotly_chart(fig_pie, use_container_width=True)
    
    # Visualization 3: Bar Chart - Frekuensi Buka per Platform
    st.subheader("📊 Frekuensi Buka Aplikasi per Platform")
    
    platform_frequency = df_usage.groupby('Nama Platform')['Frekuensi Buka'].mean().sort_values(ascending=False)
    
    fig_freq = px.bar(
        x=platform_frequency.index,
        y=platform_frequency.values,
        labels={'x': 'Platform', 'y': 'Rata-rata Frekuensi Buka per Hari'},
        title="Rata-rata Frekuensi Buka per Platform",
        color=platform_frequency.values,
        color_continuous_scale='Greens'
    )
    fig_freq.update_layout(height=CHART_CONFIG['height'])
    st.plotly_chart(fig_freq, use_container_width=True)
    
    # Visualization 4: Box Plot - Distribusi Jam Penggunaan
    st.subheader("📊 Analisis 2: Distribusi Jam Penggunaan per Platform")
    
    fig_box = px.box(
        df_usage,
        x='Nama Platform',
        y='Jam per Hari',
        title="Box Plot: Distribusi Jam Penggunaan per Platform",
        color='Nama Platform',
        color_discrete_sequence=COLOR_PALETTE['platforms']
    )
    fig_box.update_layout(height=CHART_CONFIG['height'])
    st.plotly_chart(fig_box, use_container_width=True)
    
    # Visualization 5: Histogram - Sebaran Jam Penggunaan
    st.subheader("📊 Histogram: Sebaran Jam Penggunaan Harian")
    
    fig_hist = px.histogram(
        df_usage,
        x='Jam per Hari',
        nbins=30,
        title="Distribusi Jam Penggunaan Harian (Semua Platform)",
        color_discrete_sequence=[COLOR_PALETTE['primary']]
    )
    fig_hist.update_layout(height=CHART_CONFIG['height'])
    st.plotly_chart(fig_hist, use_container_width=True)
    
    # Data Table with column selection (dosen pattern)
    st.markdown("---")
    st.subheader("📋 Detail Data Penggunaan Platform")
    
    # Multiselect untuk pilih kolom yang ditampilkan
    all_columns = df_usage.columns.tolist()
    selected_columns = st.multiselect(
        "Pilih kolom yang ingin ditampilkan:",
        options=all_columns,
        default=['Nama Responden', 'Nama Platform', 'Jam per Hari', 'Tujuan Penggunaan', 'Frekuensi Buka']
    )
    
    if selected_columns:
        st.dataframe(df_usage[selected_columns], use_container_width=True)
        
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
    
    # Sidebar
    st.sidebar.title("🧭 Navigation")
    
    # Database status indicator
    show_database_status()
    
    # Team info
    show_team_info()
    
    st.sidebar.markdown("---")
    
    # Page navigation using radio buttons (dosen pattern)
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
    elif page == "usage":
        page_usage_dashboard()
    elif page == "mental_health":
        page_mental_health()
    elif page == "demographic":
        page_demographic()
    elif page == "regression":
        page_regression()
    elif page == "conclusion":
        page_conclusion()
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📝 Project Info")
    st.sidebar.info("""
    **The Effects of Social Media on Mental Health**
    
    Database: UAS_Basdat  
    Total Responden: 100  
    Total Platform: 9
    """)

if __name__ == "__main__":
    main()