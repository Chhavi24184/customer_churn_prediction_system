
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Customer Analytics",
    page_icon="📊",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.main {
    background-color: #f5f7fb;
}
h1, h2, h3 {
    color: #253858;
}
.metric-card {
    background-color: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.title("📊 Customer Analytics Dashboard")

st.write(
    "Analyze customer data, understand churn patterns "
    "and explore important customer insights."
)

st.divider()

# ---------------- CSV UPLOAD ----------------
st.subheader("📁 Upload Customer Dataset")

uploaded_file = st.file_uploader(
    "Upload your CSV file",
    type=["csv"]
)

if uploaded_file is None:
    st.info("Please upload a customer CSV file to view analytics.")

    st.markdown("""
    **Expected input columns may include:**
    - age
    - gender
    - income_numeric
    - tenure
    - sub_plan
    - contract
    - monthly_charge
    - auto_renewal
    - late_payment
    - failed_transaction
    """)

    st.stop()

# ---------------- LOAD DATA ----------------
try:
    df = pd.read_csv(uploaded_file)

    # Clean column names
    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.lower()
    )

    if df.empty:
        st.error("The uploaded CSV file is empty.")
        st.stop()

except Exception as e:
    st.error(f"Unable to read CSV file: {e}")
    st.stop()

# ---------------- DATA OVERVIEW ----------------
st.subheader("📋 Dataset Overview")

col1, col2, col3, col4 = st.columns(4)

total_customers = len(df)
total_columns = len(df.columns)
missing_values = int(df.isnull().sum().sum())
duplicate_rows = int(df.duplicated().sum())

col1.metric("Total Customers", total_customers)
col2.metric("Total Features", total_columns)
col3.metric("Missing Values", missing_values)
col4.metric("Duplicate Records", duplicate_rows)

# ---------------- DATA PREVIEW ----------------
st.subheader("👀 Customer Data Preview")

st.dataframe(
    df.head(20),
    use_container_width=True
)

st.caption(
    f"Showing first {min(20, len(df))} records out of {len(df)}."
)

# ---------------- CHURN COLUMN DETECTION ----------------
possible_target_columns = [
    "default",
    "churn",
    "churned",
    "exited",
    "target",
    "prediction",
    "churn_prediction"
]

target_column = None

for column in possible_target_columns:
    if column in df.columns:
        target_column = column
        break

st.divider()

# ==================================================
# CHURN ANALYSIS
# ==================================================

st.subheader("🎯 Customer Churn Analysis")

if target_column is not None:

    target_values = df[target_column]

    # Convert common text labels into churn categories
    text_values = target_values.astype(str).str.strip().str.lower()

    churn_labels = [
        "1", "yes", "true", "churn", "churned",
        "default", "exited", "high risk"
    ]

    stay_labels = [
        "0", "no", "false", "stay", "stayed",
        "active", "not churned", "low risk"
    ]

    if text_values.isin(churn_labels + stay_labels).all():

        churn_count = int(text_values.isin(churn_labels).sum())
        stay_count = int(text_values.isin(stay_labels).sum())

        churn_data = pd.DataFrame({
            "Customer Status": ["Churn", "Stay"],
            "Count": [churn_count, stay_count]
        })

        churn_rate = (
            churn_count / total_customers * 100
            if total_customers > 0 else 0
        )

        col1, col2, col3 = st.columns(3)

        col1.metric("Churn Customers", churn_count)
        col2.metric("Customers Staying", stay_count)
        col3.metric("Churn Rate", f"{churn_rate:.2f}%")

        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:
            fig = px.pie(
                churn_data,
                names="Customer Status",
                values="Count",
                title="Customer Churn Distribution",
                hole=0.45
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        with chart_col2:
            fig = px.bar(
                churn_data,
                x="Customer Status",
                y="Count",
                color="Customer Status",
                title="Churn vs Non-Churn Customers",
                text="Count"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    else:
        st.warning(
            f"The column '{target_column}' exists, "
            "but its values could not be recognized as churn/stay labels. "
            "Please check the target column values."
        )

else:
    st.warning(
        "Churn target column is not available in this dataset."
    )

    st.info(
        "Your uploaded file contains customer input features only. "
        "Actual churn statistics require a labeled dataset with a "
        "'default' or 'churn' column."
    )

# ==================================================
# NUMERICAL ANALYSIS
# ==================================================

st.divider()
st.subheader("📈 Numerical Feature Analysis")

numeric_df = df.select_dtypes(include=["number"])

if not numeric_df.empty:

    selected_numeric = st.selectbox(
        "Select Numerical Feature",
        numeric_df.columns.tolist()
    )

    fig = px.histogram(
        df,
        x=selected_numeric,
        title=f"Distribution of {selected_numeric}",
        marginal="box",
        nbins=20
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader("📊 Statistical Summary")

    st.dataframe(
        numeric_df.describe().round(2),
        use_container_width=True
    )

else:
    st.info("No numerical columns found in this dataset.")

# ==================================================
# CATEGORICAL ANALYSIS
# ==================================================

st.divider()
st.subheader("📌 Categorical Feature Analysis")

categorical_df = df.select_dtypes(
    include=["object", "category", "bool"]
)

if not categorical_df.empty:

    selected_category = st.selectbox(
        "Select Categorical Feature",
        categorical_df.columns.tolist()
    )

    category_counts = (
        df[selected_category]
        .fillna("Missing")
        .astype(str)
        .value_counts()
        .reset_index()
    )

    category_counts.columns = ["Category", "Count"]

    fig = px.bar(
        category_counts,
        x="Category",
        y="Count",
        color="Category",
        title=f"Distribution of {selected_category}",
        text="Count"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:
    st.info("No categorical columns found in this dataset.")

# ==================================================
# CORRELATION ANALYSIS
# ==================================================

st.divider()
st.subheader("🔥 Correlation Analysis")

if len(numeric_df.columns) >= 2:

    correlation = numeric_df.corr()

    fig = px.imshow(
        correlation,
        text_auto=".2f",
        aspect="auto",
        color_continuous_scale="RdBu_r",
        title="Feature Correlation Heatmap"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:
    st.info(
        "At least two numerical columns are required "
        "for correlation analysis."
    )

# ==================================================
# MISSING VALUES ANALYSIS
# ==================================================

st.divider()
st.subheader("🔍 Missing Values Analysis")

missing_df = pd.DataFrame({
    "Column": df.columns,
    "Missing Values": df.isnull().sum().values,
    "Missing Percentage": (
        df.isnull().mean().values * 100
    ).round(2)
})

missing_df = missing_df.sort_values(
    by="Missing Values",
    ascending=False
)

st.dataframe(
    missing_df,
    use_container_width=True
)

# ---------------- FOOTER ----------------
st.divider()

st.success(
    "Customer Analytics Dashboard loaded successfully!"
)

st.caption(
    "Customer Churn Prediction System | Machine Learning Analytics"
)
