import pandas as pd
import plotly.graph_objects as go
import streamlit as st

def monthly_profit_graph(df):
    st.subheader("Profit Analysis")

    # Add a dropdown to select the period
    period = st.selectbox("Select Period", ["Monthly", "Quarterly"])

    # Prepare data for profit graph
    df['date_out'] = pd.to_datetime(df['date_out'])
    if period == "Monthly":
        df['period'] = df['date_out'].dt.to_period('M')
    elif period == "Quarterly":
        df['period'] = df['date_out'].dt.to_period('Q')
    profits = df.groupby('period')['P/L (INR)'].sum().reset_index()
    profits['period'] = profits['period'].astype(str)

    # Calculate cumulative sum for the curve
    profits['cumulative_profit'] = profits['P/L (INR)'].cumsum()

    # Create the graph using Plotly Graph Objects
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=profits['period'],
        y=profits['P/L (INR)'],
        name='P/L',
        text=profits['P/L (INR)'].apply(lambda x: f'₹{x:.2f}'),
        textposition='inside',
        marker_color=profits['P/L (INR)'].apply(lambda x: '#4CAF50' if x >= 0 else '#F44336')
    ))

    fig.add_trace(go.Scatter(
        x=profits['period'],
        y=profits['cumulative_profit'],
        name='Cumulative P/L',
        mode='lines+markers+text',
        line=dict(color='#FFA500', width=3),
        marker=dict(size=8),
        text=profits['cumulative_profit'].apply(lambda x: f'₹{x:.2f}'),
        textposition='top center'
    ))

    fig.update_layout(
        xaxis_title='Period',
        yaxis_title='P/L (INR)',
        xaxis_tickangle=-45,
        height=650,
        margin=dict(t=100),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#2c3e50', size=18),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#e0e0e0')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#e0e0e0')

    st.plotly_chart(fig, use_container_width=True)

    st.divider()
    # Number of trades entered graph
    st.subheader("Trades Entered: Total/Open/Booked")

    # Prepare data for number of trades entered graph
    df['date_in'] = pd.to_datetime(df['date_in'])
    if period == "Monthly":
        df['month_in'] = df['date_in'].dt.to_period('M')
    elif period == "Quarterly":
        df['month_in'] = df['date_in'].dt.to_period('Q')
    monthly_trades = df.groupby('month_in').size().reset_index(name='total_trades')
    monthly_trades['month_in'] = monthly_trades['month_in'].astype(str)

    # Prepare data for number of trades still open
    open_trades_df = df[df["quantity_left"] > 0]
    open_trades_df['date_in'] = pd.to_datetime(open_trades_df['date_in'])
    if period == "Monthly":
        open_trades_df['month_in'] = open_trades_df['date_in'].dt.to_period('M')
    elif period == "Quarterly":
        open_trades_df['month_in'] = open_trades_df['date_in'].dt.to_period('Q')
    monthly_open_trades = open_trades_df.groupby('month_in').size().reset_index(name='open_trades')
    monthly_open_trades['month_in'] = monthly_open_trades['month_in'].astype(str)

    # Prepare data for number of trades booked in a month
    booked_trades_df = df.copy()
    booked_trades_df['date_out'] = pd.to_datetime(booked_trades_df['date_out'])
    if period == "Monthly":
        booked_trades_df['month_out'] = booked_trades_df['date_out'].dt.to_period('M')
    elif period == "Quarterly":
        booked_trades_df['month_out'] = booked_trades_df['date_out'].dt.to_period('Q')
    monthly_booked_trades = booked_trades_df.groupby('month_out').size().reset_index(name='booked_trades')
    monthly_booked_trades['month_out'] = monthly_booked_trades['month_out'].astype(str)

    # Merge the three dataframes to have total trades, open trades, and booked trades in the same dataframe
    merged_df = pd.merge(pd.merge(monthly_trades, monthly_open_trades, on='month_in', how='left'), monthly_booked_trades, left_on='month_in', right_on='month_out', how='left')
    merged_df['open_trades'].fillna(0, inplace=True)  # Fill NaN with 0 for open trades
    merged_df['booked_trades'].fillna(0, inplace=True)  # Fill NaN with 0 for booked trades

    # Calculate cumulative sum for the curve
    merged_df['cumulative_total_trades'] = merged_df['total_trades'].cumsum()
    merged_df['cumulative_open_trades'] = merged_df['open_trades'].cumsum()
    merged_df['cumulative_booked_trades'] = merged_df['booked_trades'].cumsum()

    # Create the graph using Plotly Graph Objects
    fig_trades = go.Figure()
    fig_trades.add_trace(go.Bar(
        x=merged_df['month_in'],
        y=merged_df['total_trades'],
        name='Total Trades',
        text=merged_df['total_trades'],
        textposition='inside',
        marker_color='#3366cc'
    ))

    fig_trades.add_trace(go.Bar(
        x=merged_df['month_in'],
        y=merged_df['open_trades'],
        name='Open Trades',
        text=merged_df['open_trades'],
        textposition='inside',
        marker_color='#FF6347'
    ))

    fig_trades.add_trace(go.Bar(
        x=merged_df['month_in'],
        y=merged_df['booked_trades'],
        name='Booked Trades',
        text=merged_df['booked_trades'],
        textposition='inside',
        marker_color='#4CAF50'
    ))

    fig_trades.update_layout(
        xaxis_title='Month',
        yaxis_title='Number of Trades',
        xaxis_tickangle=-45,
        height=650,
        margin=dict(t=100),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#2c3e50', size=18),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    fig_trades.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#e0e0e0')
    fig_trades.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#e0e0e0')

    st.plotly_chart(fig_trades, use_container_width=True)
