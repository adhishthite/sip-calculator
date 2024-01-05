"""
(c) 2024 Adhish Thite

This module creates a UI using Streamlit to calculate the returns on investments.
"""

import streamlit as st
import plotly.graph_objects as go

import components
from calculator import calculate_sip_returns

currency = "₹"  # Indian Rupee

# Streamlit page configuration
st.set_page_config(
    layout="wide",
    page_title="SIP Return Calculator",
    page_icon="💰",
    menu_items={
        "About": "A simple calculator to calculate the returns on your SIP investments."
        "Made with ❤️ by [Adhish](https://linkedin.com/in/adhish-thite) in Pune 🇮🇳\n\n"
    },
)

# Streamlit UI components
st.markdown(
    components.title,
    unsafe_allow_html=True,
)

# Inputs in a single line using the beta_columns functionality for a better layout
col1, col2, col3, col4 = st.columns(4)
with col1:
    annual_return = st.number_input(
        "Annual Return (in %)", min_value=2.0, max_value=40.0, value=12.0, step=0.10
    )
with col2:
    monthly_investment = st.number_input(
        f"Monthly Investment ({currency})",
        min_value=500,
        max_value=100000000,
        value=1000,
        step=500,
    )
with col3:
    total_years = st.number_input(
        "Total Years", min_value=1, max_value=40, value=10, step=1
    )
with col4:
    interval_years = st.number_input(
        "Interval Years", min_value=1, max_value=5, value=2, step=1
    )

# Separator
st.markdown("---")

# Dynamic calculation without a button
auto_update = st.checkbox("Auto-update on input change")

if auto_update:
    df = calculate_sip_returns(
        annual_return / 100, monthly_investment, total_years, interval_years
    )

    # Round the specified columns to two decimal places
    df["Money Invested"] = df["Money Invested"].apply(lambda x: f"{currency} {x:,.2f}")
    df["Interest Earned"] = df["Interest Earned"].apply(
        lambda x: f"{currency} {x:,.2f}"
    )
    df["Total Returns"] = df["Total Returns"].apply(lambda x: f"{currency} {x:,.2f}")

    # Reset the index to turn the 'Year' index into a column
    df_reset = df.reset_index()

    # Create Plotly Table
    fig = go.Figure(
        data=[
            go.Table(
                header=dict(
                    values=list(df_reset.columns),
                    align="center",  # Center align header
                    font=dict(size=20),  # Increase font size for header
                    height=50,  # Increase height for header row to enhance vertical centering
                ),
                cells=dict(
                    values=[df_reset[col] for col in df_reset.columns],
                    align="center",  # Center align cells
                    font=dict(size=18),  # Increase font size for cells
                    height=50,  # Increase height for each row to enhance vertical centering
                ),
            )
        ]
    )

    # Update layout for a full-width table
    fig.update_layout(width=None, margin=dict(l=5, r=5, b=10, t=10))

    # Display Plotly Table in Streamlit
    st.plotly_chart(fig, use_container_width=True)
