import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from scipy.stats import norm

# --- Black-Scholes Formula ---
def black_scholes(S, K, T, r, sigma, option_type='call'):
    d1 = (np.log(S/K) + (r + 0.5 * sigma**2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    if option_type == 'call':
        return S * norm.cdf(d1) - K * np.exp(-r*T)*norm.cdf(d2)
    else:
        return K * np.exp(-r*T)*norm.cdf(-d2) - S * norm.cdf(-d1)

# --- Greeks ---
def delta(S, K, T, r, sigma, option_type='call'):
    d1 = (np.log(S/K) + (r + 0.5 * sigma**2)*T) / (sigma*np.sqrt(T))
    return norm.cdf(d1) if option_type == 'call' else norm.cdf(d1) - 1

def gamma(S, K, T, r, sigma):
    d1 = (np.log(S/K) + (r + 0.5 * sigma**2)*T) / (sigma*np.sqrt(T))
    return norm.pdf(d1) / (S * sigma * np.sqrt(T))

def vega(S, K, T, r, sigma):
    d1 = (np.log(S/K) + (r + 0.5 * sigma**2)*T) / (sigma*np.sqrt(T))
    return S * norm.pdf(d1) * np.sqrt(T) / 100

def theta(S, K, T, r, sigma, option_type='call'):
    d1 = (np.log(S/K) + (r + 0.5 * sigma**2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    term1 = - (S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T))
    if option_type == 'call':
        term2 = r * K * np.exp(-r*T) * norm.cdf(d2)
        return (term1 - term2) / 365
    else:
        term2 = r * K * np.exp(-r*T) * norm.cdf(-d2)
        return (term1 + term2) / 365

def rho(S, K, T, r, sigma, option_type='call'):
    d2 = (np.log(S/K) + (r - 0.5 * sigma**2)*T) / (sigma*np.sqrt(T))
    factor = K * T * np.exp(-r*T) / 100
    return factor * (norm.cdf(d2) if option_type == 'call' else -norm.cdf(-d2))

# --- App Layout ---
st.set_page_config(page_title="Black-Scholes Visualizer", layout="wide")
st.markdown("<h1 style='text-align: left;'>Black-Scholes Option Pricer & Greeks Visualizer</h1>", unsafe_allow_html=True)

# Sidebar Inputs
st.sidebar.title("Model Parameters")
S = st.sidebar.number_input("Current Asset Price", 1.0, 10000.0, 100.0)
K = st.sidebar.number_input("Strike Price", 1.0, 10000.0, 100.0)
T = st.sidebar.number_input("Time to Maturity (Years)", 0.01, 10.0, 1.0)
sigma = st.sidebar.number_input("Volatility", min_value=0.01, step=0.01)
r = st.sidebar.number_input("Risk-Free Rate", min_value=0.0, step=0.005)

# Centered Table of Parameters
st.markdown("<h3 style='text-align: left;'>Display Table</h3>", unsafe_allow_html=True)
st.markdown(f"""
<div style='text-align: center;'>
<table style='margin: auto; border-spacing: 15px; font-size: 16px;'>
<tr><th>Current Asset Price</th><th>Strike Price</th><th>Time to Maturity</th><th>Volatility</th><th>Risk-Free Rate</th></tr>
<tr>
<td>{S:.2f}</td><td>{K:.2f}</td><td>{T:.2f}</td><td>{sigma:.2f}</td><td>{r:.2f}</td>
</tr></table></div>
""", unsafe_allow_html=True)

# Option Price Cards
call_value = black_scholes(S, K, T, r, sigma, 'call')
put_value = black_scholes(S, K, T, r, sigma, 'put')

st.markdown("<h3 style='text-align: left;'>Option Prices</h3>", unsafe_allow_html=True)
st.markdown(f"""
<div style='display: flex; justify-content: center; gap: 60px;'>
  <div style="background-color: #929591; padding: 30px 50px; border-radius: 15px; border: 2px solid #3399ff; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);">
    <h4 style="text-align: center; margin: 0;">CALL Option Value</h4>
    <h2 style="text-align: center; color: #007acc;">${call_value:.2f}</h2>
  </div>
  <div style="background-color: #929591; padding: 30px 50px; border-radius: 15px; border: 2px solid #ff9933; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);">
    <h4 style="text-align: center; margin: 0;">PUT Option Value</h4>
    <h2 style="text-align: center; color: #ff6600;">${put_value:.2f}</h2>
  </div>
</div>
""", unsafe_allow_html=True)

# Heatmaps
toggle_greek = st.sidebar.radio("Greek to Visualize", ['Delta', 'Gamma', 'Vega', 'Theta', 'Rho'])
option_type = st.sidebar.radio("Option Type for Greek", ['call', 'put'])
S_min = st.sidebar.slider('Min Spot Price', 50.0, 200.0, 80.0)
S_max = st.sidebar.slider('Max Spot Price', 50.0, 200.0, 120.0)
sigma_min = st.sidebar.slider('Min Volatility', 0.05, 1.0, 0.1)
sigma_max = st.sidebar.slider('Max Volatility', 0.05, 1.0, 0.4)

spot_prices = np.linspace(S_min, S_max, 10)
volatilities = np.linspace(sigma_min, sigma_max, 10)

call_prices = np.zeros((len(volatilities), len(spot_prices)))
put_prices = np.zeros_like(call_prices)

for i, vol in enumerate(volatilities):
    for j, s in enumerate(spot_prices):
        call_prices[i, j] = black_scholes(s, K, T, r, vol, 'call')
        put_prices[i, j] = black_scholes(s, K, T, r, vol, 'put')

def plot_heatmap(z, title):
    annotations = [[f"{price:.2f}" for price in row] for row in z]
    fig = go.Figure(data=go.Heatmap(
        z=z, x=spot_prices, y=volatilities, colorscale=[[0, 'red'], [1, 'green']], zsmooth=False,
        text=annotations, texttemplate="%{text}", colorbar=dict(title="Price")
    ))
    fig.update_layout(title=title, xaxis_title="Spot Price", yaxis_title="Volatility",
                      width=500, height=500)
    return fig

st.markdown("<h3 style='text-align: left;'>Option Price Heatmaps</h3>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(plot_heatmap(call_prices, "CALL Option Heatmap"), use_container_width=True)
with col2:
    st.plotly_chart(plot_heatmap(put_prices, "PUT Option Heatmap"), use_container_width=True)

# Greek Chart
st.markdown(f"<h3 style='text-align: left;'>{toggle_greek} vs Spot Price ({option_type.upper()} Option)</h3>", unsafe_allow_html=True)
greek_spot_range = np.linspace(S_min, S_max, 100)

if toggle_greek == 'Delta':
    y_vals = [delta(s, K, T, r, sigma, option_type) for s in greek_spot_range]
elif toggle_greek == 'Gamma':
    y_vals = [gamma(s, K, T, r, sigma) for s in greek_spot_range]
elif toggle_greek == 'Vega':
    y_vals = [vega(s, K, T, r, sigma) for s in greek_spot_range]
elif toggle_greek == 'Theta':
    y_vals = [theta(s, K, T, r, sigma, option_type) for s in greek_spot_range]
elif toggle_greek == 'Rho':
    y_vals = [rho(s, K, T, r, sigma, option_type) for s in greek_spot_range]

greek_fig = go.Figure()
greek_fig.add_trace(go.Scatter(x=greek_spot_range, y=y_vals, mode='lines', name=toggle_greek))
greek_fig.update_layout(title=f"{toggle_greek} vs Spot Price", xaxis_title="Spot Price", yaxis_title=f"{toggle_greek} Value", width=1000, height=500)
st.plotly_chart(greek_fig)

# Interpretation Guide Table
st.markdown("<h3 style='text-align: left;'>Interpretation Guide</h3>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center;'>
<table style='margin: auto; border-collapse: collapse; font-size: 16px;'>
<tr style='background-color: #929591;'><th>Category</th><th>Description</th></tr>
<tr><td>Red to Green</td><td>Represents lower to higher option prices in the heatmap.</td></tr>
<tr><td>Volatility: Low (0.05–0.15)</td><td>Stable environments, options are cheaper.</td></tr>
<tr><td>Volatility: Medium (0.15–0.3)</td><td>Options more sensitive to Vega, moderate pricing.</td></tr>
<tr><td>Volatility: High (0.3–1.0)</td><td>Expensive options, Gamma becomes significant.</td></tr>
<tr><td>Delta</td><td>Measures sensitivity of option value to underlying asset price.</td></tr>
<tr><td>Gamma</td><td>Rate of change of Delta with asset price. Impacts hedging.</td></tr>
<tr><td>Vega</td><td>Sensitivity to volatility. Increases with time and moneyness.</td></tr>
<tr><td>Theta</td><td>Time decay. Value lost each day, especially near expiry.</td></tr>
<tr><td>Rho</td><td>Sensitivity to interest rate changes. More relevant for long-dated options.</td></tr>
</table>
</div>
""", unsafe_allow_html=True)

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("**Created by [Hassan Khalid](https://www.linkedin.com/in/hassan-khalid-160b36280/)**")





