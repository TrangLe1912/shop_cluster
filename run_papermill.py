import papermill as pm
import os

# ==============================
# SETUP
# ==============================
os.makedirs("notebooks/runs", exist_ok=True)
os.makedirs("data/processed", exist_ok=True)

# ==============================
# 1. PREPROCESSING + EDA
# ==============================
pm.execute_notebook(
    "notebooks/preprocessing_and_eda.ipynb",
    "notebooks/runs/preprocessing_and_eda_run.ipynb",
    parameters=dict(
        DATA_PATH="data/raw/online_retail.csv",
        COUNTRY="United Kingdom",
        OUTPUT_DIR="data/processed",

        # Tắt toàn bộ plot khi chạy batch
        PLOT_REVENUE=False,
        PLOT_TIME_PATTERNS=False,
        PLOT_PRODUCTS=False,
        PLOT_CUSTOMERS=False,
        PLOT_RFM=False,
    ),
    kernel_name="python3",
)

# ==============================
# 2. BASKET PREPARATION
# ==============================
pm.execute_notebook(
    "notebooks/basket_preparation.ipynb",
    "notebooks/runs/basket_preparation_run.ipynb",
    parameters=dict(
        CLEANED_DATA_PATH="data/processed/cleaned_uk_data.csv",
        BASKET_BOOL_PATH="data/processed/basket_bool.parquet",
        INVOICE_COL="InvoiceNo",
        ITEM_COL="Description",
        QUANTITY_COL="Quantity",
        THRESHOLD=1,
    ),
    kernel_name="python3",
)

# ==============================
# 3. FP-GROWTH MODELLING
# (NGUYÊN LIỆU ĐẦU VÀO CHO CLUSTERING)
# ==============================
pm.execute_notebook(
    "notebooks/fp_growth_modelling.ipynb",
    "notebooks/runs/fp_growth_modelling_run.ipynb",
    parameters=dict(
        BASKET_BOOL_PATH="data/processed/basket_bool.parquet",

        # FILE LUẬT CHÍNH THỨC CHO CẢ NHÓM
        RULES_OUTPUT_PATH="data/processed/rules_top50_fpgrowth.csv",

        # =========================
        # FP-Growth parameters
        # =========================
        MIN_SUPPORT=0.03,     # đủ mạnh, tránh nhiễu
        MAX_LEN=3,            # tránh luật quá dài

        # Sinh luật
        METRIC="lift",
        MIN_THRESHOLD=1.0,

        # =========================
        # FILTER RULES
        # =========================
        FILTER_MIN_SUPPORT=0.03,
        FILTER_MIN_CONF=0.3,
        FILTER_MIN_LIFT=1.2,

        FILTER_MAX_ANTECEDENTS=2,
        FILTER_MAX_CONSEQUENTS=1,

        # TOP-K LUẬT ĐƯA VÀO PHÂN CỤM
        TOP_N_RULES=50,

        # =========================
        # TẮT TOÀN BỘ PLOT
        # =========================
        PLOT_TOP_LIFT=False,
        PLOT_TOP_CONF=False,
        PLOT_SCATTER=False,
        PLOT_NETWORK=False,
        PLOT_PLOTLY_SCATTER=False,
    ),
    kernel_name="python3",
)

print("✅ Đã hoàn thành pipeline FP-Growth và xuất rules_top50_fpgrowth.csv")
