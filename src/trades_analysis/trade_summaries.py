import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

# Define the styling function
def style_dataframe(df):
    # Normalize the values for consistent color gradient across all rows
    profit_normalized = (df['P/L (INR)'] - df['P/L (INR)'].min()) / (df['P/L (INR)'].max() - df['P/L (INR)'].min())
    percent_normalized = (df['P/L in %'] - df['P/L in %'].min()) / (df['P/L in %'].max() - df['P/L in %'].min())
    
    return df.style.apply(lambda x: [f'background-color: rgba(50, 205, 50, {v})' for v in profit_normalized], 
                        subset=['P/L (INR)'])\
                .apply(lambda x: [f'background-color: rgba(124, 252, 0, {v})' for v in percent_normalized], 
                        subset=['P/L in %'])\
                .format({
                    'P/L (INR)': '{:,.2f}',
                    'P/L in %': '{:.2f}%',
                    'price_in': '{:.2f}',
                    'price_out': '{:.2f}'
                })


def trade_summaries(df, initial_amount):
    st.subheader("Trade Summaries")

    # Calculate and display summaries
    total_trades = len(df)
    open_trades = df[df["quantity_left"] > 0].shape[0]
    closed_trades = total_trades - open_trades
    partially_booked_trades = df[(df["quantity_left"] > 0) & (df["quantity_left"] < df["quantity_in"])].shape[0]
    total_profit_loss = df["P/L (INR)"].sum()
    total_balance_left = df["balance_left"].sum()
    total_amount_in = df["amount_in"].sum()
    profit_loss_percent_balance = (total_profit_loss / total_balance_left) * 100 if total_balance_left != 0 else 0
    profit_loss_percent_circulated = (total_profit_loss / total_amount_in) * 100 if total_amount_in != 0 else 0
    profit_loss_percent_invested = (total_profit_loss/initial_amount) * 100

    # Calculate profit booked for each trade base
    trade_base_profits = df.groupby("trade_base").agg({
        "P/L (INR)": "sum",
        "script_name": "count"
    }).sort_values("P/L (INR)", ascending=False)

    col1, col2, col3, col4 = st.columns([1.2, 1.5, 2, 2])
    with col1:
        st.metric("Total Trades", total_trades, delta=None, delta_color="off")
        st.metric("Open Trades", open_trades, delta=None, delta_color="off")
        st.metric("Closed Trades", closed_trades, delta=None, delta_color="off")
        st.metric("Partially Booked Trades", partially_booked_trades, delta=None, delta_color="off")

    with col2:
        top_4_trade_base_count = df[~df['trade_base'].isin(['AVG', 'LONG'])]['trade_base'].value_counts().nlargest(4)
        open_trades_by_base = df[(df["quantity_left"] > 0) & (~df['trade_base'].isin(['AVG', 'LONG']))]['trade_base'].value_counts()
        for base, count in top_4_trade_base_count.items():
            open_count = open_trades_by_base.get(base, 0)
            st.metric(f"{base}", f"{count} ({open_count} open)", delta=None, delta_color="off")

    with col3:
        # st.subheader("Top 4 Profitable Trade Bases")
        for base, row in trade_base_profits.head(4).iterrows():
            st.metric(f"{base} ({int(row['script_name'])} trades)", f"₹{row['P/L (INR)']:.2f}", delta=None, delta_color="off")

    with col4:
        st.metric("Total investement", f"₹{initial_amount}", delta=None, delta_color="normal")
        st.metric("P/L", f"{profit_loss_percent_invested:.2f}% (₹{total_profit_loss:.2f})", delta=None, delta_color="normal")
        st.metric("P/L % (Current Invested)", f"{profit_loss_percent_balance:.2f}% (₹{total_balance_left/100000:.2f}L)", delta=None, delta_color="normal")
        st.metric("P/L % (Circulated)", f"{profit_loss_percent_circulated:.2f}% (₹{total_amount_in/100000:.2f}L)", delta=None, delta_color="normal")
        # st.metric("Avg P/L %", f"{avg_profit_loss_percent:.2f}%", delta=None, delta_color="normal")

    st.divider()
    # Display top profitable trades by amount and percentage with variable input
    st.header("Top Profitable trades")
    num_trades_to_display = st.number_input("Number of Trades to Display", min_value=1, value=5)
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("By Amount")
        top_by_amount = df.groupby("script_name").agg({
            "P/L (INR)": "sum",
            "P/L in %": "mean",
            "price_in": "mean",
            "price_out": "mean"
        }).nlargest(num_trades_to_display, "P/L (INR)")
        styled_df_amount = top_by_amount.reset_index()

        # Apply styling and display
        st.dataframe(
            style_dataframe(styled_df_amount),
            use_container_width=True
        )


    with col2:
        st.subheader("By Percentage")
        top_by_percentage = df.groupby("script_name").agg({
            "P/L (INR)": "sum",
            "P/L in %": "mean",
            "price_in": "mean",
            "price_out": "mean"
        }).nlargest(num_trades_to_display, "P/L in %")
        styled_df_percentage = top_by_percentage.reset_index()
        # Apply styling and display
        st.dataframe(
            style_dataframe(styled_df_percentage),
            use_container_width=True
        )

    st.divider()
    # Display top fastest and slowest trades with user input for number of trades
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Top Fastest Trades")
        num_fastest_trades = st.number_input("Number of Fastest Trades to Display", min_value=1, value=5)
        top_by_fastest = df[df["days_taken"] > 0].nsmallest(num_fastest_trades, "days_taken")[["script_name", "days_taken", "P/L (INR)", "P/L in %", "price_in", "price_out", "trade_base"]]
        st.dataframe(style_dataframe(top_by_fastest), use_container_width=True)

    with col2:
        st.subheader("Top Slowest Trades")
        num_slowest_trades = st.number_input("Number of Slowest Trades to Display", min_value=1, value=5)
        top_by_slowest = df[df["days_taken"] > 0].nlargest(num_slowest_trades, "days_taken")[["script_name", "days_taken", "P/L (INR)", "P/L in %", "price_in", "price_out", "trade_base"]]
        st.dataframe(style_dataframe(top_by_slowest), use_container_width=True)

    st.divider()
    st.header("Recently booked trades")
    num_recent_trades = st.number_input("Number of Recent Trades to Display", min_value=1, value=5)
    df_recent = df[df["date_out"].notna()]
    df_recent = df_recent.sort_values(by=["date_out"], ascending=False)
    st.dataframe(style_dataframe(df_recent[["script_name", "price_in", "price_out", "P/L (INR)", "P/L in %", "days_taken", "date_out"]].head(num_recent_trades)), use_container_width=True)