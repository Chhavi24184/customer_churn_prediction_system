import streamlit as st
import pandas as pd
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
    margin-bottom: 18px;
}
.chart-card {
    background: #ffffff;
    padding: 20px;
    border-radius: 18px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 6px 20px rgba(15, 23, 42, 0.06);
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-header'>Analytics Intelligence Dashboard</h1>", unsafe_allow_html=True)

file = st.file_uploader("Upload dataset to initialize analysis", type=["csv"])

if file:
    with st.spinner("Generating intelligence reports..."):
        df = pd.read_csv(file)

        # ---------- KPI ----------
        total = len(df)
        churn = df["default"].sum()
        rate = churn / total * 100

        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Total Customers", f"{total:,}")
        with c2:
            st.metric("Churn Events", f"{churn:,}")
        with c3:
            st.metric("Global Churn Rate", f"{rate:.2f}%")

        st.markdown("<br>", unsafe_allow_html=True)

        # ---------- CHARTS ----------
        col_left, col_right = st.columns(2)

        with col_left:
            st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
            chart_data = df["default"].value_counts().reset_index()
            chart_data.columns = ["Status", "Count"]
            chart_data["Status"] = chart_data["Status"].map({0: "Retained", 1: "Churned"})
            
            fig1 = px.pie(
                chart_data, values="Count", names="Status",
                hole=0.6,
                color="Status",
                color_discrete_map={"Retained": "#22c55e", "Churned": "#ef4444"},
                title="<b>Customer Retention Overview</b>"
            )
            fig1.update_layout(
                paper_bgcolor='#ffffff',
                plot_bgcolor='#ffffff',
                template="plotly_white",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig1, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col_right:
            st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
            fig2 = px.histogram(
                df, x="tenure", nbins=30,
                color_discrete_sequence=["#22d3ee"],
                title="<b>Tenure Distribution</b>"
            )
            fig2.update_layout(
                paper_bgcolor='#ffffff',
                plot_bgcolor='#ffffff',
                template="plotly_white",
                xaxis_title="Months with Service",
                yaxis_title="Customer Count"
            )
            st.plotly_chart(fig2, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
        fig3 = px.box(
            df, x="default", y="monthly_charge",
            color="default",
            color_discrete_map={0: "#22c55e", 1: "#ef4444"},
            labels={"default": "Churn Status", "monthly_charge": "Monthly Charge ($)"},
            title="<b>Monthly Charge Correlation with Churn</b>"
        )
        fig3.update_layout(
            paper_bgcolor='#ffffff',
            plot_bgcolor='#ffffff',
            template="plotly_white"
        )
        st.plotly_chart(fig3, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # ---------- DOWNLOAD ----------
        csv = df.to_csv(index=False).encode()
        st.download_button(
            "📥 Export Full Intelligence Report",
            csv,
            "churn_analytics_report.csv",
            "text/csv",
            use_container_width=True
        )

else:
    st.info("👋 Please upload a customer dataset (CSV) to begin the analysis.")
    st.image("https://images.unsplash.com/photo-1551288049-bbbda540d3b9?auto=format&fit=crop&q=80&w=1000", caption="Global Churn Analytics")
