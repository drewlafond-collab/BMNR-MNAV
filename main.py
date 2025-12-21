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

# Set up the web page
st.set_page_config(page_title="BMNR mNAV Tracker", page_icon="📈", layout="centered")

refresh_rate = 60

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

    # 3. Top Metrics Section
    col_a, col_b = st.columns(2)
    col_a.metric("Total NAV", f"${total_nav / 1e9:.2f} Billion")
    col_b.metric("mNAV Multiple", f"{mnav:.3f}x")

    st.divider()

    # 4. Integrated Treasury Breakdown Table
    st.subheader("Treasury Breakdown")
    
    # We now include the live price in the "Quantity / Price" column
    assets = {
        "Asset": ["Ethereum (ETH)", "Bitcoin (BTC)", "Cash", "Eightco Stake"],
        "Quantity / Live Price": [
            f"{ETH_HELD:,} @ ${eth_price:,.2f}", 
            f"{BTC_HELD} @ ${btc_price:,.0f}", 
            "$1.0B", 
            "$38M"
        ],
        "Current Value": [val_eth, val_btc, CASH, EIGHT_STOCK_VALUE]
    }
    
    df = pd.DataFrame(assets)
    
    # Format the 'Current Value' column to show clean dollar amounts
    df["Current Value"] = df["Current Value"].map('${:,.0f}'.format)
    
    # Display the table
    st.table(df)
    
    st.info(f"BMNR Market Cap: **${market_cap / 1e9:.2f}B** | Price: **${bmnr_price:.2f}**")

except Exception as e:
    st.error(f"Error updating dashboard: {e}")

# Auto-refresh
time.sleep(refresh_rate)
st.rerun()
