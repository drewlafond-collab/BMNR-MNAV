import streamlit as st
import yfinance as yf
import pandas as pd
import time

# --- BMNR DATA (Dec 20, 2025) ---
SHARES = 421_500_000
CASH = 1_000_000_000
DEBT = 0
BTC_HELD = 193
ETH_HELD = 3_967_210  # "etc tokens"
EIGHT_STOCK_VALUE = 38_000_000

# Set up the web page
st.set_page_config(page_title="BMNR mNAV Tracker", page_icon="📈", layout="centered")

# Auto-refresh logic (reruns the script every 60 seconds)
refresh_rate = 60
st.empty() # Placeholder for refresh logic

st.title("🕷️ Bitmine (BMNR) mNAV Tracker")
st.markdown(f"**Last Updated:** {time.strftime('%H:%M:%S')}")

try:
    # 1. Fetch live market prices
    with st.spinner('Fetching live market data...'):
        bmnr_price = yf.Ticker("BMNR").fast_info.last_price
        eth_price = yf.Ticker("ETH-USD").fast_info.last_price
        btc_price = yf.Ticker("BTC-USD").fast_info.last_price

    # 2. Portfolio Value Calculations
    val_eth = ETH_HELD * eth_price
    val_btc = BTC_HELD * btc_price
    total_nav = val_eth + val_btc + CASH + EIGHT_STOCK_VALUE
    market_cap = bmnr_price * SHARES
    mnav = market_cap / total_nav

    # 3. Web Dashboard Layout
    col1, col2 = st.columns(2)
    col1.metric("BMNR Price", f"${bmnr_price:.2f}")
    col2.metric("mNAV Multiple", f"{mnav:.3f}x", delta_color="inverse")

    st.divider()

    # Asset Breakdown Table
    st.subheader("Treasury Breakdown")
    assets = {
        "Asset": ["Ethereum (ETH)", "Bitcoin (BTC)", "Cash", "Eightco Stake"],
        "Quantity": [f"{ETH_HELD:,}", f"{BTC_HELD}", "$1.0B", "$38M"],
        "Current Value": [val_eth, val_btc, CASH, EIGHT_STOCK_VALUE]
    }
    df = pd.DataFrame(assets)
    df["Current Value"] = df["Current Value"].map('${:,.0f}'.format)
    st.table(df)

    st.success(f"Total Net Asset Value (NAV): **${total_nav / 1e9:.2f} Billion**")

except Exception as e:
    st.error(f"Error fetching data: {e}")

# Footer auto-refresh mechanism
time.sleep(refresh_rate)
st.rerun()