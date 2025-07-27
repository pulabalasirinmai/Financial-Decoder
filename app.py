import streamlit as st
import google.generativeai as genai
import pandas as pd
import os
import plotly.express as px
from dotenv import load_dotenv
from streamlit_extras.add_vertical_space import add_vertical_space

# Load API Key
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=API_KEY)

# Streamlit UI Configuration
st.set_page_config(page_title="💰 Gemini Pro Financial AI", page_icon="💰", layout="wide")

# Custom CSS for Styling & Animations
st.markdown("""
    <style>
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    .main-container {
        animation: fadeIn 1.5s ease-in;
        background-color: #0F172A;
        color: #E5E7EB;
        padding: 20px;
        border-radius: 15px;
    }
    .stButton>button {
        background-color: #1E3A8A;
        color: white;
        font-size: 18px;
        border-radius: 10px;
        padding: 12px;
    }
    .stButton>button:hover {
        background-color: #3282B8;
    }
    </style>
""", unsafe_allow_html=True)

# Header Section
st.markdown("<h1 style='text-align: center; color: #BBE1FA;'>💰 Gemini Pro Financial AI</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #E5E7EB;'>Smart AI for Financial Analysis</h3>", unsafe_allow_html=True)
add_vertical_space(2)

# File Upload Section
st.sidebar.markdown("### 📂 Upload Financial Report")
uploaded_file = st.sidebar.file_uploader("Browse Files (CSV)", type=["csv"])

# Content Display
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.markdown("### 🔍 Preview of Financial Report")
    st.dataframe(df.head())

    # Bar Chart - Financial Overview
    st.subheader("📊 Financial Overview")
    if len(df.columns) >= 2:
        fig = px.bar(df, x=df.columns[0], y=df.columns[1:], title="Revenue & Expenses", barmode="group", color_discrete_sequence=["#1E3A8A", "#3282B8"])
        st.plotly_chart(fig)
    else:
        st.warning("⚠ Not enough data for bar chart.")

    # Pie Chart - Financial Ratios
    st.subheader("📊 Financial Ratios")
    ratio_data = {'Category': ['Profit Margin', 'Debt-Equity', 'ROI'], 'Values': [20, 30, 50]}
    ratio_df = pd.DataFrame(ratio_data)
    fig2 = px.pie(ratio_df, values="Values", names="Category", title="Key Financial Ratios", color_discrete_sequence=["#3282B8", "#1E3A8A", "#BBE1FA"])
    st.plotly_chart(fig2)

    # AI Summary Button
    if st.button("🚀 Generate Summary"):
        with st.spinner("Analyzing with AI..."):
            prompt = f"""
            You are a financial analyst AI. Summarize this financial data and highlight key insights.
            Here is the data:
            {df.to_string()}
            """
            model = genai.GenerativeModel("gemini-pro")
            response = model.generate_content(prompt)
            st.subheader("📑 AI-Generated Summary:")
            st.success(response.text)
