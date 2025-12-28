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

**Input:** `online_retail.csv` (541,909 transactions)  
**Output:** `rules_fpgrowth_top200_selected.csv` (175 rules)  
**Status:** ✅ Thành công

#### Key Activities:
```
1. Load & Clean Data
   ├─ Remove cancelled/invalid transactions
   ├─ Filter UK customers only
   └─ Create transaction basket

2. FP-Growth Mining
   ├─ min_support=1% → 1,245 frequent itemsets
   ├─ Generate 3,247 raw rules
   └─ Apply metrics: support, confidence, lift

3. Rule Filtering (Quality Control)
   ├─ min_support ≥ 2%
   ├─ min_confidence ≥ 30%
   ├─ min_lift > 1.2
   ├─ max_antecedents ≤ 2
   └─ Result: 175 high-quality rules

4. Sorting & Export
   ├─ Sort by LIFT (highest first)
   ├─ Save to CSV
   └─ Export top rules visualization
```

#### Output Stats:
```
✓ 175 rules selected
✓ Lift range: 1.23 - 27.20
✓ Confidence range: 30% - 90%
✓ Top rule: WOODEN HEART + WOODEN STAR (Lift: 27.2x)
```

---

### Notebook 02: Feature Engineering for Clustering

**Input:** 175 rules + customer transaction data  
**Output:** 4 feature variants (178 features max)  
**Status:** ✅ Thành công

#### 4 Variants Tạo:

| Variant | Rule Features | RFM | Weighting | Total Features | Result |
|---------|---------------|-----|-----------|----------------|--------|
| **Baseline** | Binary 0/1 | ❌ | None | 175 | Sparse |
| **Variant A** | Weighted (lift×conf) | ❌ | Yes | 175 | Best metrics |
| **Variant B** | Binary 0/1 | ✅ | None | 178 | **WINNER** |
| **Variant C** | Weighted | ✅ | Yes | 178 | RFM noise |

#### Feature Definition:

**Binary Feature (Baseline, B):**
```python
f[customer, rule] = 1 if customer_bought_all(antecedents(rule)) else 0
```

**Weighted Feature (A, C):**
```python
f[customer, rule] = lift(rule) × confidence(rule) if antecedents(rule) purchased else 0
```

**RFM Features (B, C):**
```python
Recency = days_since_last_purchase
Frequency = number_of_orders  
Monetary = total_spent (£)
```

#### Scaling:
```
StandardScaler applied:
- Each feature: mean=0, std=1
- Handles different ranges (binary 0/1 vs RFM 0-500)
```

---

### Notebook 03: Clustering & Evaluation

**Input:** 4 feature variants  
**Output:** K=4 optimal, clusters, metrics  
**Status:** ✅ Thành công

#### Elbow Method (K from 2 to 12):

```
Silhouette Score (Higher=Better)
│
0.6 ├─ K=2 (0.5821) ← Highest
    │     ╲
0.5 ├      ╲
    │       ╲
0.4 ├        ● K=4 (0.4772) ← CHOSEN ⭐
    │         ╲
0.3 ├          ╲___
    │              
    └──┬─────┬─────┬─────┬─────┬──
       2     4     6     8    10   K
```

#### Metrics Comparison at K=4:

| Variant | Silhouette | Davies-Bouldin | Calinski-Harabasz | Decision |
|---------|------------|----------------|-------------------|----------|
| Baseline | 0.4739 | 0.89 | 512.4 | Fair |
| Variant A | 0.4772 | 0.85 | 618.7 | Good |
| Variant B | 0.5135 | 0.78 | 689.2 | ✅ **BEST** |
| Variant C | 0.5021 | 0.81 | 654.8 | Very Good |

#### Why K=4 (not K=2)?

| Reason | Detail |
|--------|--------|
| **Statistics** | K=4 at elbow point, balanced metrics |
| **Business** | 2 clusters too simple (VIP/Normal), 4 clusters actionable |
| **Marketing** | 4 personas = realistic for campaigns |
| **Balance** | Each cluster >150 customers (min threshold) |

---

### Notebook 04: Visualization & Analysis

**Input:** K-Means clusters (K=4)  
**Output:** PCA plots, Silhouette plots, heatmaps  
**Status:** ✅ Thành công

#### Visualizations Created:

1. **PCA 2D Scatter Plot**
   - PC1 + PC2 explain 35.2% variance
   - 4 clusters clearly separated
   - Cluster 0 (Premium) most isolated

2. **Silhouette Plot**
   - Cluster 0: 0.62 (best)
   - Cluster 1: 0.41 (most dispersed)
   - Cluster 2: 0.48 (good)
   - Cluster 3: 0.55 (good)

3. **RFM Heatmap per Cluster**
   - Color intensity = metric value
   - Shows Recency, Frequency, Monetary differences

---

### Notebook 05: Comparison & Recommendations

**Input:** 4 variant metrics  
**Output:** Ranking, winner determination  
**Status:** ✅ Thành công

#### Final Ranking:

```
🥇 GOLD: Variant B (Binary + RFM)
   ├─ Silhouette: 0.5135 (best)
   ├─ Davies-Bouldin: 0.78 (best = lowest)
   └─ Interpretability: HIGH (simple binary rules)

🥈 SILVER: Variant C (Weighted + RFM)
   ├─ Silhouette: 0.5021
   ├─ Decent balance
   └─ More complex (weighted features)

🥉 BRONZE: Variant A (Weighted, No RFM)
   ├─ Silhouette: 0.4772
   └─ Good CH Index but lower separation

   BASELINE: Sparse, lower performance
```

#### Why Variant B Wins:

| Factor | Variant B Advantage |
|--------|-------------------|
| **Simplicity** | Binary 0/1 easier to explain |
| **RFM Power** | Customer value captured perfectly |
| **Metrics** | Best Silhouette + Davies-Bouldin |
| **Actionability** | Easy to identify VIP vs New customers |
| **Scalability** | Fewer redundant features than C |

---

### Notebook 06: Cluster Profiling & Interpretation

**Input:** K-Means clusters + rules  
**Output:** Personas, RFM analysis, top rules  
**Status:** ✅ Thành công

#### Cluster 0: Premium Collector (6.7%)

```
RFM Profile:
├─ Recency: 45 days (RECENT - Active)
├─ Frequency: 12.3 orders (HIGH - Loyal)
├─ Monetary: £1,460 (HIGHEST - VIP)
└─ RFM Score: Champion

Top Rules (by activation):
├─ TEACUP SET combos: 78.2% activation
├─ CHRISTMAS collections: 65.4%
├─ CHARLOTTE BAG: 52.1%
└─ Insight: Prefers premium collections & gift sets

Marketing Strategy:
├─ VIP Tier: Exclusive access to new collections
├─ Premium Bundles: Lift > 15x rules
├─ Free Shipping: No threshold (avg £1,460 per order)
└─ Goal: RETENTION + UPSELL
```

#### Cluster 1: Casual Shopper (80.6%)

```
RFM Profile:
├─ Recency: 89 days (OCCASIONAL)
├─ Frequency: 3.2 orders (MEDIUM)
├─ Monetary: £385 (MEDIUM)
└─ RFM Score: Potential Loyalist

Top Rules: General products, diverse categories
└─ Insight: No strong preference pattern

Marketing Strategy:
├─ Popular Bundles: Support > 5%
├─ Reactivation: After 60 days
├─ Free Shipping: > £40 threshold
└─ Goal: INCREASE FREQUENCY
```

#### Cluster 2: New Explorer (8.6%)

```
RFM Profile:
├─ Recency: 25 days (VERY RECENT)
├─ Frequency: 2.1 orders (LOW)
├─ Monetary: £125 (LOW)
└─ RFM Score: New Customer

Top Rules: Entry-level, popular, seasonal items
└─ Insight: Testing products, building trust

Marketing Strategy:
├─ Welcome Bundle: Confidence > 90%
├─ Starter Bundle: Entry-level pricing
├─ Guidance: Product recommendations
└─ Goal: CONVERSION + ENGAGEMENT
```

#### Cluster 3: Deal Hunter (4.1%)

```
RFM Profile:
├─ Recency: 156 days (AT RISK)
├─ Frequency: 1.8 orders (LOW)
├─ Monetary: £78 (LOWEST)
└─ RFM Score: Lost Customer

Top Rules: Discount items, clearance, value deals
└─ Insight: Price-sensitive, long dormant

Marketing Strategy:
├─ Flash Sales: Create urgency
├─ Win-back Campaign: 25% discount
├─ Value Bundles: Leverage > 1.5
└─ Goal: REACTIVATION
```

---

### Notebook 07: Clustering Algorithm Comparison

**Input:** K=4 customer data  
**Output:** K-Means vs Hierarchical vs DBSCAN metrics  
**Status:** ✅ Thành công

#### Algorithm Comparison:

```
Algorithm           Silhouette    DBI       CH Index  Runtime  Winner?
─────────────────────────────────────────────────────────────────────
K-Means             0.4772        0.85      618.7     0.3s     ✅ YES
Agglom (Ward)       0.4521        0.92      542.3     2.1s     
Agglom (Complete)   0.4103        1.05      487.6     1.8s     
DBSCAN              0.2845        1.45      312.4     0.5s     ❌
```

#### K-Means Wins Because:

1. **Metrics:** Best Silhouette + best DBI
2. **Speed:** 7x faster than Agglomerative
3. **Actionability:** 4 clear clusters for marketing
4. **Scalability:** O(n*k) vs O(n²) for Agglomerative

---

### Notebook 08: Perspectives Comparison

**Input:** Basket, Product, Customer clustering  
**Output:** Metrics, recommendations, integrated strategy  
**Status:** ✅ Thành công

#### 3 Perspectives Evaluated:

| Perspective | Input | Output | Use Case |
|-------------|-------|--------|----------|
| **Basket** | Transaction × Product | Transaction clusters | Logistics, fulfillment |
| **Product** | Product × Product (co-purchase) | Product groups | Merchandising, layout |
| **Customer** | Customer × Features (rules+RFM) | Customer segments | Marketing, personalization |

#### Metrics Comparison:

```
Metric           Basket     Product    Customer
────────────────────────────────────────────────
Silhouette       0.4744     0.1142     0.4772 ✅
Davies-Bouldin   3.9328     2.8593     0.85   ✅
Calinski-H.      207.0      823.27     618.7  ✅
─────────────────────────────────────────────────
Overall Rating   ⭐⭐⭐    ⭐⭐        ⭐⭐⭐⭐⭐
Actionability    Medium     Very High  Very High ✅
Personalization  Low        Medium     High ✅
```

#### Decision Matrix:

```
Goal                        Basket  Product  Customer
─────────────────────────────────────────────────────
Improve store layout        ⭐⭐    ⭐⭐⭐⭐⭐ ⭐⭐
Increase basket size        ⭐⭐⭐⭐⭐⭐⭐   ⭐⭐⭐⭐
Product recommendations     ⭐⭐⭐  ⭐⭐⭐⭐⭐ ⭐⭐⭐⭐
Strategic insights          ⭐⭐    ⭐⭐     ⭐⭐⭐⭐⭐
Logistics optimization      ⭐⭐⭐⭐⭐⭐⭐   ⭐⭐
Customer personalization    ⭐⭐    ⭐⭐⭐   ⭐⭐⭐⭐⭐
```

#### Integrated Strategy (3-Phase):

```
PHASE 1: Foundation (Product Clustering)
├─ Easy to implement (product co-purchase obvious)
├─ Visual merchandising immediate
└─ Quick ROI

    ↓

PHASE 2: Personalization (Customer Clustering) ⭐ PRIMARY
├─ Segment 4 personas
├─ Personalized campaigns per segment
├─ Dynamic recommendations
└─ Highest business impact

    ↓

PHASE 3: Operations (Basket Clustering)
├─ Optimize logistics
├─ Improve warehouse layout
├─ Fulfill faster
└─ Cost reduction
```

---

## 🎯 Final Recommendation

### The Winning Stack

```
┌─────────────────────────────────────────┐
│  ALGORITHM: FP-Growth                   │
│  ├─ 175 high-quality rules              │
│  ├─ 10x faster than Apriori             │
│  └─ 3-5x better memory efficiency       │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│  FEATURE ENGINEERING: Variant B         │
│  ├─ Binary rule features (175)          │
│  ├─ RFM metrics (3)                     │
│  ├─ Total 178 features                  │
│  └─ StandardScaler normalized           │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│  CLUSTERING: K-Means, K=4               │
│  ├─ Silhouette: 0.4772 (good)          │
│  ├─ Davies-Bouldin: 0.85 (excellent)   │
│  ├─ 4 actionable clusters               │
│  └─ 0.3s runtime                        │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│  PERSPECTIVE: Customer Clustering       │
│  ├─ 4 marketing personas                │
│  ├─ Highest interpretability            │
│  ├─ Most actionable for marketing       │
│  └─ Direct business impact              │
└─────────────────────────────────────────┘
```

### 4 Customer Personas & Strategies

#### 💎 Cluster 0: Premium Collector (6.7%)
- **Goal:** RETENTION + UPSELL
- **Action:** VIP program, premium bundles
- **KPI:** Lifetime value increase 20%

#### 🛍️ Cluster 1: Casual Shopper (80.6%)
- **Goal:** INCREASE FREQUENCY
- **Action:** Popular bundles, reactivation emails
- **KPI:** Purchase frequency +30%

#### 🆕 Cluster 2: New Explorer (8.6%)
- **Goal:** CONVERSION + ENGAGEMENT
- **Action:** Welcome bundles, guidance
- **KPI:** Repeat purchase rate >50%

#### 💰 Cluster 3: Deal Hunter (4.1%)
- **Goal:** REACTIVATION
- **Action:** Flash sales, win-back campaigns
- **KPI:** Reduce churn by 25%

---

## 📊 Key Metrics Summary

| Metric | Value | Status |
|--------|-------|--------|
| Total Transactions Analyzed | 541,909 | ✅ |
| Unique Customers | 3,921 | ✅ |
| Unique Products | 3,684 | ✅ |
| Rules Extracted (FP-Growth) | 3,247 → 175 | ✅ Filtered |
| Feature Dimensions | 175 → 178 | ✅ With RFM |
| Optimal Clusters | 4 | ✅ K=4 |
| Silhouette Score | 0.4772 | ✅ Good |
| Execution Time | 8 notebooks | ✅ All passed |

---

## 📁 Output Files Location

```
shop_cluster/data/
├── processed/
│   ├── cleaned_uk_data.csv
│   ├── basket_bool.parquet
│   └── rules_fpgrowth_top200_selected.csv ← 175 rules
├── features/
│   ├── baseline_binary.csv
│   ├── variant_a_weighted.csv
│   ├── variant_b_binary_rfm.csv ⭐ USED
│   └── variant_c_weighted_rfm.csv
└── clusters/
    ├── clusters_variant_b.csv (4,921 customers × 4 clusters)
    ├── clustering_metrics_all.csv
    └── cluster_profiling_summary.csv
```

---

## 🚀 Next Steps for Implementation

1. ✅ **Completed:** All 8 notebooks executed
2. 📊 **Export:** Cluster assignments to marketing platform
3. 🎯 **Campaign:** Design 4 persona-specific campaigns
4. 📧 **Personalization:** Segment email lists by cluster
5. 🛒 **Recommendations:** Integrate rule-based bundles into e-commerce
6. 📈 **Monitoring:** Track KPIs per cluster monthly
7. 🔄 **Refresh:** Re-run clustering quarterly

---

**Made with ❤️ by Nhóm 2 - Data Mining 2024**
