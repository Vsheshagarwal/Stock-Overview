import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("📊 Indian Script Overview")

# Input from user
symbol = st.text_input("Enter NSE stock symbol (e.g., TCS.NS)", "TCS.NS")

# Load stock data
try:
    stock = yf.Ticker(symbol)
    info = stock.info

    # Stock info section
    st.header(f"📈 {info.get('longName', symbol)} Overview")

    col1, col2, col3 = st.columns(3)
    col1.metric("📌 Current Price", f"₹{info.get('currentPrice', 'N/A')}")
    col2.metric("💰 EPS", info.get('trailingEps', 'N/A'))
    col3.metric("🧮 PE Ratio", info.get('trailingPE', 'N/A'))

    col4, col5, col6 = st.columns(3)
    col4.metric("📉 52-Week Low", f"₹{info.get('fiftyTwoWeekLow', 'N/A')}")
    col5.metric("📈 52-Week High", f"₹{info.get('fiftyTwoWeekHigh', 'N/A')}")
    col6.metric("🏦 Market Cap", f"₹{round(info.get('marketCap', 0)/1e7, 2)} Cr")

    st.divider()

    # Historical chart
    st.subheader("📅 Last 6 Months Price Trend")
    hist = stock.history(period="6mo")
    if not hist.empty:
        st.line_chart(hist['Close'])
    else:
        st.warning("No historical price data found.")

    # Bar chart of current vs 52-week high/low
    st.subheader("📊 Price Position Compared to 52-Week Range")
    try:
        current = info['currentPrice']
        low = info['fiftyTwoWeekLow']
        high = info['fiftyTwoWeekHigh']
        bar = go.Figure(go.Bar(
            x=["52-Week Low", "Current Price", "52-Week High"],
            y=[low, current, high],
            marker_color=["red", "blue", "green"]
        ))
        bar.update_layout(height=400)
        st.plotly_chart(bar)
    except:
        st.warning("Could not generate bar chart.")


except Exception as e:
    st.error(f"⚠️ Error fetching stock data: {e}")
