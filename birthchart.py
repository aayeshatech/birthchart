import streamlit as st
import pandas as pd
import random
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Vedic Market Intelligence",
    page_icon="🕉️",
    layout="wide"
)

# Simple CSS
st.markdown("""
<style>
.market-card {
    background: #f1f3f4;
    padding: 20px;
    border-radius: 10px;
    text-align: center;
    margin: 10px 0;
    border: 2px solid #e0e0e0;
}
.positive { color: #16a085; font-weight: bold; }
.negative { color: #e74c3c; font-weight: bold; }
.header {
    background: linear-gradient(45deg, #ff6b35, #f7931e);
    color: white;
    padding: 20px;
    text-align: center;
    border-radius: 10px;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# Initialize simple data
if 'markets' not in st.session_state:
    st.session_state.markets = {
        'NIFTY 50': {'price': 24780.50, 'change': -0.50},
        'BANK NIFTY': {'price': 52435.75, 'change': 0.60},
        'SENSEX': {'price': 81342.15, 'change': -0.35},
        'NIFTY IT': {'price': 32156.40, 'change': -1.31},
        'GOLD': {'price': 3326.50, 'change': 0.55},
        'SILVER': {'price': 38.25, 'change': -0.83},
        'CRUDE OIL': {'price': 82.45, 'change': -1.49},
        'BITCOIN': {'price': 97850.50, 'change': 2.57},
        'USD/INR': {'price': 83.45, 'change': -0.14}
    }

# Planetary positions
planets = {
    '☀️ Sun': 'Cancer 7°15\' (Pushya)',
    '🌙 Moon': 'Virgo 12°30\' (Hasta)', 
    '♂️ Mars': 'Virgo 25°45\' (Chitra)',
    '☿️ Mercury': 'Cancer 15°20\' (Ashlesha)',
    '♃ Jupiter': 'Gemini 22°10\' (Punarvasu)',
    '♀ Venus': 'Gemini 8°35\' (Ardra)',
    '♄ Saturn': 'Pisces 18°25\' (Revati)',
    '☊ Rahu': 'Aries 5°40\' (Ashwini)',
    '☋ Ketu': 'Libra 5°40\' (Swati)'
}

# Header
st.markdown("""
<div class="header">
    <h1>🕉️ Vedic Birth Chart & Market Intelligence</h1>
    <p>Astrological Market Analysis & Birth Chart Calculator</p>
</div>
""", unsafe_allow_html=True)

# Simple update function
def update_prices():
    for name in st.session_state.markets:
        market = st.session_state.markets[name]
        change = (random.random() - 0.5) * 1.0  # Random change
        market['change'] += change * 0.1
        market['price'] *= (1 + change/1000)

# Sidebar
with st.sidebar:
    st.header("🎛️ Controls")
    
    if st.button("📈 Update Market Prices", type="primary"):
        update_prices()
        st.success("Prices updated!")
        st.rerun()
    
    st.header("📅 Birth Details")
    birth_date = st.date_input("Birth Date", datetime(1990, 1, 1))
    birth_time = st.time_input("Birth Time")
    birth_place = st.text_input("Birth Place", "Mumbai, India")
    timezone = st.selectbox("Timezone", ["IST (+05:30)", "UTC", "EST", "PST"])
    
    if st.button("🔄 Generate Chart"):
        st.success("Birth chart generated!")
    
    st.header("🪐 Planetary Positions")
    for planet, position in planets.items():
        st.write(f"**{planet}**: {position}")

# Main content area
st.header("📊 Live Market Data")

# Create ticker display
ticker_text = " | ".join([
    f"{name}: {data['price']:.1f} ({'▲' if data['change'] >= 0 else '▼'}{abs(data['change']):.2f}%)"
    for name, data in list(st.session_state.markets.items())[:6]
])
st.info(f"📡 **Live Ticker:** {ticker_text}")

# Market cards in grid
col1, col2, col3 = st.columns(3)
cols = [col1, col2, col3]

for i, (name, data) in enumerate(st.session_state.markets.items()):
    col = cols[i % 3]
    
    with col:
        color_class = "positive" if data['change'] >= 0 else "negative"
        arrow = "▲" if data['change'] >= 0 else "▼"
        
        st.markdown(f"""
        <div class="market-card">
            <h4>{name}</h4>
            <h2>{data['price']:.2f}</h2>
            <p class="{color_class}">
                {arrow} {abs(data['change']):.2f}%
            </p>
        </div>
        """, unsafe_allow_html=True)

# Market table
st.header("📋 Market Summary")
table_data = []
for name, data in st.session_state.markets.items():
    table_data.append({
        'Market': name,
        'Current Price': f"{data['price']:.2f}",
        'Change %': f"{data['change']:+.2f}%",
        'Status': "🟢 Bullish" if data['change'] > 0 else "🔴 Bearish"
    })

df = pd.DataFrame(table_data)
st.dataframe(df, use_container_width=True)

# Tabs for analysis
tab1, tab2, tab3 = st.tabs(["📈 Technical Analysis", "🌌 Astrological Predictions", "📊 Sector Overview"])

with tab1:
    st.subheader("Market Analysis")
    
    selected_market = st.selectbox("Choose Market for Analysis", list(st.session_state.markets.keys()))
    
    analysis = {
        'NIFTY 50': {'trend': 'Bearish', 'support': '24,700', 'resistance': '24,900'},
        'BANK NIFTY': {'trend': 'Bullish', 'support': '52,200', 'resistance': '52,800'},
        'GOLD': {'trend': 'Bullish', 'support': '$3,320', 'resistance': '$3,350'},
        'BITCOIN': {'trend': 'Volatile', 'support': '$96,000', 'resistance': '$99,000'}
    }
    
    if selected_market in analysis:
        data = analysis[selected_market]
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Trend", data['trend'])
        with col2:
            st.metric("Support", data['support'])
        with col3:
            st.metric("Resistance", data['resistance'])

with tab2:
    st.subheader("Astrological Market Predictions")
    
    st.write("### Today's Planetary Influences:")
    
    predictions = [
        "🌙 **Moon in Virgo**: Analytical energy favors IT and tech stocks",
        "♂️ **Mars in Cancer**: Banking sector shows strong momentum", 
        "♃ **Jupiter in Gemini**: Communication and media stocks are favorable",
        "♀ **Venus in Gemini**: Luxury and consumer goods perform well",
        "☿️ **Mercury in Cancer**: Real estate and property stocks active"
    ]
    
    for prediction in predictions:
        st.write(prediction)
    
    st.write("### Time-based Trading Recommendations:")
    st.write("- **09:15-10:00 AM**: High volatility, avoid major positions")
    st.write("- **10:00-11:30 AM**: Best time for fresh entries")
    st.write("- **02:00-03:00 PM**: Reversal zone, book profits")
    st.write("- **03:15-03:30 PM**: Position for next day")

with tab3:
    st.subheader("Sector Performance")
    
    sectors = [
        {'name': 'Banking & Finance', 'performance': 'Bullish', 'change': '+0.8%'},
        {'name': 'Information Technology', 'performance': 'Bearish', 'change': '-1.2%'},
        {'name': 'Pharmaceuticals', 'performance': 'Neutral', 'change': '+0.1%'},
        {'name': 'Automobiles', 'performance': 'Bearish', 'change': '-0.9%'},
        {'name': 'Metals & Mining', 'performance': 'Bearish', 'change': '-1.5%'},
        {'name': 'FMCG', 'performance': 'Bullish', 'change': '+0.5%'}
    ]
    
    for sector in sectors:
        color = "🟢" if sector['performance'] == 'Bullish' else "🔴" if sector['performance'] == 'Bearish' else "🟡"
        st.write(f"{color} **{sector['name']}**: {sector['performance']} ({sector['change']})")

# Footer
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    st.caption(f"🕐 Last Updated: {datetime.now().strftime('%I:%M %p')}")
with col2:
    st.caption("📊 Data is simulated for demonstration purposes")
