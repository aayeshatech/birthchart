import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta
import time

# Page configuration
st.set_page_config(
    page_title="Vedic Market Intelligence Pro",
    page_icon="🕉️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Advanced CSS with modern design
st.markdown("""
<style>
.main-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 20px;
    text-align: center;
    border-radius: 15px;
    margin-bottom: 20px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.1);
}
.market-section {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    color: white;
    padding: 15px;
    border-radius: 12px;
    margin: 10px 0;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}
.equity-section {
    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    color: white;
    padding: 15px;
    border-radius: 12px;
    margin: 10px 0;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}
.commodity-section {
    background: linear-gradient(135deg, #fad0c4 0%, #ffd1ff 100%);
    color: #333;
    padding: 15px;
    border-radius: 12px;
    margin: 10px 0;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}
.global-section {
    background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
    color: #333;
    padding: 15px;
    border-radius: 12px;
    margin: 10px 0;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}
.market-card {
    background: rgba(255,255,255,0.95);
    color: #333;
    padding: 15px;
    border-radius: 10px;
    text-align: center;
    margin: 8px 0;
    border: 1px solid rgba(255,255,255,0.2);
    backdrop-filter: blur(10px);
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    transition: transform 0.3s ease;
}
.market-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 20px rgba(0,0,0,0.15);
}
.status-open {
    background: linear-gradient(45deg, #11998e, #38ef7d);
    color: white;
    padding: 5px 12px;
    border-radius: 20px;
    font-weight: bold;
    font-size: 0.8em;
}
.status-closed {
    background: linear-gradient(45deg, #ff416c, #ff4b2b);
    color: white;
    padding: 5px 12px;
    border-radius: 20px;
    font-weight: bold;
    font-size: 0.8em;
}
.status-pre-market {
    background: linear-gradient(45deg, #ffecd2, #fcb69f);
    color: #333;
    padding: 5px 12px;
    border-radius: 20px;
    font-weight: bold;
    font-size: 0.8em;
}
.positive { color: #28a745; font-weight: bold; }
.negative { color: #dc3545; font-weight: bold; }
.ticker-box {
    background: linear-gradient(45deg, #000428, #004e92);
    color: #00ff00;
    padding: 12px;
    font-family: 'Courier New', monospace;
    border-radius: 10px;
    margin: 10px 0;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
}
.planetary-indicator {
    background: linear-gradient(45deg, #ff9a56, #ff6b35);
    color: white;
    padding: 10px;
    border-radius: 8px;
    margin: 8px 0;
    text-align: center;
    font-weight: bold;
}
.quick-actions {
    background: rgba(255,255,255,0.1);
    backdrop-filter: blur(10px);
    padding: 15px;
    border-radius: 12px;
    margin: 10px 0;
    border: 1px solid rgba(255,255,255,0.2);
}
.sector-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 15px;
    margin: 15px 0;
}
.trend-bullish { color: #28a745; font-weight: bold; }
.trend-bearish { color: #dc3545; font-weight: bold; }
.trend-neutral { color: #ffc107; font-weight: bold; }
.trend-volatile { color: #ff6b35; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# Initialize session state with enhanced data
try:
    if 'market_data' not in st.session_state:
        st.session_state.market_data = {
            # Equity Markets (9:15 AM - 3:30 PM IST)
            'NIFTY': {'price': 24780.50, 'change': -0.50, 'high': 24920, 'low': 24750, 'market_type': 'equity'},
            'BANKNIFTY': {'price': 52435.75, 'change': 0.60, 'high': 52580, 'low': 52120, 'market_type': 'equity'},
            'SENSEX': {'price': 81342.15, 'change': -0.35, 'high': 81650, 'low': 81250, 'market_type': 'equity'},
            'NIFTY_IT': {'price': 32156, 'change': -1.31, 'high': 32600, 'low': 32100, 'market_type': 'equity'},
            'NIFTY_PHARMA': {'price': 18925, 'change': 0.84, 'high': 19050, 'low': 18750, 'market_type': 'equity'},
            'NIFTY_BANK': {'price': 52435, 'change': 0.60, 'high': 52580, 'low': 52120, 'market_type': 'equity'},
            'NIFTY_AUTO': {'price': 25380, 'change': -0.25, 'high': 25550, 'low': 25200, 'market_type': 'equity'},
            
            # Commodities (5:00 AM - 11:55 PM IST)
            'GOLD': {'price': 71850, 'change': 0.55, 'high': 72100, 'low': 71500, 'market_type': 'commodity'},
            'SILVER': {'price': 91250, 'change': 1.20, 'high': 91800, 'low': 90200, 'market_type': 'commodity'},
            'CRUDE': {'price': 6845, 'change': -1.49, 'high': 6920, 'low': 6800, 'market_type': 'commodity'},
            'NATURALGAS': {'price': 232, 'change': 0.85, 'high': 245, 'low': 220, 'market_type': 'commodity'},
            'COPPER': {'price': 755, 'change': -0.65, 'high': 765, 'low': 745, 'market_type': 'commodity'},
            
            # Global & Forex (5:00 AM - 11:55 PM IST)
            'BITCOIN': {'price': 97850.50, 'change': 2.57, 'high': 98500, 'low': 95200, 'market_type': 'global'},
            'DOWJONES': {'price': 44565, 'change': 0.85, 'high': 44750, 'low': 44200, 'market_type': 'global'},
            'NASDAQ': {'price': 20173, 'change': 1.25, 'high': 20350, 'low': 19850, 'market_type': 'global'},
            'SP500': {'price': 5547, 'change': 0.95, 'high': 5565, 'low': 5520, 'market_type': 'global'},
            'USDINR': {'price': 83.45, 'change': -0.14, 'high': 83.58, 'low': 83.42, 'market_type': 'forex'},
            'EURINR': {'price': 88.25, 'change': 0.35, 'high': 88.50, 'low': 87.90, 'market_type': 'forex'},
            'GBPINR': {'price': 102.75, 'change': -0.22, 'high': 103.05, 'low': 102.50, 'market_type': 'forex'},
            'JPYINR': {'price': 0.56, 'change': 0.18, 'high': 0.57, 'low': 0.55, 'market_type': 'forex'}
        }
    
    if 'last_update' not in st.session_state:
        st.session_state.last_update = datetime.now()
        
    if 'astro_data_date' not in st.session_state:
        st.session_state.astro_data_date = datetime.now().strftime('%Y-%m-%d %H:%M')

except Exception as e:
    st.error(f"Error initializing data: {e}")

# Market timing functions
def get_market_status(market_type):
    current_time = datetime.now()
    current_hour = current_time.hour
    current_minute = current_time.minute
    current_total_minutes = current_hour * 60 + current_minute
    
    if market_type == 'equity':
        # Indian Equity Market: 9:15 AM - 3:30 PM
        market_open = 9 * 60 + 15  # 9:15 AM
        market_close = 15 * 60 + 30  # 3:30 PM
        
        if market_open <= current_total_minutes <= market_close:
            return "OPEN", "🟢"
        elif current_total_minutes < market_open:
            return "PRE-MARKET", "🟡"
        else:
            return "CLOSED", "🔴"
    
    elif market_type in ['commodity', 'global', 'forex']:
        # Commodity & Global Markets: 5:00 AM - 11:55 PM
        market_open = 5 * 60  # 5:00 AM
        market_close = 23 * 60 + 55  # 11:55 PM
        
        if market_open <= current_total_minutes <= market_close:
            return "OPEN", "🟢"
        elif current_total_minutes < market_open:
            return "PRE-MARKET", "🟡"
        else:
            return "CLOSED", "🔴"
    
    return "UNKNOWN", "⚫"

def get_planetary_influence():
    current_time = datetime.now()
    hour = current_time.hour
    
    planetary_hours = {
        (5, 6): ("Saturn", "♄", "Restrictive energy, metals weak"),
        (6, 7): ("Jupiter", "♃", "Expansive energy, banking strong"),
        (7, 8): ("Mars", "♂️", "Aggressive energy, defense up"),
        (8, 9): ("Sun", "☀️", "Solar energy, pharma strong"),
        (9, 10): ("Venus", "♀", "Harmonious energy, auto up"),
        (10, 11): ("Mercury", "☿", "Communicative energy, IT mixed"),
        (11, 12): ("Moon", "🌙", "Emotional energy, FMCG strong"),
        (12, 13): ("Saturn", "♄", "Restrictive energy, profit booking"),
        (13, 14): ("Jupiter", "♃", "Expansive energy, banking rally"),
        (14, 15): ("Mars", "♂️", "Volatile energy, high risk"),
        (15, 16): ("Sun", "☀️", "Solar energy, closing strength"),
        (16, 17): ("Venus", "♀", "Evening harmony, recovery"),
        (17, 18): ("Mercury", "☿", "Tech hour, crypto active"),
        (18, 19): ("Moon", "🌙", "Emotional phase, commodities"),
        (19, 20): ("Saturn", "♄", "US pre-market caution"),
        (20, 21): ("Jupiter", "♃", "US session strength"),
        (21, 22): ("Mars", "♂️", "US volatility peak"),
        (22, 23): ("Sun", "☀️", "Late session energy"),
        (23, 0): ("Venus", "♀", "Night harmony"),
        (0, 5): ("Mercury", "☿", "Night tech trading")
    }
    
    for (start, end), (planet, symbol, influence) in planetary_hours.items():
        if start <= hour < end:
            return planet, symbol, influence
    
    return "Mixed", "🌟", "Multiple planetary influences"

def update_market_data():
    try:
        for market in st.session_state.market_data:
            data = st.session_state.market_data[market]
            change = (random.random() - 0.5) * 2
            data['change'] += change * 0.1
            data['price'] *= (1 + change/1000)
            
            if data['price'] > data['high']:
                data['high'] = data['price']
            if data['price'] < data['low']:
                data['low'] = data['price']
        
        st.session_state.last_update = datetime.now()
        return True
    except Exception as e:
        st.error(f"Error updating market data: {e}")
        return False

# Dynamic Header with Live Status
st.markdown("""
<div class="main-header">
    <h1>🕉️ Vedic Market Intelligence Pro</h1>
    <p>Advanced Multi-Asset Astrological Trading Platform</p>
    <small>Real-time Planetary Analysis • Equity • Commodities • Global Markets • Forex</small>
</div>
""", unsafe_allow_html=True)

# Control Panel
control_col1, control_col2, control_col3, control_col4, control_col5 = st.columns(5)

with control_col1:
    auto_refresh = st.checkbox("🔄 Auto Refresh", value=True)

with control_col2:
    if st.button("📊 Update All", type="primary"):
        if update_market_data():
            st.success("All markets updated!")
        st.rerun()

with control_col3:
    refresh_rate = st.selectbox("Refresh Rate", [5, 10, 30, 60], index=1)

with control_col4:
    view_mode = st.selectbox("Display Mode", ["Professional", "Advanced", "Compact"])

with control_col5:
    market_filter = st.selectbox("Show Markets", ["All Markets", "Open Only", "Active Signals"])

# Current Planetary Status
current_planet, current_symbol, current_influence = get_planetary_influence()
current_time = datetime.now()

st.markdown(f"""
<div class="planetary-indicator">
    <h3>{current_symbol} Current Planetary Hour: {current_planet}</h3>
    <p>⏰ {current_time.strftime('%H:%M:%S')} IST | 🌟 {current_influence}</p>
</div>
""", unsafe_allow_html=True)

# Live Ticker
try:
    ticker_items = []
    active_markets = [k for k, v in st.session_state.market_data.items() 
                     if get_market_status(v['market_type'])[0] in ['OPEN', 'PRE-MARKET']][:8]
    
    for market in active_markets:
        data = st.session_state.market_data[market]
        arrow = '📈' if data['change'] >= 0 else '📉'
        ticker_items.append(f"{market}: {data['price']:.1f} {arrow} {abs(data['change']):.2f}%")
    
    ticker_text = " | ".join(ticker_items)
    st.markdown(f'<div class="ticker-box">🔴 LIVE: {ticker_text}</div>', unsafe_allow_html=True)
except Exception as e:
    st.error(f"Error creating ticker: {e}")

# MAIN DASHBOARD - SEPARATED BY MARKET TYPE
main_tab1, main_tab2, main_tab3 = st.tabs(["💼 EQUITY MARKETS", "🏭 COMMODITY MARKETS", "🌍 GLOBAL & FOREX"])

# ==================== EQUITY MARKETS TAB ====================
with main_tab1:
    st.markdown("""
    <div class="equity-section">
        <h2>📊 Indian Equity Markets</h2>
        <p>Trading Hours: 9:15 AM - 3:30 PM IST | Live Planetary Analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Equity Market Status
    equity_status, equity_icon = get_market_status('equity')
    
    status_col1, status_col2, status_col3 = st.columns(3)
    with status_col1:
        st.markdown(f"""
        <div class="market-card">
            <h4>Market Status</h4>
            <h2>{equity_icon} {equity_status}</h2>
            <p>Indian Equity Markets</p>
        </div>
        """, unsafe_allow_html=True)
    
    with status_col2:
        st.markdown(f"""
        <div class="market-card">
            <h4>Session Time</h4>
            <h2>9:15 AM - 3:30 PM</h2>
            <p>IST Trading Hours</p>
        </div>
        """, unsafe_allow_html=True)
    
    with status_col3:
        planet_effect = "Bullish" if current_planet in ['Jupiter', 'Venus', 'Sun'] else "Bearish" if current_planet in ['Saturn', 'Mars'] else "Neutral"
        st.markdown(f"""
        <div class="market-card">
            <h4>Planetary Effect</h4>
            <h2 class="trend-{planet_effect.lower()}">{planet_effect}</h2>
            <p>{current_planet} Influence</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Equity Indices
    st.markdown("### 📈 Major Indices")
    equity_indices = ['NIFTY', 'BANKNIFTY', 'SENSEX']
    equity_cols = st.columns(3)
    
    for idx, market in enumerate(equity_indices):
        if market in st.session_state.market_data:
            data = st.session_state.market_data[market]
            color_class = "positive" if data['change'] >= 0 else "negative"
            arrow = "📈" if data['change'] >= 0 else "📉"
            
            with equity_cols[idx]:
                st.markdown(f"""
                <div class="market-card">
                    <h4>{market}</h4>
                    <h2>{data['price']:.2f}</h2>
                    <p class="{color_class}">
                        {arrow} {abs(data['change']):.2f}%
                    </p>
                    <small>H: {data['high']:.1f} | L: {data['low']:.1f}</small>
                </div>
                """, unsafe_allow_html=True)
    
    # Sector Indices
    st.markdown("### 🏭 Sector Performance")
    sector_indices = ['NIFTY_BANK', 'NIFTY_IT', 'NIFTY_PHARMA', 'NIFTY_AUTO']
    sector_cols = st.columns(4)
    
    for idx, market in enumerate(sector_indices):
        if market in st.session_state.market_data:
            data = st.session_state.market_data[market]
            color_class = "positive" if data['change'] >= 0 else "negative"
            arrow = "📈" if data['change'] >= 0 else "📉"
            
            display_name = market.replace('NIFTY_', '').title()
            
            with sector_cols[idx]:
                st.markdown(f"""
                <div class="market-card">
                    <h5>{display_name}</h5>
                    <h3>{data['price']:.0f}</h3>
                    <p class="{color_class}">
                        {arrow} {abs(data['change']):.2f}%
                    </p>
                </div>
                """, unsafe_allow_html=True)
    
    # Equity Quick Actions
    st.markdown("### ⚡ Live Equity Signals")
    if equity_status == "OPEN":
        signal_col1, signal_col2, signal_col3 = st.columns(3)
        
        with signal_col1:
            if current_planet in ['Jupiter', 'Venus']:
                st.success("🟢 BULLISH HOUR - Consider LONG positions in Banking & FMCG")
            else:
                st.info("🟡 NEUTRAL - Wait for better planetary alignment")
        
        with signal_col2:
            if current_planet in ['Saturn', 'Mars']:
                st.error("🔴 BEARISH HOUR - Consider SHORT positions or book profits")
            else:
                st.info("📊 Monitor sector rotation based on planetary hours")
        
        with signal_col3:
            st.info(f"⏰ Next planetary shift in ~1 hour | Current: {current_planet} {current_symbol}")
    else:
        st.warning(f"📴 Equity markets are {equity_status}. Next session: 9:15 AM IST")

# ==================== COMMODITY MARKETS TAB ====================
with main_tab2:
    st.markdown("""
    <div class="commodity-section">
        <h2>🏭 Commodity Markets</h2>
        <p>Trading Hours: 5:00 AM - 11:55 PM IST | Extended Planetary Coverage</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Commodity Market Status
    commodity_status, commodity_icon = get_market_status('commodity')
    
    commodity_status_col1, commodity_status_col2, commodity_status_col3 = st.columns(3)
    with commodity_status_col1:
        st.markdown(f"""
        <div class="market-card">
            <h4>Market Status</h4>
            <h2>{commodity_icon} {commodity_status}</h2>
            <p>Commodity Markets</p>
        </div>
        """, unsafe_allow_html=True)
    
    with commodity_status_col2:
        st.markdown(f"""
        <div class="market-card">
            <h4>Session Time</h4>
            <h2>5:00 AM - 11:55 PM</h2>
            <p>Extended Trading Hours</p>
        </div>
        """, unsafe_allow_html=True)
    
    with commodity_status_col3:
        commodity_effect = "Strong" if current_planet in ['Jupiter', 'Venus'] else "Weak" if current_planet == 'Saturn' else "Volatile"
        st.markdown(f"""
        <div class="market-card">
            <h4>Commodity Strength</h4>
            <h2 class="trend-{commodity_effect.lower()}">{commodity_effect}</h2>
            <p>Planetary Influence</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Precious Metals
    st.markdown("### 🥇 Precious Metals")
    metals_cols = st.columns(2)
    
    for idx, market in enumerate(['GOLD', 'SILVER']):
        if market in st.session_state.market_data:
            data = st.session_state.market_data[market]
            color_class = "positive" if data['change'] >= 0 else "negative"
            arrow = "📈" if data['change'] >= 0 else "📉"
            
            with metals_cols[idx]:
                st.markdown(f"""
                <div class="market-card">
                    <h4>{'🥇 ' if market == 'GOLD' else '🥈 '}{market}</h4>
                    <h2>₹{data['price']:,.0f}</h2>
                    <p class="{color_class}">
                        {arrow} {abs(data['change']):.2f}%
                    </p>
                    <small>H: ₹{data['high']:,.0f} | L: ₹{data['low']:,.0f}</small>
                </div>
                """, unsafe_allow_html=True)
    
    # Energy & Industrial
    st.markdown("### ⚡ Energy & Industrial Commodities")
    energy_cols = st.columns(3)
    
    for idx, market in enumerate(['CRUDE', 'NATURALGAS', 'COPPER']):
        if market in st.session_state.market_data:
            data = st.session_state.market_data[market]
            color_class = "positive" if data['change'] >= 0 else "negative"
            arrow = "📈" if data['change'] >= 0 else "📉"
            
            icon = "🛢️" if market == 'CRUDE' else "🔥" if market == 'NATURALGAS' else "🔶"
            
            with energy_cols[idx]:
                st.markdown(f"""
                <div class="market-card">
                    <h5>{icon} {market}</h5>
                    <h3>₹{data['price']:,.0f}</h3>
                    <p class="{color_class}">
                        {arrow} {abs(data['change']):.2f}%
                    </p>
                </div>
                """, unsafe_allow_html=True)
    
    # Commodity Signals
    st.markdown("### 🎯 Live Commodity Signals")
    if commodity_status == "OPEN":
        commodity_signal_col1, commodity_signal_col2 = st.columns(2)
        
        with commodity_signal_col1:
            if current_planet in ['Jupiter', 'Sun']:
                st.success("🟢 METALS BULLISH - Gold & Silver showing strength")
            elif current_planet == 'Mars':
                st.warning("⚡ ENERGY VOLATILE - Crude & Gas high volatility")
            else:
                st.info("🟡 RANGE BOUND - Wait for planetary alignment")
        
        with commodity_signal_col2:
            current_hour = datetime.now().hour
            if 20 <= current_hour <= 23:
                st.success("🌟 PRIME TIME - US session active, high liquidity")
            elif 5 <= current_hour <= 9:
                st.info("🌅 ASIAN SESSION - Lower volatility, accumulation phase")
            else:
                st.info(f"📊 Current Phase: Planetary hour {current_planet}")
    else:
        st.warning(f"📴 Commodity markets are {commodity_status}. Next session: 5:00 AM IST")

# ==================== GLOBAL & FOREX TAB ====================
with main_tab3:
    st.markdown("""
    <div class="global-section">
        <h2>🌍 Global Markets & Forex</h2>
        <p>Trading Hours: 5:00 AM - 11:55 PM IST | International Markets Coverage</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Global Market Status
    global_status, global_icon = get_market_status('global')
    
    global_status_col1, global_status_col2, global_status_col3 = st.columns(3)
    with global_status_col1:
        st.markdown(f"""
        <div class="market-card">
            <h4>Market Status</h4>
            <h2>{global_icon} {global_status}</h2>
            <p>Global Markets</p>
        </div>
        """, unsafe_allow_html=True)
    
    with global_status_col2:
        current_hour = datetime.now().hour
        if 19 <= current_hour <= 23 or 0 <= current_hour <= 2:
            session = "US ACTIVE"
            session_icon = "🇺🇸"
        elif 13 <= current_hour <= 20:
            session = "EUROPE ACTIVE"  
            session_icon = "🇪🇺"
        elif 5 <= current_hour <= 11:
            session = "ASIA ACTIVE"
            session_icon = "🇯🇵"
        else:
            session = "TRANSITION"
            session_icon = "🌐"
            
        st.markdown(f"""
        <div class="market-card">
            <h4>Active Session</h4>
            <h2>{session_icon} {session}</h2>
            <p>Primary Trading Region</p>
        </div>
        """, unsafe_allow_html=True)
    
    with global_status_col3:
        volatility = "HIGH" if current_planet in ['Mars', 'Rahu'] else "LOW" if current_planet in ['Venus', 'Moon'] else "MEDIUM"
        st.markdown(f"""
        <div class="market-card">
            <h4>Market Volatility</h4>
            <h2 class="trend-{volatility.lower()}">{volatility}</h2>
            <p>Global Risk Level</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Global Indices
    st.markdown("### 📊 Major Global Indices")
    global_indices_cols = st.columns(4)
    
    for idx, market in enumerate(['DOWJONES', 'NASDAQ', 'SP500', 'BITCOIN']):
        if market in st.session_state.market_data:
            data = st.session_state.market_data[market]
            color_class = "positive" if data['change'] >= 0 else "negative"
            arrow = "📈" if data['change'] >= 0 else "📉"
            
            icon = "🇺🇸" if market in ['DOWJONES', 'NASDAQ', 'SP500'] else "₿"
            price_format = f"${data['price']:,.0f}" if market == 'BITCOIN' else f"{data['price']:,.0f}"
            
            with global_indices_cols[idx]:
                st.markdown(f"""
                <div class="market-card">
                    <h5>{icon} {market}</h5>
                    <h3>{price_format}</h3>
                    <p class="{color_class}">
                        {arrow} {abs(data['change']):.2f}%
                    </p>
                </div>
                """, unsafe_allow_html=True)
    
    # Forex Markets
    st.markdown("### 💱 Major Currency Pairs")
    forex_cols = st.columns(4)
    
    for idx, market in enumerate(['USDINR', 'EURINR', 'GBPINR', 'JPYINR']):
        if market in st.session_state.market_data:
            data = st.session_state.market_data[market]
            color_class = "positive" if data['change'] >= 0 else "negative"
            arrow = "📈" if data['change'] >= 0 else "📉"
            
            currency_icons = {
                'USDINR': '🇺🇸/🇮🇳',
                'EURINR': '🇪🇺/🇮🇳', 
                'GBPINR': '🇬🇧/🇮🇳',
                'JPYINR': '🇯🇵/🇮🇳'
            }
            
            with forex_cols[idx]:
                st.markdown(f"""
                <div class="market-card">
                    <h6>{currency_icons[market]} {market}</h6>
                    <h3>₹{data['price']:.2f}</h3>
                    <p class="{color_class}">
                        {arrow} {abs(data['change']):.2f}%
                    </p>
                </div>
                """, unsafe_allow_html=True)
    
    # Global Signals
    st.markdown("### 🌐 Live Global Signals")
    if global_status == "OPEN":
        global_signal_col1, global_signal_col2 = st.columns(2)
        
        with global_signal_col1:
            if current_hour >= 19 and current_hour <= 23:
                st.success("🇺🇸 US PRIME TIME - High liquidity in US indices & Bitcoin")
            elif current_hour >= 13 and current_hour <= 18:
                st.info("🇪🇺 EUROPEAN SESSION - EUR pairs active, moderate volatility")
            elif current_hour >= 5 and current_hour <= 11:
                st.info("🇯🇵 ASIAN SESSION - JPY pairs focus, range trading")
            else:
                st.warning("🌙 OVERNIGHT SESSION - Low liquidity, use caution")
        
        with global_signal_col2:
            if current_planet == 'Jupiter':
                st.success("♃ JUPITER HOUR - Global expansion, crypto bullish")
            elif current_planet == 'Saturn':
                st.error("♄ SATURN HOUR - Global caution, defensive assets")
            elif current_planet == 'Mars':
                st.warning("♂️ MARS HOUR - High volatility, risk management key")
            else:
                st.info(f"{current_symbol} {current_planet} HOUR - {current_influence}")
    else:
        st.warning(f"📴 Global markets are {global_status}. Limited trading available.")

# Auto-refresh logic
if auto_refresh:
    time.sleep(refresh_rate)
    update_market_data()
    st.rerun()

# Enhanced Footer
st.markdown("---")
footer_col1, footer_col2, footer_col3, footer_col4, footer_col5 = st.columns(5)

with footer_col1:
    st.caption(f"🕐 Last Update: {st.session_state.last_update.strftime('%H:%M:%S')}")

with footer_col2:
    st.caption(f"{current_symbol} Planetary: {current_planet}")

with footer_col3:
    equity_open = get_market_status('equity')[0] == 'OPEN'
    commodity_open = get_market_status('commodity')[0] == 'OPEN'
    global_open = get_market_status('global')[0] == 'OPEN'
    
    open_markets = sum([equity_open, commodity_open, global_open])
    st.caption(f"📊 Active Markets: {open_markets}/3")

with footer_col4:
    st.caption(f"📅 Astro Data: {st.session_state.astro_data_date}")

with footer_col5:
    st.caption("🕉️ Vedic Intelligence Pro v2.0")
