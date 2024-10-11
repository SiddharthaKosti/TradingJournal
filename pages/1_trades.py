import streamlit as st
import pandas as pd
import os
from datetime import datetime
from pathlib import Path
import plotly.express as px
import sys

sys.path.append('..')
from src.trades_analysis.trade_summaries import trade_summaries
from src.trades_analysis.monthly_profit_graph import monthly_profit_graph
from src.trades_analysis.yearly_performance import yearly_performance
from src.trades_analysis.trade_data import trade_data

# Set page configuration with a custom theme
st.set_page_config(
    page_title="Track Trades",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS to improve the look and feel
st.markdown("""
    <style>
    .stApp {
        background-color: #f0f2f6;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #4e79a7;
        color: white;
        font-weight: bold;
        border-radius: 5px 5px 0 0;
    }
    .stTabs [aria-selected="true"] {
        background-color: #59a14f;
    }
    .stMetric {
        background-color: #87CEEB;  /* Changed to sky blue */
        padding: 15px;
        border-radius: 5px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    </style>
""", unsafe_allow_html=True)

csv_file = Path("trade_data.csv")
columns = [
    "script_name", "trade_base", "price_in", "quantity_in", "quantity_left", "date_in", 
    "amount_in", "balance_left", "date_out", "price_out",
    "P/L (INR)", "P/L in %", "days_taken"
]

# Check if CSV file exists
if os.path.exists(csv_file):
    # Read existing CSV file
    df = pd.read_csv(csv_file, parse_dates=["date_in", "date_out"])
    df = df[columns]
else:
    # Create an empty DataFrame if CSV doesn't exist
    df = pd.DataFrame(columns=columns)

# Streamlit app
st.title("📊 Trade Data Management")

# Create tabs with custom styling
tab1, tab2, tab3, tab4 = st.tabs(["📝 Add/Edit Trades", "📊 Trade Summaries", "📈 Monthly Profit Graph", ":chart: Yearly Performance"])

with tab1:
    trade_data(df, csv_file)

with tab2:
    trade_summaries(df)

with tab3:
    monthly_profit_graph(df)

with tab4:
    yearly_performance(df)