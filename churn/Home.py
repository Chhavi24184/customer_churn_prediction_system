import streamlit as st

st.set_page_config(layout="wide")

# ---------- STYLE ----------
st.markdown("""
<style>
.stApp { background: linear-gradient(180deg, #f8fafc 0%, #eef2ff 100%); }
.card {
    background: #ffffff;
    padding: 40px 20px;
    border-radius: 20px;
    text-align: center;
    color: #0f172a;
    border: 1px solid #e2e8f0;
    box-shadow: 0 6px 20px rgba(15, 23, 42, 0.06);
    transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
    height: 100%;
}
.card:hover {
    transform: translateY(-6px);
    box-shadow: 0 10px 28px rgba(15, 23, 42, 0.10);
    border-color: #0ea5e9;
}
.metric-title {
    font-size: 14px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: #64748b;
    margin-bottom: 12px;
}
.metric-value {
    font-size: 46px;
    font-weight: 800;
    background: linear-gradient(90deg, #0ea5e9, #6366f1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.section-header {
    font-size: 26px;
    font-weight: 700;
    color: #0f172a;
    margin-top: 40px;
    margin-bottom: 24px;
    text-align: center;
}
div[data-testid="stPageLink"] a {
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    padding: 22px !important;
    border-radius: 14px !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 14px rgba(15, 23, 42, 0.06);
}
div[data-testid="stPageLink"] a:hover {
    border-color: #0ea5e9 !important;
    transform: translateY(-2px);
}
</style>
""", unsafe_allow_html=True)

# ---------- HERO ----------
st.markdown("""
<div style='padding-top: 40px; padding-bottom: 16px;'>
    <h1 style='text-align:center;
    background:linear-gradient(90deg,#0ea5e9,#6366f1);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    font-size:80px;
    font-weight:900;
    line-height: 1.05;
    margin-bottom: 8px;'>
    Churn Intelligence
    </h1>
    <p style='text-align:center; color:#334155; font-size:20px; font-weight:400; max-width: 820px; margin: 0 auto;'>
    Predict, analyze, and prevent customer attrition with a clean, professional interface.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------- KPI CARDS ----------
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
    <div class="card">
        <div class="metric-title">Model Accuracy</div>
        <div class="metric-value">90.5%</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="card">
        <div class="metric-title">Active Insights</div>
        <div class="metric-value">6.2k</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="card">
        <div class="metric-title">Engine Status</div>
        <div class="metric-value" style="color:#22c55e; -webkit-text-fill-color:#22c55e;">LIVE</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div class='section-header'>Explore Prediction Modules</div>", unsafe_allow_html=True)

# ---------- NAVIGATION ----------
b1, b2, b3 = st.columns(3)

with b1:
    st.page_link("pages/1_Predict.py", label="🔮 Individual Prediction Console", use_container_width=True)

with b2:
    st.page_link("pages/2_Analytics.py", label="📊 Global Analytics Dashboard", use_container_width=True)

with b3:
    st.page_link("pages/3_Bulk_Predict.py", label="📂 Bulk Processing Engine", use_container_width=True)

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#64748b; font-size:14px;'>Churn Intelligence Platform • Professional Light Theme</p>", unsafe_allow_html=True)
