# Third part of case study: Shopping Cart Analysis
📊 Giới thiệu dự án
Dự án Customer Segmentation Dashboard là một hệ thống phân tích và phân cụm khách hàng tự động sử dụng kỹ thuật Association Rules Mining kết hợp với RFM Analysis và K-Means Clustering. Dự án cung cấp dashboard trực quan giúp doanh nghiệp hiểu rõ hành vi mua sắm của khách hàng và đề xuất chiến lược marketing cá nhân hóa.

🎯 Mục đích
Phân tích hành vi mua kèm: Khám phá các sản phẩm thường được mua cùng nhau

Phân cụm khách hàng: Nhóm khách hàng có đặc điểm hành vi tương tự

Đề xuất marketing: Đưa ra chiến lược tiếp thị phù hợp cho từng nhóm

Trực quan hóa: Hiển thị kết quả qua dashboard dễ sử dụng

🔄 Pipeline xử lý
Dự án thực hiện theo pipeline 7 bước:

text
1. 📝 Preprocessing & EDA → 2. 🛒 Basket Preparation → 3. 🔗 Apriori Modelling
       ↓                           ↓                           ↓
7. 🚀 Marketing Strategies ← 6. 👥 Cluster Profiling ← 5. 🎯 Clustering ← 4. 🌱 FP-Growth Modelling
📁 Cấu trúc dự án
Thư mục chính:
text
├── data/                          # Dữ liệu
│   ├── raw/                       # Dữ liệu gốc
│   └── processed/                 # Dữ liệu đã xử lý
├── notebooks/                     # Jupyter notebooks phân tích
│   ├── runs/                      # Notebooks đã execute
│   └── *.ipynb                    # 7 notebooks chính
├── app.py                         # Dashboard Streamlit
├── run_papermill.py              # Pipeline automation
└── requirements.txt              # Thư viện cần thiết

7 Notebooks phân tích:
preprocessing_and_eda.ipynb - Làm sạch dữ liệu và EDA

basket_preparation.ipynb - Chuẩn bị basket matrix

apriori_modelling.ipynb - Khai thác luật kết hợp (Apriori)

fp_growth_modelling.ipynb - Khai thác luật kết hợp (FP-Growth)

compare_apriori_fpgrowth.ipynb - So sánh 2 thuật toán

clustering_from_rules.ipynb - Phân cụm khách hàng

cluster_profiling_and_interpretation.ipynb - Diễn giải cụm và đề xuất

🚀 Tính năng chính
1. Dashboard Streamlit (app.py)
7 section tương tác với giao diện thân thiện

Visualization trực quan bằng Plotly và Matplotlib

Lọc và tìm kiếm khách hàng theo cụm

Đề xuất bundle và cross-sell tự động

2. Tự động hóa Pipeline (run_papermill.py)
Chạy end-to-end 7 notebooks tự động

Truyền parameters linh hoạt

Batch mode cho chạy production

Reproducibility đảm bảo

3. Phân tích nâng cao
Association Rules Mining với 2 thuật toán

Feature Engineering kết hợp rules + RFM

Silhouette Analysis chọn số cụm tối ưu

Cluster Profiling chi tiết

📊 Kết quả đạt được
4 Cụm khách hàng được xác định:
Cụm	Tên tiếng Việt	Tên tiếng Anh	Đặc điểm
0	Khách VIP Trung thành	VIP Loyal Customers	Recency thấp, Frequency cao, Monetary cao
1	Khách Thường xuyên	Regular Customers	Tần suất ổn định, giá trị trung bình
2	Khách Ngủ đông	Inactive Customers	Lâu không mua, cần reactivation
3	Khách Tiềm năng	Potential Customers	Mới, có tiềm năng phát triển
Chiến lược marketing cho từng cụm:
Cụm 0: Bundle cao cấp, early access, personal service

Cụm 1: Loyalty program, cross-sell, email marketing

Cụm 2: Reactivation campaign, survey, discount đặc biệt

Cụm 3: Welcome package, educational content, trial offers

📈 Các chỉ số đánh giá
Association Rules:
Support threshold: 0.03 (3%)

Confidence threshold: 0.4 (40%)

Lift threshold: 1.2

Top rules: 100 luật tốt nhất

Clustering:
Silhouette score: 0.42 (tốt với K=4)

Feature engineering: Weighted rules + RFM

Clustering algorithm: K-Means với PCA visualization