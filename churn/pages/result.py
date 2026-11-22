
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Prediction Results",
    page_icon="📊",
    layout="wide"
)

# ---------------- HEADER ----------------
st.title("📊 Customer Prediction Results")
st.write("View and analyze customer churn prediction results.")

st.divider()

# ---------------- GET RESULTS ----------------
if "bulk_results" not in st.session_state:

    st.warning(
        "No bulk prediction results available. "
        "Please visit the Bulk Prediction page and upload a CSV first."
    )

    st.stop()

df = st.session_state["bulk_results"].copy()

if df.empty:
    st.warning("No prediction records found.")
    st.stop()

# ---------------- VALID RESULTS ----------------
if "API_Status" in df.columns:
    successful_df = df[
        df["API_Status"] == "Success"
    ].copy()
else:
    successful_df = df.copy()

if successful_df.empty:
    st.error("No successful predictions available.")
    st.stop()

successful_df["Churn_Percentage"] = pd.to_numeric(
    successful_df["Churn_Percentage"],
    errors="coerce"
)

successful_df["Prediction"] = pd.to_numeric(
    successful_df["Prediction"],
    errors="coerce"
)

# ---------------- SUMMARY ----------------
total_customers = len(df)
successful_count = len(successful_df)
failed_count = total_customers - successful_count

churn_count = int(
    (successful_df["Prediction"] == 1).sum()
)

stay_count = int(
    (successful_df["Prediction"] == 0).sum()
)

churn_rate = (
    churn_count / successful_count * 100
    if successful_count else 0
)

st.subheader("📌 Overall Summary")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Customers", total_customers)
col2.metric("Successful Predictions", successful_count)
col3.metric("Churn Customers", churn_count)
col4.metric("Churn Rate", f"{churn_rate:.2f}%")

st.divider()

# ---------------- CHURN DISTRIBUTION ----------------
st.subheader("📈 Churn Distribution")

chart_col1, chart_col2 = st.columns(2)

with chart_col1:

    distribution = pd.DataFrame({
        "Customer Status": ["Churn", "Stay"],
        "Count": [churn_count, stay_count]
    })

    fig = px.pie(
        distribution,
        names="Customer Status",
        values="Count",
        title="Churn vs Non-Churn Distribution",
        hole=0.45
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with chart_col2:

    fig = px.bar(
        distribution,
        x="Customer Status",
        y="Count",
        color="Customer Status",
        text="Count",
        title="Customer Prediction Count"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ---------------- PROBABILITY ANALYSIS ----------------
st.divider()
st.subheader("🎯 Churn Probability Analysis")

fig = px.histogram(
    successful_df,
    x="Churn_Percentage",
    nbins=10,
    title="Distribution of Churn Probability",
    labels={
        "Churn_Percentage": "Churn Probability (%)"
    }
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ---------------- RISK ANALYSIS ----------------
st.subheader("⚠️ Customer Risk Analysis")

high_risk = int(
    (successful_df["Risk_Status"] == "High Risk").sum()
)

low_risk = int(
    (successful_df["Risk_Status"] == "Low Risk").sum()
)

col1, col2 = st.columns(2)

col1.metric("High Risk Customers", high_risk)
col2.metric("Low Risk Customers", low_risk)

# ---------------- COMPLETE RESULTS ----------------
st.divider()
st.subheader("📋 Complete Prediction Records")

st.dataframe(
    df,
    use_container_width=True
)

# ---------------- FILTER RESULTS ----------------
st.subheader("🔎 Filter Customers")

risk_options = successful_df["Risk_Status"].dropna().unique().tolist()

selected_risk = st.selectbox(
    "Select Risk Category",
    ["All"] + risk_options
)

if selected_risk == "All":
    filtered_df = successful_df
else:
    filtered_df = successful_df[
        successful_df["Risk_Status"] == selected_risk
    ]

st.dataframe(
    filtered_df,
    use_container_width=True
)

# ---------------- DOWNLOAD RESULTS ----------------
st.divider()

csv_data = df.to_csv(index=False).encode("utf-8")

st.download_button(
    "⬇️ Download Complete Results CSV",
    data=csv_data,
    file_name="customer_churn_results.csv",
    mime="text/csv",
    use_container_width=True
)

# ---------------- FOOTER ----------------
st.divider()

st.success("Prediction results loaded successfully!")

st.caption(
    "Customer Churn Prediction System | Results Dashboard"
)
