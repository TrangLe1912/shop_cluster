"""
🎨 Streamlit Dashboard - Phân Cụm Khách Hàng & Chiến Lược Marketing
Interactive visualization with modern UI design
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="🎯 Dashboard Phân Cụm Khách Hàng",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM CSS - MODERN DESIGN
# ============================================================================
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Styling */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Main container */
    .main .block-container {
        padding: 2rem 3rem;
        max-width: 1400px;
    }
    
    /* Main Header */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2.5rem 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
        text-align: center;
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 800;
        margin: 0 0 0.5rem 0;
        letter-spacing: -1px;
    }
    
    .main-header p {
        font-size: 1.1rem;
        opacity: 0.9;
        margin: 0;
    }
    
    /* Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        border: 1px solid #e2e8f0;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #1e293b;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 0.85rem;
        font-weight: 600;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .metric-delta {
        font-size: 0.9rem;
        color: #10b981;
        font-weight: 500;
    }
    
    /* Section Headers */
    .section-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1e293b;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #667eea;
        display: inline-block;
    }
    
    /* Cards */
    .card {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
        border: 1px solid #e2e8f0;
        margin-bottom: 1rem;
    }
    
    .card-highlight {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border: 2px solid #fbbf24;
    }
    
    /* Cluster Colors */
    .cluster-0 { border-left: 5px solid #FF6B6B; }
    .cluster-1 { border-left: 5px solid #4ECDC4; }
    .cluster-2 { border-left: 5px solid #45B7D1; }
    .cluster-3 { border-left: 5px solid #FFA07A; }
    
    /* Priority Badges */
    .badge {
        display: inline-block;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    
    .badge-high { background: linear-gradient(135deg, #ef4444, #dc2626); color: white; }
    .badge-medium { background: linear-gradient(135deg, #f59e0b, #d97706); color: white; }
    .badge-low { background: linear-gradient(135deg, #10b981, #059669); color: white; }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%);
    }
    
    [data-testid="stSidebar"] .block-container {
        padding: 2rem 1rem;
    }
    
    /* Sidebar Header */
    .sidebar-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    
    /* Strategy Box */
    .strategy-box {
        background: white;
        border-radius: 12px;
        padding: 1rem 1.2rem;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        margin-top: 3rem;
        border-top: 2px solid #e2e8f0;
        color: #64748b;
    }
    
    /* DataFrames */
    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: #f1f5f9;
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# LOAD DATA
# ============================================================================
@st.cache_data
def load_data():
    """Load all necessary data files"""
    script_dir = Path(__file__).parent.resolve()
    data_dir = script_dir / 'data'
    clusters_dir = data_dir / 'clusters'
    
    try:
        profiling_df = pd.read_csv(clusters_dir / 'cluster_profiling_summary.csv')
        rules_df = pd.read_csv(clusters_dir / 'cluster_top_rules_detailed.csv')
    except:
        profiling_df = None
        rules_df = None
    
    try:
        clustering_metrics = pd.read_csv(clusters_dir / 'clustering_metrics_all.csv')
    except:
        clustering_metrics = None
    
    return profiling_df, rules_df, clustering_metrics

profiling_df, rules_df, clustering_metrics = load_data()

# ============================================================================
# CLUSTER PROFILES
# ============================================================================
CLUSTER_PROFILES = {
    0: {
        'name': 'High-Value VIP',
        'name_vi': 'Khách VIP Chi Tiêu Cao',
        'color': '#FF6B6B',
        'icon': '💎',
        'emoji': '👑',
        'description': 'Khách hàng trung thành, mua sắm thường xuyên với giá trị cao',
        'characteristics': [
            '✓ Tần suất giao dịch cao (59 giao dịch TB)',
            '✓ Tổng chi tiêu cao (£1,460 TB)',
            '✓ Gần đây đã mua hàng (102 ngày)',
            '✓ Kích hoạt nhiều quy tắc mua sắm'
        ],
        'strategies': [
            '🎯 VIP Loyalty Program',
            '🎁 Premium Bundles',
            '💎 Upsell Premium',
            '🎉 Exclusive Events'
        ]
    },
    1: {
        'name': 'Occasional Premium',
        'name_vi': 'Khách Mua Thỉnh Thoảng',
        'color': '#4ECDC4',
        'icon': '🌟',
        'emoji': '⭐',
        'description': 'Khách hàng có khả năng chi tiêu cao nhưng mua không thường xuyên',
        'characteristics': [
            '✓ Tần suất giao dịch vừa phải',
            '✓ Giá trị đơn hàng cao (£3,595 TB)',
            '✓ Lâu không mua (67 ngày)',
            '✓ Tiềm năng phát triển lớn'
        ],
        'strategies': [
            '🔔 Re-engagement Campaign',
            '⏰ Seasonal Campaigns',
            '💝 Limited-Time Offers',
            '🌟 Surprise & Delight'
        ]
    },
    2: {
        'name': 'New Explorer',
        'name_vi': 'Khách Hàng Mới',
        'color': '#45B7D1',
        'icon': '🎯',
        'emoji': '🆕',
        'description': 'Khách hàng mới hoặc đang khám phá, chi tiêu thấp',
        'characteristics': [
            '✓ Số lượng transactions lớn nhất',
            '✓ Giá trị đơn hàng thấp',
            '✓ Gần đây có hoạt động (39 ngày)',
            '✓ Tiềm năng chuyển đổi cao'
        ],
        'strategies': [
            '🎓 Education & Onboarding',
            '🎁 Welcome Program',
            '📚 Starter Bundles',
            '⭐ Social Proof'
        ]
    },
    3: {
        'name': 'Budget Conscious',
        'name_vi': 'Khách Tìm Giá Rẻ',
        'color': '#FFA07A',
        'icon': '💰',
        'emoji': '🏷️',
        'description': 'Khách hàng nhạy cảm với giá, thích khuyến mãi',
        'characteristics': [
            '✓ Tần suất cao hoặc vừa phải',
            '✓ Giá trị đơn hàng thấp (£2,083)',
            '✓ Mua sắm dựa trên khuyến mãi',
            '✓ Phản hồi tốt với discounts'
        ],
        'strategies': [
            '💰 Discount Tiers',
            '🏷️ Bulk Deals',
            '📧 Price Drop Alerts',
            '🎪 Loyalty Cashback'
        ]
    }
}

# ============================================================================
# HEADER
# ============================================================================
st.markdown("""
<div class="main-header">
    <h1>📊 Dashboard Phân Cụm Khách Hàng</h1>
    <p>Phân tích tương tác các phân khúc khách hàng & Chiến lược Marketing được cá nhân hóa</p>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# SIDEBAR
# ============================================================================
with st.sidebar:
    st.markdown("""
    <div class="sidebar-header">
        <h3 style="margin:0;">🎯 Điều Hướng</h3>
    </div>
    """, unsafe_allow_html=True)
    
    page = st.radio(
        "Chọn Trang:",
        ["📈 Tổng Quan", "🔍 Chi Tiết Cụm", "📋 Quy Tắc Hàng Đầu", "📦 Gợi Ý Bundle", "💼 Chiến Lược Marketing"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("### 🎨 Chọn Cụm")
    
    cluster_filter = st.selectbox(
        "Cụm:",
        [0, 1, 2, 3],
        format_func=lambda x: f"{CLUSTER_PROFILES[x]['icon']} Cụm {x}: {CLUSTER_PROFILES[x]['name']}",
        label_visibility="collapsed"
    )
    
    # Cluster Info Card
    profile = CLUSTER_PROFILES[cluster_filter]
    st.markdown(f"""
    <div class="card cluster-{cluster_filter}">
        <h4 style="margin:0 0 0.5rem 0;">{profile['icon']} {profile['name']}</h4>
        <p style="font-size:0.85rem; color:#64748b; margin:0;">{profile['name_vi']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### ℹ️ Thông Tin")
    st.caption("Dashboard được xây dựng với:")
    st.caption("• K-Means Clustering (K=4)")
    st.caption("• RFM Analysis")
    st.caption("• Association Rules Mining")

# ============================================================================
# PAGE 1: OVERVIEW
# ============================================================================
if page == "📈 Tổng Quan":
    st.markdown('<p class="section-header">📊 Tổng Quan Các Cụm Khách Hàng</p>', unsafe_allow_html=True)
    
    # Metrics Row
    cols = st.columns(4)
    
    if profiling_df is not None:
        for idx, col in enumerate(cols):
            if idx < len(profiling_df):
                cluster_data = profiling_df[profiling_df['Cluster'] == idx].iloc[0]
                profile = CLUSTER_PROFILES[idx]
                
                with col:
                    st.markdown(f"""
                    <div class="metric-card cluster-{idx}">
                        <p class="metric-label">{profile['icon']} Cụm {idx}</p>
                        <p class="metric-value">{int(cluster_data['N_Customers']):,}</p>
                        <p class="metric-delta">{cluster_data['Pct_Total']}</p>
                        <p style="font-size:0.75rem; color:#94a3b8;">{profile['name']}</p>
                    </div>
                    """, unsafe_allow_html=True)
    else:
        for idx, col in enumerate(cols):
            profile = CLUSTER_PROFILES[idx]
            with col:
                st.markdown(f"""
                <div class="metric-card cluster-{idx}">
                    <p class="metric-label">{profile['icon']} Cụm {idx}</p>
                    <p class="metric-value">--</p>
                    <p style="font-size:0.75rem; color:#94a3b8;">{profile['name']}</p>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Charts Row
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("#### 💰 Phân Phối Doanh Thu")
        
        if profiling_df is not None:
            fig = px.pie(
                profiling_df,
                values='Total_Revenue_£',
                names=[f"Cụm {i}: {CLUSTER_PROFILES[i]['name']}" for i in profiling_df['Cluster']],
                color_discrete_sequence=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A'],
                hole=0.45
            )
            fig.update_traces(
                textposition='inside',
                textinfo='percent+label',
                textfont_size=12,
                marker=dict(line=dict(color='white', width=2))
            )
            fig.update_layout(
                showlegend=False,
                height=350,
                margin=dict(t=20, b=20, l=20, r=20)
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Không có dữ liệu")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("#### 👥 Số Lượng Khách Hàng")
        
        if profiling_df is not None:
            fig = px.bar(
                profiling_df,
                x='Cluster',
                y='N_Customers',
                color='Cluster',
                color_discrete_sequence=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A'],
                text='N_Customers'
            )
            fig.update_traces(
                texttemplate='%{text:,}',
                textposition='outside',
                textfont_size=14
            )
            fig.update_layout(
                showlegend=False,
                height=350,
                margin=dict(t=20, b=40, l=40, r=20),
                xaxis_title="Cụm",
                yaxis_title="Số Khách Hàng"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Không có dữ liệu")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Key Insights
    st.markdown('<div class="card card-highlight">', unsafe_allow_html=True)
    st.markdown("#### 💡 Insights Chính")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        **🎯 Cụm Giá Trị Cao Nhất:**
        - 💎 Cụm 0: High-Value VIP
        - Chiến lược: VIP Loyalty + Premium Bundles
        """)
    with col2:
        st.markdown("""
        **📈 Tiềm Năng Tăng Trưởng:**
        - 🌟 Cụm 1: Occasional Premium
        - Chiến lược: Re-engagement + Seasonal
        """)
    with col3:
        st.markdown("""
        **🆕 Cơ Hội Chuyển Đổi:**
        - 🎯 Cụm 2: New Explorer
        - Chiến lược: Onboarding + Welcome
        """)
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# PAGE 2: CLUSTER DETAILS
# ============================================================================
elif page == "🔍 Chi Tiết Cụm":
    profile = CLUSTER_PROFILES[cluster_filter]
    
    st.markdown(f"""
    <div class="card cluster-{cluster_filter}" style="background: linear-gradient(135deg, {profile['color']}15 0%, {profile['color']}05 100%);">
        <h2 style="margin:0;">{profile['icon']} Cụm {cluster_filter}: {profile['name']}</h2>
        <p style="font-size:1.1rem; color:#475569; margin:0.5rem 0 0 0;"><strong>{profile['name_vi']}</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Persona
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("#### 👤 Persona Khách Hàng")
    st.info(profile['description'])
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Metrics
    if profiling_df is not None:
        cluster_data = profiling_df[profiling_df['Cluster'] == cluster_filter].iloc[0]
        
        cols = st.columns(5)
        metrics = [
            ("👥 Khách Hàng", f"{int(cluster_data['N_Customers']):,}", ""),
            ("📈 % Tổng", cluster_data['Pct_Total'], ""),
            ("💰 Doanh Thu", f"£{cluster_data['Total_Revenue_£']:,.0f}", ""),
            ("💵 Giá Trị TB", f"£{cluster_data['Avg_Value_£']:.2f}", ""),
            ("🔄 Tần Suất", f"{float(cluster_data['Frequency']):.1f}", "giao dịch"),
        ]
        
        for col, (label, value, unit) in zip(cols, metrics):
            with col:
                st.markdown(f"""
                <div class="metric-card">
                    <p class="metric-label">{label}</p>
                    <p class="metric-value" style="font-size:1.5rem;">{value}</p>
                    <p style="font-size:0.75rem; color:#94a3b8;">{unit}</p>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Characteristics & Strategies
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("#### 🎯 Đặc Điểm Chính")
        for char in profile['characteristics']:
            st.markdown(f"<p style='margin:0.5rem 0;'>{char}</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card card-highlight">', unsafe_allow_html=True)
        st.markdown("#### 💼 Chiến Lược Marketing")
        for strategy in profile['strategies']:
            st.markdown(f"""
            <div class="strategy-box">
                <p style="margin:0; font-weight:600;">{strategy}</p>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# PAGE 3: TOP RULES
# ============================================================================
elif page == "📋 Quy Tắc Hàng Đầu":
    profile = CLUSTER_PROFILES[cluster_filter]
    
    st.markdown(f'<p class="section-header">{profile["icon"]} Quy Tắc Mua Sắm - Cụm {cluster_filter}</p>', unsafe_allow_html=True)
    st.caption(f"**{profile['name']}** - Các quy tắc mua sắm được kích hoạt nhiều nhất")
    
    if rules_df is not None:
        cluster_rules = rules_df[rules_df['Cluster_ID'] == cluster_filter].sort_values('Activation_Rate_%', ascending=False)
        
        if len(cluster_rules) > 0:
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown("#### 📊 Top 10 Quy Tắc")
                top_rules = cluster_rules.head(10)[['Rule_Rank', 'Rule_Name', 'Activation_Rate_%', 'Avg_Weight']]
                st.dataframe(top_rules, use_container_width=True, hide_index=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown("#### 📈 Activation Rate")
                fig = px.bar(
                    cluster_rules.head(10),
                    x='Activation_Rate_%',
                    y='Rule_Name',
                    orientation='h',
                    color='Activation_Rate_%',
                    color_continuous_scale='Viridis'
                )
                fig.update_layout(
                    height=400,
                    showlegend=False,
                    yaxis={'categoryorder': 'total ascending'},
                    margin=dict(l=20, r=20, t=20, b=20)
                )
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning(f"Không tìm thấy quy tắc cho Cụm {cluster_filter}")
    else:
        st.info("Không có dữ liệu quy tắc")

# ============================================================================
# PAGE 4: BUNDLE RECOMMENDATIONS
# ============================================================================
elif page == "📦 Gợi Ý Bundle":
    profile = CLUSTER_PROFILES[cluster_filter]
    
    st.markdown(f'<p class="section-header">{profile["icon"]} Gợi Ý Bundle - Cụm {cluster_filter}</p>', unsafe_allow_html=True)
    st.caption(f"**{profile['name']}** - Bundle sản phẩm dựa trên quy tắc kết hợp thực tế")
    
    # Load association rules
    try:
        rules_df = pd.read_csv('data/processed/rules_apriori_filtered.csv', encoding='utf-8')
        
        # CLUSTER-SPECIFIC SORTING STRATEGIES
        # Mỗi cụm có chiến lược khác nhau để gợi ý sản phẩm
        sorting_config = {
            0: ('lift', 'Premium Collector - Quy tắc mạnh mẽ nhất'),           # Premium: highest lift (strongest associations)
            1: ('support', 'Casual Shopper - Sản phẩm phổ biến nhất'),          # Casual: highest support (popular bundles)
            2: ('confidence', 'New Explorer - Quy tắc chắc chắn nhất'),         # New: high confidence (reliable recommendations)
            3: ('leverage', 'Deal Hunter - Quy tắc tiết kiệm nhất')             # Deal: high leverage (best value)
        }
        
        sort_by, cluster_desc = sorting_config[cluster_filter]
        rules_df_sorted = rules_df.sort_values(sort_by, ascending=False)
        
        # Thêm chỉ số để theo dõi vị trí
        rules_df_sorted = rules_df_sorted.reset_index(drop=True)
        
        # Lấy skip dựa trên cluster để hiển thị bundle khác nhau
        skip_indices = {
            0: list(range(0, 20, 3)),      # Cluster 0: bundles 0, 3, 6, 9, 12, 15
            1: list(range(1, 20, 3)),      # Cluster 1: bundles 1, 4, 7, 10, 13, 16
            2: list(range(2, 20, 3)),      # Cluster 2: bundles 2, 5, 8, 11, 14, 17
            3: list(range(0, 30, 5))       # Cluster 3: bundles 0, 5, 10, 15, 20, 25
        }
        
        # Extract bundle information
        bundles_display = []
        for cluster_idx in skip_indices[cluster_filter][:6]:
            if cluster_idx < len(rules_df_sorted):
                row = rules_df_sorted.iloc[cluster_idx]
                antecedents = row['antecedents_str'].strip()
                consequents = row['consequents_str'].strip()
                confidence = row['confidence']
                lift = row['lift']
                support = row['support']
                
                # Create bundle info
                bundle_name = f"{antecedents} + {consequents}"
                rating = "⭐" * min(5, max(1, int(confidence * 5)))
                metrics = f"Confidence: {confidence:.1%} | Lift: {lift:.2f} | Support: {support:.2%}"
                bundles_display.append((bundle_name, rating, metrics, confidence, lift))
        
        # Display cluster description
        st.info(f"🎯 {cluster_desc}")
        
        # Display bundles
        if bundles_display:
            for idx, (bundle, rating, metrics, conf, lift) in enumerate(bundles_display, 1):
                # Color code by lift value
                if lift > 10:
                    color = "#10b981"  # Green - excellent
                elif lift > 5:
                    color = "#3b82f6"  # Blue - good
                else:
                    color = "#f59e0b"  # Amber - moderate
                
                st.markdown(f"""
                <div class="card cluster-{cluster_filter}" style="border-left: 5px solid {color};">
                    <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                        <div style="flex:1;">
                            <h4 style="margin:0.5rem 0;">📦 Bundle #{idx}</h4>
                            <p style="color:#1e293b; margin:0.5rem 0; font-size:0.9rem; line-height:1.4;"><strong>{bundle}</strong></p>
                            <p style="color:#64748b; margin:0.5rem 0; font-size:0.85rem;">{metrics}</p>
                        </div>
                        <div style="text-align:right;">
                            <p style="font-size:1.2rem; margin:0;">{rating}</p>
                            <p style="color:{color}; font-weight:700; font-size:0.9rem; margin:0.5rem 0;">Lift: {lift:.2f}x</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.markdown("")
        else:
            st.info("📊 Không có dữ liệu bundle từ quy tắc kết hợp")
            
    except Exception as e:
        st.error(f"⚠️ Lỗi tải dữ liệu: {str(e)}")

# ============================================================================
# PAGE 5: MARKETING STRATEGY
# ============================================================================
else:
    profile = CLUSTER_PROFILES[cluster_filter]
    
    st.markdown(f'<p class="section-header">{profile["icon"]} Chiến Lược Marketing - Cụm {cluster_filter}</p>', unsafe_allow_html=True)
    st.caption(f"**{profile['name']}** - Chiến lược được tối ưu hóa cho phân khúc này")
    
    # Priority
    priority_map = {
        0: ("🔴 ƯU TIÊN 1", "badge-high", "Giữ Chân + Upsell"),
        1: ("🟡 ƯU TIÊN 2", "badge-medium", "Kích Hoạt Lại"),
        2: ("🟢 ƯU TIÊN 3", "badge-low", "Chuyển Đổi"),
        3: ("🟢 ƯU TIÊN 3", "badge-low", "Tăng Giỏ Hàng")
    }
    
    priority, badge_class, focus = priority_map[cluster_filter]
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-label">Mức Ưu Tiên</p>
            <p><span class="badge {badge_class}">{priority}</span></p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-label">Tập Trung</p>
            <p class="metric-value" style="font-size:1.2rem;">{focus}</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        if profiling_df is not None:
            cluster_data = profiling_df[profiling_df['Cluster'] == cluster_filter].iloc[0]
            st.markdown(f"""
            <div class="metric-card">
                <p class="metric-label">Quy Mô</p>
                <p class="metric-value" style="font-size:1.2rem;">{int(cluster_data['N_Customers']):,}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Strategies
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("#### 🎯 Chiến Lược Được Khuyến Nghị")
    
    for strategy in profile['strategies']:
        st.markdown(f"""
        <div class="strategy-box">
            <p style="margin:0; font-size:1.1rem;">{strategy}</p>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Quick Wins
    quick_wins = {
        0: ["🎁 Khởi động VIP Loyalty với 15% discount", "🎉 Tổ chức sự kiện VIP", "💎 Gợi ý sản phẩm premium"],
        1: ["🔔 Gửi email kích hoạt lại", "💝 Offer 20-30% discount", "⏰ Chiến dịch theo mùa"],
        2: ["🎁 Welcome gift 10-15% off", "📚 Gửi content giáo dục", "⭐ Show reviews & testimonials"],
        3: ["💰 Discount tier £50 = 15% off", "🏷️ Bundle clearance", "📧 Cảnh báo giảm giá"]
    }
    
    st.markdown('<div class="card card-highlight">', unsafe_allow_html=True)
    st.markdown("#### 💡 Quick Wins (Thực Hiện Ngay)")
    for win in quick_wins[cluster_filter]:
        st.markdown(f"• {win}")
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("""
<div class="footer">
    <p><strong>📊 Dashboard Phân Cụm Khách Hàng & Chiến Lược Marketing</strong></p>
    <p style="font-size:0.9rem;">
        🔬 K-Means Clustering | 📊 RFM Analysis | 🔗 Association Rules Mining
    </p>
    <p style="font-size:0.8rem; color:#94a3b8;">
        📁 Data: Retail Transaction | 🕐 Updated: December 2025
    </p>
</div>
""", unsafe_allow_html=True)
