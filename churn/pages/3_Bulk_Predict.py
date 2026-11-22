
import os
import requests
import pandas as pd
import streamlit as st
import time

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Bulk Churn Prediction",
    page_icon="📂",
    layout="wide"
)

# ---------------- API CONFIG ----------------
API_URL = os.getenv(
    "API_URL",
    "https://customer-churn-prediction-system-glmv.onrender.com"
).rstrip("/")

# ---------------- HEADER ----------------
st.title("📂 Bulk Customer Churn Prediction")
st.write(
    "Upload a CSV file to predict churn for multiple customers at once."
)

st.divider()

# ---------------- REQUIRED COLUMNS ----------------
REQUIRED_COLUMNS = [
    "age",
    "gender",
    "income_numeric",
    "tenure",
    "sub_plan",
    "contract",
    "monthly_charge",
    "auto_renewal",
    "late_payment",
    "failed_transaction"
]

# ---------------- CSV TEMPLATE ----------------
sample_data = pd.DataFrame([
    [25, "M", 1, 3, "basic", "monthly", 299, 0, 1, 1],
    [42, "F", 2, 18, "standard", "annual", 199, 1, 0, 0],
    [31, "M", 3, 24, "premium", "annual", 450, 1, 0, 0]
], columns=REQUIRED_COLUMNS)

st.download_button(
    "⬇️ Download CSV Template",
    data=sample_data.to_csv(index=False).encode("utf-8"),
    file_name="churn_template.csv",
    mime="text/csv"
)

# ---------------- FILE UPLOAD ----------------
uploaded_file = st.file_uploader(
    "Upload Customer CSV",
    type=["csv"]
)

if uploaded_file is not None:

    try:
        df = pd.read_csv(uploaded_file)
        df.columns = df.columns.str.strip().str.lower()

        st.success("CSV uploaded successfully!")

        st.subheader("📋 Uploaded Dataset")

        col1, col2, col3 = st.columns(3)

        col1.metric("Total Customers", len(df))
        col2.metric("Total Columns", len(df.columns))
        col3.metric("Missing Values", int(df.isnull().sum().sum()))

        st.dataframe(df.head(20), use_container_width=True)

        # ---------------- VALIDATION ----------------
        missing_columns = [
            col for col in REQUIRED_COLUMNS
            if col not in df.columns
        ]

        if missing_columns:
            st.error(
                "Missing required columns: "
                + ", ".join(missing_columns)
            )
            st.stop()

        if df.empty:
            st.error("Uploaded CSV is empty.")
            st.stop()

        # ---------------- PREDICTION ----------------
        if st.button("🚀 Start Bulk Prediction", use_container_width=True):

            results = []
            progress = st.progress(0)
            status = st.empty()

            for index, row in df.iterrows():

                customer_data = {}

                for col in REQUIRED_COLUMNS:
                    customer_data[col] = row[col]

                try:
                    response = requests.post(
                        f"{API_URL}/predict",
                        json=customer_data,
                        timeout=120
                    )

                    response.raise_for_status()
                    output = response.json()

                    if "error" in output:
                        raise ValueError(output["error"])

                    prediction = int(output["prediction"])
                    probability = float(output["probability"])

                    results.append({
                        "Customer_ID": index + 1,
                        "Prediction": prediction,
                        "Churn_Probability": probability,
                        "Churn_Percentage": round(probability * 100, 2),
                        "Risk_Status": (
                            "High Risk" if prediction == 1
                            else "Low Risk"
                        ),
                        "API_Status": "Success"
                    })

                except Exception as e:
                    results.append({
                        "Customer_ID": index + 1,
                        "Prediction": None,
                        "Churn_Probability": None,
                        "Churn_Percentage": None,
                        "Risk_Status": "Prediction Failed",
                        "API_Status": str(e)
                    })

                progress.progress((index + 1) / len(df))
                status.write(
                    f"Processing customer {index + 1} of {len(df)}"
                )

            # ---------------- SAVE RESULTS ----------------
            results_df = pd.DataFrame(results)

            # Combine original customer details with predictions
            final_df = pd.concat(
                [
                    df.reset_index(drop=True),
                    results_df.drop(columns=["Customer_ID"])
                ],
                axis=1
            )

            st.session_state["bulk_results"] = final_df

            success_count = int(
                (results_df["API_Status"] == "Success").sum()
            )

            failed_count = len(results_df) - success_count

            st.success("Bulk prediction process completed!")

            col1, col2, col3 = st.columns(3)

            col1.metric("Total Processed", len(df))
            col2.metric("Successful", success_count)
            col3.metric("Failed", failed_count)

            st.subheader("📊 Bulk Prediction Results")

            st.dataframe(
                final_df,
                use_container_width=True
            )

            csv_data = final_df.to_csv(index=False).encode("utf-8")

            st.download_button(
                "⬇️ Download Prediction Results",
                data=csv_data,
                file_name="bulk_churn_predictions.csv",
                mime="text/csv"
            )

    except Exception as e:
        st.error(f"Error reading CSV: {e}")

# ---------------- FOOTER ----------------
st.divider()
st.caption("Customer Churn Prediction System | Bulk Prediction")
