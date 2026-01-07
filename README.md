# Third part of case study: Shopping Cart Analysis

## Project Overview
This project focuses on analyzing online retail transaction data to uncover purchasing patterns and segment customers. The core analysis involves Market Basket Analysis (Association Rules) and Customer Clustering.

## Key Features

### 1. Data Processing & Association Rules
- Data cleaning and preprocessing.
- Mining Association Rules using Apriori and FP-Growth algorithms.
- Filtering and selecting top rules based on Lift, Confidence, and Support.

### 2. Rule-Based Customer Clustering (New)
We have implemented a specialized clustering approach that uses Association Rules as features to segment customers. This allows us to group customers not just by *what* they buy (items), but by the *patterns* of their purchases (rules).

#### Methodology
*   **Feature Engineering**:
    *   **Baseline**: Binary features representing whether a customer's basket satisfies the antecedents of a rule.
    *   **Advanced**: Weighted features (using Rule Lift or Confidence) combined with RFM (Recency, Frequency, Monetary) metrics for a holistic view.
*   **Clustering Algorithm**:
    *   Uses **K-Means** clustering.
    *   Automatically selects the optimal number of clusters ($K$) using **Silhouette Score** analysis.
*   **Visualization**:
    *   Projects high-dimensional data into 2D using **PCA** (Principal Component Analysis) or **SVD** for visualization.

#### Code Structure
*   **`src/cluster_library.py`**: Core library containing the `RuleBasedCustomerClusterer` class.
    *   `load_rules()`: Loads and filters top-k association rules.
    *   `build_customer_item_matrix()`: Creates a boolean matrix of customer purchases.
    *   `build_final_features()`: Constructs the feature matrix (Rules + RFM).
    *   `choose_k_by_silhouette()`: Evaluates K-Means performance for different $K$.
    *   `fit_kmeans()`: Fits the model and assigns cluster labels.
*   **`notebooks/clustering_from_rules.ipynb`**: The execution notebook that orchestrates the entire process, from loading data to saving results and plotting charts.

#### Outputs
*   `data/processed/customer_features_matrix.csv`: The generated feature matrix used for clustering.
*   `data/processed/customer_clusters_from_rules.csv`: Final result file containing Customer IDs and their assigned Cluster labels.
