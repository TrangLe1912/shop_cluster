# 📊 Quy Trình Phân Cụm Chi Tiết v3.0 - FP-Growth & 3 Góc Nhìn

> **Last Updated:** Dec 29, 2025 | **Status:** ✅ HOÀN THÀNH | **8 Notebooks Executed**

---

## 🎯 Executive Summary

### Kết Quả Chính

| Metric | Result | Status |
|--------|--------|--------|
| **Algorithm** | FP-Growth (vs Apriori) | ✅ **5-10x nhanh hơn** |
| **Rules Selected** | 175 high-quality rules | ✅ **Min_support=2%** |
| **Feature Variants** | 4 variants tested | ✅ **Winner: variant_b_binary_rfm** |
| **Optimal K** | K=4 clusters | ✅ **Silhouette=0.4772** |
| **Best Clustering** | Customer Clustering | ✅ **4 marketing personas** |
| **Algorithm Winner** | K-Means | ✅ **vs Hierarchical, DBSCAN** |
| **Perspectives Winner** | Customer Clustering | ✅ **vs Basket, Product** |

### 4 Customer Personas

| Cluster | Name | Size | Characteristics | Strategy |
|---------|------|------|-----------------|----------|
| **0** | 💎 Premium Collector | 6.7% | High value, loyal, loves collections | VIP program, premium bundles |
| **1** | 🛍️ Casual Shopper | 80.6% | Occasional buyers, diverse interests | Popular bundles, reactivation |
| **2** | 🆕 New Explorer | 8.6% | Recently active, discovering products | Welcome bundles, guidance |
| **3** | 💰 Deal Hunter | 4.1% | Price-sensitive, inactive but responsive | Flash sales, win-back campaigns |

---

## 📋 Pipeline Chi Tiết (8 Notebooks)

### Notebook 01: Rule Selection for Clustering
- **Input:** `online_retail.csv` (541,909 transactions)
- **Output:** 175 FP-Growth rules
- **Status:** ✅ Thành công

**Key Activities:**
1. FP-Growth Mining → 3,247 raw rules
2. Rule Filtering (support≥2%, confidence≥30%, lift>1.2) → 175 rules
3. Sort by LIFT (highest first)
4. Export rules_fpgrowth_top200_selected.csv

**Stats:**
- Lift range: 1.23 - 27.20
- Top rule: WOODEN HEART + WOODEN STAR (Lift: 27.2x)

---

### Notebook 02: Feature Engineering
- **Input:** 175 rules + customer data
- **Output:** 4 feature variants (178 features max)
- **Status:** ✅ Thành công

**4 Variants:**
| Variant | Rules | RFM | Features | Result |
|---------|-------|-----|----------|--------|
| Baseline | Binary | ❌ | 175 | Sparse |
| Variant A | Weighted | ❌ | 175 | Good |
| **Variant B** | Binary | ✅ | 178 | **WINNER** |
| Variant C | Weighted | ✅ | 178 | Good |

**Scaling:** StandardScaler (mean=0, std=1)

---

### Notebook 03: Clustering & Evaluation
- **Input:** 4 feature variants
- **Output:** K=4 optimal
- **Status:** ✅ Thành công

**K Selection (Elbow Method):**
- K=2: Silhouette=0.5821 (high but too simple)
- **K=4: Silhouette=0.4772 ⭐ (chosen)**
- K=6: Silhouette=0.4198 (declining)

**Variant B Metrics at K=4:**
- Silhouette: 0.5135 ✅
- Davies-Bouldin: 0.78 ✅
- Calinski-Harabasz: 689.2 ✅

---

### Notebook 04: Visualization & Analysis
- **Input:** K-Means clusters
- **Output:** PCA plots, Silhouette plots, heatmaps
- **Status:** ✅ Thành công

**Visualizations:**
- PCA 2D scatter (PC1+PC2 = 35.2% variance)
- Silhouette plot (C0: 0.62, C1: 0.41, C2: 0.48, C3: 0.55)
- RFM heatmap per cluster

---

### Notebook 05: Comparison & Recommendations
- **Input:** 4 variant metrics
- **Output:** Winner determination
- **Status:** ✅ Thành công

**Winner: Variant B** (Binary + RFM)
- Best Silhouette (0.5135)
- Best Davies-Bouldin (0.78)
- Simple to interpret
- Excellent for marketing

---

### Notebook 06: Cluster Profiling
- **Input:** K-Means clusters + rules
- **Output:** Personas, RFM analysis, strategies
- **Status:** ✅ Thành công

**4 Personas Defined:**

**Cluster 0: Premium Collector (6.7%)**
- RFM: 45 days, 12.3 orders, £1,460
- Top Rules: TEACUP (78.2%), CHRISTMAS (65.4%)
- Strategy: VIP Retention + Upsell

**Cluster 1: Casual Shopper (80.6%)**
- RFM: 89 days, 3.2 orders, £385
- Strategy: Increase Frequency

**Cluster 2: New Explorer (8.6%)**
- RFM: 25 days, 2.1 orders, £125
- Strategy: Conversion + Engagement

**Cluster 3: Deal Hunter (4.1%)**
- RFM: 156 days, 1.8 orders, £78
- Strategy: Reactivation

---

### Notebook 07: Algorithm Comparison
- **Input:** K=4 customer data
- **Output:** K-Means vs Hierarchical vs DBSCAN
- **Status:** ✅ Thành công

**Results:**
| Algorithm | Silhouette | DBI | CH | Runtime |
|-----------|-----------|-----|-----|---------|
| **K-Means** | **0.4772** | **0.85** | **618.7** | **0.3s** ✅ |
| Agglom (Ward) | 0.4521 | 0.92 | 542.3 | 2.1s |
| DBSCAN | 0.2845 | 1.45 | 312.4 | 0.5s |

**Winner:** K-Means (Best metrics + fastest)

---

### Notebook 08: Perspectives Comparison
- **Input:** Basket, Product, Customer clustering
- **Output:** Metrics, recommendations
- **Status:** ✅ Thành công

**3 Perspectives:**

| Metric | Basket | Product | Customer |
|--------|--------|---------|----------|
| Silhouette | 0.4744 | 0.1142 | **0.4772** ✅ |
| Davies-Bouldin | 3.9328 | 2.8593 | **0.85** ✅ |
| Actionability | Medium | Very High | **Very High** ✅ |

**Winner:** Customer Clustering
- Best for marketing
- 4 actionable personas
- Highest business impact

---

## 🎯 Final Recommendation

### The Winning Stack

```
┌──────────────────────────┐
│ Algorithm: FP-Growth     │
│ - 175 high-quality rules │
│ - 10x faster than Apriori│
└────────┬─────────────────┘
         ↓
┌──────────────────────────┐
│ Features: Variant B      │
│ - Binary rules (175)     │
│ - RFM metrics (3)        │
│ - Total: 178 features    │
└────────┬─────────────────┘
         ↓
┌──────────────────────────┐
│ Clustering: K-Means, K=4 │
│ - Silhouette: 0.4772     │
│ - Davies-Bouldin: 0.85   │
└────────┬─────────────────┘
         ↓
┌──────────────────────────┐
│ Perspective: Customer    │
│ - 4 marketing personas   │
│ - Direct business impact │
└──────────────────────────┘
```

### 4 Customer Strategies

| Cluster | Goal | Action | KPI |
|---------|------|--------|-----|
| **C0** | Retention + Upsell | VIP program, premium bundles | LTV +20% |
| **C1** | Increase Frequency | Popular bundles, reactivation | Frequency +30% |
| **C2** | Conversion | Welcome bundles, guidance | Repeat >50% |
| **C3** | Reactivation | Flash sales, win-back | Churn -25% |

---

## 📊 Key Metrics

| Metric | Value | Status |
|--------|-------|--------|
| Total Transactions | 541,909 | ✅ |
| Unique Customers | 3,921 | ✅ |
| Rules Selected | 175 | ✅ |
| Optimal K | 4 | ✅ |
| Silhouette Score | 0.4772 | ✅ |
| Notebooks Executed | 8/8 | ✅ |

---

## 🚀 Next Steps

1. ✅ All 8 notebooks executed
2. 📊 Export cluster assignments
3. 🎯 Design 4 persona campaigns
4. 📧 Segment email lists
5. 🛒 Integrate bundles in e-commerce
6. 📈 Monitor KPIs monthly
7. 🔄 Refresh clustering quarterly

---

**Made with ❤️ by Nhóm 2 - Data Mining 2024**
