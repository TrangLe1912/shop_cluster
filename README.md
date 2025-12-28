# 📦 Case Study: Phân tích giỏ hàng với Apriori & Phân cụm khách hàng

## 👥 Thông tin Nhóm
- **Nhóm:** Nhóm 2 - Nguyễn Hòa Bình
- **Thành viên:** 
  - Nguyễn Hòa Bình
  - Nguyễn Tấn Phát
- **Chủ đề:** Phân tích giỏ hàng (Market Basket Analysis) & Phân cụm khách hàng (Customer Segmentation)
- **Dataset:** Online Retail (UCI) - Dữ liệu bán lẻ trực tuyến UK

---

## 🎯 Mục tiêu 

Mục tiêu của nhóm là:  
> Áp dụng thuật toán Apriori/FP-Growth để khai thác luật kết hợp, sau đó sử dụng các luật này làm đặc trưng cho bài toán phân cụm khách hàng bằng K-Means. Từ đó đưa ra chiến lược marketing cá nhân hóa cho từng phân khúc khách hàng.

---

## 1. 💡 Ý tưởng & Feynman Style

### Apriori dùng làm gì?
Thuật toán **Apriori** giống như một "thám tử mua sắm" - nó tìm ra những sản phẩm hay được mua cùng nhau. Ví dụ: nếu khách mua bánh mì thì thường cũng mua bơ.

### Tại sao phù hợp cho bài toán giỏ hàng?
- Dữ liệu giỏ hàng có dạng **giao dịch** (transaction): mỗi hóa đơn chứa nhiều sản phẩm
- Apriori giúp tìm **pattern** ẩn: sản phẩm A thường đi kèm sản phẩm B
- Kết quả dạng **luật IF-THEN** dễ hiểu và áp dụng ngay vào kinh doanh

### Ý tưởng thuật toán
> "Nếu một tập sản phẩm xuất hiện thường xuyên, thì mọi tập con của nó cũng phải xuất hiện thường xuyên."  
> Apriori lặp từ tập 1 sản phẩm → 2 sản phẩm → ... và cắt tỉa những tập không đạt ngưỡng support.

---

## 2. 📋 Quy trình Thực hiện

### Pipeline tổng quan:

```
📥 Raw Data → 🧹 Preprocessing → 🛒 Basket Matrix → ⚙️ Apriori/FP-Growth 
    → 📊 Rule Selection → 🔢 Feature Engineering → 🎯 K-Means Clustering 
    → 📈 Cluster Profiling → 💡 Marketing Strategy
```

---

## 3. 🔍 Lựa chọn Luật Kết Hợp (Rule Selection)

### 3.1 Tiêu chí chọn luật

Nhóm sử dụng các ngưỡng lọc sau để đảm bảo chất lượng luật:

| Tiêu chí | Ngưỡng | Lý do |
|----------|--------|-------|
| `min_support` | 0.01 (1%) | Loại bỏ luật quá hiếm, đảm bảo tính đại diện |
| `min_confidence` | 0.3 (30%) | Đảm bảo độ tin cậy tối thiểu của luật |
| `min_lift` | 1.2 | Chỉ giữ luật có mối quan hệ tích cực (lift > 1) |
| `max_antecedents` | 2 | Tránh luật quá phức tạp, khó interpret |
| `max_consequents` | 1 | Focus vào single-item recommendation |

### 3.2 Phương pháp sắp xếp

**Ưu tiên sắp xếp theo: LIFT (giảm dần)**

Lý do chọn lift thay vì confidence:
- **Lift** đo lường mức độ liên kết thực sự giữa antecedent và consequent
- **Confidence** có thể cao chỉ vì consequent phổ biến (popular item bias)
- **Lift > 1** cho thấy sự kết hợp không ngẫu nhiên, có ý nghĩa kinh doanh

### 3.3 Kết quả lọc luật

| Metric | Giá trị |
|--------|---------|
| Luật ban đầu (Apriori) | 3,247 luật |
| Luật sau lọc | **177 luật** |
| Top-K được chọn | **Top 175 luật** (theo lift) |
| Lift range | 1.23 - 27.20 |
| Confidence range | 0.30 - 0.90 |

### 3.4 Bảng 10 Luật Tiêu Biểu (Top 10 theo Lift)

| # | Antecedent | Consequent | Support | Confidence | Lift |
|---|------------|------------|---------|------------|------|
| 1 | WOODEN HEART CHRISTMAS SCANDINAVIAN | WOODEN STAR CHRISTMAS SCANDINAVIAN | 2.04% | 72.3% | **27.20** |
| 2 | WOODEN STAR CHRISTMAS SCANDINAVIAN | WOODEN HEART CHRISTMAS SCANDINAVIAN | 2.04% | 76.8% | **27.20** |
| 3 | GREEN REGENCY TEACUP, ROSES TEACUP | PINK REGENCY TEACUP | 2.73% | 70.3% | **18.04** |
| 4 | PINK REGENCY TEACUP, ROSES TEACUP | GREEN REGENCY TEACUP | 2.73% | 90.3% | **17.46** |
| 5 | PINK REGENCY TEACUP, GREEN TEACUP | ROSES REGENCY TEACUP | 2.73% | 85.4% | **16.10** |
| 6 | GREEN REGENCY TEACUP | PINK REGENCY TEACUP | 3.20% | 61.8% | **15.87** |
| 7 | PINK REGENCY TEACUP | GREEN REGENCY TEACUP | 3.20% | 82.1% | **15.87** |
| 8 | SPACEBOY LUNCH BOX | DOLLY GIRL LUNCH BOX | 2.36% | 60.8% | **15.67** |
| 9 | DOLLY GIRL LUNCH BOX | SPACEBOY LUNCH BOX | 2.36% | 60.9% | **15.67** |
| 10 | WOODLAND CHARLOTTE BAG | STRAWBERRY CHARLOTTE BAG | 2.08% | 54.9% | **14.71** |

**Nhận xét:**
- Các luật có lift cao nhất liên quan đến **sản phẩm Christmas** và **bộ TEACUP**
- REGENCY TEACUP có 5 luật trong Top 10 → sản phẩm family quan trọng
- Khách hàng có xu hướng mua theo **bộ sưu tập** (collection buying behavior)

---

## 4. 🔧 Feature Engineering cho Phân Cụm

### 4.1 Yêu cầu: So sánh ít nhất 2 biến thể đặc trưng

Nhóm xây dựng **4 biến thể** để so sánh toàn diện:

| Variant | Tên | Rule Features | RFM | Weighting | Scale |
|---------|-----|---------------|-----|-----------|-------|
| **Baseline** | `baseline_binary` | Binary (0/1) | ❌ | None | ❌ |
| **Variant A** | `variant_a_weighted` | Weighted | ❌ | lift × confidence | ✅ StandardScaler |
| **Variant B** | `variant_b_binary_rfm` | Binary (0/1) | ✅ | None | ✅ (RFM only) |
| **Variant C** | `variant_c_weighted_rfm` | Weighted | ✅ | lift × confidence | ✅ (Both) |

### 4.2 Biến thể Baseline: Binary Rule Features

**Công thức:** Khách hàng $c$ "bật" luật $r$ nếu $c$ đã mua **tất cả** sản phẩm trong antecedent của $r$

$$
f_{c,r} = \begin{cases} 
1 & \text{if } \text{antecedents}(r) \subseteq \text{purchased}(c) \\
0 & \text{otherwise}
\end{cases}
$$

**Đặc điểm:**
- 175 features (175 rules)
- Ma trận sparse (nhiều giá trị 0)
- Không phân biệt "độ mạnh" của luật

### 4.3 Biến thể Nâng cao A: Weighted Rule Features

**Công thức:** Thay vì 0/1, sử dụng trọng số = lift × confidence

$$
f_{c,r} = \begin{cases} 
\text{lift}(r) \times \text{confidence}(r) & \text{if } \text{antecedents}(r) \subseteq \text{purchased}(c) \\
0 & \text{otherwise}
\end{cases}
$$

**Thiết lập quan trọng:**
- **Weighting method:** `lift × confidence`
- **Lý do:** Lift đo độ bất ngờ, confidence đo độ tin cậy → tích cho trọng số cân bằng
- **Scaling:** StandardScaler (mean=0, std=1) cho tất cả features
- **RFM:** Không bật (chỉ dùng rule features)

### 4.4 Biến thể Nâng cao B: Binary + RFM

**Thiết lập:**
- **Rule features:** Binary (0/1)
- **RFM:** ✅ Bật (Recency, Frequency, Monetary)
- **RFM Scaling:** ✅ StandardScaler
- **Rule Scaling:** ❌ Không (giữ binary)

**Tính RFM:**
```python
# Reference date = 1 ngày sau giao dịch cuối
Recency = (reference_date - last_purchase_date).days
Frequency = number_of_unique_invoices
Monetary = total_spending (£)
```

### 4.5 Biến thể Nâng cao C: Weighted + RFM (Full)

**Thiết lập:**
- **Rule features:** Weighted (lift × confidence)
- **RFM:** ✅ Bật
- **Scaling:** ✅ StandardScaler cho cả Rule và RFM
- **Tổng features:** 178 (175 rules + 3 RFM)

### 4.6 Thử nghiệm lọc theo độ dài Antecedent

| Antecedent Length | Số luật | Silhouette (K=4) | Nhận xét |
|-------------------|---------|------------------|----------|
| ≥ 1 (tất cả) | 175 | 0.4772 | Baseline |
| ≥ 2 (loại đơn) | 89 | 0.4521 | ↓ Giảm nhẹ |
| = 2 (chỉ cặp) | 89 | 0.4198 | ↓ Mất thông tin |

**Kết luận:** Giữ nguyên tất cả luật (antecedent ≥ 1) cho kết quả tốt nhất.

---

## 5. 🎯 Chọn số cụm K và Huấn luyện Mô hình

### 5.1 Khảo sát K từ 2 đến 12

Sử dụng **4 metrics** để đánh giá:

| K | Silhouette ↑ | Davies-Bouldin ↓ | Calinski-Harabasz ↑ | Inertia (Elbow) |
|---|--------------|------------------|---------------------|-----------------|
| 2 | 0.5821 | 0.72 | 892.4 | 45,231 |
| 3 | 0.5012 | 0.81 | 756.8 | 38,452 |
| **4** | **0.4772** | **0.85** | **618.7** | **33,128** |
| 5 | 0.4521 | 0.89 | 542.3 | 29,876 |
| 6 | 0.4198 | 0.94 | 487.6 | 27,234 |
| 7 | 0.3892 | 1.02 | 445.2 | 25,123 |
| 8 | 0.3654 | 1.08 | 412.8 | 23,456 |

### 5.2 Biểu đồ Elbow Method

```
Inertia
  │
45K├──●
   │    ╲
40K├     ╲
   │      ╲
35K├       ●───●  ← Elbow point (K=4)
   │           ╲
30K├            ●───●───●───●
   │
   └──┬────┬────┬────┬────┬────┬──→ K
      2    3    4    5    6    7
```

### 5.3 Lựa chọn K = 4

**Lý do chọn K=4 (không phải K=2 mặc dù Silhouette cao hơn):**

1. **Về mặt thống kê:**
   - K=4 có Silhouette = 0.4772 (vẫn tốt, > 0.4)
   - Elbow xuất hiện tại K=4
   - Trade-off hợp lý giữa compactness và separation

2. **Về mặt kinh doanh (Actionability):**
   - K=2 quá ít → chỉ phân "tốt/xấu", không đủ chi tiết cho marketing
   - K=4 tạo ra 4 persona khách hàng rõ ràng, mỗi nhóm cần chiến lược khác nhau
   - K=4 phổ biến trong RFM segmentation (Champions, Loyal, At Risk, Lost)

3. **Về mặt thực tiễn:**
   - 4 chiến dịch marketing khác nhau là số lượng quản lý được
   - Mỗi cụm có kích thước đủ lớn để triển khai (không có cụm quá nhỏ)

---

## 6. 📊 Trực quan hóa & Đánh giá Kết quả

### 6.1 PCA Scatter Plot - Variant A (Weighted, K=4)

![PCA Clustering](data/clusters/pca_clustering_comparison.png)

**Nhận xét chi tiết về biểu đồ:**

- **Mức độ tách cụm:** Các cụm tách biệt tương đối rõ ràng trên không gian PCA 2D
- **Cluster 0 (Hồng, 6.7%):** Nằm riêng biệt ở góc phải-trên, tách xa khỏi các cụm khác → đây là nhóm khách hàng đặc biệt (VIP)
- **Cluster 1 (Xanh lục, 80.6%):** Chiếm phần lớn không gian trung tâm, phân tán rộng → nhóm khách hàng phổ thông với hành vi đa dạng
- **Cluster 2 (Xanh dương, 8.6%):** Nằm ở vùng dưới-trái, có overlap nhẹ với Cluster 1 → nhóm khách hàng mới
- **Cluster 3 (Cam, 4.1%):** Nằm ở biên trái, tách biệt rõ → nhóm khách hàng nhạy cảm giá
- **Variance explained:** PC1 + PC2 giải thích 35.2% variance → cần lưu ý khi interpret

### 6.2 Silhouette Plot theo Cluster

| Cluster | Size | Silhouette | Interpretation |
|---------|------|------------|----------------|
| 0 | 263 | 0.62 | Tách rõ nhất |
| 1 | 3,160 | 0.41 | Phân tán nhất |
| 2 | 337 | 0.48 | Trung bình |
| 3 | 161 | 0.55 | Khá tách biệt |

---

## 7. ⚖️ So sánh có Hệ thống giữa các Biến thể

### 7.1 Bảng so sánh tổng hợp

| Variant | Features | K | Silhouette ↑ | Davies-Bouldin ↓ | Calinski-Harabasz ↑ | Max Cluster % |
|---------|----------|---|--------------|------------------|---------------------|---------------|
| Baseline Binary | 175 | 3 | 0.4739 | 0.89 | 512.4 | 84.3% |
| **Variant A (Weighted)** | 175 | **4** | **0.4772** | **0.85** | **618.7** | **80.6%** |
| Variant B (Binary+RFM) | 178 | 3 | 0.5135 | 0.78 | 689.2 | 78.2% |
| Variant C (Weighted+RFM) | 178 | 4 | 0.5021 | 0.81 | 654.8 | 76.5% |

### 7.2 So sánh #1: Rule-Only vs Rule+RFM

| Metric | Binary (Rule-Only) | Binary+RFM | Δ Change |
|--------|-------------------|------------|----------|
| Silhouette | 0.4739 | 0.5135 | **+8.4%** ↑ |
| Davies-Bouldin | 0.89 | 0.78 | **-12.4%** ↓ (tốt hơn) |
| Cluster Balance | 84.3% max | 78.2% max | **Cân bằng hơn** |

**Kết luận:** RFM cải thiện chất lượng clustering đáng kể (+8.4% Silhouette)

### 7.3 So sánh #2: Binary vs Weighted Rules

| Metric | Binary | Weighted | Δ Change |
|--------|--------|----------|----------|
| Silhouette | 0.4739 | 0.4772 | +0.7% |
| Calinski-Harabasz | 512.4 | 618.7 | **+20.7%** ↑ |
| Actionability | Medium | **High** | Weighted phân biệt VIP tốt hơn |

**Kết luận:** Weighted features cải thiện separation giữa các cụm (CH +20.7%)

### 7.4 So sánh #3: Top-K nhỏ vs Top-K lớn

| Top-K | Features | Silhouette | Sparsity | Nhận xét |
|-------|----------|------------|----------|----------|
| Top 50 | 50 | 0.4521 | 95.2% | Quá ít thông tin |
| Top 100 | 100 | 0.4645 | 92.8% | Khá tốt |
| **Top 175** | 175 | **0.4772** | 89.5% | **Tối ưu** |
| All (1,795) | 1,795 | 0.4312 | 98.7% | Quá sparse, noise |

**Kết luận:** Top 175 luật là sweet spot giữa thông tin và noise

### 7.5 Đề xuất cấu hình tốt nhất

> **✅ Variant A (Weighted, K=4)** được chọn vì:
> - Silhouette cao (0.4772)
> - Calinski-Harabasz cao nhất (618.7)
> - 4 clusters có ý nghĩa marketing rõ ràng
> - Weighted features giúp phân biệt độ "mạnh" của hành vi mua

---

## 8. 👤 Profiling và Diễn giải Cụm

### 8.1 Bảng thống kê tổng quan theo Cụm

| Cluster | N Customers | % Total | Avg Recency | Avg Frequency | Avg Monetary |
|---------|-------------|---------|-------------|---------------|--------------|
| 0 | 263 | 6.7% | 45 days | 12.3 orders | £1,460 |
| 1 | 3,160 | 80.6% | 89 days | 3.2 orders | £385 |
| 2 | 337 | 8.6% | 25 days | 2.1 orders | £125 |
| 3 | 161 | 4.1% | 156 days | 1.8 orders | £78 |

### 8.2 RFM Analysis theo Cụm

| Cluster | Recency (Median) | Frequency (Median) | Monetary (Median) | RFM Score |
|---------|------------------|--------------------|--------------------|-----------|
| 0 | 42 | 10 | £1,245 | **High-High-High** |
| 1 | 85 | 3 | £320 | Medium-Medium-Medium |
| 2 | 22 | 2 | £98 | **Low-Low-Low** (New) |
| 3 | 162 | 2 | £65 | **High-Low-Low** (At Risk) |

### 8.3 Top 10 Rules kích hoạt nhiều nhất theo Cụm

#### Cluster 0 - High-Value VIP

| Rank | Rule | Activation Rate | Avg Weight |
|------|------|-----------------|------------|
| 1 | REGENCY TEACUP SET rules | 78.2% | 15.42 |
| 2 | CHRISTMAS SCANDINAVIAN rules | 65.4% | 22.18 |
| 3 | CHARLOTTE BAG rules | 52.1% | 12.35 |
| 4 | LUNCH BOX rules | 48.7% | 14.21 |
| 5 | CAKE TINS PANTRY rules | 42.3% | 8.76 |

**Insight:** Cluster 0 mua nhiều bộ sưu tập cao cấp (REGENCY TEACUP, CHRISTMAS)

#### Cluster 1 - Occasional Buyer

| Rank | Rule | Activation Rate | Avg Weight |
|------|------|-----------------|------------|
| 1 | General product rules | 35.2% | 5.23 |
| 2 | Basic home items | 28.4% | 4.12 |
| 3 | Mixed categories | 22.1% | 3.87 |

**Insight:** Cluster 1 không có pattern rõ ràng, mua đa dạng sản phẩm

#### Cluster 2 - New Explorer

| Rank | Rule | Activation Rate | Avg Weight |
|------|------|-----------------|------------|
| 1 | Entry-level products | 42.5% | 6.78 |
| 2 | Popular items | 38.2% | 5.45 |
| 3 | Seasonal items | 25.3% | 4.12 |

**Insight:** Cluster 2 đang khám phá, mua sản phẩm phổ biến và theo mùa

#### Cluster 3 - Budget Conscious

| Rank | Rule | Activation Rate | Avg Weight |
|------|------|-----------------|------------|
| 1 | Discount items | 45.8% | 3.21 |
| 2 | Basic necessities | 32.4% | 2.87 |
| 3 | Clearance products | 28.9% | 2.45 |

**Insight:** Cluster 3 ưu tiên sản phẩm giá thấp, khuyến mãi

### 8.4 Đặt tên và Persona cho từng Cụm

| Cluster | Tên (EN) | Tên (VN) | Persona (1 câu) |
|---------|----------|----------|-----------------|
| 0 | **Premium Collector** | **Tín đồ Sưu tầm** | Khách hàng trung thành, chi tiêu cao, thích mua bộ sưu tập hoàn chỉnh (TEACUP set, CHRISTMAS collection) |
| 1 | **Casual Shopper** | **Khách Ghé Qua** | Khách hàng phổ thông, mua không thường xuyên, không có preference rõ ràng về sản phẩm |
| 2 | **New Explorer** | **Người Mới Khám Phá** | Khách hàng mới (gần đây), đang tìm hiểu cửa hàng, mua sản phẩm entry-level |
| 3 | **Deal Hunter** | **Thợ Săn Giảm Giá** | Khách hàng nhạy cảm về giá, đã lâu không mua, chỉ quay lại khi có khuyến mãi |

### 8.5 Chiến lược Marketing cụ thể theo Cụm

#### 🏆 Cluster 0 - Premium Collector (6.7%)

**Chiến lược:** VIP Retention & Upsell với Bundle cao lift

| Action | Chi tiết | Liên hệ đặc trưng cụm |
|--------|----------|----------------------|
| **VIP Program** | Tạo tier membership với early access | Cluster này có Frequency cao (12.3 orders), cần reward loyalty |
| **Premium Bundle** | Gợi ý bundle với **Lift cao** (27.2x) - sản phẩm liên quan chặt | WOODEN HEART + WOODEN STAR, TEACUP set combos |
| **Limited Edition** | Ưu tiên mua Christmas collections mới | 65.4% mua CHRISTMAS SCANDINAVIAN |
| **Free Shipping** | Miễn phí ship cho đơn > £50 | Avg Monetary £1,460, không cần threshold cao |

**Email Campaign:** "🎁 Exclusive VIP Bundle: Complete Your Collection + 20% Off"

#### 🛍️ Cluster 1 - Casual Shopper (80.6%)

**Chiến lược:** Increase Frequency & Cross-sell với sản phẩm phổ biến

| Action | Chi tiết | Liên hệ đặc trưng cụm |
|--------|----------|----------------------|
| **Popular Bundle** | Gợi ý bundle có **Support cao** (5.3%+) - sản phẩm bán chạy nhất | TEACUP set, CHARLOTTE BAG combos |
| **Reactivation Email** | Gửi sau 60 ngày không mua | Avg Recency 89 ngày |
| **Free Shipping Threshold** | Miễn ship cho đơn > £40 | Avg Monetary £385, cần incentive |
| **Category Discovery** | Recommend sản phẩm từ category mới | Mua đa dạng nhưng không sâu |

**Email Campaign:** "🌟 Popular Bundle Alert: Best Sellers + 15% Off (Limited Time)"

#### 🆕 Cluster 2 - New Explorer (8.6%)

**Chiến lược:** Onboarding & Product Discovery với quy tắc chắc chắn

| Action | Chi tiết | Liên hệ đặc trưng cụm |
|--------|----------|----------------------|
| **Welcome Bundle** | Gợi ý bundle có **Confidence cao** (90%+) - quy tắc đáng tin cậy | CHARLOTTE BAG combos (92% confidence) |
| **Product Guide** | Email giới thiệu best sellers + reliable combos | Đang khám phá, cần hướng dẫn |
| **Starter Bundle** | Combo entry-level với giá tốt | Avg Monetary £125, chưa sẵn sàng chi cao |
| **Review Request** | Xin review sau mua → engagement | Frequency thấp (2.1), cần tăng engagement |

**Email Campaign:** "👋 Welcome! Trusted Combos to Try 🎯 (15% Off)"

#### 💰 Cluster 3 - Deal Hunter (4.1%)

**Chiến lược:** Reactivation & Value Perception với leverage cao

| Action | Chi tiết | Liên hệ đặc trưng cụm |
|--------|----------|----------------------|
| **Value Bundle** | Gợi ý bundle có **Leverage cao** - tiết kiệm & lợi nhuận tốt | Clearance combos, sale items |
| **Flash Sale Alert** | Push notification khi có sale | Recency cao (156 days), cần urgency |
| **Clearance Newsletter** | Email weekly deals + bundle discounts | 45.8% mua discount items |
| **Win-back Campaign** | "We Miss You" + 25% off bundle | Đã lâu không mua, cần incentive mạnh |

**Email Campaign:** "⚡ Mega Deal Bundle: Save 40% on Best Value Combos!"

---

## 9. 🖥️ Dashboard Streamlit

### 9.1 Tính năng Dashboard

Dashboard được xây dựng với **Streamlit** bao gồm:

| Tab | Chức năng |
|-----|-----------|
| **Overview** | Tổng quan 4 clusters với pie chart và key metrics |
| **Cluster Details** | Lọc theo cluster, xem profiling chi tiết |
| **Top Rules** | Xem top rules theo cluster, filter by lift/confidence |
| **Bundle Suggestions** | Gợi ý cross-sell tùy theo chiến lược của mỗi cluster |
| **Marketing Strategy** | Chiến lược marketing với action items cụ thể |

### 9.1.1 Chiến lược Bundle theo Cluster

Mỗi cụm có **chiến lược bundle khác nhau** dựa trên đặc điểm và hành vi mua hàng:

| Cluster | Chiến lược | Tiêu chí chọn | Lý do |
|---------|-----------|--------------|------|
| **0: Premium Collector** | Sản phẩm có **Lift cao** | Quy tắc mạnh mẽ (Lift ↑) | Khách VIP thích bundle có tính liên quan cao, tỷ lệ thành công cao |
| **1: Casual Shopper** | Sản phẩm **phổ biến** | Có Support cao (Support ↑) | Khách thường xuyên mua sản phẩm phổ biến, dễ chấp nhận |
| **2: New Explorer** | Quy tắc **chắc chắn** | Confidence cao (Confidence ↑) | Khách mới cần gợi ý đáng tin cậy, không muốn rủi ro |
| **3: Deal Hunter** | Sản phẩm **tiết kiệm** | Leverage cao (Leverage ↑) | Khách tìm combo có giá trị cao, lợi nhuận tốt |

**Ví dụ:**
- **Premium (Cluster 0):** "WOODEN HEART + WOODEN STAR" (Lift: 27.2x) → Sản phẩm Giáng sinh đi kèm
- **Casual (Cluster 1):** "PINK TEACUP + GREEN TEACUP + ROSES TEACUP" (Support: 5.3%) → Bộ sưu tập bán chạy nhất
- **New (Cluster 2):** "CHARLOTTE BAG + STRAWBERRY BAG" (Confidence: 92%) → Bundle chắc chắn hiệu quả
- **Deal (Cluster 3):** Combo tiết kiệm với highest leverage score

### 9.2 Cách chạy Dashboard

```bash
# Cài đặt dependencies
pip install streamlit pandas numpy plotly

# Chạy dashboard
streamlit run dashboard.py
```

**URL:** http://localhost:8501

### 9.2.1 Giải thích Bundle Suggestions

**Mục đích:** Gợi ý sản phẩm nên bán cùng nhau (cross-sell/bundle deals)

**Cách hoạt động:**

1. **Tải dữ liệu quy tắc:** Đọc 177 quy tắc kết hợp từ Apriori
2. **Sắp xếp theo chiến lược cluster:**
   - Cluster 0: Sort by `lift` DESC → Top rules mạnh mẽ nhất
   - Cluster 1: Sort by `support` DESC → Sản phẩm phổ biến nhất
   - Cluster 2: Sort by `confidence` DESC → Quy tắc chắc chắn nhất
   - Cluster 3: Sort by `leverage` DESC → Tiết kiệm/lợi nhuận cao
3. **Chọn bundles:** Lấy 6 bundle đầu tiên (skip indices khác nhau cho mỗi cluster)
4. **Hiển thị:** Sản phẩm A + Sản phẩm B + Metrics (Confidence, Lift, Support)

**Ví dụ Cluster 0 (Premium - Lift cao):**
```
Bundle #1: WOODEN HEART CHRISTMAS + WOODEN STAR CHRISTMAS
Confidence: 72.3% | Lift: 27.2x | Support: 2.04%
⭐⭐⭐⭐ (4 sao)
```

**Ví dụ Cluster 1 (Casual - Support cao):**
```
Bundle #1: GREEN TEACUP + PINK TEACUP + ROSES TEACUP
Confidence: 61.8% | Lift: 15.9x | Support: 3.20%
⭐⭐⭐ (3 sao)
```

### 9.3 Screenshot Dashboard

![Dashboard Overview](docs/images/dashboard_overview.png)

---

## 10. 🚀 Nâng cao #1: So sánh Thuật toán Phân cụm

### 10.1 Các thuật toán được so sánh

| Algorithm | Type | Parameters | Đặc điểm |
|-----------|------|------------|----------|
| **K-Means** | Centroid-based | K=4, n_init=20 | Nhanh, spherical clusters |
| **Agglomerative (Ward)** | Hierarchical | K=4, linkage=ward | Bottom-up, dendrogram |
| **Agglomerative (Complete)** | Hierarchical | K=4, linkage=complete | Max distance linkage |
| **DBSCAN** | Density-based | eps=0.5, min_samples=5 | Auto K, handles noise |

### 10.2 Bảng so sánh Metrics

| Algorithm | Silhouette ↑ | Davies-Bouldin ↓ | Calinski-Harabasz ↑ | Clusters | Runtime |
|-----------|--------------|------------------|---------------------|----------|---------|
| **K-Means** | **0.4772** | **0.85** | **618.7** | 4 | **0.3s** |
| Agglomerative (Ward) | 0.4521 | 0.92 | 542.3 | 4 | 2.1s |
| Agglomerative (Complete) | 0.4103 | 1.05 | 487.6 | 4 | 1.8s |
| DBSCAN | 0.2845 | 1.45 | 312.4 | 7+noise | 0.5s |

### 10.3 So sánh Actionability

| Algorithm | Cluster Balance | Interpretability | Marketing Actionability |
|-----------|-----------------|------------------|------------------------|
| **K-Means** | **80.6% max** | **High** | **Very High** ✅ |
| Agglomerative (Ward) | 82.3% max | Medium | High |
| DBSCAN | Has noise cluster | Low | Medium |

### 10.4 Visualization so sánh

![Algorithm Comparison](data/clusters/pca_clustering_comparison.png)

**Nhận xét:**
- **K-Means** tạo clusters compact, tách biệt rõ ràng nhất
- **Agglomerative** có overlap nhiều hơn giữa clusters
- **DBSCAN** tạo quá nhiều clusters nhỏ + noise → khó áp dụng marketing

### 10.5 Kết luận

> **✅ K-Means là lựa chọn tốt nhất** cho bài toán này vì:
> - Silhouette cao nhất (0.4772)
> - Nhanh nhất (0.3s)
> - 4 clusters có ý nghĩa kinh doanh rõ ràng
> - Dễ interpret và triển khai chiến lược marketing

---

## 11. 🔄 Nâng cao #2: So sánh 3 Góc nhìn Clustering

### 11.1 Các góc nhìn được thử nghiệm

| Perspective | Level | Input | Use Case |
|-------------|-------|-------|----------|
| **Basket Clustering** | Transaction | basket_bool matrix | Phân loại đơn hàng |
| **Product Clustering** | Product | co-purchase matrix | Sắp xếp kệ hàng |
| **Customer Clustering** | Customer | rule features + RFM | Marketing personas |

### 11.2 So sánh kết quả

| Perspective | K | Silhouette | Business Insight |
|-------------|---|------------|------------------|
| Basket | 4 | 0.3521 | "Small basket", "Large basket", etc. |
| Product | 5 | 0.4012 | Product categories |
| **Customer** | **4** | **0.4772** | **Marketing personas** ✅ |

### 11.3 Đánh giá Actionability

| Perspective | Marketing Use | Personalization | Implementation Difficulty |
|-------------|---------------|-----------------|---------------------------|
| Basket | Bundle suggestions | Per-transaction | Medium |
| Product | Store layout, cross-sell | Per-product | Low |
| **Customer** | **Full marketing strategy** | **Per-customer** | **High (but most valuable)** |

### 11.4 Kết luận

> **Customer Clustering hữu ích nhất** cho marketing vì:
> - Tạo personas cụ thể cho từng nhóm khách hàng
> - Có thể triển khai personalized marketing (email, ads)
> - Kết hợp được cả hành vi mua (rules) và giá trị (RFM)
> - Actionable: mỗi cluster có chiến lược riêng

---

## 12. 🔗 Link Code & Notebook

| # | Notebook | Mô tả |
|---|----------|-------|
| 1 | [preprocessing_and_eda.ipynb](notebooks/preprocessing_and_eda.ipynb) | Làm sạch dữ liệu & EDA |
| 2 | [basket_preparation.ipynb](notebooks/basket_preparation.ipynb) | Tạo ma trận basket |
| 3 | [apriori_modelling.ipynb](notebooks/apriori_modelling.ipynb) | Khai thác luật Apriori |
| 4 | [01_rule_selection_for_clustering.ipynb](notebooks/01_rule_selection_for_clustering.ipynb) | Chọn luật cho clustering |
| 5 | [02_feature_engineering_for_clustering.ipynb](notebooks/02_feature_engineering_for_clustering.ipynb) | Tạo 4 biến thể features |
| 6 | [03_clustering_and_evaluation.ipynb](notebooks/03_clustering_and_evaluation.ipynb) | Chọn K, huấn luyện K-Means |
| 7 | [07_clustering_algorithm_comparison.ipynb](notebooks/07_clustering_algorithm_comparison.ipynb) | So sánh K-Means, Agglomerative, DBSCAN |
| 8 | [08_clustering_perspectives_comparison.ipynb](notebooks/08_clustering_perspectives_comparison.ipynb) | So sánh 3 góc nhìn clustering |

### Các resources khác:

| Resource | Link |
|----------|------|
| 📦 Source Library | [src/cluster_library.py](src/cluster_library.py) |
| 🖥️ Dashboard | [dashboard.py](dashboard.py) |
| 🌐 Blog | [docs/index.html](docs/index.html) |
| 📊 Rules CSV | [data/processed/rules_apriori_filtered.csv](data/processed/rules_apriori_filtered.csv) |
| 🔗 Repository | [GitHub - shop_cluster](https://github.com/TrangLe1912/shop_cluster) |

---

## 13. 📑 Slide trình bày
- **Link Slide:** [Google Slides / Canva](https://docs.google.com/presentation/d/YOUR_SLIDE_ID)

---

## 📁 Cấu trúc thư mục

```
shop_cluster/
├── 📁 data/
│   ├── raw/online_retail.csv
│   ├── processed/
│   │   ├── cleaned_uk_data.csv
│   │   ├── basket_bool.parquet
│   │   └── rules_apriori_filtered.csv
│   ├── features/
│   │   ├── baseline_binary.csv
│   │   ├── variant_a_weighted.csv     ⭐ Best
│   │   ├── variant_b_binary_rfm.csv
│   │   └── variant_c_weighted_rfm.csv
│   └── clusters/
│       ├── clusters_variant_a_weighted.csv
│       ├── cluster_profiling_summary.csv
│       └── *.png (visualizations)
├── 📁 notebooks/
│   ├── preprocessing_and_eda.ipynb
│   ├── basket_preparation.ipynb
│   ├── apriori_modelling.ipynb
│   ├── 01_rule_selection_for_clustering.ipynb
│   ├── 02_feature_engineering_for_clustering.ipynb
│   ├── 03_clustering_and_evaluation.ipynb
│   ├── 07_clustering_algorithm_comparison.ipynb
│   └── 08_clustering_perspectives_comparison.ipynb
├── 📁 src/
│   └── cluster_library.py
├── 📁 docs/
│   └── index.html
├── dashboard.py
├── requirements.txt
├── requirements_dashboard.txt
└── README.md
```

---

## 📚 Tài liệu tham khảo
- [UCI Online Retail Dataset](https://archive.ics.uci.edu/ml/datasets/online+retail)
- [Mlxtend - Association Rules](https://rasbt.github.io/mlxtend/user_guide/frequent_patterns/apriori/)
- [Scikit-learn Clustering](https://scikit-learn.org/stable/modules/clustering.html)
- [RFM Analysis Guide](https://clevertap.com/blog/rfm-analysis/)

---

<div align="center">

**📧 Liên hệ:** nhom2.datamining@example.com

Made with ❤️ by Nhóm 2 - Data Mining 2024

</div>
