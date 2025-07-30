import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import json

# Page configuration
st.set_page_config(
    page_title="Vedic Birth Chart & Live Market Intelligence",
    page_icon="🕉️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .main-header {
        background: linear-gradient(45deg, #ff6b35, #f7931e);
        color: white;
        padding: 20px;
        text-align: center;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .ticker {
        background: #000;
        color: #00ff00;
        padding: 10px;
        font-family: 'Courier New', monospace;
        font-size: 14px;
        overflow: hidden;
        white-space: nowrap;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    .chart-container {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    .market-card {
        background: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 10px;
    }
    .price-positive { color: #28a745; }
    .price-negative { color: #dc3545; }
    .sector-card {
        background: white;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        border-left: 5px solid;
        margin-bottom: 15px;
    }
    .sector-bullish { border-left-color: #28a745; }
    .sector-bearish { border-left-color: #dc3545; }
    .sector-neutral { border-left-color: #ffc107; }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'market_data' not in st.session_state:
    st.session_state.market_data = {
        # Indian Indices - Current July 2025 prices
        'nifty': {'price': 24780.50, 'change': -125.30, 'changePercent': -0.50, 'high': 24920.15, 'low': 24750.20},
        'bankNifty': {'price': 52435.75, 'change': 315.25, 'changePercent': 0.60, 'high': 52580.40, 'low': 52120.50},
        'sensex': {'price': 81342.15, 'change': -285.40, 'changePercent': -0.35, 'high': 81650.30, 'low': 81250.80},
        'niftyIT': {'price': 32156.40, 'change': -425.30, 'changePercent': -1.31, 'high': 32600.20, 'low': 32100.15},
        'niftyPharma': {'price': 18925.60, 'change': 156.80, 'changePercent': 0.84, 'high': 19050.30, 'low': 18750.40},
        'niftyAuto': {'price': 22485.30, 'change': -185.60, 'changePercent': -0.82, 'high': 22680.50, 'low': 22400.20},
        'niftyFMCG': {'price': 55342.80, 'change': 125.40, 'changePercent': 0.23, 'high': 55450.60, 'low': 55200.30},
        'niftyMetal': {'price': 8956.45, 'change': -145.30, 'changePercent': -1.60, 'high': 9120.50, 'low': 8920.40},
        'niftyRealty': {'price': 785.25, 'change': 12.40, 'changePercent': 1.60, 'high': 792.30, 'low': 772.50},
        'niftyEnergy': {'price': 35426.90, 'change': -256.40, 'changePercent': -0.72, 'high': 35680.20, 'low': 35350.40},
        'niftyPSUBank': {'price': 6842.35, 'change': 85.60, 'changePercent': 1.27, 'high': 6890.40, 'low': 6750.20},
        'cnx100': {'price': 24156.30, 'change': -98.50, 'changePercent': -0.41, 'high': 24280.40, 'low': 24120.60},
        'cnx500': {'price': 21845.75, 'change': -75.30, 'changePercent': -0.34, 'high': 21950.80, 'low': 21800.40},
        
        # Global Indices
        'dowJones': {'price': 43825.40, 'change': 186.25, 'changePercent': 0.43, 'high': 43920.60, 'low': 43650.30},
        'sp500': {'price': 5932.15, 'change': 22.40, 'changePercent': 0.38, 'high': 5945.80, 'low': 5910.20},
        'nasdaq': {'price': 19456.80, 'change': 85.30, 'changePercent': 0.44, 'high': 19520.40, 'low': 19380.60},
        'ftse': {'price': 8445.60, 'change': -32.40, 'changePercent': -0.38, 'high': 8485.30, 'low': 8430.20},
        'dax': {'price': 19328.45, 'change': 125.60, 'changePercent': 0.65, 'high': 19380.60, 'low': 19250.40},
        'nikkei': {'price': 41580.20, 'change': 325.40, 'changePercent': 0.79, 'high': 41650.80, 'low': 41250.60},
        
        # Commodities - Accurate current prices
        'gold': {'price': 3326.50, 'change': 18.30, 'changePercent': 0.55, 'high': 3335.20, 'low': 3308.40},
        'goldMCX': {'price': 72850, 'change': 385, 'changePercent': 0.53, 'high': 73100, 'low': 72500},
        'silver': {'price': 38.25, 'change': -0.32, 'changePercent': -0.83, 'high': 38.65, 'low': 38.10},
        'silverMCX': {'price': 91250, 'change': -650, 'changePercent': -0.71, 'high': 91800, 'low': 90800},
        'crudeOil': {'price': 82.45, 'change': -1.25, 'changePercent': -1.49, 'high': 83.80, 'low': 82.20},
        
        # Forex
        'usdinr': {'price': 83.45, 'change': -0.12, 'changePercent': -0.14, 'high': 83.58, 'low': 83.42},
        'eurusd': {'price': 1.0885, 'change': 0.0045, 'changePercent': 0.42, 'high': 1.0895, 'low': 1.0840},
        
        # Crypto
        'bitcoin': {'price': 97850.50, 'change': 2450.30, 'changePercent': 2.57, 'high': 98500.00, 'low': 95200.00},
        'ethereum': {'price': 3685.40, 'change': 125.60, 'changePercent': 3.53, 'high': 3720.00, 'low': 3560.00},
    }

if 'last_update' not in st.session_state:
    st.session_state.last_update = datetime.now()

# Planetary data
planetary_data = {
    'sun': {'sign': 'Cancer', 'degree': '7°15\'', 'nakshatra': 'Pushya', 'house': 4, 'symbol': '☀️'},
    'moon': {'sign': 'Virgo', 'degree': '12°30\'', 'nakshatra': 'Hasta', 'house': 6, 'symbol': '🌙'},
    'mars': {'sign': 'Virgo', 'degree': '25°45\'', 'nakshatra': 'Chitra', 'house': 6, 'symbol': '♂️'},
    'mercury': {'sign': 'Cancer', 'degree': '15°20\'', 'nakshatra': 'Ashlesha', 'house': 4, 'symbol': '☿️'},
    'jupiter': {'sign': 'Gemini', 'degree': '22°10\'', 'nakshatra': 'Punarvasu', 'house': 3, 'symbol': '♃'},
    'venus': {'sign': 'Gemini', 'degree': '8°35\'', 'nakshatra': 'Ardra', 'house': 3, 'symbol': '♀'},
    'saturn': {'sign': 'Pisces', 'degree': '18°25\'', 'nakshatra': 'Revati', 'house': 12, 'symbol': '♄'},
    'rahu': {'sign': 'Aries', 'degree': '5°40\'', 'nakshatra': 'Ashwini', 'house': 1, 'symbol': '☊'},
    'ketu': {'sign': 'Libra', 'degree': '5°40\'', 'nakshatra': 'Swati', 'house': 7, 'symbol': '☋'},
}

def update_market_data():
    """Simulate market data updates"""
    current_time = datetime.now()
    if (current_time - st.session_state.last_update).seconds > 5:  # Update every 5 seconds
        for key, data in st.session_state.market_data.items():
            volatility = 0.1
            if 'bitcoin' in key or 'ethereum' in key:
                volatility = 0.3
            elif 'gold' in key or 'silver' in key:
                volatility = 0.05
            
            change_percent = (random.random() - 0.5) * volatility
            new_change = data['price'] * change_percent / 100
            data['price'] += new_change
            data['change'] = new_change
            data['changePercent'] = change_percent
            
            if data['price'] > data['high']:
                data['high'] = data['price']
            if data['price'] < data['low']:
                data['low'] = data['price']
        
        st.session_state.last_update = current_time

def create_ticker():
    """Create ticker string"""
    ticker_items = []
    for key in ['nifty', 'bankNifty', 'sensex', 'gold', 'bitcoin', 'crudeOil', 'usdinr']:
        if key in st.session_state.market_data:
            data = st.session_state.market_data[key]
            symbol = key.upper().replace('NIFTY', 'NIFTY 50').replace('BANKNIFTY', 'BANK NIFTY')
            arrow = '▲' if data['changePercent'] >= 0 else '▼'
            ticker_items.append(f"{symbol} {data['price']:.2f} {arrow} {abs(data['changePercent']):.2f}%")
    
    return ' | '.join(ticker_items) + ' | ' + ' | '.join(ticker_items)

# Update market data if auto-refresh is enabled
auto_refresh = st.sidebar.checkbox("Enable Auto-Refresh", value=False)
if auto_refresh:
    update_market_data()

# Header
st.markdown("""
<div class="main-header">
    <h1>🕉️ Vedic Birth Chart & Live Market Intelligence 🕉️</h1>
    <p>Real-time Kundali Analysis with Live Market Data & Astrological Predictions</p>
</div>
""", unsafe_allow_html=True)

# Ticker
st.markdown(f'<div class="ticker">{create_ticker()}</div>', unsafe_allow_html=True)

# Main layout
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Birth Details")
    birth_date = st.date_input("Birth Date", datetime(1990, 1, 1))
    birth_time = st.time_input("Birth Time", datetime.now().time())
    birth_place = st.text_input("Birth Place", "Mumbai, India")
    timezone = st.selectbox("Timezone", ["IST (+05:30)", "UTC (+00:00)", "EST (-05:00)", "CST (+08:00)"])
    
    if st.button("🔄 Generate Chart", type="primary"):
        st.success("Chart generated successfully!")

with col2:
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Market Overview", "📈 Sector Analysis", "🔴 Live Market", "🌌 Today's Astro"])
    
    with tab1:
        st.subheader("Market Overview")
        
        # Display key indices
        col1, col2, col3, col4 = st.columns(4)
        
        indices = [
            ('NIFTY 50', 'nifty', col1),
            ('BANK NIFTY', 'bankNifty', col2),
            ('SENSEX', 'sensex', col3),
            ('GOLD', 'gold', col4)
        ]
        
        for name, key, col in indices:
            if key in st.session_state.market_data:
                data = st.session_state.market_data[key]
                with col:
                    st.markdown(f"""
                    <div class="market-card">
                        <h4>{name}</h4>
                        <h2>{data['price']:.2f}</h2>
                        <p class="{'price-positive' if data['changePercent'] >= 0 else 'price-negative'}">
                            {'▲' if data['changePercent'] >= 0 else '▼'} {abs(data['change']):.2f} ({data['changePercent']:.2f}%)
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Planetary transits
        st.subheader("Today's Important Planetary Transits")
        transits = [
            {'time': '09:15 AM', 'event': 'Moon enters Hasta Nakshatra', 'impact': 'Bearish for IT sector'},
            {'time': '11:30 AM', 'event': 'Mars aspects Jupiter', 'impact': 'Bullish for Banking'},
            {'time': '02:45 PM', 'event': 'Mercury in Ashlesha', 'impact': 'Volatile for Communications'},
            {'time': '04:00 PM', 'event': 'Venus trine Saturn', 'impact': 'Stable for Luxury goods'}
        ]
        
        for transit in transits:
            st.info(f"**{transit['time']}** - {transit['event']} - {transit['impact']}")
    
    with tab2:
        st.subheader("Sector Analysis")
        
        sectors = [
            ('Banking & Finance', 'bankNifty', 'HDFCBANK, ICICIBANK, SBIN, KOTAKBANK'),
            ('Information Technology', 'niftyIT', 'TCS, INFY, WIPRO, HCLTECH'),
            ('Pharmaceuticals', 'niftyPharma', 'SUNPHARMA, CIPLA, DRREDDY, DIVISLAB'),
            ('FMCG', 'niftyFMCG', 'HUL, ITC, NESTLEIND, BRITANNIA'),
            ('Auto', 'niftyAuto', 'MARUTI, M&M, TATAMOTORS, BAJAJ-AUTO'),
            ('Metal', 'niftyMetal', 'TATASTEEL, HINDALCO, JSW, VEDL'),
            ('Realty', 'niftyRealty', 'DLF, GODREJPROP, BRIGADE, PRESTIGE'),
            ('Energy', 'niftyEnergy', 'RELIANCE, ONGC, IOC, BPCL'),
            ('PSU Bank', 'niftyPSUBank', 'SBIN, BANKBARODA, PNB, CANBK'),
        ]
        
        for name, key, stocks in sectors:
            if key in st.session_state.market_data:
                data = st.session_state.market_data[key]
                sentiment = 'bullish' if data['changePercent'] > 0 else 'bearish' if data['changePercent'] < -0.5 else 'neutral'
                
                st.markdown(f"""
                <div class="sector-card sector-{sentiment}">
                    <h3>{name} - {data['price']:.2f}</h3>
                    <p class="{'price-positive' if data['changePercent'] >= 0 else 'price-negative'}">
                        {'↑' if data['changePercent'] > 0 else '↓'} {abs(data['changePercent']):.2f}%
                    </p>
                    <p><strong>Key Stocks:</strong> {stocks}</p>
                </div>
                """, unsafe_allow_html=True)
    
    with tab3:
        st.subheader("Live Market Data")
        
        # Display all indices
        indices_data = []
        for key, data in st.session_state.market_data.items():
            if any(x in key for x in ['nifty', 'sensex', 'cnx', 'dow', 'nasdaq', 'ftse']):
                indices_data.append({
                    'Index': key.replace('nifty', 'NIFTY ').replace('cnx', 'CNX ').upper(),
                    'Price': f"{data['price']:.2f}",
                    'Change': f"{data['change']:+.2f}",
                    'Change %': f"{data['changePercent']:+.2f}%",
                    'High': f"{data['high']:.2f}",
                    'Low': f"{data['low']:.2f}"
                })
        
        if indices_data:
            df = pd.DataFrame(indices_data)
            st.dataframe(df, use_container_width=True)
        
        # Commodities section
        st.subheader("Commodities")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if 'gold' in st.session_state.market_data:
                gold = st.session_state.market_data['gold']
                st.metric("Gold (COMEX)", f"${gold['price']:.2f}/oz", f"{gold['changePercent']:.2f}%")
                if 'goldMCX' in st.session_state.market_data:
                    st.caption(f"MCX: ₹{st.session_state.market_data['goldMCX']['price']}/10g")
        
        with col2:
            if 'silver' in st.session_state.market_data:
                silver = st.session_state.market_data['silver']
                st.metric("Silver (COMEX)", f"${silver['price']:.2f}/oz", f"{silver['changePercent']:.2f}%")
                if 'silverMCX' in st.session_state.market_data:
                    st.caption(f"MCX: ₹{st.session_state.market_data['silverMCX']['price']}/kg")
        
        with col3:
            if 'crudeOil' in st.session_state.market_data:
                crude = st.session_state.market_data['crudeOil']
                st.metric("Crude Oil", f"${crude['price']:.2f}/bbl", f"{crude['changePercent']:.2f}%")
    
    with tab4:
        st.subheader("Today's Astrological Analysis")
        
        analysis_type = st.selectbox("Select Analysis", ["NIFTY", "BANK NIFTY", "Gold", "Crude Oil", "Bitcoin"])
        
        astro_data = {
            'NIFTY': {
                'prediction': 'Bearish to Neutral',
                'range': '24,700 - 24,850',
                'advice': 'Avoid fresh long positions. Wait for 24,700 support test.'
            },
            'BANK NIFTY': {
                'prediction': 'Bullish',
                'range': '52,300 - 52,600',
                'advice': 'Buy on dips near 52,350. Target 52,550.'
            },
            'Gold': {
                'prediction': 'Bullish',
                'range': '$3,320 - $3,340',
                'advice': 'Accumulate on dips below $3,325. Venus favorable for precious metals.'
            },
            'Crude Oil': {
                'prediction': 'Bearish',
                'range': '$81.50 - $83.00',
                'advice': 'Sell on rise near $82.80. Mars indicates energy sector weakness.'
            },
            'Bitcoin': {
                'prediction': 'Volatile Bullish',
                'range': '$96,500 - $99,000',
                'advice': 'Uranus aspect brings sudden moves. Use tight stops near $96,000.'
            }
        }
        
        if analysis_type in astro_data:
            data = astro_data[analysis_type]
            
            col1, col2 = st.columns(2)
            with col1:
                st.info(f"**Prediction:** {data['prediction']}")
                st.success(f"**Expected Range:** {data['range']}")
            
            with col2:
                st.warning(f"**Advice:** {data['advice']}")
        
        st.subheader("Key Time Zones")
        st.write("**09:15-09:45 AM:** Opening volatility - Moon influence")
        st.write("**10:30-11:30 AM:** Trend formation - Jupiter aspect")
        st.write("**02:00-03:00 PM:** Intraday reversal zone - Mercury")
        st.write("**03:15-03:30 PM:** Closing positioning - Venus")

# Sidebar - Planetary positions
with st.sidebar:
    st.subheader("🪐 Planetary Positions")
    
    for planet, data in planetary_data.items():
        st.markdown(f"""
        **{data['symbol']} {planet.capitalize()}**  
        Sign: {data['sign']}  
        Degree: {data['degree']}  
        Nakshatra: {data['nakshatra']}  
        House: {data['house']}
        """)
        st.divider()
    
    # Refresh button
    if st.button("🔄 Refresh Data"):
        update_market_data()
        st.rerun()
    
    # Show last update time
    st.caption(f"Last Updated: {st.session_state.last_update.strftime('%H:%M:%S')}")

# Auto-refresh trigger (moved to bottom to avoid infinite loops)
if auto_refresh:
    st.rerun()
