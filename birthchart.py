import streamlit as st
import pandas as pd
import random
from datetime import datetime
import time

# Page configuration
st.set_page_config(
    page_title="Vedic Market Intelligence",
    page_icon="🕉️",
    layout="wide"
)

# Simple CSS that won't break
st.markdown("""
<style>
.main-header {
    background: linear-gradient(45deg, #ff6b35, #f7931e);
    color: white;
    padding: 20px;
    text-align: center;
    border-radius: 10px;
    margin-bottom: 20px;
}
.market-card {
    background: #f8f9fa;
    padding: 15px;
    border-radius: 10px;
    text-align: center;
    margin: 10px 0;
    border: 2px solid #dee2e6;
}
.positive { color: #28a745; font-weight: bold; }
.negative { color: #dc3545; font-weight: bold; }
.ticker-box {
    background: #000;
    color: #00ff00;
    padding: 10px;
    font-family: monospace;
    border-radius: 5px;
    margin: 10px 0;
}
.chart-box {
    background: white;
    padding: 20px;
    border-radius: 10px;
    border: 2px solid #ddd;
    margin: 10px 0;
}
.planet-info {
    background: #e3f2fd;
    padding: 10px;
    border-radius: 5px;
    margin: 5px 0;
    border-left: 3px solid #2196f3;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state with error handling
try:
    if 'market_data' not in st.session_state:
        st.session_state.market_data = {
            'NIFTY': {'price': 24780.50, 'change': -0.50, 'high': 24920, 'low': 24750},
            'BANKNIFTY': {'price': 52435.75, 'change': 0.60, 'high': 52580, 'low': 52120},
            'SENSEX': {'price': 81342.15, 'change': -0.35, 'high': 81650, 'low': 81250},
            'GOLD': {'price': 3326.50, 'change': 0.55, 'high': 3335, 'low': 3308},
            'BITCOIN': {'price': 97850.50, 'change': 2.57, 'high': 98500, 'low': 95200},
            'CRUDE': {'price': 82.45, 'change': -1.49, 'high': 83.80, 'low': 82.20},
            'USDINR': {'price': 83.45, 'change': -0.14, 'high': 83.58, 'low': 83.42},
            'NIFTY_IT': {'price': 32156, 'change': -1.31, 'high': 32600, 'low': 32100},
            'NIFTY_PHARMA': {'price': 18925, 'change': 0.84, 'high': 19050, 'low': 18750}
        }
    
    if 'planetary_data' not in st.session_state:
        st.session_state.planetary_data = {
            'Sun': {'sign': 'Cancer', 'degree': '7°15\'', 'nakshatra': 'Pushya', 'house': 4, 'symbol': '☀️'},
            'Moon': {'sign': 'Virgo', 'degree': '12°30\'', 'nakshatra': 'Hasta', 'house': 6, 'symbol': '🌙'},
            'Mars': {'sign': 'Virgo', 'degree': '25°45\'', 'nakshatra': 'Chitra', 'house': 6, 'symbol': '♂️'},
            'Mercury': {'sign': 'Cancer', 'degree': '15°20\'', 'nakshatra': 'Ashlesha', 'house': 4, 'symbol': '☿️'},
            'Jupiter': {'sign': 'Gemini', 'degree': '22°10\'', 'nakshatra': 'Punarvasu', 'house': 3, 'symbol': '♃'},
            'Venus': {'sign': 'Gemini', 'degree': '8°35\'', 'nakshatra': 'Ardra', 'house': 3, 'symbol': '♀'},
            'Saturn': {'sign': 'Pisces', 'degree': '18°25\'', 'nakshatra': 'Revati', 'house': 12, 'symbol': '♄'},
            'Rahu': {'sign': 'Aries', 'degree': '5°40\'', 'nakshatra': 'Ashwini', 'house': 1, 'symbol': '☊'},
            'Ketu': {'sign': 'Libra', 'degree': '5°40\'', 'nakshatra': 'Swati', 'house': 7, 'symbol': '☋'}
        }
    
    if 'last_update' not in st.session_state:
        st.session_state.last_update = datetime.now()

except Exception as e:
    st.error(f"Error initializing data: {e}")

# Update function
def update_market_data():
    try:
        for market in st.session_state.market_data:
            data = st.session_state.market_data[market]
            # Simple random change
            change = (random.random() - 0.5) * 2
            data['change'] += change * 0.1
            data['price'] *= (1 + change/1000)
            
            # Update high/low
            if data['price'] > data['high']:
                data['high'] = data['price']
            if data['price'] < data['low']:
                data['low'] = data['price']
        
        st.session_state.last_update = datetime.now()
        return True
    except Exception as e:
        st.error(f"Error updating market data: {e}")
        return False

# Header - Updated without Om symbol in title
st.markdown("""
<div class="main-header">
    <h1>Vedic Birth Chart & Live Market Intelligence</h1>
    <p>Real-time Kundali Analysis with Live Market Data & Astrological Predictions</p>
</div>
""", unsafe_allow_html=True)

# Controls
col1, col2, col3 = st.columns(3)

with col1:
    auto_refresh = st.checkbox("🔄 Auto-Refresh", value=False)

with col2:
    if st.button("📈 Update Now", type="primary"):
        if update_market_data():
            st.success("Data updated!")
        st.rerun()

with col3:
    refresh_rate = st.selectbox("Rate (sec)", [5, 10, 30], index=0)

# Show current time and status
st.write(f"🕐 **Current Time:** {datetime.now().strftime('%H:%M:%S')}")
st.write(f"📊 **Last Update:** {st.session_state.last_update.strftime('%H:%M:%S')}")

# Auto-refresh logic
if auto_refresh:
    time.sleep(refresh_rate)
    update_market_data()
    st.rerun()

# Ticker display
try:
    ticker_items = []
    for market, data in list(st.session_state.market_data.items())[:5]:  # Show first 5
        arrow = '▲' if data['change'] >= 0 else '▼'
        ticker_items.append(f"{market}: {data['price']:.1f} {arrow} {abs(data['change']):.2f}%")
    
    ticker_text = " | ".join(ticker_items)
    st.markdown(f'<div class="ticker-box">📡 LIVE: {ticker_text}</div>', unsafe_allow_html=True)
except Exception as e:
    st.error(f"Error creating ticker: {e}")

# Main content layout
main_col1, main_col2 = st.columns([1, 1])

with main_col1:
    st.markdown('<div class="chart-box">', unsafe_allow_html=True)
    st.subheader("🎯 Vedic Birth Chart")
    
    # Birth chart inputs
    col_a, col_b = st.columns(2)
    with col_a:
        birth_date = st.date_input(
            "Birth Date", 
            value=datetime(1990, 1, 1),
            min_value=datetime(1900, 1, 1),
            max_value=datetime(2025, 12, 31)
        )
        birth_place = st.text_input("Birth Place", "Mumbai, India")
    with col_b:
        birth_time = st.time_input(
            "Birth Time", 
            value=datetime.now().time(),
            help="Select exact birth time for accurate chart"
        )
        timezone = st.selectbox(
            "Timezone", 
            ["IST (+05:30)", "UTC (+00:00)", "EST (-05:00)", "PST (-08:00)", "CST (+08:00)", "JST (+09:00)"],
            help="Choose your birth location timezone"
        )
    
    if st.button("✨ Generate Chart"):
        st.success(f"Birth chart generated for {birth_date} at {birth_time}!")
        st.info(f"📍 Location: {birth_place} | 🕐 Timezone: {timezone}")
        # Update planetary positions based on birth date
        try:
            # Simple calculation based on birth date
            birth_year = birth_date.year
            day_offset = (datetime.now() - datetime(birth_year, birth_date.month, birth_date.day)).days
            
            # Update planetary positions (simplified)
            for planet in st.session_state.planetary_data:
                current_degree = (15 + (day_offset * 0.1)) % 30
                degree_str = f"{int(current_degree)}°{int((current_degree % 1) * 60)}'"
                st.session_state.planetary_data[planet]['degree'] = degree_str
            
            st.balloons()
        except Exception as e:
            st.warning(f"Chart generated with default positions. Error: {e}")
    
    # Alternative year input if date picker doesn't work
    st.write("**Alternative:** If date picker doesn't work:")
    year_input = st.number_input(
        "Enter Birth Year", 
        min_value=1900, 
        max_value=2025, 
        value=1990,
        step=1
    )
    month_input = st.selectbox(
        "Birth Month", 
        list(range(1, 13)), 
        index=0,
        format_func=lambda x: datetime(2000, x, 1).strftime('%B')
    )
    day_input = st.number_input(
        "Birth Day", 
        min_value=1, 
        max_value=31, 
        value=1
    )
    
    # Simple birth chart representation
    st.write("### 📊 Birth Chart (North Indian Style)")
    st.info("💡 **Tip:** This is a simplified representation. For detailed calculations, exact birth time and location are crucial.")
    
    # Create a simple 4x4 grid for the chart - FIXED with unique column names
    chart_data = [
        ['12♓', '1♈', '2♉', '3♊'],
        ['11♒', '🕉️', 'Rasi', '4♋'],
        ['10♑', 'Chart', '⭐', '5♌'],
        ['9♐', '8♏', '7♎', '6♍']
    ]
    
    # Fix: Use unique column names instead of empty strings
    chart_df = pd.DataFrame(chart_data, columns=['Col1', 'Col2', 'Col3', 'Col4'])
    
    # Display without column headers using st.dataframe with hide_index
    st.dataframe(chart_df, hide_index=True, use_container_width=True, 
                 column_config={
                     "Col1": st.column_config.TextColumn(label=""),
                     "Col2": st.column_config.TextColumn(label=""),
                     "Col3": st.column_config.TextColumn(label=""),
                     "Col4": st.column_config.TextColumn(label="")
                 })
    
    # Display current birth details
    st.write(f"**Current Settings:** {birth_date} | {birth_time} | {birth_place}")
    
    # Show planetary placements in houses
    st.write("### 🏠 Planetary House Placements")
    house_placements = {
        1: "☊ Rahu (Ashwini)",
        3: "♃ Jupiter, ♀ Venus (Punarvasu, Ardra)", 
        4: "☀️ Sun, ☿️ Mercury (Pushya, Ashlesha)",
        6: "🌙 Moon, ♂️ Mars (Hasta, Chitra)",
        7: "☋ Ketu (Swati)",
        12: "♄ Saturn (Revati)"
    }
    
    for house, planets in house_placements.items():
        st.write(f"**House {house}:** {planets}")
    
    # Planetary positions
    st.write("### 🪐 Planetary Positions")
    try:
        for planet, data in st.session_state.planetary_data.items():
            st.markdown(f"""
            <div class="planet-info">
                <strong>{data['symbol']} {planet}</strong> - {data['sign']} {data['degree']}<br>
                Nakshatra: {data['nakshatra']} | House: {data['house']}
            </div>
            """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error displaying planetary data: {e}")
    
    st.markdown('</div>', unsafe_allow_html=True)

with main_col2:
    st.markdown('<div class="chart-box">', unsafe_allow_html=True)
    st.subheader("📊 Live Market Dashboard")
    
    # Display market cards
    try:
        major_markets = ['NIFTY', 'BANKNIFTY', 'SENSEX', 'GOLD', 'BITCOIN', 'USDINR']
        
        for i in range(0, len(major_markets), 2):
            col_x, col_y = st.columns(2)
            
            # First market
            if i < len(major_markets):
                market = major_markets[i]
                data = st.session_state.market_data[market]
                color_class = "positive" if data['change'] >= 0 else "negative"
                arrow = "▲" if data['change'] >= 0 else "▼"
                
                col_x.markdown(f"""
                <div class="market-card">
                    <h4>{market}</h4>
                    <h2>{data['price']:.2f}</h2>
                    <p class="{color_class}">
                        {arrow} {abs(data['change']):.2f}%
                    </p>
                    <small>H: {data['high']:.1f} | L: {data['low']:.1f}</small>
                </div>
                """, unsafe_allow_html=True)
            
            # Second market
            if i + 1 < len(major_markets):
                market = major_markets[i + 1]
                data = st.session_state.market_data[market]
                color_class = "positive" if data['change'] >= 0 else "negative"
                arrow = "▲" if data['change'] >= 0 else "▼"
                
                col_y.markdown(f"""
                <div class="market-card">
                    <h4>{market}</h4>
                    <h2>{data['price']:.2f}</h2>
                    <p class="{color_class}">
                        {arrow} {abs(data['change']):.2f}%
                    </p>
                    <small>H: {data['high']:.1f} | L: {data['low']:.1f}</small>
                </div>
                """, unsafe_allow_html=True)
    
    except Exception as e:
        st.error(f"Error displaying market cards: {e}")
    
    # Market influences
    st.write("### 🌟 Current Market Influences")
    st.info("🌙 **Moon in Virgo:** Technical analysis favored for IT stocks")
    st.info("♂️ **Mars aspect:** Banking sector showing strength")
    st.info("☿️ **Mercury transit:** Communication stocks volatile")
    st.info("♃ **Jupiter favorable:** Long-term investments positive")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Detailed analysis tabs
st.write("---")
tab1, tab2, tab3 = st.tabs(["📈 Market Analysis", "🔴 Live Data", "🌌 Astro Analysis"])

with tab1:
    st.subheader("📈 Market Analysis")
    
    # Market table
    try:
        table_data = []
        for market, data in st.session_state.market_data.items():
            table_data.append({
                'Market': market,
                'Price': f"{data['price']:.2f}",
                'Change %': f"{data['change']:+.2f}%",
                'High': f"{data['high']:.2f}",
                'Low': f"{data['low']:.2f}",
                'Status': "🟢 Bullish" if data['change'] > 0 else "🔴 Bearish"
            })
        
        df = pd.DataFrame(table_data)
        st.dataframe(df, use_container_width=True)
        
        # Sector analysis
        st.write("### 📊 Sector Performance")
        sectors = {
            'Banking': 'Bullish (+0.6%)',
            'IT': 'Bearish (-1.3%)',
            'Pharma': 'Bullish (+0.8%)',
            'Auto': 'Neutral (-0.1%)',
            'FMCG': 'Bullish (+0.3%)',
            'Metal': 'Bearish (-1.6%)'
        }
        
        for sector, performance in sectors.items():
            color = "🟢" if "Bullish" in performance else "🔴" if "Bearish" in performance else "🟡"
            st.write(f"{color} **{sector}:** {performance}")
            
    except Exception as e:
        st.error(f"Error in market analysis: {e}")

with tab2:
    st.subheader("🔴 Live Market Data")
    
    # Market highlights
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Market Status", "OPEN", "Live Trading")
    with col2:
        st.metric("FII Activity", "₹2,345 Cr", "Net Buy")
    with col3:
        st.metric("Advances/Declines", "1285/765", "Positive")
    with col4:
        st.metric("VIX", "14.25", "-3.45%")
    
    # Live updates
    st.write("### 📊 Real-time Updates")
    try:
        for market, data in list(st.session_state.market_data.items())[:6]:
            col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
            
            with col1:
                st.write(f"**{market}**")
            with col2:
                st.write(f"{data['price']:.2f}")
            with col3:
                color = "🟢" if data['change'] >= 0 else "🔴"
                st.write(f"{color} {data['change']:+.2f}%")
            with col4:
                st.write("LIVE")
    except Exception as e:
        st.error(f"Error in live data: {e}")

with tab3:
    st.subheader("🌌 Astrological Analysis")
    
    analysis_choice = st.selectbox("Select Market", ["NIFTY", "BANKNIFTY", "GOLD", "BITCOIN"])
    
    predictions = {
        'NIFTY': {'trend': 'Bearish to Neutral', 'range': '24,700 - 24,850', 'advice': 'Wait for support test'},
        'BANKNIFTY': {'trend': 'Bullish', 'range': '52,300 - 52,600', 'advice': 'Buy on dips'},
        'GOLD': {'trend': 'Bullish', 'range': '$3,320 - $3,340', 'advice': 'Accumulate below $3,325'},
        'BITCOIN': {'trend': 'Volatile', 'range': '$96,000 - $99,000', 'advice': 'Use tight stops'}
    }
    
    pred = predictions.get(analysis_choice, predictions['NIFTY'])
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"**Trend:** {pred['trend']}")
        st.success(f"**Range:** {pred['range']}")
    
    with col2:
        st.warning(f"**Advice:** {pred['advice']}")
    
    # Time zones
    st.write("### ⏰ Key Trading Time Zones")
    st.write("🕘 **09:15-10:00 AM:** Opening volatility (Moon influence)")
    st.write("🕚 **10:30-11:30 AM:** Trend formation (Jupiter aspect)")
    st.write("🕐 **02:00-03:00 PM:** Reversal zone (Mercury)")
    st.write("🕞 **03:15-03:30 PM:** Closing positions (Venus)")

# Footer
st.write("---")
footer_col1, footer_col2 = st.columns(2)

with footer_col1:
    st.caption(f"🕐 Last Updated: {st.session_state.last_update.strftime('%H:%M:%S')}")

with footer_col2:
    st.caption("🕉️ Vedic Market Intelligence - Demo Version")

# Debug info (you can remove this later)
with st.expander("🔧 Debug Info (Click to expand)"):
    st.write("**Session State Keys:**", list(st.session_state.keys()))
    st.write("**Market Data Status:**", "✅ Loaded" if 'market_data' in st.session_state else "❌ Missing")
    st.write("**Planetary Data Status:**", "✅ Loaded" if 'planetary_data' in st.session_state else "❌ Missing")
    if 'market_data' in st.session_state:
        st.write("**Number of Markets:**", len(st.session_state.market_data))
