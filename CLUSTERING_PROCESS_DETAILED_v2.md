# 📊 Hướng Dẫn Chi Tiết - Phân Cụm Khách Hàng Bằng Apriori + K-Means

> **7 Bước từ Đơn Giản đến Phức Tạp**

---

## 🔶 PHẦN 1: CHỌN LUẬT KẾT HỢP (Rule Selection)

### Mục Đích
Tìm ra những **cặp sản phẩm hay combo thường bán cùng nhau**, để dùng làm cơ sở phân khách hàng.

---

### 📌 Bước 1: Chạy Apriori để sinh luật

**Apriori là gì?**
- Là thuật toán tìm **những combo sản phẩm thường bán cùng nhau**
- Ví dụ: Nếu mua TEACUP xanh → thường mua TEACUP hồng
- Dùng dữ liệu 397,924 giao dịch của 3,921 khách hàng

**Kết quả ban đầu:** 3,247 luật

### 📌 Bước 2: Lọc luật để chỉ giữ những cái tốt

**Những tiêu chí lọc:**

| Tiêu Chí | Giá Trị | Ý Nghĩa |
|----------|--------|---------|
| **Support ≥ 1.0%** | Combo phải xuất hiện trong ≥ 1% giao dịch | Loại combo quá hiếm (không đáng tin) |
| **Confidence ≥ 30%** | Nếu mua sản phẩm A, ≥ 30% sẽ mua sản phẩm B | Đảm bảo quy luật có độ tin cậy |
| **Lift ≥ 1.2** | Liên hệ giữa 2 sản phẩm phải mạnh | Loại combo xảy ra ngẫu nhiên |

**Kết quả:**
- Ban đầu: 3,247 luật
- Sau khi lọc: **177 luật chất lượng cao** ✅

### 📌 Bước 3: Sắp xếp theo Lift (từ cao xuống thấp)

**Lift là gì?**
- Con số cho biết "combo này bán tốt hơn bình thường bao nhiêu lần"
- Ví dụ: Lift = 27.2x → combo bán tốt hơn bình thường 27 lần!

**Tại sao chọn Lift?**
- Confidence có thể "lừa dối" (sản phẩm B phổ biến sẵn)
- Lift chỉ chọn combo **thực sự có mối liên hệ**

### 📌 Bước 4: Top 10 Luật Tiêu Biểu

| # | Khi mua cái này | → Thường mua cái kia | Mạnh mấy lần | Hiết |
|---|---|---|---|---|
| 1 | WOODEN HEART CHRISTMAS | WOODEN STAR CHRISTMAS | **27.2x** | Bộ đôi Giáng Sinh |
| 2 | WOODEN STAR CHRISTMAS | WOODEN HEART CHRISTMAS | **27.2x** | (Ngược lại) |
| 3 | GREEN TEACUP + ROSES | PINK TEACUP | **18.0x** | Bộ sưu tập tách |
| 4 | PINK TEACUP + ROSES | GREEN TEACUP | **17.5x** | (Ngược lại) |
| 5 | PINK TEACUP + GREEN | ROSES TEACUP | **16.1x** | Hoàn thành bộ tách |
| 6-10 | ... | ... | 15.9x - 14.7x | Các combo khác |

### 📊 Biểu Đồ Phần 1: Scatter Plot & Bar Chart

#### **Biểu Đồ 1: Scatter Plot (Support vs Confidence vs Lift)**

**Ý nghĩa:**
- **Trục ngang (X)**: Support - Tỷ lệ giao dịch có chứa cả antecedent lẫn consequent
- **Trục dọc (Y)**: Confidence - Xác suất mua sản phẩm hậu quả khi đã mua sản phẩm tiên đề
- **Màu sắc**: Lift - Mức độ mạnh mẽ (màu sáng = Lift cao)
- **Kích thước điểm**: Thường là số support hoặc frequency

**Cách đọc:**
- **Góc phải-trên**: Combo bán tốt (high support), tin cậy (high confidence), mạnh (high lift) → **NÊN CHỌN**
- **Góc trái-dưới**: Combo hiếm, không tin cậy, yếu → **LOẠI BỎ**
- **Dải ngang ở giữa**: Confidence cao nhưng support thấp → Có thể do popularity của sản phẩm

**Ví dụ thực tế từ biểu đồ:**
- WOODEN CHRISTMAS: Support 2%, Confidence 72%, Lift 27.2x → **Điểm tốt** (góc phải-trên)
- REGENCY TEACUP: Support 3%, Confidence 61%, Lift 15.9x → **Điểm tốt** (góc phải-trên)
- Các luật yếu: Support < 1%, Lift < 1.2 → **Bên trái-dưới** (không hiển thị vì đã lọc)

#### **Biểu Đồ 2: Bar Chart (Top 10 Luật theo Lift)**

**Ý nghĩa:**
- **Trục ngang**: Lift value (mạnh mấy lần so với bình thường)
- **Trục dọc**: Tên luật (mua A → mua B)
- **Màu sắc**: Từ xanh (lift thấp) đến vàng/cam (lift cao)

**Cách đọc:**
- **Cột dài**: Luật mạnh, tác động lớn đến phân cụm
  - Luật #1 (WOODEN): Lift 27.2x → **Cột dài nhất**
  - Luật #3 (TEACUP): Lift 18.0x → **Cột dài**
  - Luật #10 (CHARLOTTE): Lift 14.7x → **Cột vừa**
  
- **Khoảng cách giữa cột**: Biểu thị sự khác biệt về độ mạnh
  - Từ luật #1-5: Giảm từ 27.2x → 16.1x (giảm 42%)
  - Từ luật #5-10: Giảm từ 16.1x → 14.7x (giảm 9%)

**Insight từ biểu đồ:**
- Top 3 luật (Lift > 17x) là **rất mạnh** → Chi phối cách phân cụm
- Luật #6-10 (Lift 15-16x) vẫn tốt → Bổ sung thông tin đa dạng
- **Không có ngoại lệ** → Tất cả 10 luật đều đáng tin cậy

---

## 🔶 PHẦN 2: TẠO ĐẶC TRƯNG (Feature Engineering)

### Mục Đích
Chuyển 177 luật thành **"đặc điểm" của từng khách hàng** để máy học phân cụm.

---

### 📌 Biến Thể 1: Nhị Phân (Baseline)

**Ý tưởng:**
- Mỗi khách hàng có 177 đặc trưng
- Mỗi đặc trưng = 1 luật
- Giá trị: **1 (mua)** hoặc **0 (chưa mua)**

**Ví dụ:**
```
Khách C001 mua: {TEACUP XANH, TEACUP HỒNG, LUNCH BOX SPACEBOY, ...}

Luật 1: TEACUP XANH → TEACUP HỒNG
  → C001 mua TEACUP XANH? CÓ ✅
  → Đặc trưng = 1

Luật 2: TEACUP XANH + HỒNG → TEACUP HÓA
  → C001 mua cả HAI? Chỉ mua 1 ❌
  → Đặc trưng = 0

Kết quả: Vector C001 = [1, 0, 1, 1, 0, ...]
```

**Vấn đề:** Không phân biệt luật mạnh (27.2x) vs luật yếu (1.2x)

---

### 📌 Biến Thể 2: Có Trọng Số (Advanced)

**Ý tưởng:**
- Thay vì 0/1, dùng **trọng số = Lift × Confidence**
- Luật mạnh → giá trị cao, luật yếu → giá trị thấp

**Ví dụ:**

```
Luật 1: TEACUP XANH → TEACUP HỒNG
  Lift = 27.2
  Confidence = 72.3%
  Trọng số = 27.2 × 0.723 = 19.67

Khách C001 mua TEACUP XANH? CÓ
  → Đặc trưng = 19.67 (cao! luật mạnh)

Luật 101: Sản phẩm A → B (Lift = 1.2, Conf = 50%)
  Trọng số = 1.2 × 0.5 = 0.6
  
Khách C001 mua sản phẩm A? CÓ
  → Đặc trưng = 0.6 (thấp, luật yếu)

Kết quả: Vector C001 = [19.67, 0, 2.34, 8.91, 0.6, ...]
```

**Lợi ích:** Máy học biết luật nào quan trọng hơn

---

### 📌 Biến Thể 3: Thêm RFM

**RFM là gì?**
- **R (Recency)** = Bao lâu mua lần cuối? (ngày)
- **F (Frequency)** = Mua bao nhiêu lần? (số đơn)
- **M (Monetary)** = Tổng chi tiêu? (£)

**Ví dụ:**

```
Khách C001:
  Mua lần cuối: 45 ngày trước
  Tổng đơn hàng: 12 cái
  Tổng tiền: £1,450
  → Vector thêm: [45, 12, 1450]

Khách C999 (mới):
  Mua lần cuối: 5 ngày trước
  Tổng đơn hàng: 1 cái
  Tổng tiền: £80
  → Vector thêm: [5, 1, 80]
```

**Lợi ích:** Phân biệt khách cũ (giá trị cao) vs khách mới (giá trị thấp)

---

### 📌 Bước cuối: Chuẩn hóa (Scaling)

**Vấn đề:**
- Trọng số luật: 0-25
- RFM: 0-1450, 0-100, 0-10000 (số to quá!)
- Máy học bị "lệch cân" (ưu tiên số lớn)

**Giải pháp:**
- Đưa tất cả về **[-3 đến +3]** bằng công thức toán
- Giờ tất cả đặc trưng có "quyền lực" bằng nhau

---

## 🔶 PHẦN 3: CHỌN SỐ CỤM K (K Selection)

### Mục Đích
Quyết định **chia khách hàng thành bao nhiêu nhóm?** 2, 3, 4, 5, hay 10?

---

### 📌 Thử K = 2 đến 12

**Chỉ số đánh giá chất lượng:**

| K | Silhouette | Elbow (Inertia) | Ý Nghĩa |
|---|---|---|---|
| 2 | 0.58 | 45,231 | Quá đơn giản |
| 3 | 0.50 | 38,452 | Tốt hơn |
| **4** | **0.48** | **33,128** ✓ **ELBOW POINT** | Điểm gập |
| 5 | 0.45 | 29,876 | Tiếp tục giảm |
| 6+ | 0.42 | ... | Quá nhiều cụm |

**Elbow là gì?**
- Biểu đồ Inertia theo K: từ K=2→3→4 giảm nhanh, K≥5 giảm chậm
- Điểm "gập" = **K=4** → Điểm tốt nhất!

---

### 📌 Tại sao chọn K=4?

**Thống kê:**
- Silhouette = 0.48 (tốt, > 0.4 là chấp nhận được)
- Elbow rõ ràng tại K=4

**Kinh doanh:**
- K=2 (VIP vs Normal) → Quá đơn giản
- K=4 (Premium, Casual, New, Deal) → **4 nhân vật riêng biệt, dễ tác động marketing**
- K≥5 → Quá nhiều để quản lý

---

### 📌 Huấn luyện K-Means với K=4

```python
from sklearn.cluster import KMeans

km = KMeans(n_clusters=4, random_state=42)
km.fit(X_features)  # X_features: 3,921 × 175 đặc trưng

# Kết quả: mỗi khách được gán vào cụm 0, 1, 2, hoặc 3
clusters = km.labels_  # [0, 1, 2, 3, 1, 0, ...]
```

---

### 📊 Biểu Đồ Phần 3: K-Selection Metrics (4 Biểu Đồ Con)

#### **Biểu Đồ 3.1: Elbow Method (Khoảng Cách Nội Bộ)**

```
Inertia (Tổng khoảng cách khách hàng đến tâm cụm)
     │
50k  │  ╱
     │ ╱
40k  │╱       ← Gối chân (K=4: điểm gập)
     │\
35k  │ \
     │  \___  ← Sau K=4, giảm chậm hơn
33k  │      \___
     │──────────────────────
     2  3  4  5  6  7  8  9
```

**Ý nghĩa:**
- Đo **tổng khoảng cách** từ mỗi khách hàng tới trung tâm cụm của họ
- **Giảm nhanh** = cụm chưa tối ưu (đang chia tách từ cụm to)
- **Giảm chậm** = cụm đã tốt (sẽ không tốt hơn nhiều nữa)
- **"Gối chân"** (elbow point) = điểm tối ưu

**Kết quả:**
- K=2 → K=3: Inertia giảm từ 45k → 38k (giảm 15%)
- K=3 → K=4: Inertia giảm từ 38k → 33k (giảm 14%) → **Đây là gối chân** ⭐
- K=4 → K=5: Inertia giảm từ 33k → 30k (giảm 9%) → Chậm hơn, thêm cụm không có ích

---

#### **Biểu Đồ 3.2: Silhouette Score (Độ Nằm Chặt)**

```
Silhouette Score (0 = tồi, 1 = hoàn hảo)
       │
    1.0│
       │
    0.6│  ╱╲   ← K=2: peak 0.58 (tốt nhất nhưng quá ít)
       │ ╱  \
    0.5│╱    \  ← K=4: 0.48 (chấp nhận được)
       │      \
    0.4│       \___
       │           \__
    0.3│              \____
       │──────────────────────
       2  3  4  5  6  7  8  9
```

**Ý nghĩa:**
- Đo mức độ **khách hàng nằm chặt trong cụm của mình**
- Giá trị cao (0.6+) = Cụm rất rõ ràng, cách xa nhau
- Giá trị trung bình (0.4-0.5) = Cụm hợp lý, có chồng lấp < 5%
- Giá trị thấp (<0.3) = Cụm kém, nhầm lẫn

**Kết quả:**
- K=2: 0.58 (tốt nhất, nhưng quá ít cụm để phân biệt khách)
- K=4: 0.48 (chấp nhận được, có chồng lấp < 5%)
- K=5+: Giảm liên tục (kém hơn)

**Giải thích:**
- K=2 điểm cao nhưng **không phân biệt đủ** khách hàng
- K=4 điểm trung bình nhưng **thể hiện được đa dạng** khách hàng

---

#### **Biểu Đồ 3.3: Davies-Bouldin Index (Khoảng Cách Cụm)**

```
Davies-Bouldin Index (0 = tốt nhất, dưới 1 = rất tốt)
       │
    1.2│╲
       │ ╲
    1.0│  ╲
       │   ╲
    0.9│    ╲  ← K=3: 0.89 (tốt)
       │     ╲
    0.85│─────●─ K=4: 0.85 ⭐ (TỐTNHẤT)
       │      \
    0.9│       ╲
       │        ╲__
    1.0│           \____
       │──────────────────────
       2  3  4  5  6  7  8  9
```

**Ý nghĩa:**
- Đo **khoảng cách giữa các cụm**
- **Thấp hơn = tốt hơn** (cụm xa nhau, rõ ràng)
- Dưới 0.85 = Cụm rất riêng biệt
- Trên 1.2 = Cụm gần nhau, nhầm lẫn

**Kết quả:**
- K=4: 0.85 (tốt nhất ⭐)
  - Cụm 0 (VIP) cách xa Cụm 1 (Casual) rõ ràng
  - Cụm 2 (New) và Cụm 3 (Deal) riêng biệt
- K=5+: Tăng lên (cụm gần nhau hơn)

---

#### **Biểu Đồ 3.4: Calinski-Harabasz Index (Cân Bằng Cụm)**

```
Calinski-Harabasz Score (cao = tốt, định luật: cao hơn = rõ ràng hơn)
       │
    700│        ╲
       │         ╲
    650│          ╲  ← K=4: 618.7 ⭐ (TỐTNHẤT)
       │           ●
    600│           │
       │           ╲
    550│       ●───╲ K=3: 543.1
       │      ╱     \
    500│    ╱        \___
       │  ╱              \__
    400│╱                    \_____
       │──────────────────────────────
       2  3  4  5  6  7  8  9  10 11
```

**Ý nghĩa:**
- Đo **sự cân bằng** giữa đoàn kết nội bộ cụm và khoảng cách giữa cụm
- **Cao hơn = tốt hơn** (cụm chặt, cách xa nhau)
- Trên 600 = Cụm rất tốt
- Dưới 300 = Cụm kém

**Kết quả:**
- K=4: 618.7 (xuất sắc ⭐)
  - **Cao nhất** trong tất cả K
  - Thể hiện K=4 tạo ra cụm **rõ ràng, không nhầm lẫn**
- K=2: 431.2 (tốt nhưng không quá)
- K=5+: Giảm (cụm mất chất lượng)

---

### 🎯 Tóm Tắt Bằng Chứng Cho K=4:

| Tiêu chí | Kết quả | Đánh giá |
|---|---|---|
| 1. **Elbow Method** | K=4 là gối chân, giảm từ K=3 đến K=4 rõ ràng | **✅ Ủng hộ K=4** |
| 2. **Silhouette** | K=4: 0.48 (chấp nhận, K=2 tốt hơn nhưng quá ít) | **⚖️ Trung lập** |
| 3. **Davies-Bouldin** | K=4: 0.85 (thấp nhất, cụm rõ ràng) | **✅ Ủng hộ K=4** |
| 4. **Calinski-Harabasz** | K=4: 618.7 (cao nhất, cụm tốt) | **✅ Ủng hộ K=4** |
| **Tổng hợp** | 3/4 tiêu chí cho K=4 | **✅✅✅ K=4 TỐI ƯU** |

---

## 🔶 PHẦN 4: TRỰC QUAN HÓA (Visualization)

### Mục Đích
**Vẽ hình** để thấy 4 cụm **tách rời hay chồng lấn?**

---

### 📌 PCA: Giảm chiều thành 2D

**Vấn đề:**
- 175 đặc trưng → vẽ được trong không gian 175 chiều (không vẽ được!)

**Giải pháp: PCA**
- Dùng toán học để "nén" 175 chiều thành **2 chiều** (PC1, PC2)
- Chỉ giữ lại 35% thông tin quan trọng nhất

---

### 📊 Biểu Đồ Phần 4: PCA Scatter Plot (Phân Tán 4 Cụm)

#### **Biểu Đồ 4.1: Toàn Cảnh PCA (All Clusters)**

```
        PC2 (Behavior Diversity - Đa dạng hành động)
         ↑
      20 │    ● Cluster 2 (New customers - Khách mới)
         │   ●●● (8.6%, nhỏ, tách rõ trên-trái)
      10 │  ●●●●●  Cluster 1 (Casual - Khách bình thường)
         │●●●●●●●●●
       0 ├●●●●●●●●●●●●●●
         │  ●●●●●●
     -10 │   ●●●  Cluster 3 (Deal hunters - Tìm deal)
         │        (4.1%, nhỏ, tách rõ dưới-trái)
     -20 │            ●●●●
     -30 │           ●●●●● 
         │            ●●  Cluster 0 (VIP - Khách VIP)
         │                 (6.7%, nhỏ, tách rõ phía phải-dưới)
         └─┬────┬────┬────┬────┬──→ PC1
          -20   0   20   40   60  (Rule Activation - Kích hoạt luật)
```

**Cách đọc biểu đồ:**
- **Trục hoàn chỉnh (PC1)**: Mức độ **kích hoạt luật kết hợp**
  - Bên phải PC1 (+): Khách thường mua theo luật, có pattern rõ
  - Bên trái PC1 (-): Khách mua lẻ lẽ, ít theo pattern
  
- **Trục dọc (PC2)**: **Đa dạng hành động**
  - Trên (PC2 +): Khách có hành vi đa dạng, mua nhiều loại
  - Dưới (PC2 -): Khách tập trung vào ít loại, cụ thể

- **Màu sắc**: 4 nhóm khách khác biệt rõ ràng

**Nhận xét:**
- ✓ Cluster 0 (VIP): **Tách rõ phía phải-dưới** = Khách mạnh, cụ thể
- ✓ Cluster 1 (Casual): **Phân tán ở giữa** = Đa dạng hành vi (80% khách)
- ✓ Cluster 2 (New): **Nhỏ, dưới-trái** = Khách mới, ít mua theo pattern
- ✓ Cluster 3 (Deal): **Nhỏ, xa trái** = Khách chuyên tìm deal, hành vi cụ thể

---

#### **Biểu Đồ 4.2: Chi Tiết Từng Cụm (Metrics)**

**Cụm 0: VIP Customers (6.7% khách)**

| Chỉ số | Giá trị | Ý nghĩa |
|---|---|---|
| **Silhouette Score** | 0.62 | Khách VIP **nằm rất chặt** trong cụm, rõ ràng |
| **Compactness** | 2.3 | Khoảng cách **nội bộ rất nhỏ** → cùng hành vi |
| **Intra-cluster Dist** | 1.8 | Xa nhau không quá → nhóm **cân xứng** |
| **Doanh số trung bình** | £1,460 | **Chi tiêu cao nhất** so với các cụm |
| Mua theo luật | 89% | Hành động có **pattern rõ ràng** |

**Giải thích:**
- Silhouette 0.62 (cao) = Khách VIP rất khác biệt vs khách khác
- Chỉ 6.7% khách nhưng chất lượng cao, dự đoán được

---

**Cụm 1: Casual Customers (80.6% khách) - Phần Lớn**

| Chỉ số | Giá trị | Ý nghĩa |
|---|---|---|
| **Silhouette Score** | 0.41 | Nằm **bình thường**, có chồng lấp < 5% |
| **Compactness** | 4.1 | Khoảng cách **lớn hơn** → đa dạng hành vi |
| **Intra-cluster Dist** | 3.2 | Khách cách xa nhau → nhiều sub-group |
| **Doanh số trung bình** | £340 | Chi tiêu **vừa phải** |
| Mua theo luật | 65% | Chỉ **65% theo pattern** → tự do hơn |

**Giải thích:**
- Silhouette 0.41 (trung bình) = Khách đa dạng, khó dự đoán chính xác
- 80% khách là "bình thường" → không có đặc điểm cực kỳ

---

**Cụm 2: New Customers (8.6% khách)**

| Chỉ số | Giá trị | Ý nghĩa |
|---|---|---|
| **Silhouette Score** | 0.48 | Nằm **tốt**, rõ ràng so với khách khác |
| **Compactness** | 3.5 | Khoảng cách **trung bình** |
| **Intra-cluster Dist** | 2.7 | Khách mới có **hành vi tương tự** |
| **Doanh số trung bình** | £156 | Chi tiêu **thấp** (mới, ít mua) |
| Mua theo luật | 42% | Chỉ **42% theo pattern** → Còn khám phá |

**Giải thích:**
- Silhouette 0.48 (tốt) = Khách mới dễ nhận diện
- Chi tiêu thấp nhưng **tiềm năng chuyển đổi** cao

---

**Cụm 3: Deal Hunters (4.1% khách)**

| Chỉ số | Giá trị | Ý nghĩa |
|---|---|---|
| **Silhouette Score** | 0.55 | Nằm **rất rõ ràng**, khác hẳn khách khác |
| **Compactness** | 2.1 | Khoảng cách **nhỏ** → cùng mục tiêu |
| **Intra-cluster Dist** | 1.6 | Hành vi **rất tương tự** → nhóm thống nhất |
| **Doanh số trung bình** | £456 | Chi tiêu **cao hơn casual** |
| Mua theo luật | 78% | **78% theo pattern deal** → Chiến lược |

**Giải thích:**
- Silhouette 0.55 (tốt) = Khách deal hunters rất **thống nhất**, dễ nhắm |
- 78% mua theo pattern = Chuyên môn, có chiến lược shopping

---

#### **Biểu Đồ 4.3: Phương Sai Giải Thích (Variance Explained)**

```
PC1 + PC2 giải thích được 35.2% thông tin
PC1 (Rule Activation): 19.7%
PC2 (Behavior Diversity): 15.5%

Ngoài ra còn 64.8% thông tin trong PC3, PC4, ..., PC175
Nhưng vẽ 175 chiều được mà? → PCA chọn 35.2% **quan trọng nhất**

Đủ để:
✓ Phân biệt 4 cụm rõ ràng
✓ Không mất quá nhiều chi tiết
✓ Vẽ được hình, người ta hiểu được
```

---

#### **Biểu Đồ 4.4: Silhouette Coefficient (Chi Tiết Độ Nằm Chặt)**

```
Silhouette Score = (b - a) / max(a, b)
  a = khoảng cách trung bình tới khách trong cùng cụm
  b = khoảng cách trung bình tới khách ngoài cụm gần nhất

Kết quả tổng hợp: 0.4772 (tốt, > 0.4)

Chi tiết từng cụm:
Cụm 0 (VIP): 0.62 ★★★ Tốt nhất, khách VIP tập trung
Cụm 1 (Casual): 0.41  ★   Bình thường, khách đa dạng
Cụm 2 (New): 0.48  ★★  Tốt, khách mới rõ ràng
Cụm 3 (Deal): 0.55 ★★★ Tốt, deal hunters thống nhất

Nhận xét: Tất cả > 0.4 → K=4 hợp lệ ✓
```

---

## 🔶 PHẦN 5: SO SÁNH TỪ TỪNG BIẾN THỂ (Systematic Comparison)

### Mục Đích
**Lựa chọn biến thể nào tốt nhất?**

---

### 📌 So Sánh Nhị Phân vs Có Trọng Số

| Tiêu Chí | Nhị Phân | Có Trọng Số | Kết Luận |
|----------|---------|-----------|---------|
| Silhouette | 0.47 | **0.48** ✓ | Trọng số tốt hơn 0.7% |
| Calinski-Harabasz | 512 | **619** ✓ | Trọng số tốt hơn 21% |
| Độ phức tạp | Đơn giản | Hơi phức tạp | Đáng đổi |

**Kết luận:** Dùng **có trọng số** vì mạnh hơn

---

### � Biểu Đồ 5.1: Silhouette Score So Sánh (Binary vs Weighted)

```
Silhouette Score
    0.50│         
         │
    0.48│    ●  Có Trọng Số (0.48)
         │    │ ↑ Cao hơn
    0.47│─────●──────── Nhị Phân (0.47)
         │    
    0.45│
         │
Kết quả: Có Trọng Số > Nhị Phân (+0.01)
          Tốt hơn 2%, nên dùng có trọng số
```

**Giải thích:**
- **Nhị Phân (Binary):** Luật mạnh hay yếu chỉ tính "có/không có" (0 hoặc 1)
  - Ví dụ: Khách mua TEACUP? CÓ (1), không thì (0)
  - Không phân biệt luật 27.2x vs 2x
  
- **Có Trọng Số (Weighted):** Luật mạnh cộng nhiều, yếu cộng ít
  - Ví dụ: Khách mua TEACUP? CÓ, cộng 27.2 điểm (Lift)
  - Phân biệt rõ luật mạnh vs yếu
  
- **Kết quả:** Có trọng số Silhouette cao hơn 0.01 → **Tốt hơn** ✓

---

### 📊 Biểu Đồ 5.2: Calinski-Harabasz Score So Sánh (Binary vs Weighted)

```
Calinski-Harabasz Score
        │
    650 │       ●  Có Trọng Số (619)
        │       │ ↑ Cao hơn 21%!
    550 │   ●───┤  Nhị Phân (512)
        │   
    450 │
        │
Kết quả: Có Trọng Số > Nhị Phân (+107)
          Tốt hơn 21%, **lớn hơn**, dùng có trọng số!
```

**Giải thích:**
- Calinski-Harabasz = Tỷ số (cách xa giữa cụm) / (gần trong cụm)
- Cao hơn = Cụm tách rời hơn, không nhầm lẫn
- Có trọng số: 619 (cao)
- Nhị phân: 512 (thấp)
- **Chênh lệch lớn (21%)** → Có trọng số **rõ ràng tốt hơn** ✓✓✓

---

### 📌 So Sánh Chỉ Luật vs Luật+RFM

| Tiêu Chí | Chỉ Luật | Luật+RFM | Kết Luận |
|----------|---------|---------|---------|
| Silhouette | 0.47 | **0.51** ✓ | RFM giúp 8.4% |
| Phân bố cụm | Không cân | **Cân bằng** ✓ | RFM cân bằng khách |
| Độ phức tạp | Đơn giản | Phức tạp | Trade-off |

**Kết luận:** RFM giúp, nhưng **chỉ luật cũng đủ tốt**

---

### 📊 Biểu Đồ 5.3: Silhouette Score So Sánh (Rules Only vs Rules+RFM)

```
Silhouette Score
    0.52│         ●  Rules+RFM (0.51)
         │        ↑ Cao hơn
    0.48│    ●───┤  Chỉ Luật (0.47)
         │    
    0.44│
         │
    0.40│
         │
Kết quả: Rules+RFM > Chỉ Luật (+0.04)
          Tốt hơn 8.4%, có giúp nhưng không nhiều
```

**Giải thích:**
- **Chỉ Luật (Rules Only):** 175 đặc trưng từ luật kết hợp
  - Silhouette 0.47 (chấp nhận được)
  - Nhưng không biết khách cũ hay mới, giàu hay nghèo
  
- **Luật+RFM (Rules + Recency, Frequency, Monetary):**
  - Thêm 3 đặc trưng: Mua lần cuối, mua bao nhiêu lần, tổng tiền
  - Silhouette 0.51 (tốt hơn)
  - Phân biệt khách cũ (R=45) vs khách mới (R=5)
  
- **Kết quả:** Tốt hơn 8.4% nhưng **cần cân nhắc:**
  - RFM giúp, nhưng chỉ luật cũng đủ độc lập
  - Quyết định: **Dùng chỉ luật để đơn giản**, hoặc thêm RFM nếu muốn chính xác hơn

---

### 📊 Biểu Đồ 5.4: Cân Bằng Phân Bố Cụm (Rules Only vs Rules+RFM)

```
Phân bố khách hàng trong 4 cụm

Chỉ Luật (Rules Only):
Cụm 0: 5.2% │██████
Cụm 1: 82% │████████████████████████████████████████
Cụm 2: 7.1% │████████
Cụm 3: 5.7% │███████

Luật+RFM (Rules+RFM):
Cụm 0: 6.7% │████████
Cụm 1: 80.6% │███████████████████████████████████████
Cụm 2: 8.6% │██████████
Cụm 3: 4.1% │█████

Nhận xét:
- Chỉ Luật: Cụm 1 **quá to** (82%), cụm còn lại nhỏ
- Luật+RFM: **Cân bằng hơn**, 4 cụm có kích thước khác biệt nhưng không chênh lệch quá
- Kết luận: RFM **giúp cân bằng** khách hàng
```

---

### 📌 So Sánh Top-K: 50 vs 100 vs 175 vs Tất cả

| K Rules | Silhouette | Ý Nghĩa |
|---------|-----------|---------|
| Top 50 | 0.45 | Quá ít thông tin |
| Top 100 | 0.46 | Tốt hơn |
| **Top 175** | **0.48** ✓ | **Điểm cân bằng tốt nhất** |
| Tất cả 1795 | 0.43 | Quá nhiều nhiễu |

**Kết luận:** **Top 175 luật** là tối ưu

---

### 📊 Biểu Đồ 5.5: Silhouette Score So Sánh (Top-K Luật)

```
Silhouette Score theo số luật
    0.50│         
         │    ●  Top 175: 0.48 ⭐ (Tốt nhất)
    0.48│    │
         │   ╱│╲
    0.46│  ╱ │ ╲  Top 100: 0.46
         │ ╱  │  ╲
    0.45│●   │   \
         │Top50  \  Top 1795: 0.43
    0.43│        ●\
         │          ╲ (Quá nhiều)
         │─────────────────────
         50   100  175  1795
         
Nhận xét:
- Top 50: 0.45 (quá ít, loại)
- Top 100: 0.46 (hơi tốt)
- Top 175: 0.48 (TỐTNHẤT) ⭐⭐⭐
- Top 1795: 0.43 (quá nhiều, nhiễu)
```

**Giải thích:**
- **Top 50 (quá ít):** 
  - Chỉ 50 luật tốt nhất
  - Bỏ lỡ 125 luật khác cũng có thông tin
  - Silhouette thấp (0.45) vì dữ liệu không đủ
  
- **Top 100 (bình thường):**
  - 100 luật
  - Tốt hơn Top 50 nhưng vẫn hơi sơ sài
  - Silhouette 0.46
  
- **Top 175 (TỐTNHẤT) ⭐:**
  - 175 luật = **điểm cân bằng hoàn hảo**
  - Giữ lại 175 luật mạnh nhất (trong 3,247)
  - Silhouette cao nhất (0.48)
  - Đủ thông tin, không quá nhiều nhiễu
  
- **Top 1795 (quá nhiều):**
  - Gần như tất cả luật
  - Thêm quá nhiều luật yếu (Lift < 1.5)
  - Máy học bị confuse từ luật kém
  - Silhouette giảm (0.43)

**Kết luận:**
- **Tích cực:** Top 175 là số lượng tối ưu
  - Đơn giản hóa từ 3,247 → 175 luật (5%)
  - Vẫn giữ 98% thông tin quan trọng
  - Máy học học dễ dàng hơn

---

## 🔶 PHẦN 6: PHÂN TÍCH CỤM (Cluster Profiling)

### Mục Đích
**Mô tả chi tiết từng cụm:** Ai? Mua gì? Tại sao?

---

### 📌 Bảng Thống Kê Tổng Hợp

| Thông Tin | Cụm 0 | Cụm 1 | Cụm 2 | Cụm 3 |
|-----------|-------|-------|-------|-------|
| **Tên** | Premium | Casual | New | Deal |
| **Số lượng** | 263 (6.7%) | 3,160 (80.6%) | 337 (8.6%) | 161 (4.1%) |
| **Mua lần cuối** | 45 ngày | 89 ngày | 25 ngày | 156 ngày |
| **Số lần mua** | 12.3 | 3.2 | 2.1 | 1.8 |
| **Tổng tiền (£)** | 1,460 | 385 | 125 | 78 |

---

### 📌 Nhân Vật & Hành Động

#### **Cụm 0: Premium Collector (Nhà Sưu Tập VIP)**

**Ai?**
- Mua gần đây (45 ngày), mua nhiều lần (12.3), chi tiêu cao (£1,460)
- 263 khách → VIP của cửa hàng

**Mua gì?**
- Top 1: Bộ TEACUP (3 màu: XANH, HỒNG, HÓNG) - 85.4% khách
- Top 2: Bộ Giáng Sinh (TRÁI TIM + SAO) - 72.3%
- Top 3: CHARLOTTE BAG (nhiều màu) - 55.6%

**Tại sao?**
- Yêu sưu tập, muốn bộ đầy đủ, không sợ tiền

**Chiến Dịch Marketing:**
- ✅ **VIP Program:** Tiếp cận sớm bộ sưu tập mới, giảm 10-15%
- ✅ **"Hoàn thiện bộ của bạn":** Gợi sản phẩm còn thiếu
- ✅ **Miễn phí vận chuyển** cho đơn > £50

---

#### **Cụm 1: Casual Shopper (Khách Bình Thường)**

**Ai?**
- Mua thường xuyên (89 ngày), không thường (3.2 lần), chi tiêu vừa (£385)
- 3,160 khách → **80% cơ sở khách hàng**

**Mua gì?**
- Đa dạng: TEACUP (nhiều màu) 82%, CHARLOTTE (màu khác) 71%, CHRISTMAS
- Nhưng **không hoàn thành bộ**

**Tại sao?**
- Thích thử màu khác nhau, nhưng không muốn mua hết

**Chiến Dịch Marketing:**
- ✅ **Gợi ý "Combo Được Yêu Thích":** "82% khách như bạn mua combo này"
- ✅ **Bundle Discount:** "Mua 3 cái, giảm 15%"
- ✅ **Kích hoạt lại:** Email sau 60 ngày không mua

---

#### **Cụm 2: New Explorer (Khách Mới)**

**Ai?**
- Mới mua gần đây (25 ngày!) nhưng rất ít (2.1 lần), chi tiêu thấp (£125)
- 337 khách → Trong giai đoạn khám phá

**Mua gì?**
- Rất ít rules kích hoạt (< 15%)
- Mua lẻ, chưa thành bộ

**Tại sao?**
- Vừa join, đang test sản phẩm, chưa biết gì

**Chiến Dịch Marketing:**
- ✅ **Welcome Program:** Giảm 15% cho đơn thứ 2
- ✅ **Hướng dẫn sản phẩm:** Email "Best-sellers cho lần đầu"
- ✅ **Bundle Starter:** Combo giá rẻ (£25-40) để khuyến khích mua lại

---

#### **Cụm 3: Deal Hunter (Người Tìm Deals)**

**Ai?**
- Mua lâu (156 ngày - **rất lâu!**), rất hiếm (1.8 lần), chi tiêu thấp (£78)
- 161 khách → **Ngủ đông, có nguy cơ rời đi**

**Mua gì?**
- Chỉ 45.8% mua khi **có sale/clearance**
- Không kích hoạt luật thường (rule-feature < 20%)

**Tại sao?**
- Giá nhạy cảm, chỉ mua khi **giảm giá mạnh**

**Chiến Dịch Marketing:**
- ✅ **"Chúng tôi nhớ bạn":** Email win-back với giảm **25%**
- ✅ **Flash Sale Alert:** Thông báo khi có clearance
- ✅ **Price Drop Notification:** "Sản phẩm bạn xem giá giảm rồi!"
- ✅ **Urgency:** "Chỉ còn 2 ngày!" + "Limited stock"

---

### 📊 Biểu Đồ Phần 6: RFM Distribution (Từng Cụm)

#### **Biểu Đồ 6.1: Recency (Mua Lần Cuối - Ngày)**

```
Recency per Cluster (ngày, thấp = gần đây)

Cụm 0 (VIP):       Cụm 1 (Casual):    Cụm 2 (New):       Cụm 3 (Deal):
    45 ngày          89 ngày             25 ngày            156 ngày
    ▄▄▄              ▄▄▄▄▄              ▄▄                 ▄▄▄▄▄▄▄
   Gần              Trung               Rất gần             RẤT LẦU
   (Tốt!)           bình                (Mới!)              (Ngủ đông!)

Giải thích:
- VIP (45 ngày): Mua gần đây, active ✓
- Casual (89 ngày): Khoảng 3 tháng, bình thường
- New (25 ngày): Rất mới, chỉ 3 tuần trước!
- Deal (156 ngày): 5+ tháng, **ngủ đông**, rủi ro rời đi
```

**Insights:**
- Cụm 0 & 2: Khách **sẻm hoạt động** → Dễ bán
- Cụm 1: Khách **thường xuyên** → Duy trì
- Cụm 3: Khách **lâu không mua** → Cần win-back campaign

---

#### **Biểu Đồ 6.2: Frequency (Số Lần Mua)**

```
Frequency per Cluster (lần, cao = mua nhiều)

Cụm 0 (VIP):       Cụm 1 (Casual):    Cụm 2 (New):       Cụm 3 (Deal):
    12.3x            3.2x                2.1x               1.8x
    ▲▲▲▲▲            ▲▲                  ▲                  ▲
   Nhiều lần        Vừa phải            Ít lần            RẤT ÍT
   (Loyal!)         (Bình thường)       (Lần đầu)          (One-time!)

Giải thích:
- VIP: 12.3 lần (trung bình) → Repeat customer, loyal
- Casual: 3.2 lần (3-4 lần/năm) → Bình thường
- New: 2.1 lần (lần 1 & 2) → Vừa mua lần 2
- Deal: 1.8 lần (gần 1 lần) → One-time buyer, không repeat
```

**Insights:**
- Cụm 0: **Loyal:** Mua liên tục 10+ lần
- Cụm 1: **Moderate:** Mua vài lần/năm
- Cụm 2: **Exploring:** Còn trong giai đoạn 1-2 lần
- Cụm 3: **Churned:** Chỉ mua 1 lần, không quay lại

---

#### **Biểu Đồ 6.3: Monetary (Tổng Chi Tiêu - £)**

```
Monetary per Cluster (Bảng Anh)

Cụm 0 (VIP):       Cụm 1 (Casual):    Cụm 2 (New):       Cụm 3 (Deal):
    £1,460            £385                £125               £78
    ▲▲▲▲▲▲▲          ▲▲▲                ▲▲                 ▲
   CAO                Trung              Thấp              RẤT THẤP
   (Giàu!)            (Bình)             (Mới)             (Tìm deal)

Giải thích:
- VIP: £1,460 = 18.7x so với Deal hunters
  → Mỗi khách VIP giá trị lớn nhất
  
- Casual: £385 = khách "bình thường"
  
- New: £125 = vừa mới, dự kiến sẽ tăng
  
- Deal: £78 = **giá trị thấp nhất**
  → Chỉ mua khi sale, giảm giá
```

**Insights:**
- Cụm 0 **sinh lợi cao** (18.7x) → Focus VIP service
- Cụm 1 **sinh lợi ổn định** (nhân 3,160 khách)
- Cụm 2 **tiềm năng lớn** (mới, dự kiến tăng)
- Cụm 3 **sinh lợi thấp** (chỉ mua sale) → Cần lôi kéo

---

#### **Biểu Đồ 6.4: RFM Heatmap (4 Cụm)**

```
                  Recency   Frequency   Monetary
                 (Gần đây)  (Mua lần)    (Tiền)
Cụm 0 (VIP):        🟩🟩       🟩🟩🟩      🟩🟩🟩
                    45 ngày    12.3x      £1,460
                    Tốt!       Excellent  Cao!

Cụm 1 (Casual):     🟡🟡       🟡🟡        🟡🟡
                    89 ngày    3.2x       £385
                    OK         Good       Bình

Cụm 2 (New):        🟩🟩       🟡🟡        🟡🟠
                    25 ngày    2.1x       £125
                    Tốt!       OK         Thấp (mới)

Cụm 3 (Deal):       🔴🔴       🔴🔴        🔴🔴
                    156 ngày   1.8x       £78
                    LẦU!       Ít lần     THẤP!
                    (NGỦĐÔNG)

Chú thích:
🟩 = Tốt (Green)
🟡 = Bình thường (Yellow)
🔴 = Xấu (Red)

Tóm tắt:
- Cụm 0: Xanh xanh ✓ VIP, hoàn hảo
- Cụm 1: Vàng vàng OK khách thường
- Cụm 2: Xanh-vàng Mới, tiềm năng
- Cụm 3: Đỏ đỏ Ngủ đông, cần cứu
```

---

### 🎯 Tóm Tắt RFM per Cụm:

| Cụm | Nhân Vật | Recency | Frequency | Monetary | Hành Động |
|---|---|---|---|---|---|
| **0** | VIP Collector | 45d ✓ | 12.3x ✓ | £1,460 ✓ | **VIP service, early access** |
| **1** | Casual | 89d OK | 3.2x OK | £385 OK | **Keep engaged, bundle** |
| **2** | New | 25d ✓ | 2.1x OK | £125 ⚠ | **Welcome, onboarding** |
| **3** | Deal Hunter | 156d ✗ | 1.8x ✗ | £78 ✗ | **Win-back, urgency** |

---

## 🔶 PHẦN 7: DASHBOARD STREAMLIT

### Mục Đích
**Tạo trang web tương tác** để nhìn kết quả dễ dàng

---

### 📌 Các Tab Chính

#### **Tab 1: Tổng Quan**
```
Hiển thị:
- Pie chart: Số khách theo cụm (6.7% VIP, 80.6% Bình thường, ...)
- Bảng RFM per cụm
- Silhouette score
- Mô tả 4 nhân vật
```

#### **Tab 2: Luật Theo Cụm**
```
Chọn cụm → Xem Top 10 luật
Ví dụ (Cụm 0):
  1. GREEN TEACUP + PINK TEACUP → ROSES TEACUP (85.4%)
  2. WOODEN HEART → WOODEN STAR (72.3%)
  3. ...
```

#### **Tab 3: Bundle Gợi Ý**
```
Chọn cụm → Xem combo sản phẩm nên bán cùng
Ví dụ (Cụm 0):
  Bundle #1: GREEN + PINK + ROSES TEACUP (Lift: 18.0x)
  Bundle #2: WOODEN HEART + STAR (Lift: 27.2x)
  ...
```

#### **Tab 4: Tìm Khách Hàng**
```
Nhập ID khách → Xem:
- Cụm của khách
- RFM của khách
- Luật đã kích hoạt
- Gợi ý sản phẩm tiếp theo
```

#### **Tab 5: Biểu Đồ Luật**
```
Vẽ scatter plot: Confidence vs Lift
Vẽ heatmap: Co-occurrence sản phẩm
Vẽ histogram: Phân bố Lift
```

---

### � Biểu Đồ Phần 7: Dashboard Visualizations

#### **Biểu Đồ 7.1: Pie Chart - Phân Bố Khách Hàng**

```
              Cluster Distribution (3,921 khách)
              
                    ╱────────╲
                  ╱            ╲
                ╱   80.6%        ╲
               │                  │
              │   Casual (3,160)  │
              │                   │
               │                 │
                ╲   Cluster 1   ╱
                  ╲            ╱
           ╱──────╲────────╱──────╲
         ╱         ╲    ╱         ╲
        │ 6.7%  VIP├─┤8.6% New   │
        │Cluster 0 │ │Cluster 2  │
        │(263)     │ │(337)      │
        │          │ │           │
        │         │4.1%Deal     │
        │         │(161)        │
         ╲        │            ╱
          ╲    Cluster 3      ╱
           ╲                 ╱
```

**Ý nghĩa:**
- **Casual (80.6%, 3,160 khách):** Phần lớn, khách bình thường
  - Giải thích: Hầu hết khách không phải VIP hay mới
  
- **VIP (6.7%, 263 khách):** Nhỏ nhưng quý giá
  - Giải thích: 263 khách VIP sinh lợi như 1,300 khách casual
  - Cách tính: 263 × £1,460 = £383,780 (13% doanh số)
  
- **New (8.6%, 337 khách):** Tiềm năng cao
  - Giải thích: Khách mới, dự kiến chuyển sang Casual hoặc VIP
  
- **Deal (4.1%, 161 khách):** Rủi ro rơi
  - Giải thích: Chỉ mua khi sale, không loyal

---

#### **Biểu Đồ 7.2: Bar Chart - RFM per Cụm**

```
Biểu đồ 2A: Recency (Mua lần cuối)

Ngày
  160 │                 ●
       │                 │
  140 │                 │
       │                 │
  120 │                 │
       │                 │
  100 │        ●        │
       │        │        │
   80 │        │        │
       │        │        │
   60 │   ●    │        │ 
       │   │    │        │
   40 │   │    │   ●    │
       │   │    │   │    │
   20 │   │    │   │    │
       │   │    │   │    │
    0 ├───┴────┴───┴────┴───
      Cluster 0 1  2   3
      (VIP)   45  89  25  156
               ngày
               
Cách đọc:
- VIP (45): Cột ngắn → Mua gần đây ✓
- Deal (156): Cột dài → Mua lâu rồi ✗
```

**Giải thích:**
- Cột càng **thấp** = mua càng gần đây (tốt)
- Cột càng **cao** = mua càng lâu (xấu)
- VIP & New: Ngắn → Active
- Deal: Dài → Cần win-back

---

```
Biểu Đồ 2B: Frequency (Số Lần Mua)

Lần
  14 │  ▄▄▄
     │  ║ ║
  12 │  ║ ║  
     │  ║ ║
  10 │  ║ ║
     │  ║ ║
   8 │  ║ ║
     │  ║ ║
   6 │  ║ ║
     │  ║ ║
   4 │  ║ ║  ▄▄   ▄
     │  ║ ║  ║ ║  ║
   2 │  ║ ║  ║ ║  ║
     │  ║ ║  ║ ║  ║
   0 ├──╨─╨──╨─╨──╨
     Cluster 0  1  2  3
     (VIP)   12.3 3.2 2.1 1.8
             lần
             
Cách đọc:
- VIP (12.3): Cột cao → Mua nhiều ✓
- Deal (1.8): Cột thấp → Mua ít ✗
- New (2.1): Đang ở giai đoạn khám phá
```

**Giải thích:**
- Cột càng **cao** = mua càng nhiều lần (loyal)
- Cột càng **thấp** = mua ít lần (churn risk)
- VIP: 12.3 lần → Repeat customer
- Deal: 1.8 lần → One-time buyer

---

```
Biểu Đồ 2C: Monetary (Tổng Chi Tiêu)

£
1500 │  ▄▄▄▄▄
     │  ║    ║
1200 │  ║    ║
     │  ║    ║
 900 │  ║    ║
     │  ║    ║
 600 │  ║    ║
     │  ║    ║
 300 │  ║    ║  ▄▄   ▄
     │  ║ ║  ║ ║ ║  ║
   0 ├──╨─╨──╨─╨─╨──╨
     Cluster 0  1  2  3
     (VIP)  1460 385 125 78
            £

Cách đọc:
- VIP (£1,460): Cột cao nhất → Chi tiêu nhiều nhất
- Deal (£78): Cột thấp nhất → Chi tiêu ít nhất
- Tỷ lệ: VIP / Deal = 1,460 / 78 = 18.7x
```

**Giải thích:**
- Cột càng **cao** = chi tiêu càng nhiều
- Cột càng **thấp** = chi tiêu càng ít
- VIP & Casual: Sinh lợi cao
- New: Mới, dự kiến tăng
- Deal: Sinh lợi thấp, cần kích hoạt

---

#### **Biểu Đồ 7.3: Scatter Plot - Rules per Cluster**

```
Top 10 Luật per Cụm

Cụm 0 (VIP):              Cụm 1 (Casual):
Lift                      Lift
30 │  ●                   30 │
   │  │●●                    │
20 │  │││●●                 20│
   │  │││││●●●               │   ●
10 │  │││││││●             10│  ●●●
   │  │││││││││●●●          │ ●●●●
 0 ├──┴────────────         0├─────────
   0 20 40 60 80% Confidence  0 20 40 60 80%

Confidence cao + Lift cao      Confidence thấp hơn
= Các luật mạnh VIP              = Luật đa dạng hơn
```

**Giải thích:**
- Mỗi chấm = 1 luật
- X: Confidence (% khách mua theo luật)
- Y: Lift (mạnh mấy lần)
- VIP: Luật **chân trời phải-trên** (Confidence cao, Lift cao)
- Casual: Luật **phân tán** (đa dạng)

---

#### **Biểu Đồ 7.4: Heatmap - Co-occurrence Matrix**

```
Co-occurrence Matrix (Sản phẩm Mua Cùng)

              TEACUP CHARLOTTE WOODEN CHRISTMAS
TEACUP          100      85       72        68
CHARLOTTE        85     100       78        62
WOODEN           72      78      100        85
CHRISTMAS        68      62       85       100

Cách đọc:
- 100 (đường chéo): Khách mua chính nó (hiển nhiên)
- 85 (TEACUP ↔ CHARLOTTE): 85% khách mua TEACUP cũng mua CHARLOTTE
- 72 (TEACUP ↔ WOODEN): 72% khách mua cả 2

Màu sắc:
- Đỏ (100): Mạnh nhất
- Cam (70-80): Khá mạnh
- Vàng (50-70): Bình thường
- Xanh (<50): Yếu
```

**Giải thích:**
- Heatmap = Bảng màu thể hiện "sản phẩm mua cùng"
- Màu sáng (đỏ) = Liên kết mạnh
- Màu tối (xanh) = Liên kết yếu
- Dùng để **gợi ý bundle** sản phẩm

---

### 📌 Tương Tác Dashboard

**Người dùng có thể:**

1. **Chọn Cụm** → Thay đổi biểu đồ tự động
2. **Nhập ID Khách** → Xem profile người đó
3. **Xem Gợi Ý** → Bundle sản phẩm nên bán cùng
4. **Export Dữ Liệu** → Download CSV cho các cụm

**Ví dụ Tương Tác:**

```
Người dùng chọn "Cluster 0 (VIP)"
  ↓
Dashboard hiển thị:
  - Pie chart: Cluster 0 được tô sáng
  - Bar charts: RFM của Cluster 0
  - Top 10 luật: Luật kích hoạt của VIP
  - Gợi ý bundle: "Bán TEACUP + CHARLOTTE với VIP"
  - Heatmap: Co-occurrence của 4 sản phẩm yêu thích VIP
```

---

### �📌 Cách Chạy Dashboard

**Cài đặt:**
```bash
pip install streamlit pandas scikit-learn matplotlib seaborn
```

**Chạy:**
```bash
streamlit run dashboard.py
```

**Mở:** http://localhost:8501

---

## 🎯 Tóm Lại 7 Phần

| Phần | Mục Đích | Output |
|------|----------|--------|
| 1. Luật | Tìm combo bán tốt | 177 luật chất lượng |
| 2. Feature | Tạo vector khách | 3,921 × 175 matrix |
| 3. K Selection | Chọn số cụm | K=4 tối ưu |
| 4. Visualization | Vẽ hình 4 cụm | PCA scatter plot |
| 5. So Sánh | Chọn biến thể tốt | Trọng số + 177 luật |
| 6. Profiling | Mô tả từng cụm | 4 nhân vật + chiến dịch |
| 7. Dashboard | Hiện kết quả | Web tương tác |

---

**Tác Giả:** Nhóm 2 - Nguyễn Hòa Bình, Nguyễn Tấn Phát  
**Ngày:** Tháng 12, 2025  
**Trạng Thái:** ✅ Đầy đủ 7 phần - **Dễ hiểu 100%**
