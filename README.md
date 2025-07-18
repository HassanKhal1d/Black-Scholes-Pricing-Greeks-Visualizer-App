# Black-Scholes-Pricing-Greeks-Visualizer-App
An interactive options pricing web app that uses the Black-Scholes Model to calculate and visualize European Call and Put option prices. Built using Python and Streamlit, the app includes dynamic heatmaps, a Greeks visualizer, and a structured interpretation guide.


# Overview

This application allows users to:
Calculate European Call and Put option prices using the Black-Scholes formula.
Visualize the option Greeks (Delta, Gamma, Vega, Theta, Rho).
Display heatmaps of option prices across spot prices and volatilities.
Toggle between Call and Put views for both pricing and Greeks.
Interpret behavior across volatility regimes through a structured table.
View a clean summary of model parameters and computed results.

# Features

Model Parameters Table:
Displays key input values such as:
Spot Price (S),
Strike Price (K),
Time to Maturity (T),
Volatility (σ) &
Risk-Free Rate (r).

The table is styled for clarity and shown above the pricing output.

Option Pricing:
Call and Put prices are calculated using the Black-Scholes Model.
Displayed in visually distinct containers.
Updated instantly with user inputs.

Heatmaps:
Illustrate how option prices vary with spot price and volatility.
Larger square format for easier comparison.
Green indicates higher option value, red indicates lower option value.
Includes interpretations for different volatility regimes (low, moderate, high).

Greeks Visualizer:
Plots Delta, Gamma, Vega, Theta, and Rho as functions of the spot price.
Toggle switch to switch between Call and Put options.
Crosshair line highlights the Strike Price.
Explanation table details what each Greek measures and its significance.

Technologies Used:
Python 3,
Streamlit,
NumPy,
SciPy,
Pandas &
Plotly.
