import streamlit as st
import pandas as pd
import plotly.express as px

from src.data_processing import load_and_clean
from src.model import train_model
from src.prediction import score_dataframe
from src.utils import risk_level
from reports.excel_report import generate_excel

# ─────────────────────────────────────────────
# Page Config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Employee Attrition Dashboard",
    layout="wide"
)

# ─────────────────────────────────────────────
# Load CSS
# ─────────────────────────────────────────────
with open("assets/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Sidebar (Controls)
# ─────────────────────────────────────────────
st.sidebar.title("⚙️ Controls")

st.sidebar.info("""
📌 Upload HR Dataset:
- Must include Attrition/Left column
- Accepts Yes/No, Resigned, Exit
- Missing columns handled automatically
""")

uploaded = st.sidebar.file_uploader("Upload CSV File")

# ─────────────────────────────────────────────
# Load Data
# ─────────────────────────────────────────────
try:
    if uploaded:
        df = load_and_clean(uploaded)
    else:
        df = load_and_clean("data/ibm_hr_data.csv")
except Exception as e:
    st.error("❌ Data Loading Failed")
    st.write(str(e))
    st.stop()

# ─────────────────────────────────────────────
# Dataset Preview Section
# ─────────────────────────────────────────────
st.title("👥 Employee Attrition Analytics Dashboard")

st.subheader("📂 Dataset Preview")
st.dataframe(df.head(), use_container_width=True)

st.subheader("📊 Columns Detected")
st.write(df.columns.tolist())

st.subheader("🎯 Attrition Distribution")
st.bar_chart(df['Left'].value_counts())

# ─────────────────────────────────────────────
# Train Model
# ─────────────────────────────────────────────
try:
    model, encoders, auc = train_model(df)
except Exception as e:
    st.error("❌ Model Training Failed")
    st.write(str(e))

    st.warning("""
Possible reasons:
- Dataset has only one class (all Yes or all No)
- Dataset not suitable for attrition prediction
""")
    st.stop()

# ─────────────────────────────────────────────
# Predictions
# ─────────────────────────────────────────────
df = score_dataframe(df, model, encoders)
df['RiskLevel'] = df['RiskScore'].apply(risk_level)

# ─────────────────────────────────────────────
# Tabs
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Overview", "🏢 Department", "📋 Risk Table", "📈 Insights"
])

# ─────────────────────────────────────────────
# TAB 1 — OVERVIEW
# ─────────────────────────────────────────────
with tab1:
    st.subheader("📊 Workforce Overview")

    total = len(df)
    left = df['Left'].sum()
    rate = round(left / total * 100, 1)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Employees", total)
    c2.metric("Employees Left", left)
    c3.metric("Attrition Rate", f"{rate}%")
    c4.metric("Model AUC", round(auc, 3))

    if 'Department' in df.columns:
        dept = df.groupby('Department')['Left'].mean().mul(100).reset_index()

        fig = px.bar(
            dept,
            x='Department',
            y='Left',
            color='Left',
            title="Attrition Rate by Department",
            color_continuous_scale='RdYlGn_r'
        )
        st.plotly_chart(fig, use_container_width=True)

# ─────────────────────────────────────────────
# TAB 2 — DEPARTMENT ANALYSIS
# ─────────────────────────────────────────────
with tab2:
    st.subheader("🏢 Department Insights")

    if 'Department' in df.columns and 'MonthlyIncome' in df.columns:
        fig = px.box(
            df,
            x='Department',
            y='MonthlyIncome',
            color='Department',
            title="Salary Distribution by Department"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Department or Salary data not available")

# ─────────────────────────────────────────────
# TAB 3 — RISK TABLE
# ─────────────────────────────────────────────
with tab3:
    st.subheader("📋 Employee Risk Table")

    risk_filter = st.multiselect(
        "Filter by Risk Level",
        ["High", "Medium", "Low"],
        default=["High", "Medium", "Low"],
        key="risk_filter_tab3"
    )

    df_filtered = df[df['RiskLevel'].isin(risk_filter)]

    display_cols = [col for col in ['Department', 'JobRole', 'RiskScore', 'RiskLevel'] if col in df.columns]

    df_display = df_filtered[display_cols].sort_values('RiskScore', ascending=False)

    st.dataframe(df_display, use_container_width=True)

    # 🔥 EXPORT BUTTON
    st.markdown("### 📥 Download Report")

    excel_file = generate_excel(df_display)

    st.download_button(
        label="⬇️ Download Excel Report",
        data=excel_file,
        file_name="attrition_report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
# ─────────────────────────────────────────────
# TAB 4 — INSIGHTS
# ─────────────────────────────────────────────
with tab4:
    st.subheader("📈 Advanced Insights")

    if 'Age' in df.columns:
        fig = px.histogram(
            df,
            x='Age',
            color='Left',
            title="Age Distribution vs Attrition"
        )
        st.plotly_chart(fig, use_container_width=True)

    if 'MonthlyIncome' in df.columns:
        fig2 = px.box(
            df,
            x='Left',
            y='MonthlyIncome',
            title="Salary vs Attrition"
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.info("💡 Insight: High attrition is often linked to overtime and low satisfaction.")