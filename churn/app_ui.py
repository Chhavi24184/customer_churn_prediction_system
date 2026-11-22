
import os
import streamlit as st
import requests
import plotly.graph_objects as go

# ---------------- CONFIGURATION ----------------

st.set_page_config(
    page_title="AI Customer Churn Intelligence",
    page_icon="📊",
    layout="wide"
)

# Local testing uses localhost.
# Render deployment uses the API_URL environment variable.
API_URL = os.getenv(
    "API_URL",
    "http://127.0.0.1:5000"
).rstrip("/")


# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>

body {
    background: linear-gradient(120deg, #0f172a, #020617);
}

.hero {
    text-align: center;
    font-size: 48px;
    font-weight: 800;
    background: linear-gradient(90deg, #22d3ee, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.subtitle {
    text-align: center;
    color: #94a3b8;
    font-size: 18px;
}

.glass {
    background: rgba(255,255,255,0.08);
    padding: 35px;
    border-radius: 20px;
    backdrop-filter: blur(14px);
    box-shadow: 0 6px 40px rgba(0,0,0,0.5);
}

</style>
""", unsafe_allow_html=True)


# ---------------- HEADER ----------------

st.markdown(
    '<p class="hero">AI Customer Churn Intelligence</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="subtitle">Predict churn risk instantly using machine learning analytics</p>',
    unsafe_allow_html=True
)

st.write("")


# ---------------- CUSTOMER INPUT FORM ----------------

st.markdown('<div class="glass">', unsafe_allow_html=True)

c1, c2 = st.columns(2)

with c1:

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
        "Income Level",
        [1, 2, 3]
    )

    tenure = st.number_input(
        "Tenure",
        min_value=1,
        max_value=30,
        value=5
    )

    sub_plan = st.selectbox(
        "Subscription Plan",
        ["basic", "standard", "premium"]
    )


with c2:

    contract = st.selectbox(
        "Contract",
        ["monthly", "annual"]
    )

    monthly_charge = st.number_input(
        "Monthly Charge",
        min_value=50,
        max_value=500,
        value=100
    )

    auto_renewal = st.selectbox(
        "Auto Renewal",
        [0, 1]
    )

    late_payment = st.selectbox(
        "Late Payment",
        [0, 1]
    )

    failed_transaction = st.selectbox(
        "Failed Transaction",
        [0, 1]
    )


st.markdown('</div>', unsafe_allow_html=True)

st.write("")

predict = st.button(
    "Predict Churn",
    use_container_width=True
)


# ---------------- PREDICTION ----------------

if predict:

    data = {
        "age": age,
        "gender": gender,
        "income_numeric": income_numeric,
        "tenure": tenure,
        "sub_plan": sub_plan,
        "contract": contract,
        "monthly_charge": monthly_charge,
        "auto_renewal": auto_renewal,
        "late_payment": late_payment,
        "failed_transaction": failed_transaction
    }

    try:

        with st.spinner("Analyzing customer data..."):

            response = requests.post(
                f"{API_URL}/predict",
                json=data,
                timeout=60
            )

            response.raise_for_status()

            res = response.json()

        # Check API response
        if "prediction" not in res or "probability" not in res:
            st.error(f"Invalid API response: {res}")

        else:

            prediction = int(res["prediction"])
            prob = float(res["probability"])

            # Validate probability
            if not 0 <= prob <= 1:
                st.error("Invalid probability received from backend.")

            else:

                st.subheader("Customer Churn Prediction Result")

                # Gauge Chart
                fig = go.Figure(
                    go.Indicator(
                        mode="gauge+number",
                        value=prob * 100,
                        title={
                            "text": "Churn Probability (%)"
                        },
                        gauge={
                            "axis": {
                                "range": [0, 100]
                            },
                            "bar": {
                                "color": "#22d3ee"
                            },
                            "steps": [
                                {
                                    "range": [0, 50],
                                    "color": "#164e63"
                                },
                                {
                                    "range": [50, 100],
                                    "color": "#7f1d1d"
                                }
                            ]
                        }
                    )
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

                # Prediction Result
                if prediction == 1:

                    st.error("⚠️ High churn risk")

                    st.write(
                        "This customer is predicted to churn."
                    )

                elif prediction == 0:

                    st.success("✅ Low churn risk")

                    st.write(
                        "This customer is predicted to stay."
                    )

                st.metric(
                    "Churn Probability",
                    f"{prob * 100:.2f}%"
                )

    except requests.exceptions.ConnectionError:

        st.error(
            "Backend connection failed. "
            "Please check whether the Flask API is running."
        )

    except requests.exceptions.Timeout:

        st.error(
            "Backend request timed out. Please try again."
        )

    except requests.exceptions.HTTPError as e:

        st.error(
            f"Backend HTTP error: {e}"
        )

        try:
            st.code(response.text)
        except Exception:
            pass

    except requests.exceptions.RequestException as e:

        st.error(
            f"API connection error: {e}"
        )

    except (ValueError, TypeError, KeyError) as e:

        st.error(
            f"Prediction response error: {e}"
        )
