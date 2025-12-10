"""
Database Connection Module
Handles MySQL database connection for Mental Health Survey Dashboard
"""

import mysql.connector
from mysql.connector import Error
import pandas as pd
from typing import Optional, List, Tuple
from config import DB_CONFIG    


class Database:
    """Database connection and query handler"""
    
    def __init__(self, host: str = "localhost", user: str = "root", 
                 password: str = "", database: str = "uas_basdat"):
        """
        Initialize database connection parameters
        
        Args:
            host: MySQL server host
            user: MySQL username
            password: MySQL password
            database: Database name
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None
    
    def connect(self) -> bool:
        """
        Establish connection to MySQL database
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                self.cursor = self.connection.cursor()
                return True
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return False
    
    def disconnect(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection and self.connection.is_connected():
            self.connection.close()
    
    def execute_query(self, query: str, params: tuple = None) -> Optional[pd.DataFrame]:
        """
        Execute SELECT query and return results as pandas DataFrame
        
        Args:
            query: SQL query string
            params: Query parameters for prepared statements
            
        Returns:
            DataFrame with query results or None if error
        """
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
            
            df = pd.read_sql(query, self.connection, params=params)
            return df
        except Error as e:
            print(f"Error executing query: {e}")
            return None
    
    def test_connection(self) -> Tuple[bool, str]:
        """
        Test database connection and return status
        
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            if self.connect():
                cursor = self.connection.cursor()
                cursor.execute("SELECT DATABASE()")
                db_name = cursor.fetchone()[0]
                cursor.close()
                return True, f"Connected to database: {db_name}"
            else:
                return False, "Failed to connect to database"
        except Error as e:
            return False, f"Connection error: {str(e)}"
    
    def get_table_info(self) -> Optional[pd.DataFrame]:
        """
        Get information about all tables in database
        
        Returns:
            DataFrame with table names and row counts
        """
        query = """
        SELECT 
            TABLE_NAME as table_name,
            TABLE_ROWS as row_count
        FROM information_schema.TABLES
        WHERE TABLE_SCHEMA = %s
        ORDER BY TABLE_NAME
        """
        return self.execute_query(query, (self.database,))
    
    # ================================================================
    # BASIC DATA RETRIEVAL METHODS (For all team members)
    # ================================================================
    
    def get_all_respondents(self) -> Optional[pd.DataFrame]:
        """
        Get all respondents data
        
        Returns:
            DataFrame with all responden records
        """
        query = """
        SELECT 
            id_responden,
            nama,
            usia,
            jenis_kelamin,
            status_hubungan,
            pekerjaan,
            menggunakan_medsos
        FROM responden
        ORDER BY id_responden
        """
        return self.execute_query(query)
    
    def view_all_respondents(self):
        """
        Get all respondents using cursor (dosen pattern)
        
        Returns:
            List of tuples with respondent data
        """
        if not self.cursor:
            self.connect()
        self.cursor.execute('SELECT * FROM responden ORDER BY nama ASC')
        return self.cursor.fetchall()
    
    def get_all_platforms(self) -> Optional[pd.DataFrame]:
        """
        Get all platforms
        
        Returns:
            DataFrame with platform data
        """
        query = """
        SELECT id_platform, nama_platform
        FROM master_platform
        ORDER BY nama_platform
        """
        return self.execute_query(query)
    
    def view_usage_with_details(self):
        """
        Get usage data with responden and platform details (dosen JOIN pattern)
        
        Returns:
            List of tuples with complete usage information
        """
        if not self.cursor:
            self.connect()
        self.cursor.execute('''
            SELECT 
                pp.id_penggunaan,
                pp.id_responden,
                r.nama AS nama_responden,
                r.usia,
                r.jenis_kelamin,
                pp.id_platform,
                mp.nama_platform,
                pp.jam_per_hari,
                pp.tujuan_penggunaan,
                pp.frekuensi_buka_per_hari
            FROM 
                penggunaan_per_platform pp
            JOIN 
                responden r ON pp.id_responden = r.id_responden
            JOIN 
                master_platform mp ON pp.id_platform = mp.id_platform
            ORDER BY 
                r.nama ASC, mp.nama_platform ASC
        ''')
        return self.cursor.fetchall()
    
    def get_all_usage_data(self) -> Optional[pd.DataFrame]:
        """
        Get all platform usage data
        
        Returns:
            DataFrame with usage data
        """
        query = """
        SELECT 
            pp.id_penggunaan,
            pp.id_responden,
            r.nama,
            pp.id_platform,
            mp.nama_platform,
            pp.jam_per_hari,
            pp.tujuan_penggunaan,
            pp.frekuensi_buka_per_hari
        FROM penggunaan_per_platform pp
        JOIN responden r ON pp.id_responden = r.id_responden
        JOIN master_platform mp ON pp.id_platform = mp.id_platform
        ORDER BY pp.id_responden, mp.nama_platform
        """
        return self.execute_query(query)
    
    def get_all_mental_health_data(self) -> Optional[pd.DataFrame]:
        """
        Get all mental health data
        
        Returns:
            DataFrame with mental health records
        """
        query = """
        SELECT 
            km.id_kesehatan,
            km.id_responden,
            r.nama,
            km.gangguan_fokus,
            km.gelisah,
            km.kecemasan,
            km.kesulitan_konsentrasi,
            km.perbandingan_diri,
            km.sentimen_posting,
            km.mencari_validasi,
            km.depresi,
            km.fluktuasi_minat,
            km.sulit_tidur
        FROM kesehatan_mental km
        JOIN responden r ON km.id_responden = r.id_responden
        ORDER BY km.id_responden
        """
        return self.execute_query(query)
    
    def get_master_dataframe(self) -> Optional[pd.DataFrame]:
        """
        Get complete master dataframe with all joins
        This will be used by Nabil for data preparation
        
        Returns:
            DataFrame with all data joined
        """
        query = """
        SELECT 
            r.id_responden,
            r.nama,
            r.usia,
            r.jenis_kelamin,
            r.status_hubungan,
            r.pekerjaan,
            r.menggunakan_medsos,
            mp.id_platform,
            mp.nama_platform,
            pp.jam_per_hari,
            pp.tujuan_penggunaan,
            pp.frekuensi_buka_per_hari,
            km.gangguan_fokus,
            km.gelisah,
            km.kecemasan,
            km.kesulitan_konsentrasi,
            km.perbandingan_diri,
            km.sentimen_posting,
            km.mencari_validasi,
            km.depresi,
            km.fluktuasi_minat,
            km.sulit_tidur
        FROM responden r
        LEFT JOIN penggunaan_per_platform pp ON r.id_responden = pp.id_responden
        LEFT JOIN master_platform mp ON pp.id_platform = mp.id_platform
        LEFT JOIN kesehatan_mental km ON r.id_responden = km.id_responden
        ORDER BY r.id_responden, mp.nama_platform
        """
        return self.execute_query(query)
    
    def get_summary_statistics(self) -> dict:
        """
        Get summary statistics for dashboard overview

        Returns:
            Dictionary with summary stats
        """
        stats = {}

        # Total responden
        query = "SELECT COUNT(*) as total FROM responden"
        result = self.execute_query(query)
        stats['total_responden'] = int(result['total'].iloc[0]) if result is not None else 0

        # Total platform
        query = "SELECT COUNT(*) as total FROM master_platform"
        result = self.execute_query(query)
        stats['total_platform'] = int(result['total'].iloc[0]) if result is not None else 0

        # Rata-rata jam penggunaan
        query = "SELECT AVG(jam_per_hari) as avg_jam FROM penggunaan_per_platform"
        result = self.execute_query(query)
        stats['avg_jam_penggunaan'] = float(result['avg_jam'].iloc[0]) if result is not None else 0

        # Rata-rata kesehatan mental (semua atribut)
        query = """
        SELECT 
            AVG((gangguan_fokus + gelisah + kecemasan + kesulitan_konsentrasi + 
                perbandingan_diri + mencari_validasi + depresi + 
                fluktuasi_minat + sulit_tidur) / 9.0) as avg_mental_health
        FROM kesehatan_mental
        """
        result = self.execute_query(query)
        stats['avg_mental_health'] = float(result['avg_mental_health'].iloc[0]) if result is not None else 0

        return stats
    
    # ================================================================
    # VERA: DEMOGRAPHIC EFFECTS ANALYSIS METHODS
    # ================================================================
    
    def get_gender_comparison_data(self) -> Tuple[Optional[pd.DataFrame], Optional[pd.DataFrame], Optional[pd.DataFrame]]:
        """
        Get all data required for Gender Comparison (Metrics, Radar, Favorite Platform)
        
        Returns:
            Tuple of (metrics_df, radar_df, favorit_df)
        """
        
        # 1. Query untuk Metrik Rata-rata (Jam, Depresi, Kecemasan)
        SQL_METRICS = """
        SELECT
            r.jenis_kelamin,
            AVG(p.jam_per_hari) AS avg_jam_guna,
            AVG(km.depresi) AS avg_depresi,
            AVG(km.kecemasan) AS avg_kecemasan
        FROM
            responden r
        JOIN
            penggunaan_per_platform p ON r.id_responden = p.id_responden
        JOIN
            kesehatan_mental km ON r.id_responden = km.id_responden
        GROUP BY
            r.jenis_kelamin;
        """

        # 2. Query untuk Radar Chart (Semua skor Mental Health)
        SQL_RADAR = """
        SELECT
            r.jenis_kelamin,
            AVG(km.gangguan_fokus) AS Fokus,
            AVG(km.gelisah) AS Gelisah,
            AVG(km.kecemasan) AS Kecemasan,
            AVG(km.kesulitan_konsentrasi) AS Konsentrasi,
            AVG(km.perbandingan_diri) AS Banding_Diri,
            AVG(km.mencari_validasi) AS Validasi,
            AVG(km.depresi) AS Depresi,
            AVG(km.sulit_tidur) AS Sulit_Tidur
        FROM
            responden r
        JOIN
            kesehatan_mental km ON r.id_responden = km.id_responden
        GROUP BY
            r.jenis_kelamin;
        """

        # 3. Query untuk Platform Favorit (Mencari platform dengan total frekuensi tertinggi per gender)
        SQL_FAVORIT = """
        WITH RankedUsage AS (
            SELECT
                r.jenis_kelamin,
                mp.nama_platform,
                SUM(p.frekuensi_buka_per_hari) AS total_frekuensi,
                ROW_NUMBER() OVER (PARTITION BY r.jenis_kelamin ORDER BY SUM(p.frekuensi_buka_per_hari) DESC) AS rank_num
            FROM
                responden r
            JOIN
                penggunaan_per_platform p ON r.id_responden = p.id_responden
            JOIN
                master_platform mp ON p.id_platform = mp.id_platform
            GROUP BY
                r.jenis_kelamin, mp.nama_platform
        )
        SELECT
            jenis_kelamin,
            nama_platform AS platform_favorit
        FROM
            RankedUsage
        WHERE
            rank_num = 1;
        """
        
        # Eksekusi semua query
        metrics_df = self.execute_query(SQL_METRICS)
        radar_df = self.execute_query(SQL_RADAR)
        favorit_df = self.execute_query(SQL_FAVORIT)
        
        return metrics_df, radar_df, favorit_df
    
    def get_status_comparison_data(self) -> Tuple[Optional[pd.DataFrame], Optional[pd.DataFrame]]:
        """
        Get all data required for Relationship Status Comparison (Donut Chart, Detail Table)
        
        Returns:
            Tuple of (depression_df, detail_df)
        """
    
        # 1. Query untuk Rata-rata Depresi per Status (untuk Donut Chart)
        SQL_DEPRESSION = """
        SELECT
            status_hubungan,
            AVG(km.depresi) AS avg_depresi
        FROM
            responden r
        JOIN
            kesehatan_mental km ON r.id_responden = km.id_responden
        GROUP BY
            status_hubungan;
        """

        # 2. Query untuk Detail Rata-rata Mental Health per Status (untuk Tabel Detail)
        SQL_DETAIL = """
        SELECT
            r.status_hubungan,
            AVG(km.depresi) AS Depresi,
            AVG(km.kecemasan) AS Kecemasan,
            AVG(km.gelisah) AS Gelisah,
            AVG(km.sulit_tidur) AS Sulit_Tidur,
            AVG(km.perbandingan_diri) AS Perbandingan_Diri
        FROM
            responden r
        JOIN
            kesehatan_mental km ON r.id_responden = km.id_responden
        GROUP BY
            r.status_hubungan
        ORDER BY
            AVG(km.depresi) DESC;
        """
        
        depression_df = self.execute_query(SQL_DEPRESSION)
        detail_df = self.execute_query(SQL_DETAIL)
        
        return depression_df, detail_df
