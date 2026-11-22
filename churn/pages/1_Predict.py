
import os
import requests
import streamlit as st
import plotly.graph_objects as go

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Customer Churn Prediction",
    page_icon="📊",
    layout="wide"
)

# ---------------- BACKEND API ----------------
API_URL = os.getenv(
    "API_URL",
    "https://customer-churn-prediction-system-glmv.onrender.com"
).rstrip("/")

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.main {
    background-color: #f5f7fb;
}
.title {
    font-size: 35px;
    font-weight: bold;
    color: #253858;
}
.subtitle {
    color: #64748b;
    font-size: 16px;
}
.stButton button {
    width: 100%;
    background-color: #2563eb;
    color: white;
    font-weight: bold;
    border-radius: 8px;
    height: 45px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown(
    '<div class="title">Customer Churn Prediction</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Enter customer details to predict the probability of churn.</div>',
    unsafe_allow_html=True
)

st.divider()

# ---------------- CUSTOMER INPUT FORM ----------------
st.subheader("👤 Customer Information")

with st.form("churn_prediction_form"):

    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input(
            "Age",
            min_value=18,
            max_value=80,
            value=30
        )

        gender = st.selectbox(
            "Gender",
            ["M", "F"]
        )

        income_numeric = st.selectbox(
            "Income Category",
            [1, 2, 3],
            format_func=lambda x: {
                1: "Low",
                2: "Medium",
                3: "High"
            }[x]
        )

        tenure = st.number_input(
            "Tenure (Months)",
            min_value=1,
            max_value=30,
            value=12
        )

        sub_plan = st.selectbox(
            "Subscription Plan",
            ["basic", "standard", "premium"]
        )

    with col2:
        contract = st.selectbox(
            "Contract Type",
            ["monthly", "annual"]
        )

        monthly_charge = st.number_input(
            "Monthly Charge",
            min_value=50.0,
            max_value=500.0,
            value=200.0,
            step=10.0
        )

        auto_renewal = st.selectbox(
            "Auto Renewal",
            [1, 0],
            format_func=lambda x: "Yes" if x == 1 else "No"
        )

        late_payment = st.selectbox(
            "Late Payment",
            [0, 1],
            format_func=lambda x: "Yes" if x == 1 else "No"
        )

        failed_transaction = st.selectbox(
            "Failed Transaction",
            [0, 1],
            format_func=lambda x: "Yes" if x == 1 else "No"
        )

    submitted = st.form_submit_button(
        "🔍 Predict Customer Churn"
    )

# ---------------- PREDICTION ----------------
if submitted:

    data = {
        "age": int(age),
        "gender": gender,
        "income_numeric": int(income_numeric),
        "tenure": int(tenure),
        "sub_plan": sub_plan,
        "contract": contract,
        "monthly_charge": float(monthly_charge),
        "auto_renewal": int(auto_renewal),
        "late_payment": int(late_payment),
        "failed_transaction": int(failed_transaction)
    }

    with st.spinner("Analyzing customer data... Please wait."):

        try:
            response = requests.post(
                f"{API_URL}/predict",
                json=data,
                timeout=120
            )

            response.raise_for_status()
            result = response.json()

            if "error" in result:
                st.error(f"Backend Error: {result['error']}")

            elif "prediction" not in result or "probability" not in result:
                st.error("Invalid response received from prediction API.")

            else:
                prediction = int(result["prediction"])
                probability = float(result["probability"])

                # Convert probability into percentage
                churn_percentage = probability * 100

                st.divider()
                st.subheader("📊 Prediction Results")

                col1, col2 = st.columns(2)

                with col1:
                    st.metric(
                        "Churn Probability",
                        f"{churn_percentage:.2f}%"
                    )

                with col2:
                    st.metric(
                        "Customer Status",
                        "Likely to Churn" if prediction == 1
                        else "Likely to Stay"
                    )

                # ---------------- GAUGE CHART ----------------
                fig = go.Figure(
                    go.Indicator(
                        mode="gauge+number",
                        value=churn_percentage,
                        title={
                            "text": "Churn Risk (%)"
                        },
                        number={
                            "suffix": "%"
                        },
                        gauge={
                            "axis": {
                                "range": [0, 100]
                            },
                            "bar": {
                                "color": "#2563eb"
                            },
                            "steps": [
                                {
                                    "range": [0, 40],
                                    "color": "#bbf7d0"
                                },
                                {
                                    "range": [40, 70],
                                    "color": "#fde68a"
                                },
                                {
                                    "range": [70, 100],
                                    "color": "#fecaca"
                                }
                            ],
                            "threshold": {
                                "line": {
                                    "color": "red",
                                    "width": 4
                                },
                                "thickness": 0.75,
                                "value": 70
                            }
                        }
                    )
                )

                fig.update_layout(
                    height=350,
                    margin=dict(
                        l=30,
                        r=30,
                        t=60,
                        b=20
                    )
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

                # ---------------- RISK MESSAGE ----------------
                if prediction == 1:
                    st.error(
                        "⚠️ High Churn Alert: This customer is predicted to churn."
                    )

                    st.info(
                        "Recommended Action: Offer personalized discounts, "
                        "improve customer support, and provide retention benefits."
                    )

                else:
                    st.success(
                        "✅ Low Churn Alert: This customer is predicted to stay."
                    )

                    st.info(
                        "Recommended Action: Maintain customer engagement "
                        "and continue providing good service."
                    )

        except requests.exceptions.Timeout:
            st.error(
                "Request timed out. The backend may be waking up. "
                "Please wait and try again."
            )

        except requests.exceptions.ConnectionError:
            st.error(
                "Connection Error: Unable to connect to the deployed backend. "
                "Please check the backend URL and Render service status."
            )

        except requests.exceptions.HTTPError as e:
            st.error(f"HTTP Error: {e}")

        except Exception as e:
            st.error(f"Unexpected Error: {str(e)}")

# ---------------- FOOTER ----------------
st.divider()

st.caption(
    "Customer Churn Prediction System | Powered by Machine Learning"
)
