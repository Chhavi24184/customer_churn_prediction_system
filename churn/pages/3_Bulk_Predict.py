import streamlit as st
import pandas as pd
import requests
import plotly.express as px

st.set_page_config(layout="wide")

# ---------- STYLE ----------
st.markdown("""
<style>
.stApp { background: linear-gradient(180deg, #f8fafc 0%, #eef2ff 100%); }
.main-header {
    text-align: center;
    background: linear-gradient(90deg, #0ea5e9, #6366f1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 54px;
    font-weight: 900;
    margin-bottom: 24px;
}
.status-card {
    background: #ffffff;
    padding: 18px;
    border-radius: 16px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 6px 20px rgba(15, 23, 42, 0.06);
    margin-bottom: 16px;
}
.stButton button {
    background: linear-gradient(90deg, #0ea5e9, #6366f1) !important;
    color: #ffffff !important;
    font-weight: 700 !important;
    border-radius: 12px !important;
    padding: 10px 25px !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-header'>Bulk Processing Engine</h1>", unsafe_allow_html=True)

file = st.file_uploader("Upload customer batch file", type=["csv", "xlsx"])

if file is not None:
    # read file
    if file.name.endswith(".csv"):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)

    st.markdown(f"""
    <div class='status-card'>
        <h4 style='margin:0; color:#22d3ee;'>Batch Metadata</h4>
        <p style='margin:5px 0 0 0; color:#94a3b8;'>File: {file.name} | Records: {len(df)}</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander("🔍 Preview Raw Data"):
        st.dataframe(df.head(10), use_container_width=True)

    # fast demo limit
    process_df = df.head(200).copy()

    st.markdown("---")
    if st.button("🚀 Execute Neural Analysis", use_container_width=True):
        preds = []
        total = len(process_df)
        
        progress_bar = st.progress(0)
        status_text = st.empty()

        for i, (_, row) in enumerate(process_df.iterrows()):
            status_text.text(f"Processing record {i+1} of {total}...")
            
            payload = {
                "age": row["age"],
                "gender": row["gender"],
                "income_numeric": row["income_numeric"],
                "tenure": row["tenure"],
                "sub_plan": row["sub_plan"],
                "contract": row["contract"],
                "monthly_charge": row["monthly_charge"],
                "auto_renewal": row["auto_renewal"],
                "late_payment": row["late_payment"],
                "failed_transaction": row["failed_transaction"]
            }

            try:
                res = requests.post(
                    "http://127.0.0.1:5000/predict",
                    json=payload
                ).json()
                preds.append(res.get("prediction", None))
            except:
                preds.append(None)

            progress_bar.progress((i + 1) / total)

        process_df["churn_prediction"] = preds
        status_text.success(f"Analysis complete for {total} records!")

        # Results visualization
        col1, col2 = st.columns([1, 1.5])
        
        with col1:
            st.subheader("Distribution")
            chart = process_df["churn_prediction"].value_counts().reset_index()
            chart.columns = ["Risk Level", "Count"]
            chart["Risk Level"] = chart["Risk Level"].map({0: "Low Risk", 1: "High Risk"})
            
            fig = px.pie(
                chart, values="Count", names="Risk Level", 
                hole=0.6,
                color="Risk Level",
                color_discrete_map={"Low Risk": "#22c55e", "High Risk": "#ef4444"}
            )
            fig.update_layout(
                paper_bgcolor='#ffffff',
                plot_bgcolor='#ffffff',
                template="plotly_white",
                showlegend=True
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("High Risk Segment")
            high_risk = process_df[process_df["churn_prediction"] == 1]
            st.dataframe(high_risk, use_container_width=True)

        # Download
        csv = process_df.to_csv(index=False).encode()
        st.download_button(
            "📥 Download Augmented Dataset",
            csv,
            "bulk_predictions.csv",
            "text/csv",
            use_container_width=True
        )
else:
    st.info("Please upload a CSV or Excel file containing customer profiles to run bulk analysis.")
    st.markdown("""
    **Required Columns:**
    `age`, `gender`, `income_numeric`, `tenure`, `sub_plan`, `contract`, `monthly_charge`, `auto_renewal`, `late_payment`, `failed_transaction`
    """)
