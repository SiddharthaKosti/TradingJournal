import pandas as pd
import streamlit as st
from pathlib import Path
import os

def trade_data(df, csv_file):
    # Function to calculate derived columns
    def calculate_derived_columns(df):
        # Convert date_in and date_out to datetime if they're not already
        df['date_in'] = pd.to_datetime(df['date_in'], format='%d/%m', errors='coerce')
        df['date_out'] = pd.to_datetime(df['date_out'], format='%d/%m', errors='coerce')
        df["amount_in"] = df["price_in"] * df["quantity_in"]
        df["balance_left"] = df["price_in"] * df["quantity_left"]
        df["P/L (INR)"] = (df["price_out"] - df["price_in"]) * (df["quantity_in"] - df["quantity_left"])
        df["P/L in %"] = df.apply(lambda row: 0 if pd.isna(row["price_out"]) else 
                                        ((row["price_out"] - row["price_in"]) / row["price_in"]) * 100, axis=1)
        df["days_taken"] = df.apply(lambda row: 0 if pd.isna(row["date_out"]) or pd.isna(row["date_in"]) else 
                                    (row["date_out"] - row["date_in"]).days, axis=1)
        return df
    
    st.subheader("Amount Invested")
    
    initial_amount = st.number_input("Initial Amount Invested (INR)", min_value=0, value=1000000)
    st.metric("Initial Amount Invested", f"₹{initial_amount}", delta=None, delta_color="off")

    st.divider()
    st.subheader("Add/Edit Data")

    edited_df = st.data_editor(
        df,
        # hide_index=True,
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "trade_base": st.column_config.TextColumn(width="small"),
            "price_in": st.column_config.NumberColumn(width="small", format="₹%.2f"),
            "quantity_in": st.column_config.NumberColumn(width="small"),
            "amount_in": st.column_config.NumberColumn(width="small", format="₹%.2f"),
            "quantity_left": st.column_config.NumberColumn(width="small"),
            "balance_left": st.column_config.NumberColumn(width="small", format="₹%.2f"),
            "date_in": st.column_config.DateColumn(width="small"),
            "date_out": st.column_config.DateColumn(width="small"),
            "price_out": st.column_config.NumberColumn(width="small", format="₹%.2f"),
            "P/L (INR)": st.column_config.NumberColumn(width="small", format="₹%.2f"),
            "P/L in %": st.column_config.NumberColumn(width="small", format="%.2f%%"),
            "days_taken": st.column_config.NumberColumn(width="small"),
        }
    )

    def highlight_survived(df):
        if df["quantity_left"] == 0:
            return ['background-color: #8ef05d']*len(df)
        elif df["quantity_left"] < df["quantity_in"]:
            return ['background-color: lightblue']*len(df)
        else:
            return ['background-color: pink']*len(df)


    if st.button("Save Data", key="save_button"):
        edited_df = calculate_derived_columns(edited_df)
        edited_df.to_csv(csv_file, index=False)
        st.success("Data saved successfully!")

    st.divider()
    st.write(":green-background[**Fully Booked**]", ":blue-background[**Partially Booked**]", ":red-background[**Not Booked**]")
    edited_df['date_in'] = pd.to_datetime(edited_df['date_in']).dt.date
    edited_df['date_out'] = pd.to_datetime(edited_df['date_out']).dt.date
    edited_df["price_in"] = edited_df["price_in"].apply(lambda x: round(x,2))
    edited_df["price_out"] = edited_df["price_out"].apply(lambda x: round(x,2))
    st.dataframe(edited_df.style.apply(highlight_survived, axis=1), use_container_width=True)

    return initial_amount
