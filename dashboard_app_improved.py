import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

# ==================== CẤU HÌNH TRANG ====================
st.set_page_config(
    page_title="Dashboard So sánh 2 CSV - Chất lượng Không khí",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== LOAD DỮ LIỆU TỪ CSV ====================

@st.cache_data
def load_csv_data(filename):
    """
    Tải dữ liệu từ file CSV (GỐC, không xử lý)
    """
    try:
        df = pd.read_csv(filename)
        # Chỉ chuẩn hóa tên cột
        df.columns = df.columns.str.lower().str.strip()
        return df
    except FileNotFoundError:
        st.error(f"❌ Không tìm thấy file: {filename}")
        return None

# ==================== CÁC HÀM VẼ BIỂU ĐỒ SONG SONG ====================

def plot_distributions_comparison(df1, df2, col_name, label1="CSV 1", label2="CSV 2"):
    """Vẽ biểu đồ phân phối 2 CSV song song"""
    if col_name not in df1.columns or col_name not in df2.columns:
        st.warning(f"Cột '{col_name}' không có trong một hoặc cả 2 file CSV")
        return None
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # CSV 1
    try:
        axes[0].hist(df1[col_name].dropna(), bins=40, color='#FF6B6B', alpha=0.7, edgecolor='black')
        axes[0].set_title(f'Phân phối {col_name}\n{label1}', fontsize=12, fontweight='bold')
        axes[0].set_xlabel(col_name, fontsize=10)
        axes[0].set_ylabel('Tần suất', fontsize=10)
        axes[0].grid(axis='y', linestyle='--', alpha=0.5)
    except Exception as e:
        axes[0].text(0.5, 0.5, f"Lỗi: {str(e)}", ha='center', va='center')
    
    # CSV 2
    try:
        axes[1].hist(df2[col_name].dropna(), bins=40, color='#4ECDC4', alpha=0.7, edgecolor='black')
        axes[1].set_title(f'Phân phối {col_name}\n{label2}', fontsize=12, fontweight='bold')
        axes[1].set_xlabel(col_name, fontsize=10)
        axes[1].set_ylabel('Tần suất', fontsize=10)
        axes[1].grid(axis='y', linestyle='--', alpha=0.5)
    except Exception as e:
        axes[1].text(0.5, 0.5, f"Lỗi: {str(e)}", ha='center', va='center')
    
    plt.tight_layout()
    return fig


def plot_boxplots_comparison(df1, df2, col_name, label1="CSV 1", label2="CSV 2"):
    """Vẽ biểu đồ Box Plot 2 CSV song song"""
    if col_name not in df1.columns or col_name not in df2.columns:
        st.warning(f"Cột '{col_name}' không có trong một hoặc cả 2 file CSV")
        return None
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # CSV 1
    try:
        sns.boxplot(y=df1[col_name].dropna(), ax=axes[0], color='#FF6B6B')
        axes[0].set_title(f'Box Plot {col_name}\n{label1}', fontsize=12, fontweight='bold')
        axes[0].set_ylabel(col_name, fontsize=10)
        axes[0].grid(axis='y', linestyle='--', alpha=0.5)
    except Exception as e:
        axes[0].text(0.5, 0.5, f"Lỗi: {str(e)}", ha='center', va='center')
    
    # CSV 2
    try:
        sns.boxplot(y=df2[col_name].dropna(), ax=axes[1], color='#4ECDC4')
        axes[1].set_title(f'Box Plot {col_name}\n{label2}', fontsize=12, fontweight='bold')
        axes[1].set_ylabel(col_name, fontsize=10)
        axes[1].grid(axis='y', linestyle='--', alpha=0.5)
    except Exception as e:
        axes[1].text(0.5, 0.5, f"Lỗi: {str(e)}", ha='center', va='center')
    
    plt.tight_layout()
    return fig


def plot_correlation_heatmap_comparison(df1, df2, label1="CSV 1", label2="CSV 2"):
    """Vẽ heatmap tương quan 2 CSV song song"""
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    # CSV 1
    try:
        corr1 = df1.select_dtypes(include=[np.number]).corr()
        sns.heatmap(corr1, annot=False, cmap='coolwarm', vmin=-1, vmax=1, 
                    ax=axes[0], cbar_kws={'label': 'Correlation'})
        axes[0].set_title(f'Tương quan\n{label1}', fontsize=12, fontweight='bold')
    except Exception as e:
        axes[0].text(0.5, 0.5, f"Lỗi: {str(e)}", ha='center', va='center')
    
    # CSV 2
    try:
        corr2 = df2.select_dtypes(include=[np.number]).corr()
        sns.heatmap(corr2, annot=False, cmap='coolwarm', vmin=-1, vmax=1, 
                    ax=axes[1], cbar_kws={'label': 'Correlation'})
        axes[1].set_title(f'Tương quan\n{label2}', fontsize=12, fontweight='bold')
    except Exception as e:
        axes[1].text(0.5, 0.5, f"Lỗi: {str(e)}", ha='center', va='center')
    
    plt.tight_layout()
    return fig


def plot_statistics_comparison(df1, df2, label1="CSV 1", label2="CSV 2"):
    """Hiển thị thống kê so sánh giữa 2 CSV"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Thống kê CSV 1
    try:
        numeric_df1 = df1.select_dtypes(include=[np.number])
        stats1 = numeric_df1.describe().T[['count', 'mean', 'std', 'min', 'max']]
        
        axes[0].axis('off')
        table1 = axes[0].table(cellText=np.round(stats1.values, 3),
                              colLabels=stats1.columns,
                              rowLabels=stats1.index,
                              cellLoc='center',
                              loc='center',
                              colWidths=[0.12]*5)
        table1.auto_set_font_size(False)
        table1.set_fontsize(8)
        table1.scale(1, 1.5)
        axes[0].set_title(f'Thống kê Mô tả\n{label1}', fontsize=12, fontweight='bold', pad=20)
    except Exception as e:
        axes[0].text(0.5, 0.5, f"Lỗi: {str(e)}", ha='center', va='center')
    
    # Thống kê CSV 2
    try:
        numeric_df2 = df2.select_dtypes(include=[np.number])
        stats2 = numeric_df2.describe().T[['count', 'mean', 'std', 'min', 'max']]
        
        axes[1].axis('off')
        table2 = axes[1].table(cellText=np.round(stats2.values, 3),
                              colLabels=stats2.columns,
                              rowLabels=stats2.index,
                              cellLoc='center',
                              loc='center',
                              colWidths=[0.12]*5)
        table2.auto_set_font_size(False)
        table2.set_fontsize(8)
        table2.scale(1, 1.5)
        axes[1].set_title(f'Thống kê Mô tả\n{label2}', fontsize=12, fontweight='bold', pad=20)
    except Exception as e:
        axes[1].text(0.5, 0.5, f"Lỗi: {str(e)}", ha='center', va='center')
    
    plt.tight_layout()
    return fig


def plot_missing_values_comparison(df1, df2, label1="CSV 1", label2="CSV 2"):
    """Vẽ biểu đồ missing values 2 CSV song song"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # CSV 1
    try:
        missing1 = df1.isnull().sum()
        missing1 = missing1[missing1 > 0].sort_values(ascending=False)
        if len(missing1) > 0:
            axes[0].barh(missing1.index, missing1.values, color='#FF6B6B')
            axes[0].set_title(f'Missing Values\n{label1}', fontsize=12, fontweight='bold')
            axes[0].set_xlabel('Số lượng', fontsize=10)
        else:
            axes[0].text(0.5, 0.5, 'Không có missing values', ha='center', va='center')
            axes[0].set_title(f'Missing Values\n{label1}', fontsize=12, fontweight='bold')
    except Exception as e:
        axes[0].text(0.5, 0.5, f"Lỗi: {str(e)}", ha='center', va='center')
    
    # CSV 2
    try:
        missing2 = df2.isnull().sum()
        missing2 = missing2[missing2 > 0].sort_values(ascending=False)
        if len(missing2) > 0:
            axes[1].barh(missing2.index, missing2.values, color='#4ECDC4')
            axes[1].set_title(f'Missing Values\n{label2}', fontsize=12, fontweight='bold')
            axes[1].set_xlabel('Số lượng', fontsize=10)
        else:
            axes[1].text(0.5, 0.5, 'Không có missing values', ha='center', va='center')
            axes[1].set_title(f'Missing Values\n{label2}', fontsize=12, fontweight='bold')
    except Exception as e:
        axes[1].text(0.5, 0.5, f"Lỗi: {str(e)}", ha='center', va='center')
    
    plt.tight_layout()
    return fig


def plot_timeseries_comparison(df1, df2, col_name, label1="CSV 1", label2="CSV 2"):
    """Vẽ chuỗi thời gian 2 CSV song song"""
    if col_name not in df1.columns or col_name not in df2.columns:
        st.warning(f"Cột '{col_name}' không có trong một hoặc cả 2 file CSV")
        return None
    
    fig, axes = plt.subplots(2, 1, figsize=(14, 8))
    
    # CSV 1
    try:
        axes[0].plot(range(len(df1)), df1[col_name].values, color='#FF6B6B', alpha=0.7, linewidth=1)
        axes[0].set_title(f'Chuỗi thời gian {col_name} - {label1}', fontsize=12, fontweight='bold')
        axes[0].set_ylabel(col_name, fontsize=10)
        axes[0].grid(True, alpha=0.3)
        axes[0].set_xlim(0, len(df1))
    except Exception as e:
        axes[0].text(0.5, 0.5, f"Lỗi: {str(e)}", ha='center', va='center')
    
    # CSV 2
    try:
        axes[1].plot(range(len(df2)), df2[col_name].values, color='#4ECDC4', alpha=0.7, linewidth=1)
        axes[1].set_title(f'Chuỗi thời gian {col_name} - {label2}', fontsize=12, fontweight='bold')
        axes[1].set_ylabel(col_name, fontsize=10)
        axes[1].set_xlabel('Index', fontsize=10)
        axes[1].grid(True, alpha=0.3)
        axes[1].set_xlim(0, len(df2))
    except Exception as e:
        axes[1].text(0.5, 0.5, f"Lỗi: {str(e)}", ha='center', va='center')
    
    plt.tight_layout()
    return fig


# ==================== MAIN APP ====================

st.title("📊 Dashboard So sánh 2 CSV")
st.markdown("Công cụ so sánh và phân tích dữ liệu từ 2 file CSV song song")

# ==================== SIDEBAR ====================
st.sidebar.header("⚙️ Cấu hình")

csv1_file = st.sidebar.text_input(
    "📁 Tên file CSV 1 (trước khi xử lý):", 
    value="hcmc_aqi_dataset_after_preprocess.csv",
    help="Nhập tên file CSV (đặt cùng thư mục với script)"
)

csv2_file = st.sidebar.text_input(
    "📁 Tên file CSV 2 (sau khi xử lý):", 
    value="hcmc_aqi_dataset_before_preprocess.csv",
    help="Nhập tên file CSV (đặt cùng thư mục với script)"
)

# Load dữ liệu
df1 = load_csv_data(csv1_file)
df2 = load_csv_data(csv2_file)

if df1 is None or df2 is None:
    st.error("❌ Không thể tải một hoặc cả 2 file CSV. Vui lòng kiểm tra tên file.")
    st.stop()

# Lấy label từ tên file
label1 = csv1_file.split('.')[0][:30]
label2 = csv2_file.split('.')[0][:30]

st.sidebar.success(f"✅ Loaded: {label1}")
st.sidebar.success(f"✅ Loaded: {label2}")

# ==================== THÔNG TIN DỮ LIỆU ====================
st.sidebar.markdown("---")
st.sidebar.subheader("📈 Thông tin Dữ liệu")

col1, col2 = st.sidebar.columns(2)
with col1:
    st.metric("CSV 1 - Rows", df1.shape[0])
    st.metric("CSV 1 - Cols", df1.shape[1])
with col2:
    st.metric("CSV 2 - Rows", df2.shape[0])
    st.metric("CSV 2 - Cols", df2.shape[1])

# ==================== MENU CHÍNH ====================
st.sidebar.markdown("---")
st.sidebar.subheader("🎯 Chọn Loại Biểu đồ")

analysis_type = st.sidebar.radio(
    "Phân tích:",
    [
        "📊 Tổng quan Dữ liệu",
        "📉 Phân phối (Distribution)",
        "📦 Box Plot - Ngoại lai",
        "🔗 Tương quan (Correlation)",
        "⏱️ Chuỗi Thời gian",
        "👁️ Missing Values"
    ]
)

# ==================== NỘI DUNG CHÍNH ====================

if analysis_type == "📊 Tổng quan Dữ liệu":
    st.header("📊 Tổng quan Dữ liệu")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(f"🔍 {label1}")
        st.info(f"**Shape:** {df1.shape}")
        st.write("**Các cột:**")
        st.write(df1.columns.tolist())
        with st.expander("Xem 5 dòng đầu"):
            st.dataframe(df1.head(), use_container_width=True)
    
    with col2:
        st.subheader(f"🔍 {label2}")
        st.info(f"**Shape:** {df2.shape}")
        st.write("**Các cột:**")
        st.write(df2.columns.tolist())
        with st.expander("Xem 5 dòng đầu"):
            st.dataframe(df2.head(), use_container_width=True)
    
    st.markdown("---")
    
    # Thống kê mô tả
    st.subheader("📋 Thống kê Mô tả")
    fig = plot_statistics_comparison(df1, df2, label1, label2)
    if fig:
        st.pyplot(fig, use_container_width=True)


elif analysis_type == "📉 Phân phối (Distribution)":
    st.header("📉 Biểu đồ Phân phối")
    
    # Lấy các cột số
    numeric_cols1 = df1.select_dtypes(include=[np.number]).columns.tolist()
    numeric_cols2 = df2.select_dtypes(include=[np.number]).columns.tolist()
    common_cols = list(set(numeric_cols1) & set(numeric_cols2))
    
    if not common_cols:
        st.warning("❌ Không có cột số chung giữa 2 file CSV")
        st.stop()
    
    selected_col = st.selectbox("Chọn cột để vẽ:", common_cols, key='dist')
    
    fig = plot_distributions_comparison(df1, df2, selected_col, label1, label2)
    if fig:
        st.pyplot(fig, use_container_width=True)


elif analysis_type == "📦 Box Plot - Ngoại lai":
    st.header("📦 Biểu đồ Box Plot")
    
    numeric_cols1 = df1.select_dtypes(include=[np.number]).columns.tolist()
    numeric_cols2 = df2.select_dtypes(include=[np.number]).columns.tolist()
    common_cols = list(set(numeric_cols1) & set(numeric_cols2))
    
    if not common_cols:
        st.warning("❌ Không có cột số chung giữa 2 file CSV")
        st.stop()
    
    selected_col = st.selectbox("Chọn cột để vẽ:", common_cols, key='box')
    
    fig = plot_boxplots_comparison(df1, df2, selected_col, label1, label2)
    if fig:
        st.pyplot(fig, use_container_width=True)


elif analysis_type == "🔗 Tương quan (Correlation)":
    st.header("🔗 Bản đồ Tương quan")
    
    st.markdown("**So sánh ma trận tương quan giữa 2 CSV**")
    
    fig = plot_correlation_heatmap_comparison(df1, df2, label1, label2)
    if fig:
        st.pyplot(fig, use_container_width=True)


elif analysis_type == "⏱️ Chuỗi Thời gian":
    st.header("⏱️ Biểu đồ Chuỗi Thời gian")
    
    numeric_cols1 = df1.select_dtypes(include=[np.number]).columns.tolist()
    numeric_cols2 = df2.select_dtypes(include=[np.number]).columns.tolist()
    common_cols = list(set(numeric_cols1) & set(numeric_cols2))
    
    if not common_cols:
        st.warning("❌ Không có cột số chung giữa 2 file CSV")
        st.stop()
    
    selected_col = st.selectbox("Chọn cột để vẽ:", common_cols, key='ts')
    
    fig = plot_timeseries_comparison(df1, df2, selected_col, label1, label2)
    if fig:
        st.pyplot(fig, use_container_width=True)


elif analysis_type == "👁️ Missing Values":
    st.header("👁️ Phân tích Missing Values")
    
    fig = plot_missing_values_comparison(df1, df2, label1, label2)
    if fig:
        st.pyplot(fig, use_container_width=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(f"Chi tiết {label1}")
        missing1 = df1.isnull().sum()
        st.dataframe(missing1[missing1 > 0].sort_values(ascending=False), use_container_width=True)
    
    with col2:
        st.subheader(f"Chi tiết {label2}")
        missing2 = df2.isnull().sum()
        st.dataframe(missing2[missing2 > 0].sort_values(ascending=False), use_container_width=True)

# ==================== FOOTER ====================
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #7f8c8d;'>
    <p>🚀 Dashboard So sánh 2 CSV | Phát triển bằng Streamlit</p>
    <p>💡 Để sử dụng: Đặt 2 file CSV cùng thư mục với dashboard_app.py</p>
    </div>
""", unsafe_allow_html=True)
