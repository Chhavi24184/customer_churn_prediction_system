import streamlit as st
import plotly.graph_objects as go

st.set_page_config(layout="wide")

st.title("Prediction Result Dashboard")

# ----- Check if prediction exists -----
if "prediction" not in st.session_state or "probability" not in st.session_state:
    st.warning("Please run prediction first from the Prediction page.")
    st.stop()

# ----- Get values -----
pred = st.session_state["prediction"]
prob = st.session_state["probability"]

# ----- KPI -----
c1, c2 = st.columns(2)
c1.metric("Prediction Probability", f"{prob:.2f}")
c2.metric("Churn Risk", "HIGH" if pred == 1 else "LOW")

# ----- Gauge Chart -----
fig = go.Figure(go.Indicator(
    mode="gauge+number",
    value=prob * 100,
    title={'text': "Churn Probability (%)"},
    gauge={
        'axis': {'range': [0, 100]},
        'steps': [
            {'range': [0, 40], 'color': "green"},
            {'range': [40, 70], 'color': "orange"},
            {'range': [70, 100], 'color': "red"}
        ]
    }
))

st.plotly_chart(fig, use_container_width=True)

# ----- Recommendation -----
st.subheader("Recommended Action")

if pred == 1:
    st.error("High churn risk detected. Offer retention benefits or targeted engagement.")
else:
    st.success("Customer likely to stay. Maintain engagement and loyalty programs.")
