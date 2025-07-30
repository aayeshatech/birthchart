import streamlit as st
import random
from datetime import datetime

# Basic page config
st.set_page_config(page_title="Vedic Market App", page_icon="🕉️", layout="wide")

# Minimal CSS
st.markdown("""
<style>
.card {
    background: #f0f2f6;
    padding: 15px;
    border-radius: 8px;
    margin: 5px 0;
    text-align: center;
}
.green { color: #00AA00; font-weight: bold; }
.red { color: #FF0000; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# Initialize data
if 'data' not in st.session_state:
    st.session_state.data = {
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
st.write("Real-time market data with astrological analysis")

# Sidebar
with st.sidebar:
    st.header("Controls")
    
    if st.button("🔄 Update Prices"):
        for market in st.session_state.data:
            change = (random.random() - 0.5) * 2
            st.session_state.changes[market] += change * 0.1
            st.session_state.data[market] *= (1 + change/1000)
        st.success("Updated!")
        st.rerun()
    
    st.header("Birth Chart")
    birth_date = st.date_input("Date")
    birth_time = st.time_input("Time")
    birth_place = st.text_input("Place", "Mumbai")
    
    if st.button("Generate Chart"):
        st.success("Chart Generated!")

# Main content
st.header("📊 Market Dashboard")

# Quick ticker
ticker = " | ".join([f"{k}: {v:.0f}" for k, v in st.session_state.data.items()])
st.info(f"📡 {ticker}")

# Market cards
col1, col2, col3 = st.columns(3)
markets = list(st.session_state.data.items())

for i, (name, price) in enumerate(markets):
    col = [col1, col2, col3][i % 3]
    change = st.session_state.changes[name]
    color = "green" if change >= 0 else "red"
    arrow = "▲" if change >= 0 else "▼"
    
    with col:
        st.markdown(f"""
        <div class="card">
            <h4>{name}</h4>
            <h3>{price:.0f}</h3>
            <p class="{color}">{arrow} {abs(change):.1f}%</p>
        </div>
        """, unsafe_allow_html=True)

# Data table
st.header("📋 Market Summary")
import pandas as pd

table_data = []
for name, price in st.session_state.data.items():
    change = st.session_state.changes[name]
    table_data.append({
        'Market': name,
        'Price': f"{price:.0f}",
        'Change %': f"{change:+.1f}%",
        'Trend': "🟢 Up" if change > 0 else "🔴 Down"
    })

df = pd.DataFrame(table_data)
st.dataframe(df, use_container_width=True)

# Tabs
tab1, tab2 = st.tabs(["📈 Analysis", "🌌 Astrology"])

with tab1:
    st.subheader("Market Analysis")
    
    selected = st.selectbox("Select Market", list(st.session_state.data.keys()))
    
    predictions = {
        'NIFTY': 'Bearish trend expected',
        'BANKNIFTY': 'Strong bullish momentum',
        'SENSEX': 'Sideways consolidation',
        'GOLD': 'Upward breakout likely',
        'BITCOIN': 'High volatility ahead'
    }
    
    st.info(f"**{selected}**: {predictions.get(selected, 'Neutral outlook')}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Support", "24,500" if selected == 'NIFTY' else "TBD")
    with col2:
        st.metric("Resistance", "25,000" if selected == 'NIFTY' else "TBD")

with tab2:
    st.subheader("Planetary Influence")
    
    planets = [
        "☀️ Sun in Cancer - Emotional trading decisions",
        "🌙 Moon in Virgo - Analytical market approach", 
        "♂️ Mars in Cancer - Banking sector strength",
        "♃ Jupiter in Gemini - Communication stocks favorable",
        "♀ Venus in Gemini - Consumer goods perform well"
    ]
    
    for planet in planets:
        st.write(f"• {planet}")
    
    st.subheader("Trading Times")
    st.write("🕘 **09:15-10:00**: High volatility")
    st.write("🕚 **10:00-11:30**: Best entry time")
    st.write("🕐 **14:00-15:00**: Profit booking zone")
    st.write("🕞 **15:15-15:30**: Position for tomorrow")

# Footer
st.markdown("---")
st.caption(f"Last updated: {datetime.now().strftime('%H:%M:%S')} | Data simulated for demo")
