import streamlit as st
import yfinance as yf
import pandas as pd
import time

# --- BMNR DATA (Dec 20, 2025) ---
SHARES = 421_500_000
CASH = 1_000_000_000
BTC_HELD = 193
ETH_HELD = 3_967_210  
EIGHT_STOCK_VALUE = 38_000_000

st.set_page_config(page_title="BMNR mNAV Tracker", page_icon="📈", layout="centered")

refresh_rate = 60
st.title("Bitmine (BMNR) mNAV Tracker")
st.markdown(f"**Last Updated:** {time.strftime('%H:%M:%S')}")

try:
    # 1. Fetch live market prices
    with st.spinner('Updating market data...'):
        bmnr_price = yf.Ticker("BMNR").fast_info.last_price
        eth_price = yf.Ticker("ETH-USD").fast_info.last_price
        btc_price = yf.Ticker("BTC-USD").fast_info.last_price

    # 2. Portfolio Calculations
    val_eth = ETH_HELD * eth_price
    val_btc = BTC_HELD * btc_price
    total_nav = val_eth + val_btc + CASH + EIGHT_STOCK_VALUE
    market_cap = bmnr_price * SHARES
    mnav = market_cap / total_nav

    # 3. Summary Metrics
    m1, m2 = st.columns(2)
    m1.metric("Total NAV", f"${total_nav / 1e9:.2f}B")
    m2.metric("mNAV Multiple", f"{mnav:.3f}x")

    st.divider()

    # 4. Detailed Treasury Breakdown Table
    st.subheader("Treasury Breakdown")
    
    # Defining the data with separate columns for prices
    assets = {
        "Asset": ["Ethereum (ETH)", "Bitcoin (BTC)", "Cash", "Eightco Stake"],
        "Quantity": [f"{ETH_HELD:,}", f"{BTC_HELD:,}", "-", "-"],
        "Live Price": [f"${eth_price:,.2f}", f"${btc_price:,.0f}", "-", "-"],
        "Current Value": [val_eth, val_btc, CASH, EIGHT_STOCK_VALUE]
    }
    
    df = pd.DataFrame(assets)
    
    # Formatting the final value column for readability
    df["Current Value"] = df["Current Value"].map('${:,.0f}'.format)
    
    # Use st.dataframe for a clean, interactive look
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    st.info(f"**BMNR Stats:** Price: ${bmnr_price:.2f} | Market Cap: ${market_cap / 1e9:.2f}B")
