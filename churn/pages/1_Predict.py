import streamlit as st
import requests
import plotly.graph_objects as go

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
    font-size: 60px;
    font-weight: 900;
    margin-bottom: 30px;
}
.predict-btn button {
    background: linear-gradient(90deg, #0ea5e9, #6366f1) !important;
    color: #ffffff !important;
    font-weight: 700 !important;
    border: none !important;
    padding: 14px !important;
    border-radius: 12px !important;
    font-size: 18px !important;
    transition: all 0.2s ease !important;
}
.predict-btn button:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 22px rgba(14, 165, 233, 0.25) !important;
}
.result-card {
    background: #ffffff;
    padding: 24px;
    border-radius: 18px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 6px 20px rgba(15, 23, 42, 0.06);
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-header'>Prediction Console</h1>", unsafe_allow_html=True)

with st.container():
    st.markdown("<div class='result-card'>", unsafe_allow_html=True)
    st.subheader("👤 Customer Profile Details")
    
    col1, col2 = st.columns(2)
    
    with col1:
        age = st.number_input("Age", 18, 80, 30)
        gender = st.selectbox("Gender", ["M", "F"])
        income_numeric = st.selectbox("Income Level", [1, 2, 3], help="1: Low, 2: Medium, 3: High")
        tenure = st.number_input("Tenure (Months)", 1, 120, 5)
        sub_plan = st.selectbox("Subscription Plan", ["basic", "standard", "premium"])
        
    with col2:
        contract = st.selectbox("Contract Type", ["monthly", "annual"])
        monthly_charge = st.number_input("Monthly Charge ($)", 10, 1000, 100)
        auto_renewal = st.selectbox("Auto Renewal", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
        late_payment = st.selectbox("Late Payment History", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
        failed_transaction = st.selectbox("Failed Transaction History", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")

    st.markdown("<div class='predict-btn'>", unsafe_allow_html=True)
    predict = st.button("Analyze Churn Risk", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ---------- RESULT ----------
if predict:
    with st.spinner("Processing customer profile through AI engine..."):
        payload = {
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
            res = requests.post("http://127.0.0.1:5000/predict", json=payload).json()
            
            if "prediction" not in res:
                st.error(f"API Error: {res}")
                st.stop()

            pred = res["prediction"]
            prob = res["probability"]

            st.markdown("<div class='result-card'>", unsafe_allow_html=True)
            st.subheader("🎯 Analysis Results")
            
            res_col1, res_col2 = st.columns([2, 1])
            
            with res_col1:
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=prob*100,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    gauge={
                        'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#94a3b8"},
                        'bar': {'color': "#22d3ee"},
                        'bgcolor': "rgba(0,0,0,0)",
                        'borderwidth': 2,
                        'bordercolor': "#334155",
                        'steps': [
                            {'range': [0, 30], 'color': 'rgba(34, 197, 94, 0.2)'},
                            {'range': [30, 70], 'color': 'rgba(234, 179, 8, 0.2)'},
                            {'range': [70, 100], 'color': 'rgba(239, 68, 68, 0.2)'}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 70
                        }
                    }
                ))
                fig.update_layout(
                    paper_bgcolor='#ffffff',
                    plot_bgcolor='#ffffff',
                    font={'color': "#0f172a", 'family': "Arial"},
                    height=300,
                    margin=dict(l=20, r=20, t=50, b=20)
                )
                st.plotly_chart(fig, use_container_width=True)

            with res_col2:
                st.markdown("<br><br>", unsafe_allow_html=True)
                if pred == 1:
                    st.markdown("""
                    <div style='background: #fff7f7; padding: 18px; border-radius: 14px; border: 1px solid #ef4444;'>
                        <h3 style='color: #ef4444; margin:0;'>⚠️ HIGH RISK</h3>
                        <p style='color: #0f172a; margin-top:10px;'>Customer shows strong patterns of potential churn.</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div style='background: #f6fff9; padding: 18px; border-radius: 14px; border: 1px solid #22c55e;'>
                        <h3 style='color: #22c55e; margin:0;'>✅ LOW RISK</h3>
                        <p style='color: #0f172a; margin-top:10px;'>Customer is likely to remain loyal to the service.</p>
                    </div>
                    """, unsafe_allow_html=True)
                
            st.markdown("</div>", unsafe_allow_html=True)
            st.balloons()

        except Exception as e:
            st.error(f"Connection Error: Ensure the prediction engine is running. ({str(e)})")
