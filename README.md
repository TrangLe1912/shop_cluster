# MINI PROJECT: PHÂN CỤM KHÁCH HÀNG DỰA TRÊN LUẬT KẾT HỢP

![Project Banner](https://img.shields.io/badge/Python-3.10%2B-blue) ![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red) ![Scikit--Learn](https://img.shields.io/badge/Scikit--Learn-1.3%2B-orange)

## Giới thiệu dự án

Dự án này là một phần của môn **Data Mining** dưới sự hướng dẫn của **ThS. Lê Thị Thùy Trang**. Mục tiêu chính là phân cụm khách hàng dựa trên các luật kết hợp (association rules) được khai phá từ dữ liệu giao dịch bán lẻ (UK Retail Data). Thay vì sử dụng các đặc trưng truyền thống như RFM (Recency, Frequency, Monetary), dự án tập trung vào việc biến các luật kết hợp từ thuật toán Apriori hoặc FP-Growth thành vector đặc trưng để phân cụm khách hàng bằng K-Means (và so sánh với Agglomerative Clustering). 

Điều này giúp xác định các nhóm khách hàng có hành vi mua sắm tương đồng (ví dụ: thường mua các sản phẩm thảo mộc cùng nhau), từ đó đề xuất chiến lược marketing cá nhân hóa như bundle/cross-sell, ưu đãi VIP, hoặc chiến dịch kích hoạt khách ngủ đông.

### Mục tiêu
- Hiểu quy trình kết hợp giữa khai phá luật và phân cụm.
- Trích xuất đặc trưng từ luật kết hợp và RFM.
- Áp dụng thuật toán phân cụm (K-Means chính, Agglomerative so sánh) để tìm nhóm hành vi.
- Trực quan hóa và diễn giải các cụm.
- Đề xuất chiến lược kinh doanh dựa trên profiling cụm.
- Xây dựng dashboard Streamlit để trực quan hóa kết quả.

Dự án sử dụng dữ liệu không nhãn, phù hợp với Unsupervised Learning. K-Means được chọn vì dễ triển khai, dễ diễn giải, và hoạt động tốt với dữ liệu đa chiều (sau khi chuẩn hóa).


## Yêu cầu hệ thống
- **Python:** 3.10+ (đã kiểm tra với 3.10.19 và 3.11.5).
- **Môi trường ảo:** Sử dụng Conda (tên: `shopping_env`).
- **Thư viện chính:** 
  - Data processing: pandas, numpy.
  - Visualization: matplotlib, seaborn, plotly.
  - Machine Learning: scikit-learn (KMeans, AgglomerativeClustering, PCA, metrics như silhouette_score).
  - Dashboard: streamlit.
- **Dữ liệu:** Dữ liệu gốc từ `data/raw/online_retail.csv`. Dữ liệu đã xử lý lưu ở `data/processed`.

## Cài đặt và Chạy
### 1. Clone repository
```bash
git clone https://github.com/ngocsonn2005/mini-project-shop_cluster-.git
cd mini-project-shop_cluster-
```

### 2. Tạo và kích hoạt môi trường ảo
```bash
conda create -n shopping_env python=3.10
conda activate shopping_env
```

### 3. Cài đặt dependencies
Tất cả thư viện được liệt kê trong `requirements.txt`. Chạy lệnh:
```bash
pip install -r requirements.txt
```

### 4. Chạy các Notebook
Dự án được tổ chức qua các Jupyter Notebook trong thư mục `notebooks/`. Chạy để tái tạo pipeline:
```bash
python run_papermill.py
```

Mở notebook bằng Jupyter:
```bash
jupyter notebook
```

### 5. Chạy Dashboard Streamlit
Dashboard trực quan hóa kết quả (profiling cụm, phân tích rules, tìm kiếm khách hàng). Chạy từ file `app.py`:
```bash
streamlit run app.py
```
- Truy cập tại: http://localhost:8501.
- Dashboard tải dữ liệu từ `data/processed` (profiling report, clusters, rules, features).

### 6. Cấu trúc thư mục
```
MINI-PROJECT-SHOP-CLUSTER-
├── data/
│   ├── raw/                  # Dữ liệu gốc (online_retail.csv)
│   ├── processed/            # Dữ liệu đã xử lý
│   │   ├── cleaned_uk_data.csv  # Dữ liệu sạch
│   │   ├── rules_apriori_filtered.csv  # Luật từ Apriori
│   │   ├── rules_fpgrowth_filtered.csv # Luật từ FP-Growth
│   │   ├── selected_rules_for_clustering.csv  # Top 200 luật chọn lọc
│   │   ├── customer_clusters.csv  # Nhãn cụm cho khách hàng
│   │   ├── cluster_profiling_report.csv  # Báo cáo profiling
│   │   └── features/         # Features (binary, combined, RFM scaled, etc.)
│   │       ├── metadata.json
│   │       ├── X_binary.npy
│   │       ├── X_combined.npy
│   │       └── ...
├── notebooks/                # Các Jupyter Notebook
│   ├── preprocessing_and_eda.ipynb
│   ├── apriori_modelling.ipynb
│   ├── fp_growth_modelling.ipynb
│   ├── basket_preparation.ipynb
│   ├── clustering_from_rules.ipynb
│   ├── compare_apriori_fpgrowth.ipynb
│   ├── my_complete_project.ipynb  # Notebook tổng hợp
│   └── .ipynb_checkpoints/   # Checkpoint tự động
├── src/                      # Source code (thư viện tùy chỉnh)
│   ├── __pycache__/
│   └── cluster_library.py    # Lớp chính: RuleBasedCustomerClusterer, etc.
├── app.py                    # Dashboard Streamlit
├── .gitignore                # Ignore file
├── LICENSE.txt               # License
├── README.md                 # Tài liệu này
├── requirements.txt          # Dependencies
└── run_papermill.py          # Script chạy papermill (nếu cần)
```

## Pipeline Thực Hiện
Dựa trên yêu cầu dự án (từ 2.2.1 đến 2.2.7):

1. **Chọn và Trình bày Luật Kết Hợp (2.2.1)**: Sử dụng FP-Growth (ưu tiên), lọc với min_support=0.01, min_confidence=0.3, min_lift=1.5. Chọn top 200 luật theo lift. Hiển thị 10 luật tiêu biểu (ví dụ: herb markers với lift cao ~74).

2. **Feature Engineering (2.2.2)**: Xây dựng 2 biến thể:
   - **Baseline**: Binary (0/1) dựa trên luật (shape: 3921 khách × 200 luật).
   - **Nâng cao**: Weighted (lift × confidence) + RFM, scale bằng StandardScaler/MinMaxScaler (shape: 3921 × 66).

3. **Phân Cụm và Đánh Giá (2.2.3-2.2.4)**: Chọn K=2 bằng Elbow/Silhouette. Sử dụng K-Means (best Silhouette: 0.42 cho biến thể nâng cao). So sánh với Agglomerative. Đánh giá: Silhouette và Davies-Bouldin.

4. **Visualization (2.2.5)**: PCA 2D scatter plot, Elbow/Silhouette plots.

5. **Profiling và Diễn Giải (2.2.6)**: 2 cụm chính (ví dụ: "Khách VIP trung thành" với Monetary cao £2864, "Khách mua ít" với £622). Đề xuất chiến lược (VIP program, win-back campaigns).

6. **Dashboard (2.2.7)**: Streamlit app với tabs: Tổng quan, Profiling, Phân tích Rules, Tìm kiếm KH.

### Kết quả chính
- Tổng luật: 1794 (FP-Growth).
- Số cụm: 2 (best từ biến thể nâng cao).
- Khách hàng: 3921.
- Output: Files ở `data/processed` (clusters, profiling report).

## Khuyến khích Nâng cấp
- So sánh thêm DBSCAN.
- Phân cụm basket hoặc sản phẩm.

## Tác giả và Thông tin
- **Nhóm:** 7 (Data Mining Class).
- **Giảng viên:** ThS. Lê Thị Thùy Trang.
- **Liên hệ:** [GitHub Repo](https://github.com/ngocsonn2005/mini-project-shop_cluster-) (nếu có).
- **License:** MIT (xem LICENSE.txt).

Nếu gặp lỗi, kiểm tra đường dẫn project (`E:\Data Mining\mini-project-shop_cluster-`) và đảm bảo dữ liệu tồn tại. Cảm ơn! 🚀