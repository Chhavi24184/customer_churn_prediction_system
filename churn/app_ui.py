import streamlit as st
import requests
import plotly.graph_objects as go

st.set_page_config(layout="wide")

st.markdown("""
<style>
body {
    background: linear-gradient(120deg,#0f172a,#020617);
}
.hero {
    text-align:center;
    font-size:48px;
    font-weight:800;
    background: linear-gradient(90deg,#22d3ee,#a78bfa);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}
.subtitle {
    text-align:center;
    color:#94a3b8;
    font-size:18px;
}
.glass {
    background: rgba(255,255,255,0.08);
    padding:35px;
    border-radius:20px;
    backdrop-filter: blur(14px);
    box-shadow:0 6px 40px rgba(0,0,0,0.5);
}
.btn {
    background: linear-gradient(90deg,#22d3ee,#a78bfa);
    color:white;
    padding:12px;
    border-radius:12px;
    text-align:center;
    font-weight:bold;
}
</style>
""", unsafe_allow_html=True)


st.markdown('<p class="hero">AI Customer Churn Intelligence</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Predict churn risk instantly using machine learning analytics</p>', unsafe_allow_html=True)

st.write("")

st.markdown('<div class="glass">', unsafe_allow_html=True)

c1, c2 = st.columns(2)

with c1:
    age = st.number_input("Age", 18, 80, 30)
    gender = st.selectbox("Gender", ["M","F"])
    income_numeric = st.selectbox("Income Level", [1,2,3])
    tenure = st.number_input("Tenure", 1, 30, 5)
    sub_plan = st.selectbox("Subscription Plan", ["basic","standard","premium"])

with c2:
    contract = st.selectbox("Contract", ["monthly","annual"])
    monthly_charge = st.number_input("Monthly Charge", 50, 500, 100)
    auto_renewal = st.selectbox("Auto Renewal", [0,1])
    late_payment = st.selectbox("Late Payment", [0,1])
    failed_transaction = st.selectbox("Failed Transaction", [0,1])

predict = st.button("Predict Churn", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)


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

    res = requests.post("http://127.0.0.1:5000/predict", json=data).json()
    prob = res["probability"]

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=prob*100,
        gauge={'axis':{'range':[0,100]},
               'bar':{'color':"#22d3ee"}}
    ))

    st.plotly_chart(fig, use_container_width=True)

    if res["prediction"] == 1:
        st.error("⚠️ High churn risk")
    else:
        st.success("✅ Low churn risk")
