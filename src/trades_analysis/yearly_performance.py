import pandas as pd
import plotly.express as px
import streamlit as st

def yearly_performance(df):
    st.subheader("Yearly Profit Performance")

    # Prepare data for yearly performance graph
    df['date_out'] = pd.to_datetime(df['date_out'])
    df['year'] = df['date_out'].dt.year
    yearly_profits = df.groupby('year')['P/L (INR)'].sum().reset_index()

    # Create the graph using Plotly Express
    fig_yearly = px.bar(yearly_profits, x='year', y='P/L (INR)', text='P/L (INR)')
    fig_yearly.update_traces(texttemplate='%{text:.2s}', textposition='inside')

    fig_yearly.update_layout(
        xaxis_title='Year',
        yaxis_title='P/L (INR)',
        xaxis_tickangle=-45,
        height=650,
        margin=dict(t=100),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#2c3e50', size=18),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    fig_yearly.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#e0e0e0')
    fig_yearly.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#e0e0e0')

    st.plotly_chart(fig_yearly, use_container_width=True)
