import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- Cấu hình trang ---
st.set_page_config(
    page_title="Dashboard Phân Cụm Khách Hàng",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Đường dẫn dữ liệu ---
DATA_DIR = "data/processed"
CLUSTERS_PATH = os.path.join(DATA_DIR, "customer_clusters_from_rules.csv")
FEATURES_PATH = os.path.join(DATA_DIR, "customer_features_matrix.csv")
RULES_PATH = os.path.join(DATA_DIR, "rules_top50_fpgrowth.csv")

# --- Hàm load dữ liệu ---
@st.cache_data
def load_data():
    data = {}
    try:
        if os.path.exists(CLUSTERS_PATH):
            data["clusters"] = pd.read_csv(CLUSTERS_PATH, dtype={'CustomerID': str})
        
        if os.path.exists(FEATURES_PATH):
            data["features"] = pd.read_csv(FEATURES_PATH, dtype={'CustomerID': str})
            
        if os.path.exists(RULES_PATH):
            data["rules"] = pd.read_csv(RULES_PATH)
            
        return data
    except Exception as e:
        st.error(f"Lỗi khi đọc dữ liệu: {e}")
        return {}

data = load_data()
df_clusters = data.get("clusters")
df_features = data.get("features")
df_rules = data.get("rules")

# --- Tiêu đề ---
st.title("🛍️ Dashboard Phân Tích & Phân Cụm Khách Hàng")
st.markdown("---")

if df_clusters is None:
    st.warning("Chưa tìm thấy file kết quả phân cụm. Vui lòng chạy notebook phân cụm trước.")
    st.stop()

# --- Sidebar: Bộ lọc ---
st.sidebar.header("🔍 Bộ lọc")

# Chọn cụm
if 'cluster' in df_clusters.columns:
    all_clusters = sorted(df_clusters['cluster'].unique())
    selected_cluster = st.sidebar.selectbox("Chọn Cụm Khách Hàng (Cluster)", ["Tất cả"] + list(all_clusters))
else:
    st.error("File kết quả không chứa cột 'cluster'.")
    st.stop()

# --- Phần 1: Tổng quan ---
st.header("1. Tổng Quan Phân Cụm")

# Metrics tổng quan
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Tổng số khách hàng", len(df_clusters))
with col2:
    st.metric("Số lượng cụm", len(all_clusters))
with col3:
    if 'Recency' in df_clusters.columns:
        st.metric("TB Recency (Ngày)", f"{df_clusters['Recency'].mean():.1f}")
with col4:
    if 'Monetary' in df_clusters.columns:
        st.metric("TB Monetary ($)", f"{df_clusters['Monetary'].mean():.1f}")

# Biểu đồ phân phối cụm
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("Phân bố khách hàng theo cụm")
    fig_count = px.bar(
        df_clusters['cluster'].value_counts().reset_index(),
        x='cluster', y='count',
        labels={'cluster': 'Cụm', 'count': 'Số lượng khách hàng'},
        color='cluster'
    )
    st.plotly_chart(fig_count, use_container_width=True)

with col_chart2:
    st.subheader("Đặc điểm RFM trung bình theo cụm")
    if {'Recency', 'Frequency', 'Monetary'}.issubset(df_clusters.columns):
        rfm_summary = df_clusters.groupby('cluster')[['Recency', 'Frequency', 'Monetary']].mean().reset_index()
        fig_rfm = px.scatter(
            rfm_summary, x='Recency', y='Frequency', size='Monetary', color='cluster',
            hover_data=['Monetary'],
            labels={'Recency': 'Recency (Thấp tốt)', 'Frequency': 'Frequency (Cao tốt)'},
            title="Biểu đồ RFM (Kích thước bóng = Monetary)"
        )
        st.plotly_chart(fig_rfm, use_container_width=True)
    else:
        st.info("Dữ liệu không có đủ cột RFM để vẽ biểu đồ.")

# --- Phần 2: Chi tiết Cụm & Chiến lược ---
st.header(f"2. Chi tiết & Chiến lược Marketing: {'Tất cả' if selected_cluster == 'Tất cả' else f'Cụm {selected_cluster}'}")

if selected_cluster != "Tất cả":
    # Lọc dữ liệu
    cluster_data = df_clusters[df_clusters['cluster'] == selected_cluster]
    
    # Hiển thị chỉ số RFM của cụm
    if {'Recency', 'Frequency', 'Monetary'}.issubset(cluster_data.columns):
        avg_r = cluster_data['Recency'].mean()
        avg_f = cluster_data['Frequency'].mean()
        avg_m = cluster_data['Monetary'].mean()
        
        c1, c2, c3 = st.columns(3)
        c1.info(f"**Recency TB:** {avg_r:.1f} ngày")
        c2.info(f"**Frequency TB:** {avg_f:.1f} lần")
        c3.info(f"**Monetary TB:** ${avg_m:.1f}")
    
    # --- Phân tích Luật kết hợp (Top Rules) ---
    st.subheader("🔥 Top Luật Kết Hợp & Sản Phẩm Đặc Trưng")
    
    if df_features is not None and df_rules is not None:
        # Merge features with cluster info
        rule_cols = [c for c in df_features.columns if c.startswith("Rule_")]
        
        if rule_cols:
            # Lấy features của các khách hàng trong cụm này
            cluster_cust_ids = cluster_data['CustomerID']
            cluster_feats = df_features[df_features['CustomerID'].isin(cluster_cust_ids)]
            
            if not cluster_feats.empty:
                # Tính trung bình mức độ kích hoạt của từng luật trong cụm
                rule_activation = cluster_feats[rule_cols].mean().sort_values(ascending=False)
                
                # Lấy Top 10 luật mạnh nhất
                top_rules_indices = rule_activation.head(10).index
                
                # Hiển thị
                top_rules_data = []
                for rule_col in top_rules_indices:
                    try:
                        rule_idx = int(rule_col.replace("Rule_", ""))
                        if rule_idx < len(df_rules):
                            rule_info = df_rules.iloc[rule_idx]
                            activation_score = rule_activation[rule_col]
                            
                            # Chỉ hiển thị nếu có activation > 0
                            if activation_score > 0:
                                top_rules_data.append({
                                    "Luật (Rule)": rule_info.get('rule_str', f"{rule_info['antecedents']} -> {rule_info['consequents']}"),
                                    "Độ kích hoạt TB": activation_score,
                                    "Lift": rule_info.get('lift', 0),
                                    "Confidence": rule_info.get('confidence', 0),
                                    "Sản phẩm mua kèm (Consequents)": rule_info.get('consequents_str', str(rule_info['consequents']))
                                })
                    except:
                        continue
                
                if top_rules_data:
                    df_top_rules = pd.DataFrame(top_rules_data)
                    st.dataframe(df_top_rules.style.background_gradient(subset=['Độ kích hoạt TB'], cmap='Greens'), use_container_width=True)
                    
                    # --- Gợi ý Bundle/Cross-sell ---
                    st.subheader("💡 Gợi ý Chiến lược Bundle / Cross-sell")
                    
                    top_rule = df_top_rules.iloc[0]
                    st.success(f"**Chiến lược đề xuất:** Dựa trên luật phổ biến nhất, hãy tạo gói combo gồm các sản phẩm trong **{top_rule['Luật (Rule)'].split('→')[0]}** để kích thích mua thêm **{top_rule['Sản phẩm mua kèm (Consequents)']}**.")
                    
                    st.markdown("#### Các gợi ý cụ thể:")
                    for idx, row in df_top_rules.head(5).iterrows():
                        st.markdown(f"- **Gợi ý {idx+1}:** Khách mua `{row['Luật (Rule)'].split('→')[0]}` -> Gợi ý mua thêm `{row['Sản phẩm mua kèm (Consequents)']}` (Độ tin cậy: {row['Confidence']:.2f})")
                else:
                    st.info("Không tìm thấy luật nổi bật nào cho cụm này (Độ kích hoạt = 0).")
            else:
                st.warning("Không tìm thấy dữ liệu features cho các khách hàng trong cụm này.")
        else:
            st.warning("Không tìm thấy cột đặc trưng luật (Rule_*) trong file features.")
    else:
        st.warning("Thiếu file features hoặc rules để phân tích chi tiết luật.")

else:
    st.info("👈 Vui lòng chọn một cụm cụ thể từ thanh bên để xem chi tiết luật và đề xuất chiến lược.")
    
    # Hiển thị bảng dữ liệu thô
    with st.expander("Xem dữ liệu chi tiết"):
        st.dataframe(df_clusters)

# --- Footer ---
st.markdown("---")
st.caption("Dashboard được xây dựng bằng Streamlit - Mini Project Data Mining")
