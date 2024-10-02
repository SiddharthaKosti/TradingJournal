import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Trade Data Management", page_icon="💼", layout="wide",)

st.title("Trade Data Management")

st.write("""
Welcome to the Trade Data Management app! This application is designed to help you efficiently manage and analyze your trading data.

Here's what you can do with this app:

1. **Add and Edit Trades**: Easily input new trades or modify existing ones.
2. **View Trade Summaries**: Get a quick overview of your trading performance, including total profits, open trades, and more.
3. **Analyze Monthly Profits**: Visualize your profit trends over time with interactive graphs.
4. **Track Trade Bases**: See which trading strategies are performing best.

To get started, navigate to the 'Track Trades' page using the sidebar. There, you'll find detailed options for managing your trade data and viewing insightful analytics.

Happy trading!
""")

st.sidebar.success("Select a page above.")

# Create a simple line curve with text labels
st.subheader("Investment Growth Calculator")

col1, col2, col3 = st.columns(3)
initial_amount = col1.number_input("Initial Amount Investing (INR)", min_value=0, value=1000000, step=100000)
annual_profit_percent = col2.number_input("Annual Profit Target (%)", min_value=0, value=20, step=1)
years_to_project = col3.number_input("Number of Years", min_value=1, value=10, step=1)

years = []
amounts = []
amount = initial_amount
year = 0

while year < years_to_project:  
    years.append(year)
    amounts.append(amount)
    amount = amount * (1 + annual_profit_percent / 100)  # cumulative growth
    year += 1

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=years,
    y=[a/10000000 for a in amounts],  # Divide by 10000000 to convert to Crore
    mode='lines+markers+text',
    line=dict(color='#007ACC', width=3),  # Changed line color to a more vibrant blue
    marker=dict(size=10, color='#FFA500'),  # Changed marker color to a vibrant orange
    text=[f"{a/10000000:.2f}Cr" for a in amounts],
    textposition='top center'
))

st.divider()

st.subheader("Growth of Investment")

fig.update_layout(
    xaxis_title='Years',
    yaxis_title='Amount (INR) Crore',  # Updated y-axis title to show amount in Crore
    plot_bgcolor='rgb(255, 255, 255)',  # Changed background color to white for better contrast
    xaxis=dict(
        ticklen=4,
        zeroline=True,
        gridcolor='rgb(204, 204, 204)',
    ),
    yaxis=dict(
        ticklen=4,
        gridcolor='rgb(204, 204, 204)',
    ),
    height=600,  # Set height to be relative to the container to remove extra white space
    margin=dict(t=0),  # Removed top margin to remove extra white space
)

st.plotly_chart(fig)
