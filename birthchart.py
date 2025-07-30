import streamlit as st
from datetime import datetime
import random

# Page setup
st.set_page_config(page_title="Vedic Market App", page_icon="🕉️")

# CSS
st.markdown("""
<style>
div[data-testid="column"] {
    background: #f0f2f6;
    padding: 10px;
    border-radius: 5px;
    margin: 2px;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'prices' not in st.session_state:
    st.session_state.prices = {
        'NIFTY': 24780,
        'BANKNIFTY': 52435, 
        'SENSEX': 81342,
        'GOLD': 3326,
        'BITCOIN': 97850
    }
    st.session_state.changes = {
        'NIFTY': -0.5,
        'BANKNIFTY': 0.6,
        'SENSEX': -0.3, 
        'GOLD': 0.5,
        'BITCOIN': 2.5
    }

# Header
st.title("🕉️ Vedic Market Intelligence")
st.write("Astrological market analysis with live data")

# Sidebar controls
with st.sidebar:
    st.header("📊 Controls")
    
    if st.button("🔄 Update Market Data", type="primary"):
        # Simple price update
        for market in st.session_state.prices:
            change = (random.random() - 0.5) * 1.0
            st.session_state.changes[market] += change * 0.1
            st.session_state.prices[market] += st.session_state.prices[market] * change / 1000
        st.success("Market data updated!")
        st.rerun()
    
    st.header("📅 Birth Details")
    birth_date = st.date_input("Birth Date")
    birth_time = st.time_input("Birth Time")
    birth_place = st.text_input("Birth Place", "Mumbai, India")
    
    if st.button("✨ Generate Chart"):
        st.success("Birth chart calculated!")
    
    st.header("🪐 Planets Today")
    st.text("☀️ Sun: Cancer")
    st.text("🌙 Moon: Virgo") 
    st.text("♂️ Mars: Cancer")
    st.text("♃ Jupiter: Gemini")
    st.text("♀ Venus: Gemini")

# Main dashboard
st.header("📈 Live Market Dashboard")

# Ticker display
ticker_text = ""
for market, price in st.session_state.prices.items():
    change = st.session_state.changes[market]
    arrow = "▲" if change >= 0 else "▼"
    ticker_text += f"{market}: {price:.0f} {arrow} {abs(change):.1f}% | "

st.info(f"📡 LIVE: {ticker_text}")

# Market grid
col1, col2, col3 = st.columns(3)
columns = [col1, col2, col3]

market_list = list(st.session_state.prices.items())
for i, (market, price) in enumerate(market_list):
    col_index = i % 3
    change = st.session_state.changes[market]
    
    with columns[col_index]:
        st.subheader(market)
        st.metric(
            label="Price",
            value=f"{price:.0f}",
            delta=f"{change:.1f}%"
        )

# Market summary using built-in components
st.header("📋 Market Summary")

# Create table manually with columns
col1, col2, col3, col4 = st.columns([2, 2, 2, 2])

with col1:
    st.write("**Market**")
    for market in st.session_state.prices:
        st.write(market)

with col2:
    st.write("**Price**")
    for market, price in st.session_state.prices.items():
        st.write(f"{price:.0f}")

with col3:
    st.write("**Change %**")
    for market in st.session_state.prices:
        change = st.session_state.changes[market]
        st.write(f"{change:+.1f}%")

with col4:
    st.write("**Status**")
    for market in st.session_state.prices:
        change = st.session_state.changes[market]
        status = "🟢 UP" if change > 0 else "🔴 DOWN"
        st.write(status)

# Analysis sections
st.header("📊 Market Analysis")

# Analysis selector
selected_market = st.selectbox("Choose Market for Analysis", list(st.session_state.prices.keys()))

# Simple analysis based on selection
if selected_market == 'NIFTY':
    st.info("**NIFTY Analysis**: Bearish trend expected. Support at 24,500")
elif selected_market == 'BANKNIFTY':
    st.info("**BANK NIFTY Analysis**: Strong bullish momentum. Target 53,000")
elif selected_market == 'GOLD':
    st.info("**GOLD Analysis**: Bullish breakout likely. Target $3,400")
elif selected_market == 'BITCOIN':
    st.info("**BITCOIN Analysis**: High volatility expected. Use tight stops")
else:
    st.info("**SENSEX Analysis**: Sideways consolidation expected")

# Astrological predictions
st.header("🌌 Astrological Predictions")

st.write("### Today's Planetary Influences:")
st.write("• ☀️ **Sun in Cancer**: Emotional decision making in markets")
st.write("• 🌙 **Moon in Virgo**: Analytical approach favors IT stocks")
st.write("• ♂️ **Mars in Cancer**: Banking sector shows strength")
st.write("• ♃ **Jupiter in Gemini**: Communication stocks favorable")
st.write("• ♀ **Venus in Gemini**: FMCG and consumer goods perform well")

st.write("### Best Trading Times:")
st.write("🕘 **9:15-10:00 AM**: High volatility - avoid major positions")
st.write("🕚 **10:00-11:30 AM**: Best time for fresh entries")
st.write("🕐 **2:00-3:00 PM**: Profit booking zone")
st.write("🕞 **3:15-3:30 PM**: Position for next trading day")

# Sector predictions
st.header("📈 Sector Outlook")

sectors = [
    ("Banking & Finance", "Bullish", "+0.8%"),
    ("Information Technology", "Bearish", "-1.2%"),
    ("Pharmaceuticals", "Neutral", "+0.1%"),
    ("Automobiles", "Bearish", "-0.9%"),
    ("FMCG", "Bullish", "+0.5%"),
    ("Metals", "Bearish", "-1.5%")
]

for sector, outlook, change in sectors:
    color = "🟢" if outlook == "Bullish" else "🔴" if outlook == "Bearish" else "🟡"
    st.write(f"{color} **{sector}**: {outlook} ({change})")

# Footer
st.markdown("---")
current_time = datetime.now().strftime("%H:%M:%S")
st.caption(f"🕐 Last Updated: {current_time} | 📊 Data simulated for demonstration")
st.caption("🕉️ Vedic Market Intelligence - Combining ancient wisdom with modern markets")
