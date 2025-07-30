import streamlit as st
import pandas as pd
import random
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Vedic Market App",
    page_icon="🕉️",
    layout="wide"
)

# Simple CSS
st.markdown("""
<style>
.market-card {
    background: #f8f9fa;
    padding: 15px;
    border-radius: 8px;
    text-align: center;
    margin: 5px;
    border: 1px solid #ddd;
}
.positive { color: #28a745; font-weight: bold; }
.negative { color: #dc3545; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# Initialize data
if 'data' not in st.session_state:
    st.session_state.data = {
        'NIFTY': {'price': 24780, 'change': -0.5},
        'BANKNIFTY': {'price': 52435, 'change': 0.6},
        'SENSEX': {'price': 81342, 'change': -0.3},
        'GOLD': {'price': 3326, 'change': 0.5},
        'BITCOIN': {'price': 97850, 'change': 2.5},
        'CRUDE': {'price': 82.45, 'change': -1.4}
    }

# Header
st.title("🕉️ Vedic Market Intelligence")

# Quick refresh function
def update_data():
    for key in st.session_state.data:
        change = (random.random() - 0.5) * 2
        st.session_state.data[key]['change'] += change * 0.1
        st.session_state.data[key]['price'] *= (1 + change/1000)

# Sidebar
with st.sidebar:
    st.header("Controls")
    if st.button("🔄 Update Prices"):
        update_data()
        st.rerun()
    
    st.header("Birth Details")
    birth_date = st.date_input("Date", datetime(1990, 1, 1))
    birth_time = st.time_input("Time")
    birth_place = st.text_input("Place", "Mumbai")

# Main content
col1, col2, col3 = st.columns(3)

# Display markets in cards
markets = list(st.session_state.data.items())
for i, (name, data) in enumerate(markets):
    col = [col1, col2, col3][i % 3]
    
    with col:
        st.markdown(f"""
        <div class="market-card">
            <h4>{name}</h4>
            <h3>{data['price']:.2f}</h3>
            <p class="{'positive' if data['change'] >= 0 else 'negative'}">
                {'▲' if data['change'] >= 0 else '▼'} {abs(data['change']):.2f}%
            </p>
        </div>
        """, unsafe_allow_html=True)

# Market table
st.subheader("Market Overview")
df_data = []
for name, data in st.session_state.data.items():
    df_data.append({
        'Market': name,
        'Price': f"{data['price']:.2f}",
        'Change %': f"{data['change']:+.2f}%"
    })

st.dataframe(pd.DataFrame(df_data), use_container_width=True)

# Tabs
tab1, tab2 = st.tabs(["📈 Analysis", "🌌 Astrology"])

with tab1:
    st.subheader("Market Analysis")
    
    selected = st.selectbox("Choose Market", list(st.session_state.data.keys()))
    
    predictions = {
        'NIFTY': 'Bearish trend expected',
        'BANKNIFTY': 'Bullish momentum',
        'SENSEX': 'Sideways movement',
        'GOLD': 'Strong upward trend',
        'BITCOIN': 'High volatility expected',
        'CRUDE': 'Bearish pressure'
    }
    
    st.info(f"**{selected} Prediction:** {predictions.get(selected, 'Neutral')}")

with tab2:
    st.subheader("Planetary Influence")
    
    st.write("🌙 **Moon in Virgo:** Analytical energy affecting IT stocks")
    st.write("♂️ **Mars in Cancer:** Banking sector shows strength")
    st.write("☀️ **Sun in Leo:** Leadership stocks performing well")
    st.write("♃ **Jupiter Transit:** Long-term bullish for commodities")

# Footer
st.markdown("---")
st.caption(f"Last updated: {datetime.now().strftime('%H:%M:%S')}")
