import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta
import time
import threading

# Page configuration
st.set_page_config(
    page_title="Vedic Market Intelligence",
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
        border-radius: 15px;
        margin-bottom: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    .ticker {
        background: #000;
        color: #00ff00;
        padding: 15px;
        font-family: 'Courier New', monospace;
        font-size: 14px;
        border-radius: 10px;
        margin-bottom: 20px;
        overflow: hidden;
        white-space: nowrap;
        animation: scroll-left 30s linear infinite;
    }
    @keyframes scroll-left {
        0% { transform: translate3d(100%, 0, 0); }
        100% { transform: translate3d(-100%, 0, 0); }
    }
    .market-card {
        background: linear-gradient(145deg, #f8f9fa, #e9ecef);
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin: 10px 0;
        border: 2px solid #dee2e6;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        transition: transform 0.3s;
    }
    .market-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.15);
    }
    .price-positive { 
        color: #28a745; 
        font-weight: bold; 
        text-shadow: 0 0 10px rgba(40, 167, 69, 0.3);
    }
    .price-negative { 
        color: #dc3545; 
        font-weight: bold; 
        text-shadow: 0 0 10px rgba(220, 53, 69, 0.3);
    }
    .chart-container {
        background: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin: 20px 0;
    }
    .planetary-card {
        background: linear-gradient(145deg, #e3f2fd, #bbdefb);
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 4px solid #2196f3;
    }
    .sector-card {
        background: white;
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        border-left: 5px solid;
        transition: all 0.3s;
    }
    .sector-card:hover {
        transform: translateX(5px);
    }
    .sector-bullish { border-left-color: #28a745; }
    .sector-bearish { border-left-color: #dc3545; }
    .sector-neutral { border-left-color: #ffc107; }
    .birth-chart-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        grid-template-rows: repeat(4, 1fr);
        gap: 2px;
        background: #8B4513;
        border-radius: 10px;
        overflow: hidden;
        max-width: 400px;
        margin: 0 auto;
    }
    .house-cell {
        background: linear-gradient(45deg, #F5DEB3, #DDD0C0);
        padding: 8px;
        font-size: 10px;
        text-align: center;
        position: relative;
        min-height: 80px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    .house-number {
        position: absolute;
        top: 3px;
        left: 3px;
        font-weight: bold;
        color: #8B4513;
        font-size: 11px;
    }
    .house-sign {
        font-size: 9px;
        font-weight: bold;
        color: #4169E1;
        margin-bottom: 3px;
    }
    .planet-symbol {
        font-size: 12px;
        color: #d32f2f;
        font-weight: bold;
        margin: 1px;
    }
    .center-cell {
        background: linear-gradient(45deg, #ff6b35, #f7931e);
        color: white;
        font-weight: bold;
        font-size: 9px;
    }
    .info-box {
        background: linear-gradient(145deg, #e3f2fd, #bbdefb);
        padding: 15px;
        border-radius: 10px;
        margin: 15px 0;
        border: 1px solid #2196f3;
    }
    .transit-item {
        background: #f8f9fa;
        padding: 10px;
        border-radius: 8px;
        margin: 5px 0;
        border-left: 3px solid #ff6b35;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'market_data' not in st.session_state:
    st.session_state.market_data = {
        # Indian Indices
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
        'hangseng': {'price': 19845.60, 'change': -156.30, 'changePercent': -0.78, 'high': 20050.40, 'low': 19820.30},
        'shanghai': {'price': 3045.80, 'change': -28.60, 'changePercent': -0.93, 'high': 3080.40, 'low': 3040.20},
        
        # Commodities
        'gold': {'price': 3326.50, 'change': 18.30, 'changePercent': 0.55, 'high': 3335.20, 'low': 3308.40},
        'goldMCX': {'price': 72850, 'change': 385, 'changePercent': 0.53, 'high': 73100, 'low': 72500},
        'silver': {'price': 38.25, 'change': -0.32, 'changePercent': -0.83, 'high': 38.65, 'low': 38.10},
        'silverMCX': {'price': 91250, 'change': -650, 'changePercent': -0.71, 'high': 91800, 'low': 90800},
        'crudeOil': {'price': 82.45, 'change': -1.25, 'changePercent': -1.49, 'high': 83.80, 'low': 82.20},
        'crudeOilMCX': {'price': 6842, 'change': -95, 'changePercent': -1.37, 'high': 6950, 'low': 6820},
        
        # Forex
        'usdinr': {'price': 83.45, 'change': -0.12, 'changePercent': -0.14, 'high': 83.58, 'low': 83.42},
        'eurinr': {'price': 90.85, 'change': 0.25, 'changePercent': 0.28, 'high': 90.95, 'low': 90.60},
        'eurusd': {'price': 1.0885, 'change': 0.0045, 'changePercent': 0.42, 'high': 1.0895, 'low': 1.0840},
        
        # Crypto
        'bitcoin': {'price': 97850.50, 'change': 2450.30, 'changePercent': 2.57, 'high': 98500.00, 'low': 95200.00},
        'ethereum': {'price': 3685.40, 'change': 125.60, 'changePercent': 3.53, 'high': 3720.00, 'low': 3560.00},
    }

if 'last_update' not in st.session_state:
    st.session_state.last_update = datetime.now()

if 'planetary_data' not in st.session_state:
    st.session_state.planetary_data = {}

# Dynamic market data updater
def update_market_data():
    """Update market data with realistic movements"""
    for key, data in st.session_state.market_data.items():
        # Different volatility for different asset classes
        if 'bitcoin' in key.lower() or 'ethereum' in key.lower():
            volatility = 0.5  # Higher for crypto
        elif 'gold' in key.lower() or 'silver' in key.lower():
            volatility = 0.1  # Lower for precious metals
        elif 'usd' in key.lower() or 'eur' in key.lower():
            volatility = 0.05  # Very low for forex
        else:
            volatility = 0.2  # Normal for indices
        
        # Generate realistic price movement
        change_percent = random.gauss(0, 1) * volatility
        new_change = data['price'] * change_percent / 100
        
        # Update price and prevent negative prices
        new_price = max(data['price'] + new_change, data['price'] * 0.01)
        data['price'] = new_price
        data['change'] = new_change
        data['changePercent'] = change_percent
        
        # Update high/low
        if data['price'] > data['high']:
            data['high'] = data['price']
        if data['price'] < data['low']:
            data['low'] = data['price']
    
    st.session_state.last_update = datetime.now()

# Get dynamic planetary data
def get_planetary_data():
    """Calculate dynamic planetary positions"""
    now = datetime.now()
    day_of_year = now.timetuple().tm_yday
    
    base_positions = {
        'sun': {'sign': 'Cancer', 'base_degree': 7.25, 'daily_move': 1.0, 'nakshatra': 'Pushya', 'house': 4, 'symbol': '☀️'},
        'moon': {'sign': 'Virgo', 'base_degree': 12.50, 'daily_move': 13.2, 'nakshatra': 'Hasta', 'house': 6, 'symbol': '🌙'},
        'mars': {'sign': 'Virgo', 'base_degree': 25.75, 'daily_move': 0.5, 'nakshatra': 'Chitra', 'house': 6, 'symbol': '♂️'},
        'mercury': {'sign': 'Cancer', 'base_degree': 15.33, 'daily_move': 1.3, 'nakshatra': 'Ashlesha', 'house': 4, 'symbol': '☿️'},
        'jupiter': {'sign': 'Gemini', 'base_degree': 22.17, 'daily_move': 0.08, 'nakshatra': 'Punarvasu', 'house': 3, 'symbol': '♃'},
        'venus': {'sign': 'Gemini', 'base_degree': 8.58, 'daily_move': 1.2, 'nakshatra': 'Ardra', 'house': 3, 'symbol': '♀'},
        'saturn': {'sign': 'Pisces', 'base_degree': 18.42, 'daily_move': 0.03, 'nakshatra': 'Revati', 'house': 12, 'symbol': '♄'},
        'rahu': {'sign': 'Aries', 'base_degree': 5.67, 'daily_move': -0.05, 'nakshatra': 'Ashwini', 'house': 1, 'symbol': '☊'},
        'ketu': {'sign': 'Libra', 'base_degree': 5.67, 'daily_move': -0.05, 'nakshatra': 'Swati', 'house': 7, 'symbol': '☋'},
    }
    
    planetary_data = {}
    for planet, data in base_positions.items():
        current_degree = (data['base_degree'] + (day_of_year * data['daily_move'])) % 30
        degree_str = f"{int(current_degree)}°{int((current_degree % 1) * 60)}'"
        
        planetary_data[planet] = {
            'sign': data['sign'],
            'degree': degree_str,
            'nakshatra': data['nakshatra'],
            'house': data['house'],
            'symbol': data['symbol']
        }
    
    return planetary_data

# Create ticker display
def create_ticker():
    """Create scrolling ticker"""
    ticker_items = []
    for key in ['nifty', 'bankNifty', 'sensex', 'gold', 'bitcoin', 'crudeOil', 'usdinr']:
        if key in st.session_state.market_data:
            data = st.session_state.market_data[key]
            symbol = key.upper().replace('NIFTY', 'NIFTY 50').replace('BANKNIFTY', 'BANK NIFTY')
            arrow = '▲' if data['changePercent'] >= 0 else '▼'
            ticker_items.append(f"{symbol}: {data['price']:.2f} {arrow} {abs(data['changePercent']):.2f}%")
    
    return ' | '.join(ticker_items) + ' | ' + ' | '.join(ticker_items)

# Create birth chart
def create_birth_chart(planetary_data):
    """Generate North Indian style birth chart"""
    # Chart layout mapping
    layout = [
        {'house': 12, 'planets': ['saturn']}, {'house': 1, 'planets': ['rahu']}, 
        {'house': 2, 'planets': []}, {'house': 3, 'planets': ['venus', 'jupiter']},
        {'house': 11, 'planets': []}, {'center': True, 'content': 'birth'}, 
        {'center': True, 'content': 'time'}, {'house': 4, 'planets': ['sun', 'mercury']},
        {'house': 10, 'planets': []}, {'center': True, 'content': 'rasi'}, 
        {'center': True, 'content': 'chart'}, {'house': 5, 'planets': []},
        {'house': 9, 'planets': []}, {'house': 8, 'planets': []}, 
        {'house': 7, 'planets': ['ketu']}, {'house': 6, 'planets': ['moon', 'mars']}
    ]
    
    house_signs = {1: 'Ar', 2: 'Ta', 3: 'Ge', 4: 'Ca', 5: 'Le', 6: 'Vi', 
                   7: 'Li', 8: 'Sc', 9: 'Sg', 10: 'Cp', 11: 'Aq', 12: 'Pi'}
    
    chart_html = '<div class="birth-chart-grid">'
    
    for cell in layout:
        if cell.get('center'):
            if cell['content'] == 'birth':
                chart_html += '<div class="house-cell center-cell">Vedic<br>Chart</div>'
            elif cell['content'] == 'time':
                chart_html += '<div class="house-cell center-cell">Real-time<br>Analysis</div>'
            elif cell['content'] == 'rasi':
                chart_html += '<div class="house-cell center-cell">Rasi<br>Kundali</div>'
            else:
                chart_html += '<div class="house-cell center-cell">Live<br>Market</div>'
        else:
            house_num = cell['house']
            sign = house_signs[house_num]
            planets_html = ''
            
            for planet in cell['planets']:
                if planet in planetary_data:
                    planets_html += f'<span class="planet-symbol">{planetary_data[planet]["symbol"]}</span>'
            
            chart_html += f'''
            <div class="house-cell">
                <div class="house-number">{house_num}</div>
                <div class="house-sign">{sign}</div>
                <div>{planets_html}</div>
            </div>
            '''
    
    chart_html += '</div>'
    return chart_html

# Header
st.markdown("""
<div class="main-header">
    <h1>🕉️ Vedic Birth Chart & Live Market Intelligence 🕉️</h1>
    <p>Real-time Kundali Analysis with Live Market Data & Astrological Predictions</p>
</div>
""", unsafe_allow_html=True)

# Auto-refresh controls
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    auto_refresh = st.checkbox("🔄 Enable Auto-Refresh (every 5 seconds)", value=True)
with col2:
    if st.button("📈 Update Now", type="primary"):
        update_market_data()
        st.session_state.planetary_data = get_planetary_data()
        st.success("Data updated!")
with col3:
    refresh_rate = st.selectbox("Refresh Rate", [3, 5, 10, 30], index=1)

# Auto-refresh logic
if auto_refresh:
    time.sleep(refresh_rate)
    update_market_data()
    st.session_state.planetary_data = get_planetary_data()
    st.rerun()

# Update planetary data if not exists
if not st.session_state.planetary_data:
    st.session_state.planetary_data = get_planetary_data()

# Ticker display
ticker_text = create_ticker()
st.markdown(f'<div class="ticker">{ticker_text}</div>', unsafe_allow_html=True)

# Sidebar - Birth Chart Inputs
with st.sidebar:
    st.header("📅 Birth Chart Details")
    
    birth_date = st.date_input("Birth Date", datetime(1990, 1, 1))
    birth_time = st.time_input("Birth Time", datetime.now().time())
    birth_place = st.text_input("Birth Place", "Mumbai, India")
    timezone = st.selectbox("Timezone", ["IST (+05:30)", "UTC (+00:00)", "EST (-05:00)", "CST (+08:00)"])
    
    if st.button("✨ Generate Chart", type="primary"):
        st.session_state.planetary_data = get_planetary_data()
        st.success("Birth chart updated!")
        st.rerun()
    
    st.header("🪐 Current Planetary Positions")
    for planet, data in st.session_state.planetary_data.items():
        st.markdown(f"""
        <div class="planetary-card">
            <strong>{data['symbol']} {planet.capitalize()}</strong><br>
            Sign: {data['sign']}<br>
            Degree: {data['degree']}<br>
            Nakshatra: {data['nakshatra']}<br>
            House: {data['house']}
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.caption(f"Last Updated: {st.session_state.last_update.strftime('%H:%M:%S')}")

# Main content layout
main_col1, main_col2 = st.columns([1, 1])

with main_col1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("🎯 Birth Chart - North Indian Style")
    
    # Current info
    st.markdown(f"""
    <div class="info-box">
        <strong>📅 Date & Time:</strong> {birth_date} {birth_time}<br>
        <strong>📍 Location:</strong> {birth_place}<br>
        <strong>🕰️ Timezone:</strong> {timezone}<br>
        <strong>🔄 Last Update:</strong> {st.session_state.last_update.strftime('%H:%M:%S')}
    </div>
    """, unsafe_allow_html=True)
    
    # Birth chart
    chart_html = create_birth_chart(st.session_state.planetary_data)
    st.markdown(chart_html, unsafe_allow_html=True)
    
    # Today's transits
    st.markdown("""
    <div class="info-box">
        <h4>🌌 Today's Key Planetary Transits</h4>
        <div class="transit-item">
            <strong>09:15 AM:</strong> Moon enters Hasta Nakshatra - Bearish for IT sector
        </div>
        <div class="transit-item">
            <strong>11:30 AM:</strong> Mars aspects Jupiter - Bullish for Banking
        </div>
        <div class="transit-item">
            <strong>02:45 PM:</strong> Mercury in Ashlesha - Volatile for Communications
        </div>
        <div class="transit-item">
            <strong>04:00 PM:</strong> Venus trine Saturn - Stable for Luxury goods
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

with main_col2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("📊 Live Market Dashboard")
    
    # Key market cards
    major_markets = ['nifty', 'bankNifty', 'sensex', 'gold', 'bitcoin', 'usdinr']
    
    for i in range(0, len(major_markets), 2):
        col1, col2 = st.columns(2)
        
        for j, col in enumerate([col1, col2]):
            if i + j < len(major_markets):
                key = major_markets[i + j]
                data = st.session_state.market_data[key]
                name = key.replace('nifty', 'NIFTY 50').replace('bankNifty', 'BANK NIFTY').upper()
                
                color_class = "price-positive" if data['changePercent'] >= 0 else "price-negative"
                arrow = "▲" if data['changePercent'] >= 0 else "▼"
                
                col.markdown(f"""
                <div class="market-card">
                    <h4>{name}</h4>
                    <h2>{data['price']:.2f}</h2>
                    <p class="{color_class}">
                        {arrow} {abs(data['change']):.2f} ({data['changePercent']:+.2f}%)
                    </p>
                    <small>High: {data['high']:.2f} | Low: {data['low']:.2f}</small>
                </div>
                """, unsafe_allow_html=True)
    
    # Market influences
    st.markdown("""
    <div class="info-box">
        <h4>🌟 Current Market Influences</h4>
        <p>🌙 <strong>Moon in Virgo:</strong> Technical analysis favored for IT stocks</p>
        <p>♂️ <strong>Mars aspect:</strong> Banking sector showing strength</p>
        <p>☿️ <strong>Mercury transit:</strong> Communication stocks volatile</p>
        <p>♃ <strong>Jupiter favorable:</strong> Long-term investments positive</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Main tabs for detailed analysis
tab1, tab2, tab3, tab4 = st.tabs(["📈 Market Analysis", "🔴 Live Data", "🌌 Astro Analysis", "📊 Sector Overview"])

with tab1:
    st.subheader("📈 Comprehensive Market Analysis")
    
    analysis_tabs = st.tabs(["Indian Indices", "Global Markets", "Commodities", "Forex & Crypto"])
    
    with analysis_tabs[0]:
        st.subheader("🇮🇳 Indian Market Indices")
        
        # Create market table
        indian_indices = ['nifty', 'bankNifty', 'sensex', 'niftyIT', 'niftyPharma', 'niftyAuto', 'niftyFMCG']
        table_data = []
        
        for key in indian_indices:
            data = st.session_state.market_data[key]
            name = key.replace('nifty', 'NIFTY ').replace('bankNifty', 'BANK NIFTY').upper()
            table_data.append({
                'Index': name,
                'Price': f"{data['price']:.2f}",
                'Change': f"{data['change']:+.2f}",
                'Change %': f"{data['changePercent']:+.2f}%",
                'High': f"{data['high']:.2f}",
                'Low': f"{data['low']:.2f}",
                'Status': "🟢 Bullish" if data['changePercent'] > 0 else "🔴 Bearish"
            })
        
        df = pd.DataFrame(table_data)
        st.dataframe(df, use_container_width=True)
    
    with analysis_tabs[1]:
        st.subheader("🌍 Global Market Indices")
        
        global_indices = ['dowJones', 'sp500', 'nasdaq', 'ftse', 'dax', 'nikkei']
        
        for i in range(0, len(global_indices), 3):
            cols = st.columns(3)
            for j, col in enumerate(cols):
                if i + j < len(global_indices):
                    key = global_indices[i + j]
                    data = st.session_state.market_data[key]
                    
                    flags = {'dowJones': '🇺🇸', 'sp500': '🇺🇸', 'nasdaq': '🇺🇸', 
                            'ftse': '🇬🇧', 'dax': '🇩🇪', 'nikkei': '🇯🇵'}
                    
                    flag = flags.get(key, '🌍')
                    name = key.replace('dowJones', 'Dow Jones').replace('sp500', 'S&P 500').upper()
                    
                    col.metric(
                        f"{flag} {name}",
                        f"{data['price']:.2f}",
                        f"{data['changePercent']:+.2f}%"
                    )
    
    with analysis_tabs[2]:
        st.subheader("🏆 Commodities Market")
        
        commodities = ['gold', 'silver', 'crudeOil']
        
        for key in commodities:
            data = st.session_state.market_data[key]
            mcx_key = key + 'MCX'
            
            col1, col2 = st.columns(2)
            
            with col1:
                name = key.replace('crudeOil', 'Crude Oil').title()
                symbol = '$' if key != 'crudeOil' else '$'
                unit = '/oz' if key in ['gold', 'silver'] else '/bbl'
                
                st.metric(
                    f"{name} (COMEX)",
                    f"{symbol}{data['price']:.2f}{unit}",
                    f"{data['changePercent']:+.2f}%"
                )
            
            with col2:
                if mcx_key in st.session_state.market_data:
                    mcx_data = st.session_state.market_data[mcx_key]
                    mcx_unit = '/10g' if key == 'gold' else '/kg' if key == 'silver' else '/bbl'
                    
                    st.metric(
                        f"{name} (MCX)",
                        f"₹{mcx_data['price']:.0f}{mcx_unit}",
                        f"{mcx_data['changePercent']:+.2f}%"
                    )
    
    with analysis_tabs[3]:
        st.subheader("💱 Forex & Cryptocurrency")
        
        forex_crypto = ['usdinr', 'eurusd', 'bitcoin', 'ethereum']
        
        for i in range(0, len(forex_crypto), 2):
            cols = st.columns(2)
            for j, col in enumerate(cols):
                if i + j < len(forex_crypto):
                    key = forex_crypto[i + j]
                    data = st.session_state.market_data[key]
                    
                    if key in ['bitcoin', 'ethereum']:
                        name = key.title()
                        prefix = '$'
                        decimals = 2
                    else:
                        name = key.upper().replace('USDINR', 'USD/INR').replace('EURUSD', 'EUR/USD')
                        prefix = ''
                        decimals = 4
                    
                    col.metric(
                        name,
                        f"{prefix}{data['price']:.{decimals}f}",
                        f"{data['changePercent']:+.2f}%"
                    )

with tab2:
    st.subheader("🔴 Live Market Data Stream")
    
    # Real-time highlights
    st.markdown("### 📊 Market Highlights")
    
    highlight_col1, highlight_col2, highlight_col3, highlight_col4 = st.columns(4)
    
    with highlight_col1:
        st.metric("Market Status", "OPEN", "Live Trading")
    with highlight_col2:
        advances = 1285
        declines = 765
        st.metric("Advances/Declines", f"{advances}/{declines}", f"Ratio: {advances/declines:.2f}")
    with highlight_col3:
        st.metric("FII Activity", "₹2,345 Cr", "Net Buy")
    with highlight_col4:
        st.metric("VIX", "14.25", "-3.45%")
    
    # Live market grid
    st.markdown("### 📈 Live Price Updates")
    
    live_markets = ['nifty', 'bankNifty', 'sensex', 'gold', 'bitcoin', 'crudeOil']
    
    for i in range(0, len(live_markets), 3):
        cols = st.columns(3)
        for j, col in enumerate(cols):
            if i + j < len(live_markets):
                key = live_markets[i + j]
                data = st.session_state.market_data[key]
                name = key.replace('nifty', 'NIFTY 50').replace('bankNifty', 'BANK NIFTY').replace('crudeOil', 'CRUDE OIL').upper()
                
                color_class = "price-positive" if data['changePercent'] >= 0 else "price-negative"
                
                col.markdown(f"""
                <div class="market-card">
                    <h4>🔴 LIVE - {name}</h4>
                    <h3>{data['price']:.2f}</h3>
                    <p class="{color_class}">
                        {'▲' if data['changePercent'] >= 0 else '▼'} {abs(data['change']):.2f} ({data['changePercent']:+.2f}%)
                    </p>
                    <small>H: {data['high']:.2f} | L: {data['low']:.2f}</small>
                </div>
                """, unsafe_allow_html=True)

with tab3:
    st.subheader("🌌 Astrological Market Analysis")
    
    astro_choice = st.selectbox("Select Market for Astrological Analysis", 
                               ["NIFTY", "BANK NIFTY", "Gold", "Crude Oil", "Bitcoin"])
    
    predictions = {
        'NIFTY': {
            'trend': 'Bearish to Neutral',
            'range': '24,700 - 24,850',
            'advice': 'Avoid fresh long positions. Wait for 24,700 support test.',
            'key_times': [
                '09:15-09:45 AM: Bearish opening (Moon in 6th house)',
                '10:30-11:30 AM: Recovery expected (Jupiter aspect)',
                '02:00-03:00 PM: Volatile (Mercury influence)',
                '03:15-03:30 PM: Day\'s decision time'
            ]
        },
        'BANK NIFTY': {
            'trend': 'Bullish',
            'range': '52,300 - 52,600',
            'advice': 'Buy on dips near 52,350. Target 52,550.',
            'key_times': [
                '09:15-10:00 AM: Positive opening expected',
                '11:00-12:00 PM: Strong momentum (Jupiter favorable)',
                '01:30-02:30 PM: Profit booking zone',
                '03:00-03:30 PM: EOD positioning'
            ]
        },
        'Gold': {
            'trend': 'Bullish',
            'range': '$3,320 - $3,340',
            'advice': 'Accumulate on dips below $3,325. Venus favorable for precious metals.',
            'key_times': [
                '09:00 AM: Asian session positive',
                '01:30 PM: European session momentum',
                '07:00 PM: US session volatility',
                '11:30 PM: Fed speakers impact'
            ]
        },
        'Crude Oil': {
            'trend': 'Bearish',
            'range': '$81.50 - $83.00',
            'advice': 'Sell on rise near $82.80. Mars indicates energy sector weakness.',
            'key_times': [
                '09:30 AM: API data impact',
                '11:00 AM: EIA inventory report',
                '02:30 PM: OPEC news sensitivity',
                '04:00 PM: US market close effect'
            ]
        },
        'Bitcoin': {
            'trend': 'Volatile Bullish',
            'range': '$96,500 - $99,000',
            'advice': 'Uranus aspect brings sudden moves. Use tight stops near $96,000.',
            'key_times': [
                '24/7 Market: High volatility periods',
                'US Morning: Institutional buying',
                'Asian Evening: Retail activity',
                'Weekend: Lower liquidity risks'
            ]
        }
    }
    
    pred = predictions.get(astro_choice, predictions['NIFTY'])
    
    col1, col2 = st.columns(2)
    
    with col1:
        trend_color = "🟢" if "Bullish" in pred['trend'] else "🔴" if "Bearish" in pred['trend'] else "🟡"
        
        st.markdown(f"""
        <div class="info-box">
            <h4>🔮 {astro_choice} Prediction</h4>
            <p><strong>Trend:</strong> {trend_color} {pred['trend']}</p>
            <p><strong>Expected Range:</strong> {pred['range']}</p>
            <p><strong>Astrological Advice:</strong> {pred['advice']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-box">
            <h4>🪐 Current Planetary Influences</h4>
            <p>☽ <strong>Moon in Virgo (6th house):</strong> Technical analysis favored</p>
            <p>♃ <strong>Jupiter in Gemini (3rd house):</strong> Communication sector volatility</p>
            <p>☿ <strong>Mercury in Cancer (4th house):</strong> Domestic market focus</p>
            <p>♂ <strong>Mars in Virgo (6th house):</strong> Healthcare sector active</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### ⏰ Key Time Zones & Planetary Windows")
    
    for time_info in pred['key_times']:
        st.markdown(f"""
        <div class="transit-item">
            {time_info}
        </div>
        """, unsafe_allow_html=True)

with tab4:
    st.subheader("📊 Sector Performance Overview")
    
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
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                    <h3>{name}</h3>
                    <span style="color: {'#28a745' if data['changePercent'] > 0 else '#dc3545'}; font-size: 24px; font-weight: bold;">
                        {'↑' if data['changePercent'] > 0 else '↓'} {abs(data['changePercent']):.2f}%
                    </span>
                </div>
                <p><strong>Index Value:</strong> {data['price']:.2f}</p>
                <p><strong>Key Stocks:</strong> {stocks}</p>
                <p><strong>Market Sentiment:</strong> {sentiment.title()}</p>
            </div>
            """, unsafe_allow_html=True)

# Footer
st.markdown("---")
footer_col1, footer_col2, footer_col3 = st.columns(3)

with footer_col1:
    st.caption(f"🕐 Last Updated: {st.session_state.last_update.strftime('%H:%M:%S')}")
with footer_col2:
    st.caption("📊 Data simulated for demonstration purposes")
with footer_col3:
    st.caption("🕉️ Vedic Market Intelligence - Ancient Wisdom, Modern Markets")
