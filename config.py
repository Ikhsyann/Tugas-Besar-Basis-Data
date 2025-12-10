"""
Configuration Module
Contains all configuration settings for the Streamlit dashboard
"""

# Database connection configuration
DB_CONFIG = {
    'host': '127.0.0.1',
    'user': 'root',
    'database': 'uas_basdat',
    'password': ''
}

# Column definitions for DataFrame display
COLUMN_DEFINITIONS = {
    'responden': ["id_responden", "nama", "usia", "jenis_kelamin", "status_hubungan", "pekerjaan", "menggunakan_medsos"],
    'usage_with_details': ["id_penggunaan", "id_responden", "nama_responden", "usia", "jenis_kelamin", "id_platform", "nama_platform", "jam_per_hari", "tujuan_penggunaan", "frekuensi_buka_per_hari"],
    'mental_health': ["id_kesehatan", "id_responden", "gangguan_fokus", "gelisah", "kecemasan", "kesulitan_konsentrasi", "perbandingan_diri", "sentimen_posting", "mencari_validasi", "depresi", "fluktuasi_minat", "sulit_tidur"]
}

# Page Configuration
PAGE_CONFIG = {
    'page_title': 'Mental Health Survey Dashboard - UAS Basis Data',
    'page_icon': '🧠',
    'layout': 'wide',
    'initial_sidebar_state': 'expanded'
}

# Team Information
TEAM_INFO = {
    'project_name': 'The Effects of Social Media on Mental Health',
    'course': 'UAS Basis Data',
    'members': {
        'Nabil': 'Data Mentah & Data Preparation',
        'Ikhsyan': 'Usage Dashboard',
        'Aji': 'Mental Health Dashboard',
        'Vera': 'Demographic Effects',
        'Nazwa': 'Regression & Conclusion'
    }
}

# Color Schemes for Visualizations
COLOR_PALETTE = {
    'primary': '#1f77b4',
    'secondary': '#ff7f0e',
    'success': '#2ca02c',
    'danger': '#d62728',
    'warning': '#ffbb00',
    'info': '#17a2b8',
    'platforms': [
        '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
        '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'
    ],
    'gradient': ['#0d47a1', '#1976d2', '#42a5f5', '#90caf9', '#bbdefb'],
    'mental_health': {
        'low': '#2ca02c',      # Green (1-2)
        'medium': '#ffbb00',    # Yellow (3)
        'high': '#ff7f0e',      # Orange (4)
        'severe': '#d62728'     # Red (5)
    }
}

# Chart Configuration
CHART_CONFIG = {
    'bar_chart': {
        'height': 400,
        'color': COLOR_PALETTE['primary'],
        'use_container_width': True
    },
    'pie_chart': {
        'height': 400,
        'hole': 0.4,  # For donut chart
        'colors': COLOR_PALETTE['platforms']
    },
    'box_plot': {
        'height': 500,
        'colors': COLOR_PALETTE['platforms']
    },
    'histogram': {
        'height': 400,
        'nbins': 20,
        'color': COLOR_PALETTE['secondary']
    },
    'radar_chart': {
        'height': 500,
        'fill': 'toself',
        'colors': COLOR_PALETTE['platforms']
    },
    'heatmap': {
        'height': 600,
        'colorscale': 'RdYlGn_r'  # Red-Yellow-Green reversed
    },
    'scatter': {
        'height': 500,
        'colors': COLOR_PALETTE['platforms']
    }
}

# Mental Health Attributes (Indonesian)
MENTAL_HEALTH_ATTRIBUTES = {
    'gangguan_fokus': 'Gangguan Fokus',
    'gelisah': 'Gelisah',
    'kecemasan': 'Kecemasan',
    'kesulitan_konsentrasi': 'Kesulitan Konsentrasi',
    'perbandingan_diri': 'Perbandingan Diri',
    'sentimen_posting': 'Sentimen Posting',
    'mencari_validasi': 'Mencari Validasi',
    'depresi': 'Depresi',
    'fluktuasi_minat': 'Fluktuasi Minat',
    'sulit_tidur': 'Sulit Tidur'
}

# Platform List
PLATFORMS = [
    'Facebook', 'Twitter', 'Instagram', 'YouTube', 'Discord',
    'Reddit', 'Snapchat', 'Pinterest', 'TikTok'
]

# Filter Options
FILTER_CONFIG = {
    'min_age': 17,
    'max_age': 45,
    'gender_options': ['Semua', 'Laki-laki', 'Perempuan'],
    'status_options': [
        'Semua',
        'Belum Kawin',
        'Kawin',
        'Cerai Hidup',
        'Cerai Mati'
    ],
    'job_options': [
        'Semua',
        'Mahasiswa',
        'Pelajar',
        'Pekerja',
        'Pensiunan'
    ],
    'purpose_options': [
        'Semua',
        'Hiburan',
        'Komunikasi',
        'Informasi',
        'Pekerjaan',
        'Lainnya'
    ],
    'medsos_options': [
        'Semua',
        'Ya',
        'Tidak'
    ]
}

# Data Processing Configuration
DATA_CONFIG = {
    'decimal_places': 2,
    'percentage_format': '{:.2f}%',
    'hour_format': '{:.1f} jam',
    'frequency_format': '{:.0f}x',
    'cache_ttl': 300  # Cache time-to-live in seconds (5 minutes)
}

# Export Configuration
EXPORT_CONFIG = {
    'csv_encoding': 'utf-8',
    'excel_engine': 'openpyxl',
    'date_format': '%Y-%m-%d %H:%M:%S'
}

# Error Messages
ERROR_MESSAGES = {
    'db_connection': '❌ Gagal terhubung ke database. Periksa konfigurasi database Anda.',
    'no_data': '⚠️ Tidak ada data yang tersedia.',
    'query_error': '❌ Terjadi kesalahan saat mengambil data.',
    'invalid_filter': '⚠️ Filter yang dipilih tidak valid.',
    'empty_result': 'ℹ️ Tidak ada data yang sesuai dengan filter yang dipilih.'
}

# Success Messages
SUCCESS_MESSAGES = {
    'data_loaded': '✅ Data berhasil dimuat',
    'export_success': '✅ Data berhasil diekspor',
    'filter_applied': '✅ Filter berhasil diterapkan'
}

# Info Messages
INFO_MESSAGES = {
    'loading': '⏳ Memuat data...',
    'processing': '⏳ Memproses data...',
    'exporting': '⏳ Mengekspor data...'
}

# Navigation Pages
PAGES = {
    'home': '🏠 Home / Overview',
    'data_mentah': '📊 Data Mentah',
    'usage_dashboard': '📱 Usage Dashboard',
    'mental_health': '🧠 Mental Health Dashboard',
    'demographic': '👥 Demographic Effects',
    'regression': '📈 Regression & Correlation',
    'conclusion': '💡 Conclusion & Insight'
}

# Statistical Analysis Configuration
STATS_CONFIG = {
    'confidence_level': 0.95,
    'show_outliers': True,
    'outlier_method': 'IQR',  # Interquartile Range
    'iqr_multiplier': 1.5
}

# Text Content for Pages
TEXT_CONTENT = {
    'home_intro': """
    Dashboard ini merupakan hasil analisis dari survey mengenai **Pengaruh Media Sosial terhadap Kesehatan Mental**.
    Data dikumpulkan dari 100 responden dengan berbagai latar belakang usia, pekerjaan, dan pola penggunaan media sosial.
    """,
    'home_objective': """
    **Tujuan Penelitian:**
    - Menganalisis pola penggunaan media sosial di berbagai platform
    - Mengevaluasi kondisi kesehatan mental responden
    - Mengidentifikasi korelasi antara penggunaan media sosial dan kesehatan mental
    - Memberikan insight untuk penggunaan media sosial yang lebih sehat
    """,
    'data_source': 'Data bersumber dari survey yang dilakukan pada tahun 2025',
    'disclaimer': '⚠️ Data yang ditampilkan adalah data dummy untuk keperluan demonstrasi UAS Basis Data'
}

# Insight Templates (for Nazwa's section)
INSIGHT_CATEGORIES = [
    'Platform Usage Patterns',
    'Mental Health Trends',
    'Correlation Findings',
    'Demographic Differences',
    'Key Recommendations'
]
