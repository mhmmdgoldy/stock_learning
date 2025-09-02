# i18n.py - Internationalization for Streamlit Finance Webapp

# Translation dictionary for all UI text
T = {
    # Navigation
    'Homepage': {'en': 'Homepage', 'id': 'Beranda'},
    'Stock Overview': {'en': 'Stock Overview', 'id': 'Ringkasan Saham'},
    'Fundamental Overview': {'en': 'Fundamental Overview', 'id': 'Ringkasan Fundamental'},
    'Syaria Stock Overview': {'en': 'Syaria Stock Overview', 'id': 'Ringkasan Saham Syariah'},
    'Analysis': {'en': 'Analysis', 'id': 'Analisis'},
    # Homepage
    'Welcome to the Finance Webapp!': {'en': 'Welcome to the Finance Webapp!', 'id': 'Selamat datang di Webapp Keuangan!'},
    'This website provides:': {'en': 'This website provides:', 'id': 'Website ini menyediakan:'},
    'Stock data visualization (line/candlestick)': {'en': 'Stock data visualization (line/candlestick)', 'id': 'Visualisasi data saham (line/candlestick)'},
    'Fundamental metrics': {'en': 'Fundamental metrics', 'id': 'Metrik fundamental'},
    'Sharia (Syariah) stock screening': {'en': 'Sharia (Syariah) stock screening', 'id': 'Penyaringan saham Syariah'},
    'Portfolio analysis (Classic and Hybrid)': {'en': 'Portfolio analysis (Classic and Hybrid)', 'id': 'Analisis portofolio (Klasik dan Hibrida)'},
    # Syariah Table
    'Business Activity': {'en': 'Business Activity', 'id': 'Aktivitas Bisnis'},
    'Non-halal revenue < 10%': {'en': 'Non-halal revenue < 10%', 'id': 'Pendapatan non-halal < 10%'},
    'Interest-based Assets': {'en': 'Interest-based Assets', 'id': 'Aset berbasis bunga'},
    'Non-halal assets < 45%': {'en': 'Non-halal assets < 45%', 'id': 'Aset non-halal < 45%'},
    'Debt Ratio': {'en': 'Debt Ratio', 'id': 'Rasio Utang'},
    'Debt/Asset < 45%': {'en': 'Debt/Asset < 45%', 'id': 'Utang/Aset < 45%'},
    'Criterion': {'en': 'Criterion', 'id': 'Kriteria'},
    'Threshold': {'en': 'Threshold', 'id': 'Ambang Batas'},
    'Value': {'en': 'Value', 'id': 'Nilai'},
    'Result': {'en': 'Result', 'id': 'Hasil'},
    'Pass': {'en': '✅', 'id': '✅'},
    'Fail': {'en': '❌', 'id': '❌'},
    'N/A': {'en': 'N/A', 'id': 'Tidak Tersedia'},
    '✅ SHARIA COMPLIANT': {'en': '✅ SHARIA COMPLIANT', 'id': '✅ SESUAI SYARIAH'},
    '❌ NOT SHARIA COMPLIANT': {'en': '❌ NOT SHARIA COMPLIANT', 'id': '❌ TIDAK SESUAI SYARIAH'},
    'No forbidden business activities (gambling, alcohol, tobacco, conventional finance, etc.)': {'en': 'No forbidden business activities (gambling, alcohol, tobacco, conventional finance, etc.)', 'id': 'Tidak ada aktivitas bisnis terlarang (judi, alkohol, tembakau, keuangan konvensional, dll.)'},
    'Interest-based Debt/Equity < 45% (proxy for Debt/Assets)': {'en': 'Interest-based Debt/Equity < 45% (proxy for Debt/Assets)', 'id': 'Utang berbasis bunga/Ekuitas < 45% (proksi Utang/Aset)'},
    'Interest & other non-halal income / revenue < 10%': {'en': 'Interest & other non-halal income / revenue < 10%', 'id': 'Pendapatan bunga & non-halal lainnya / pendapatan < 10%'},
    # Sectors/Industries
    'Technology': {'en': 'Technology', 'id': 'Teknologi'},
    'Consumer Electronics': {'en': 'Consumer Electronics', 'id': 'Elektronik Konsumen'},
    'Financial Services': {'en': 'Financial Services', 'id': 'Layanan Keuangan'},
    'Healthcare': {'en': 'Healthcare', 'id': 'Kesehatan'},
    'Industrials': {'en': 'Industrials', 'id': 'Industri'},
    'Basic Materials': {'en': 'Basic Materials', 'id': 'Material Dasar'},
    'Consumer Cyclical': {'en': 'Consumer Cyclical', 'id': 'Konsumsi Siklis'},
    'Consumer Defensive': {'en': 'Consumer Defensive', 'id': 'Konsumsi Non-Siklis'},
    'Energy': {'en': 'Energy', 'id': 'Energi'},
    'Utilities': {'en': 'Utilities', 'id': 'Utilitas'},
    'Real Estate': {'en': 'Real Estate', 'id': 'Properti'},
    'Communication Services': {'en': 'Communication Services', 'id': 'Layanan Komunikasi'},
    'Telecommunication': {'en': 'Telecommunication', 'id': 'Telekomunikasi'},
    'Transportation': {'en': 'Transportation', 'id': 'Transportasi'},
    'Software': {'en': 'Software', 'id': 'Perangkat Lunak'},
    'Hardware': {'en': 'Hardware', 'id': 'Perangkat Keras'},
    'Semiconductors': {'en': 'Semiconductors', 'id': 'Semikonduktor'},
    'Banks': {'en': 'Banks', 'id': 'Perbankan'},
    'Insurance': {'en': 'Insurance', 'id': 'Asuransi'},
    'Pharmaceuticals': {'en': 'Pharmaceuticals', 'id': 'Farmasi'},
    'Biotechnology': {'en': 'Biotechnology', 'id': 'Bioteknologi'},
    'Retail': {'en': 'Retail', 'id': 'Ritel'},
    'Automobiles': {'en': 'Automobiles', 'id': 'Otomotif'},
    'Aerospace & Defense': {'en': 'Aerospace & Defense', 'id': 'Dirgantara & Pertahanan'},
    'Metals & Mining': {'en': 'Metals & Mining', 'id': 'Logam & Pertambangan'},
    'Oil & Gas': {'en': 'Oil & Gas', 'id': 'Minyak & Gas'},
    'Chemicals': {'en': 'Chemicals', 'id': 'Kimia'},
    'Food & Beverage': {'en': 'Food & Beverage', 'id': 'Makanan & Minuman'},
    'Household & Personal Products': {'en': 'Household & Personal Products', 'id': 'Produk Rumah Tangga & Pribadi'},
    'Construction': {'en': 'Construction', 'id': 'Konstruksi'},
    'Media': {'en': 'Media', 'id': 'Media'},
    'Entertainment': {'en': 'Entertainment', 'id': 'Hiburan'},
    # Add more as needed
    # Stock Overview
    'Visualize stock prices and general info.': {'en': 'Visualize stock prices and general info.', 'id': 'Visualisasikan harga saham dan info umum.'},
    'Compare Stock': {'en': 'Compare Stock', 'id': 'Bandingkan Saham'},
    'Stock Ticker': {'en': 'Stock Ticker', 'id': 'Kode Saham'},
    'Stock Ticker 1': {'en': 'Stock Ticker 1', 'id': 'Kode Saham 1'},
    'Stock Ticker 2': {'en': 'Stock Ticker 2', 'id': 'Kode Saham 2'},
    'Chart Type': {'en': 'Chart Type', 'id': 'Jenis Grafik'},
    'Interval': {'en': 'Interval', 'id': 'Interval'},
    'Range': {'en': 'Range', 'id': 'Rentang'},
    'Indicator': {'en': 'Indicator', 'id': 'Indikator'},
    'Use custom date range': {'en': 'Use custom date range', 'id': 'Gunakan rentang tanggal khusus'},
    'Start Date': {'en': 'Start Date', 'id': 'Tanggal Mulai'},
    'End Date': {'en': 'End Date', 'id': 'Tanggal Akhir'},
    'Current Price and General Info': {'en': 'Current Price and General Info', 'id': 'Harga Saat Ini dan Info Umum'},
    'Company Description': {'en': 'Company Description', 'id': 'Deskripsi Perusahaan'},
    'No description available.': {'en': 'No description available.', 'id': 'Deskripsi tidak tersedia.'},
    # Fundamental Overview
    'View all available fundamental metrics for a stock.': {'en': 'View all available fundamental metrics for a stock.', 'id': 'Lihat semua metrik fundamental yang tersedia untuk sebuah saham.'},
    'Stock Ticker for Fundamentals': {'en': 'Stock Ticker for Fundamentals', 'id': 'Kode Saham untuk Fundamental'},
    'No fundamental data available.': {'en': 'No fundamental data available.', 'id': 'Data fundamental tidak tersedia.'},
    'Could not retrieve fundamentals:': {'en': 'Could not retrieve fundamentals:', 'id': 'Tidak dapat mengambil data fundamental:'},
    # Syaria Stock Overview
    'Check if a stock is Sharia (Syariah) compliant based on OJK/HISSA-like (HISSA) criteria, using Yahoo Finance data.': {
        'en': 'Check if a stock is Sharia (Syariah) compliant based on OJK/HISSA-like (HISSA) criteria, using Yahoo Finance data.',
        'id': 'Periksa apakah saham memenuhi syariah berdasarkan kriteria OJK/HISSA (HISSA), menggunakan data Yahoo Finance.'
    },
    'Stock Ticker for Syaria Analysis': {'en': 'Stock Ticker for Syaria Analysis', 'id': 'Kode Saham untuk Analisis Syariah'},
    'No syariah data available.': {'en': 'No syariah data available.', 'id': 'Data syariah tidak tersedia.'},
    'Could not retrieve or analyze:': {'en': 'Could not retrieve or analyze:', 'id': 'Tidak dapat mengambil/menganalisis data:'},
    # Portfolio Analysis
    'Portfolio Analysis': {'en': 'Portfolio Analysis', 'id': 'Analisis Portofolio'},
    'Create and analyze your custom stock portfolio. Enter tickers and weights below.': {'en': 'Create and analyze your custom stock portfolio. Enter tickers and weights below.', 'id': 'Buat dan analisis portofolio saham kustom Anda. Masukkan kode saham dan bobot di bawah.'},
    'Portfolio Formation Tool': {'en': 'Portfolio Formation Tool', 'id': 'Alat Pembentukan Portofolio'},
    'Portfolio Construction Method': {'en': 'Portfolio Construction Method', 'id': 'Metode Pembentukan Portofolio'},
    'Historical Data Period': {'en': 'Historical Data Period', 'id': 'Periode Data Historis'},
    'Risk-free rate (annual, %)': {'en': 'Risk-free rate (annual, %)', 'id': 'Tingkat Bebas Risiko (tahunan, %)'},
    'Enter stock tickers (comma separated)': {'en': 'Enter stock tickers (comma separated)', 'id': 'Masukkan kode saham (pisahkan dengan koma)'},
    'Enter weights (comma separated, must sum to 1)': {'en': 'Enter weights (comma separated, must sum to 1)', 'id': 'Masukkan bobot (pisahkan dengan koma, total 1)'},
    'Expected annual return:': {'en': 'Expected annual return:', 'id': 'Ekspektasi return tahunan:'},
    'Expected annual volatility:': {'en': 'Expected annual volatility:', 'id': 'Ekspektasi volatilitas tahunan:'},
    'Sharpe Ratio (risk-free rate': {'en': 'Sharpe Ratio (risk-free rate', 'id': 'Rasio Sharpe (tingkat bebas risiko'},
    'Portfolio Allocation': {'en': 'Portfolio Allocation', 'id': 'Alokasi Portofolio'},
    'This tool uses historical data and allows several portfolio construction methods: Classic and Hybrid.': {'en': 'This tool uses historical data and allows several portfolio construction methods: Classic and Hybrid.', 'id': 'Alat ini menggunakan data historis dan mendukung berbagai metode pembentukan portofolio: Classic dan Hybrid.'},
    'Number of tickers and weights must match, and weights must sum to 1.': {'en': 'Number of tickers and weights must match, and weights must sum to 1.', 'id': 'Jumlah saham dan bobot harus sama, dan bobot harus berjumlah 1.'},
    'Dropped invalid tickers:': {'en': 'Dropped invalid tickers:', 'id': 'Kode saham tidak valid dihapus:'},
    'No valid tickers with price data. Please check your input.': {'en': 'No valid tickers with price data. Please check your input.', 'id': 'Tidak ada kode saham valid dengan data harga. Mohon cek input Anda.'},
    'Could not fetch data or calculate portfolio:': {'en': 'Could not fetch data or calculate portfolio:', 'id': 'Tidak dapat mengambil data atau menghitung portofolio:'},
    # ACO Settings
    'ACO Settings (Advanced)': {'en': 'ACO Settings (Advanced)', 'id': 'Pengaturan ACO (Lanjutan)'},
    'Ants per iteration': {'en': 'Ants per iteration', 'id': 'Jumlah semut per iterasi'},
    'Iterations': {'en': 'Iterations', 'id': 'Jumlah iterasi'},
    'Pheromone evaporation (rho)': {'en': 'Pheromone evaporation (rho)', 'id': 'Evaporasi feromon (rho)'},
    'Dirichlet concentration (alpha0)': {'en': 'Dirichlet concentration (alpha0)', 'id': 'Konsentrasi Dirichlet (alpha0)'},
    'Top-ant fraction': {'en': 'Top-ant fraction', 'id': 'Fraksi semut terbaik'},
    'Random seed': {'en': 'Random seed', 'id': 'Seed acak'},
    #About
    'About Us': {'en': 'About Us', 'id': 'Tentang Kami'},
    'This Project brought to you by:': {'en': 'This Project brought to you by:', 'id': 'Proyek ini dibawa kepada Anda oleh:'},
    'Department of Mathematics Education': {'en': 'Department of Mathematics Education', 'id': 'Departemen Pendidikan Matematika'},
    'Universitas Negeri Yogyakarta': {'en': 'Universitas Negeri Yogyakarta', 'id': 'Universitas Negeri Yogyakarta'},
    'Build with Python Streamlit': {'en': 'Build with Python Streamlit', 'id': 'Dibangun dengan Python Streamlit'},

    # General
    'Language': {'en': 'Language', 'id': 'Bahasa'},
    'Currency': {'en': 'Currency', 'id': 'Mata Uang'},
}

# Current language code (default to 'en')
_current_lang = 'en'

def set_language(lang_code):
    global _current_lang
    _current_lang = lang_code

def get_language():
    return _current_lang

def tr(key):
    """Translate a key to the current language."""
    return T.get(key, {}).get(_current_lang, key)
