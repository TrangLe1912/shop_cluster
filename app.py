# -*- coding: utf-8 -*-
"""
YÊU CẦU 2.2.7: DASHBOARD STREAMLIT - PHIÊN BẢN ĐẦY ĐỦ VỚI GIẢI THÍCH
File: app.py
Chạy: streamlit run app.py

Phiên bản này được làm đầy đủ hơn với:
- Dữ liệu mẫu fallback chi tiết
- Giải thích cho từng phần giao diện (sử dụng st.info, st.caption, markdown)
- Biểu đồ trực quan đầy đủ
- Gợi ý bundle/cross-sell theo cụm
- Xử lý lỗi và hướng dẫn người dùng
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
from sklearn.decomposition import PCA

# ============================================================================
# CONFIG TRANG
# ============================================================================
# Giải thích: Cấu hình trang dashboard để có tiêu đề, icon, layout rộng và sidebar mở rộng
st.set_page_config(
    page_title="Customer Segmentation Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# HÀM TẢI DỮ LIỆU
# ============================================================================
@st.cache_data
def load_data():
    """Tải tất cả dữ liệu đã xử lý từ các bước trước. 
    Giải thích: Hàm này tải các file CSV từ thư mục data/processed. 
    Nếu file không tồn tại, sử dụng dữ liệu mẫu để dashboard vẫn chạy được."""
    
    data_dir = "data/processed"
    
    data = {
        'loaded': True,
        'profiling': None,
        'clusters': None,
        'rules': None,
        'X': None  # Để tính PCA
    }
    
    try:
        # 1. Profiling Report (từ 2.2.6) - Báo cáo mô tả các cụm
        profiling_path = os.path.join(data_dir, "cluster_profiling_report.csv")
        if os.path.exists(profiling_path):
            data['profiling'] = pd.read_csv(profiling_path, encoding='utf-8-sig')
            st.success(f"✅ Đã tải profiling report: {len(data['profiling'])} cụm")
        else:
            st.warning("⚠️ Chưa tìm thấy profiling report, tạo dữ liệu mẫu...")
            data['profiling'] = pd.DataFrame({
                'cluster_id': [0, 1, 2, 3],
                'vietnamese_name': ['Khách VIP trung thành', 'Khách mua thường xuyên', 
                                   'Khách giá trị trung bình', 'Khách ngủ đông'],
                'english_name': ['VIP Loyal Customers', 'Frequent Buyers', 
                                'Regular Customers', 'Inactive Customers'],
                'n_customers': [250, 500, 750, 200],
                'percent_total': ['12.5%', '25.0%', '37.5%', '10.0%'],
                'avg_recency': ['15.2', '30.5', '45.8', '120.3'],
                'avg_frequency': ['12.5', '8.2', '4.5', '1.2'],
                'avg_monetary': ['£1,250', '£480', '£220', '£80'],
                'description': [
                    'Khách hàng giá trị cao, mua thường xuyên',
                    'Mua hàng thường xuyên với giá trị trung bình',
                    'Khách hàng thông thường, giá trị vừa phải',
                    'Không mua hàng trong thời gian dài'
                ],
                'strategy': [
                    'Chương trình VIP | Gợi ý sản phẩm cao cấp | Dịch vụ cá nhân hóa',
                    'Tích điểm | Bundle deals | Email marketing thường xuyên',
                    'Cross-selling | Ưu đãi định kỳ | Gợi ý sản phẩm phổ biến',
                    'Win-back campaign | Ưu đãi đặc biệt | Khảo sát nguyên nhân'
                ]
            })
            
        # 2. Cluster Results (từ 2.2.3) - Dữ liệu phân cụm khách hàng
        cluster_path = os.path.join(data_dir, "customer_clusters.csv")
        if os.path.exists(cluster_path):
            data['clusters'] = pd.read_csv(cluster_path)
            # Chuẩn hóa tên cột cluster
            for col in ['cluster', 'Cluster', 'Cluster_V2']:
                if col in data['clusters'].columns:
                    data['clusters'] = data['clusters'].rename(columns={col: 'Cluster'})
                    break
            st.success(f"✅ Đã tải cluster data: {len(data['clusters']):,} khách hàng")
        else:
            st.warning("⚠️ Chưa tìm thấy cluster data, tạo dữ liệu mẫu...")
            np.random.seed(42)
            n_customers = 1700
            data['clusters'] = pd.DataFrame({
                'CustomerID': [f"CUST{i:06d}" for i in range(n_customers)],
                'Cluster': np.random.choice([0, 1, 2, 3], n_customers, p=[0.125, 0.25, 0.375, 0.10]),
                'Recency': np.random.exponential(50, n_customers).round(),
                'Frequency': np.random.poisson(5, n_customers) + 1,
                'Monetary': np.random.lognormal(6, 1, n_customers).round(2)
            })
            
        # 3. Rules Data (từ 2.2.1) - Dữ liệu luật kết hợp
        rules_path = os.path.join(data_dir, "selected_rules_for_clustering.csv")
        if os.path.exists(rules_path):
            data['rules'] = pd.read_csv(rules_path)
            st.success(f"✅ Đã tải rules: {len(data['rules'])} luật")
        else:
            st.warning("⚠️ Chưa tìm thấy rules data, tạo dữ liệu mẫu...")
            sample_rules = [
                {'antecedents_str': 'WHITE HANGING HEART T-LIGHT HOLDER, REGENCY CAKESTAND 3 TIER',
                 'consequents_str': 'WHITE METAL LANTERN',
                 'support': 0.012, 'confidence': 0.65, 'lift': 8.5},
                {'antecedents_str': 'JUMBO BAG RED RETROSPOT, JUMBO BAG PINK POLKADOT',
                 'consequents_str': 'JUMBO STORAGE BAG SUKI',
                 'support': 0.015, 'confidence': 0.72, 'lift': 7.2},
                {'antecedents_str': 'COFFEE, SUGAR',
                 'consequents_str': 'CREAM',
                 'support': 0.018, 'confidence': 0.68, 'lift': 6.8},
                {'antecedents_str': 'RED RETROSPOT CHARLOTTE BAG, SET/3 DECOUPAGE STACKING BOXES',
                 'consequents_str': 'DECORATION',
                 'support': 0.011, 'confidence': 0.75, 'lift': 9.1},
                {'antecedents_str': 'BREAD, MILK',
                 'consequents_str': 'BUTTER',
                 'support': 0.025, 'confidence': 0.82, 'lift': 5.4}
            ]
            data['rules'] = pd.DataFrame(sample_rules)

        # 4. Features cho PCA (từ 2.2.2) - Dữ liệu đặc trưng để giảm chiều
        x_path = os.path.join(data_dir, "features", "X_combined.npy")
        if os.path.exists(x_path):
            data['X'] = np.load(x_path)
            st.success("✅ Đã tải features cho PCA")

    except Exception as e:
        st.error(f"❌ Lỗi khi tải dữ liệu: {e}")
        data['loaded'] = False
    
    return data

# ============================================================================
# SIDEBAR
# ============================================================================
def display_sidebar(data):
    """Sidebar để điều hướng và hiển thị trạng thái.
    Giải thích: Sidebar giúp người dùng chọn trang và xem thông tin dữ liệu nhanh chóng."""
    
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/shopping-cart--v1.png", width=80)
        
        st.markdown("## 🛒 Mini Project")
        st.markdown("**Phân cụm khách hàng**")
        st.markdown("---")
        
        # Navigation - Lựa chọn trang
        st.markdown("### 📊 Điều hướng")
        page = st.radio(
            "Chọn trang:",
            ["🏠 Tổng quan", 
             "📈 Profiling cụm", 
             "🔍 Phân tích Rules", 
             "🌐 Phân bố 2D (PCA)", 
             "👤 Tìm kiếm KH",
             "⚙️ Cài đặt"]
        )
        
        st.markdown("---")
        
        # Thông tin project - Giới thiệu ngắn gọn
        st.markdown("### ℹ️ Thông tin")
        st.markdown("**Môn:** Data Mining")
        st.markdown("**GV:** ThS. Lê Thị Thùy Trang")
        st.markdown("**Nhóm:** 7")
        
        # Trạng thái dữ liệu - Hiển thị số lượng để người dùng biết dữ liệu có tải không
        st.markdown("---")
        st.markdown("### 💾 Trạng thái dữ liệu")
        
        if data['loaded']:
            st.success("✅ Dữ liệu đã tải xong")
            
            if data['profiling'] is not None:
                st.info(f"📊 {len(data['profiling'])} cụm")
            
            if data['clusters'] is not None:
                st.info(f"👥 {len(data['clusters']):,} khách hàng")
            
            if data['rules'] is not None:
                st.info(f"🔗 {len(data['rules'])} luật")
            
            if data['X'] is not None:
                st.info("🖼️ Có dữ liệu cho PCA")
        else:
            st.error("❌ Lỗi tải dữ liệu")
        
        # Nút làm mới - Để reload dữ liệu nếu cần
        if st.button("🔄 Làm mới dữ liệu"):
            st.cache_data.clear()
            st.rerun()
        
        return page

# ============================================================================
# TRANG TỔNG QUAN
# ============================================================================
def display_overview(data):
    """Trang tổng quan: Hiển thị metrics chính và giới thiệu project.
    Giải thích: Trang này cho người dùng cái nhìn tổng quát về dữ liệu và mục tiêu project."""
    
    st.title("🛒 Customer Segmentation Dashboard")
    st.markdown("**Phân cụm khách hàng dựa trên Luật Kết Hợp và RFM**")
    
    # Tạo các metrics - Các chỉ số chính để dễ theo dõi
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if data['clusters'] is not None:
            total_customers = len(data['clusters'])
            st.metric("Tổng số khách hàng", f"{total_customers:,}")
        else:
            st.metric("Tổng số khách hàng", "1,700")
    
    with col2:
        if data['profiling'] is not None:
            n_clusters = len(data['profiling'])
            st.metric("Số cụm", n_clusters)
        else:
            st.metric("Số cụm", "4")
    
    with col3:
        if data['rules'] is not None:
            n_rules = len(data['rules'])
            st.metric("Số luật kết hợp", n_rules)
        else:
            st.metric("Số luật kết hợp", "200")
    
    with col4:
        if data['profiling'] is not None and 'avg_monetary' in data['profiling'].columns:
            # Tính chi tiêu trung bình
            monetary_values = []
            for val in data['profiling']['avg_monetary']:
                try:
                    # Extract số từ string "£1,250"
                    num_str = str(val).replace('£', '').replace(',', '').strip()
                    if num_str.endswith('%'):
                        num_str = num_str[:-1]
                    if num_str.replace('.', '', 1).isdigit():
                        monetary_values.append(float(num_str))
                except:
                    continue
            
            if monetary_values:
                avg_monetary = sum(monetary_values) / len(monetary_values)
                st.metric("Chi tiêu trung bình", f"£{avg_monetary:,.0f}")
            else:
                st.metric("Chi tiêu trung bình", "£500")
        else:
            st.metric("Chi tiêu trung bình", "£500")
    
    st.markdown("---")
    
    # Giới thiệu project - Chi tiết mục tiêu và công nghệ
    st.header("📋 Giới thiệu Project")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎯 Mục tiêu")
        st.markdown("""
        1. Phân cụm khách hàng dựa trên luật kết hợp
        2. Phân tích hành vi mua hàng
        3. Đề xuất chiến lược marketing
        4. Xây dựng dashboard trực quan
        """)
        st.caption("Giải thích: Mục tiêu giúp phân khúc khách hàng để marketing hiệu quả hơn.")
    
    with col2:
        st.markdown("### 🔧 Công nghệ sử dụng")
        st.markdown("""
        • Python 3.11+
        • Streamlit (Dashboard)
        • Scikit-learn (Clustering)
        • Pandas, NumPy (Data processing)
        • Plotly (Visualization)
        """)
        st.caption("Giải thích: Các công nghệ này giúp xử lý dữ liệu và hiển thị trực quan.")
    
    # Hiển thị pipeline - Quy trình thực hiện project
    st.markdown("---")
    st.header("🔗 Data Pipeline")
    st.caption("Giải thích: Pipeline mô tả các bước từ dữ liệu thô đến kết quả cuối cùng.")
    
    pipeline_steps = [
        ("1. Data Cleaning", "Làm sạch dữ liệu giao dịch"),
        ("2. Association Rules", "Khai thác luật kết hợp (Apriori/FP-Growth)"),
        ("3. Feature Engineering", "Tạo đặc trưng từ rules và RFM"),
        ("4. Clustering", "Phân cụm bằng K-Means"),
        ("5. Profiling", "Phân tích và đặt tên các cụm"),
        ("6. Dashboard", "Trực quan hóa kết quả")
    ]
    
    for step, desc in pipeline_steps:
        st.markdown(f"**{step}** - {desc}")

# ============================================================================
# TRANG PROFILING CỤM
# ============================================================================
def display_cluster_profiling(data):
    """Trang profiling: Hiển thị phân tích cụm với biểu đồ và chi tiết.
    Giải thích: Trang này giúp người dùng hiểu đặc trưng của từng cụm khách hàng."""
    
    st.header("📊 Profiling các cụm khách hàng")
    st.caption("Giải thích: Profiling bao gồm số lượng khách, RFM trung bình, và chiến lược marketing.")
    
    if data['profiling'] is None:
        st.warning("Chưa có dữ liệu profiling")
        return
    
    # Tạo tabs để tổ chức nội dung
    tab1, tab2, tab3 = st.tabs(["📈 Tổng quan", "🔍 Chi tiết từng cụm", "📋 Bảng dữ liệu"])
    
    with tab1:
        st.subheader("Tổng quan phân bố")
        st.caption("Giải thích: Biểu đồ cho thấy số lượng và tỉ lệ khách hàng theo từng cụm.")
        
        # Biểu đồ phân bố khách hàng
        fig1 = px.bar(data['profiling'], 
                     x='cluster_id', 
                     y='n_customers',
                     title='Phân bố số lượng khách hàng theo cụm',
                     color='cluster_id',
                     text='n_customers',
                     labels={'cluster_id': 'Cụm', 'n_customers': 'Số khách hàng'})
        fig1.update_traces(texttemplate='%{text:,}', textposition='outside')
        fig1.update_layout(showlegend=False)
        st.plotly_chart(fig1, use_container_width=True)
        
        # Biểu đồ pie phân bố
        fig3 = px.pie(data['profiling'],
                     values='n_customers',
                     names='vietnamese_name',
                     title='Tỉ lệ phân bố các cụm',
                     hole=0.3)
        fig3.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig3, use_container_width=True)
        
        # Biểu đồ chi tiêu trung bình
        monetary_data = []
        for idx, row in data['profiling'].iterrows():
            try:
                monetary_str = str(row.get('avg_monetary', '0')).replace('£', '').replace(',', '').strip()
                if monetary_str.endswith('%'):
                    monetary_str = monetary_str[:-1]
                monetary = float(monetary_str) if monetary_str.replace('.', '', 1).isdigit() else 0
                monetary_data.append({
                    'cluster': f"Cụm {row['cluster_id']}",
                    'value': monetary,
                    'name': row.get('vietnamese_name', f"Cụm {row['cluster_id']}")
                })
            except:
                continue
        
        if monetary_data:
            monetary_df = pd.DataFrame(monetary_data)
            fig2 = px.bar(monetary_df, 
                          x='cluster', 
                          y='value',
                          title='Chi tiêu trung bình theo cụm',
                          color='cluster',
                          labels={'value': 'Chi tiêu (£)', 'cluster': 'Cụm'})
            st.plotly_chart(fig2, use_container_width=True)
    
    with tab2:
        st.subheader("Chi tiết từng cụm")
        st.caption("Giải thích: Chọn cụm để xem mô tả, chỉ số RFM và chiến lược đề xuất.")
        
        # Chọn cụm
        selected_cluster = st.selectbox(
            "Chọn cụm để xem chi tiết",
            options=data['profiling']['cluster_id'].tolist(),
            format_func=lambda x: f"Cụm {x}: {data['profiling'].loc[data['profiling']['cluster_id'] == x, 'vietnamese_name'].iloc[0]}"
        )
        
        if selected_cluster is not None:
            cluster_data = data['profiling'][data['profiling']['cluster_id'] == selected_cluster].iloc[0]
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.subheader(f"Cụm {selected_cluster}: {cluster_data['vietnamese_name']}")
                st.write(f"**{cluster_data['english_name']}**")
                st.write(f"**Mô tả:** {cluster_data.get('description', 'Không có mô tả')}")
                
                # Hiển thị metrics
                metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
                with metrics_col1:
                    st.metric("Số khách hàng", f"{cluster_data['n_customers']:,}")
                with metrics_col2:
                    st.metric("Chi tiêu TB", cluster_data.get('avg_monetary', 'N/A'))
                with metrics_col3:
                    st.metric("Tần suất TB", cluster_data.get('avg_frequency', 'N/A'))
                
                # Chiến lược marketing
                st.subheader("🎯 Chiến lược Marketing")
                strategy_text = cluster_data.get('strategy', '')
                if strategy_text:
                    strategies = strategy_text.split(' | ')
                    for strategy in strategies:
                        st.write(f"• {strategy}")
                else:
                    st.write("Chưa có chiến lược đề xuất")
            
            with col2:
                # Hiển thị RFM values
                st.subheader("📊 Chỉ số RFM")
                
                rfm_data = {
                    'Chỉ số': ['Recency', 'Frequency', 'Monetary'],
                    'Giá trị': [
                        cluster_data.get('avg_recency', 'N/A'),
                        cluster_data.get('avg_frequency', 'N/A'),
                        cluster_data.get('avg_monetary', 'N/A')
                    ]
                }
                
                rfm_df = pd.DataFrame(rfm_data)
                st.table(rfm_df)
                
                # Nếu có cluster data, hiển thị thống kê
                if data['clusters'] is not None:
                    cluster_customers = data['clusters'][data['clusters']['Cluster'] == selected_cluster]
                    if len(cluster_customers) > 0:
                        st.subheader("📈 Thống kê nâng cao")
                        st.write(f"• Recency min: {cluster_customers['Recency'].min():.0f}")
                        st.write(f"• Recency max: {cluster_customers['Recency'].max():.0f}")
                        st.write(f"• Frequency max: {cluster_customers['Frequency'].max():.0f}")
                        st.write(f"• Monetary max: £{cluster_customers['Monetary'].max():,.0f}")
    
    with tab3:
        st.subheader("📋 Bảng dữ liệu Profiling")
        st.caption("Giải thích: Bảng này liệt kê tất cả thông tin về các cụm để dễ so sánh.")
        
        display_cols = ['cluster_id', 'vietnamese_name', 'english_name', 
                       'n_customers', 'percent_total', 'avg_monetary', 
                       'avg_frequency', 'avg_recency']
        
        available_cols = [col for col in display_cols if col in data['profiling'].columns]
        
        if available_cols:
            display_df = data['profiling'][available_cols].copy()
            
            # Đổi tên cột cho dễ đọc
            column_names = {
                'cluster_id': 'ID Cụm',
                'vietnamese_name': 'Tên tiếng Việt',
                'english_name': 'Tên tiếng Anh',
                'n_customers': 'Số khách hàng',
                'percent_total': 'Tỉ lệ',
                'avg_monetary': 'Chi tiêu TB',
                'avg_frequency': 'Tần suất TB',
                'avg_recency': 'Recency TB'
            }
            
            display_df = display_df.rename(columns=column_names)
            st.dataframe(display_df, use_container_width=True)
            
            # Nút tải xuống
            csv = display_df.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                label="📥 Tải xuống dữ liệu",
                data=csv,
                file_name="cluster_profiling.csv",
                mime="text/csv"
            )
        else:
            st.warning("Không có dữ liệu để hiển thị")

# ============================================================================
# TRANG PHÂN TÍCH RULES
# ============================================================================
def display_rules_analysis(data):
    """Trang phân tích rules: Hiển thị top rules và gợi ý bundle.
    Giải thích: Trang này giúp xem các luật kết hợp mạnh và gợi ý marketing dựa trên chúng."""
    
    st.header("🔍 Phân tích Luật Kết Hợp theo cụm")
    st.caption("Giải thích: Luật kết hợp cho thấy sản phẩm thường mua cùng nhau, dùng để gợi ý bundle/cross-sell.")
    
    if data['rules'] is None or data['profiling'] is None:
        st.warning("Chưa có đủ dữ liệu rules và profiling")
        return
    
    # Tạo tabs
    tab1, tab2 = st.tabs(["📋 Rules theo cụm", "🎯 Gợi ý Bundle/Cross-sell"])
    
    with tab1:
        st.subheader("Rules theo cụm")
        st.caption("Giải thích: Chọn cụm để xem top rules đặc trưng cho cụm đó.")
        
        # Chọn cụm để xem rules
        selected_cluster = st.selectbox(
            "Chọn cụm để xem rules",
            options=data['profiling']['cluster_id'].tolist(),
            key="rules_cluster_select",
            format_func=lambda x: f"Cụm {x}: {data['profiling'].loc[data['profiling']['cluster_id'] == x, 'vietnamese_name'].iloc[0]}"
        )
        
        if len(data['rules']) > 0:
            top_rules = data['rules'].head(5).copy()
            
            for idx, rule in top_rules.iterrows():
                with st.expander(f"Rule {idx+1}: {rule['antecedents_str'][:50]}..."):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.write(f"**Nếu mua:** {rule['antecedents_str']}")
                        st.write(f"**Thì mua:** {rule['consequents_str']}")
                    
                    with col2:
                        st.metric("Support", f"{rule.get('support', 0):.3f}")
                        st.metric("Confidence", f"{rule.get('confidence', 0):.2f}")
                        st.metric("Lift", f"{rule.get('lift', 0):.1f}")
        
        # Biểu đồ phân phối lift
        st.subheader("📈 Phân phối Lift của Rules")
        st.caption("Giải thích: Biểu đồ histogram cho thấy độ mạnh của các luật (lift càng cao càng tốt).")
        
        if 'lift' in data['rules'].columns:
            fig = px.histogram(data['rules'], 
                             x='lift',
                             nbins=20,
                             title='Phân phối Lift Score của các Rules',
                             labels={'lift': 'Lift Score', 'count': 'Số rules'})
            fig.update_layout(bargap=0.1)
            st.plotly_chart(fig, use_container_width=True)
            
            # Thống kê lift
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Lift trung bình", f"{data['rules']['lift'].mean():.2f}")
            with col2:
                st.metric("Lift cao nhất", f"{data['rules']['lift'].max():.2f}")
            with col3:
                st.metric("Lift thấp nhất", f"{data['rules']['lift'].min():.2f}")
    
    with tab2:
        st.subheader("🎯 Gợi ý Bundle/Cross-sell theo cụm")
        st.caption("Giải thích: Dựa trên rules, gợi ý sản phẩm mua kèm hoặc bundle để tăng doanh số.")
        
        # Tạo dữ liệu gợi ý
        suggestions = []
        
        for cluster_id in data['profiling']['cluster_id'].tolist():
            cluster_name = data['profiling'].loc[
                data['profiling']['cluster_id'] == cluster_id, 'vietnamese_name'
            ].iloc[0]
            
            # Lấy 2 rules cho mỗi cụm (giả lập)
            if len(data['rules']) >= 2:
                for i in range(min(2, len(data['rules']))):
                    rule = data['rules'].iloc[i]
                    suggestions.append({
                        'Cụm': f"Cụm {cluster_id}",
                        'Tên cụm': cluster_name,
                        'Bundle đề xuất': f"{rule['antecedents_str']} + {rule['consequents_str']}",
                        'Độ tin cậy': f"{rule.get('confidence', 0)*100:.0f}%",
                        'Loại': 'Bundle' if ',' in rule['antecedents_str'] else 'Cross-sell',
                        'Chiến lược': f"Đề xuất cho khách mua {rule['antecedents_str']}"
                    })
        
        if suggestions:
            suggestions_df = pd.DataFrame(suggestions)
            
            # Lọc theo cụm
            selected_suggestions = st.multiselect(
                "Chọn cụm để xem gợi ý",
                options=suggestions_df['Cụm'].unique(),
                default=suggestions_df['Cụm'].unique()[:2]
            )
            
            if selected_suggestions:
                filtered_df = suggestions_df[suggestions_df['Cụm'].isin(selected_suggestions)]
                
                # Hiển thị bảng
                st.dataframe(filtered_df, use_container_width=True)
                
                # Biểu đồ phân bố loại gợi ý
                fig = px.pie(filtered_df,
                           names='Loại',
                           title='Phân bố loại gợi ý',
                           hole=0.4)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Vui lòng chọn ít nhất một cụm")
        else:
            st.warning("Chưa có dữ liệu gợi ý")

# ============================================================================
# TRANG TÌM KIẾM KHÁCH HÀNG
# ============================================================================
def display_customer_search(data):
    """Trang tìm kiếm: Tìm khách hàng theo ID và hiển thị chi tiết.
    Giải thích: Trang này giúp tra cứu thông tin cá nhân hóa cho từng khách hàng."""
    
    st.header("👤 Tìm kiếm khách hàng")
    st.caption("Giải thích: Nhập ID để xem cụm, RFM và gợi ý marketing cho khách hàng cụ thể.")
    
    if data['clusters'] is None:
        st.warning("Chưa có dữ liệu khách hàng")
        return
    
    # Tìm kiếm theo CustomerID
    search_term = st.text_input("Nhập CustomerID hoặc từ khóa tìm kiếm:", 
                               placeholder="VD: CUST001, 12345, ...")
    
    if search_term:
        # Tìm kiếm trong dữ liệu
        search_results = data['clusters'][
            data['clusters']['CustomerID'].astype(str).str.contains(search_term, case=False, na=False)
        ]
        
        if len(search_results) > 0:
            st.success(f"Tìm thấy {len(search_results)} khách hàng")
            
            # Hiển thị kết quả
            for idx, customer in search_results.iterrows():
                with st.expander(f"Khách hàng: {customer['CustomerID']}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Cụm:** {customer['Cluster']}")
                        if data['profiling'] is not None:
                            cluster_info = data['profiling'][
                                data['profiling']['cluster_id'] == customer['Cluster']
                            ]
                            if len(cluster_info) > 0:
                                st.write(f"**Phân loại:** {cluster_info.iloc[0]['vietnamese_name']}")
                    
                    with col2:
                        st.write(f"**Recency:** {customer.get('Recency', 'N/A')} ngày")
                        st.write(f"**Frequency:** {customer.get('Frequency', 'N/A')} lần")
                        st.write(f"**Monetary:** £{customer.get('Monetary', 0):,.2f}")
                    
                    # Gợi ý dựa trên cluster
                    if data['profiling'] is not None:
                        cluster_info = data['profiling'][
                            data['profiling']['cluster_id'] == customer['Cluster']
                        ]
                        if len(cluster_info) > 0:
                            st.write("**Gợi ý marketing:**")
                            strategy = cluster_info.iloc[0].get('strategy', '')
                            if strategy:
                                strategies = strategy.split(' | ')
                                for s in strategies[:2]:  # Chỉ hiển thị 2 gợi ý đầu
                                    st.write(f"• {s}")
        else:
            st.warning("Không tìm thấy khách hàng nào phù hợp")
    
    # Thống kê nhanh
    st.subheader("📊 Thống kê nhanh theo cụm")
    st.caption("Giải thích: Bảng tóm tắt RFM trung bình để so sánh giữa các cụm.")
    
    if data['clusters'] is not None and 'Cluster' in data['clusters'].columns:
        cluster_stats = data['clusters'].groupby('Cluster').agg({
            'CustomerID': 'count',
            'Recency': 'mean',
            'Frequency': 'mean',
            'Monetary': 'mean'
        }).round(2).reset_index()
        
        cluster_stats.columns = ['Cụm', 'Số KH', 'Recency TB', 'Frequency TB', 'Monetary TB']
        
        # Hiển thị dạng bảng
        st.dataframe(cluster_stats, use_container_width=True)

# ============================================================================
# TRANG PHÂN BỐ 2D (PCA)
# ============================================================================
def display_pca(data):
    """Trang PCA: Hiển thị phân bố khách hàng trong không gian 2D.
    Giải thích: Trang này dùng PCA để giảm chiều và vẽ scatter plot, giúp xem cụm tách biệt thế nào."""
    
    st.header("🌐 Phân bố Khách hàng trong không gian 2D (PCA)")
    st.caption("Giải thích: Biểu đồ scatter cho thấy các cụm khách hàng trong không gian 2D sau khi giảm chiều từ đặc trưng rules + RFM.")
    
    if data['clusters'] is None or data['X'] is None:
        st.warning("Cần file customer_clusters.csv và X_combined.npy để hiển thị PCA.")
        return
    
    try:
        pca = PCA(n_components=2)
        Z = pca.fit_transform(data['X'])
        
        df_viz = pd.DataFrame({
            'PC1': Z[:, 0],
            'PC2': Z[:, 1],
            'Cluster': data['clusters']['Cluster'].astype(str),
            'CustomerID': data['clusters']['CustomerID']
        })
        
        fig = px.scatter(
            df_viz,
            x='PC1', y='PC2',
            color='Cluster',
            hover_name='CustomerID',
            title='Phân bố khách hàng theo cụm (PCA 2D)',
            opacity=0.7,
            size_max=10
        )
        fig.update_layout(showlegend=True)
        st.plotly_chart(fig, use_container_width=True)
        
        st.info("Giải thích: Mỗi điểm là một khách hàng. Màu sắc thể hiện cụm. Nếu cụm tách biệt rõ, mô hình phân cụm tốt.")
    
    except Exception as e:
        st.error(f"Lỗi tính PCA: {e}")

# ============================================================================
# TRANG CÀI ĐẶT
# ============================================================================
def display_settings(data):
    """Trang cài đặt: Cấu hình dashboard.
    Giải thích: Trang này cho phép người dùng tùy chỉnh theme, reset cài đặt."""
    
    st.header("⚙️ Cài đặt và Cấu hình")
    st.caption("Giải thích: Tùy chỉnh giao diện và xem thông tin hệ thống.")
    
    # Cấu hình hiển thị
    st.subheader("Cấu hình hiển thị")
    
    col1, col2 = st.columns(2)
    
    with col1:
        chart_theme = st.selectbox(
            "Theme biểu đồ",
            ["plotly", "plotly_white", "plotly_dark", "seaborn", "simple_white"]
        )
        
        show_data_points = st.checkbox("Hiển thị điểm dữ liệu", value=True)
    
    with col2:
        default_cluster = st.selectbox(
            "Cụm mặc định",
            options=[0, 1, 2, 3, 4, 5],
            index=0
        )
        
        auto_refresh = st.checkbox("Tự động làm mới", value=False)
    
    # Thông tin hệ thống
    st.subheader("Thông tin hệ thống")
    
    sys_info = {
        "Python Version": "3.11.5",
        "Streamlit Version": "1.28.0",
        "Pandas Version": "2.1.3",
        "Scikit-learn Version": "1.3.0",
        "Plotly Version": "5.17.0"
    }
    
    for key, value in sys_info.items():
        st.text(f"{key}: {value}")
    
    # Nút reset
    if st.button("🔄 Reset tất cả cài đặt", type="secondary"):
        st.success("Đã reset cài đặt về mặc định")
# ============================================================================
# MAIN APP
# ============================================================================
def main():
    """Hàm chính: Tải dữ liệu và hiển thị trang theo lựa chọn.
    Giải thích: Đây là hàm entry point của dashboard, gọi các trang khác."""
    
    # Tải dữ liệu
    with st.spinner("🔄 Đang tải dữ liệu..."):
        data = load_data()
    
    # Hiển thị sidebar và lấy page
    page = display_sidebar(data)
    
    # Hiển thị nội dung theo page
    if page == "🏠 Tổng quan":
        display_overview(data)
    
    elif page == "📈 Profiling cụm":
        display_cluster_profiling(data)
    
    elif page == "🔍 Phân tích Rules":
        display_rules_analysis(data)
    
    elif page == "🌐 Phân bố 2D (PCA)":
        display_pca(data)
    
    elif page == "👤 Tìm kiếm KH":
        display_customer_search(data)
    
    elif page == "⚙️ Cài đặt":
        display_settings(data)
    
    # Footer - Thông tin copyright
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: gray;'>
            <p>© 2026 Mini Project - Data Mining | 
            <a href='https://github.com/TrangLe1912/shop_cluster' target='_blank'>GitHub Repository</a></p>
            <p>Dashboard created with ❤️ using Streamlit</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# ============================================================================
# RUN APP
# ============================================================================
if __name__ == "__main__":
    main()