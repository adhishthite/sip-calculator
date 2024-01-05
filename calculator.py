"""
(c) 2024 Adhish Thite

This module contains functions to calculate the returns on investments.
"""

import pandas as pd


def calculate_sip_returns(
    annual_return, monthly_investment, total_years, interval_years
):
    """
    Calculate the returns on a SIP investment and return a dataframe.

    Parameters:
    annual_return (float): The annualized average return (in decimal form).
    monthly_investment (int): The amount invested per month.
    total_years (int): The total duration of the investment in years.
    interval_years (int): The interval in years for the dataframe.

    Returns:
    pd.DataFrame: A dataframe with the breakdown of investment, interest earned, and total returns.
    """
    compounding_frequency = 12  # Monthly compounding

    # Function to calculate future value of SIP
    def calculate_future_value(principal, rate, time, n):
        return principal * ((((1 + rate / n) ** (n * time)) - 1) / (rate / n))

    # Creating data for the DataFrame
    data = []
    for year in range(interval_years, total_years + 1, interval_years):
        total_investment = monthly_investment * compounding_frequency * year
        total_returns = calculate_future_value(
            monthly_investment, annual_return, year, compounding_frequency
        )
        interest_earned = total_returns - total_investment
        data.append([total_investment, interest_earned, total_returns])

    # Creating the DataFrame
    df = pd.DataFrame(
        data,
        columns=["Money Invested", "Interest Earned", "Total Returns"],
        index=range(interval_years, total_years + 1, interval_years),
    )
    df.index.name = "Year"

    return df
