import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta
import time
import pytz

# Set up IST timezone and get current time - MOVED TO TOP
ist_tz = pytz.timezone('Asia/Kolkata')
current_date = datetime.now(ist_tz)
current_date_str = current_date.strftime('%d %B %Y')
current_day = current_date.strftime('%A')
current_time_str = current_date.strftime('%H:%M:%S')
current_hour = current_date.hour
tomorrow_date = (current_date + timedelta(days=1)).strftime('%d %B %Y')
tomorrow_day = (current_date + timedelta(days=1)).strftime('%A')

# Page configuration
st.set_page_config(
    page_title="Vedic Market Intelligence",
    page_icon="🕉️",
    layout="wide"
)

# Enhanced CSS with new styles for all features
st.markdown("""
<style>
.main-header {
    background: linear-gradient(45deg, #ff6b35, #f7931e);
    color: white;
    padding: 20px;
    text-align: center;
    border-radius: 15px;
    margin-bottom: 20px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.2);
}
.date-display {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 25px;
    text-align: center;
    border-radius: 15px;
    margin: 20px 0;
    box-shadow: 0 8px 25px rgba(0,0,0,0.3);
}
.market-card {
    background: #f8f9fa;
    padding: 15px;
    border-radius: 10px;
    text-align: center;
    margin: 10px 0;
    border: 2px solid #dee2e6;
    transition: all 0.3s ease;
}
.market-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}
.section-header {
    background: linear-gradient(135deg, #ff9a56 0%, #ff6b35 100%);
    color: #ffffff;
    padding: 20px;
    border-radius: 12px;
    margin: 20px 0;
    text-align: center;
    box-shadow: 0 6px 20px rgba(0,0,0,0.2);
}
.report-section {
    background: #ffffff;
    padding: 20px;
    border-radius: 12px;
    margin: 15px 0;
    border: 2px solid #e9ecef;
    box-shadow: 0 4px 15px rgba(0,0,0,0.05);
}
.positive { color: #28a745; font-weight: bold; }
.negative { color: #dc3545; font-weight: bold; }
.ticker-box {
    background: #000;
    color: #00ff00;
    padding: 12px;
    font-family: monospace;
    border-radius: 8px;
    margin: 10px 0;
    overflow: hidden;
    white-space: nowrap;
}
.planet-info {
    background: linear-gradient(45deg, #e3f2fd, #bbdefb);
    color: #1565c0;
    padding: 15px;
    border-radius: 10px;
    margin: 10px 0;
    border-left: 5px solid #2196f3;
    font-weight: 500;
}
.live-signal {
    background: linear-gradient(45deg, #11998e, #38ef7d);
    color: #ffffff;
    padding: 12px;
    border-radius: 8px;
    margin: 8px 0;
    text-align: center;
    font-weight: bold;
    animation: pulse 2s infinite;
}
.warning-signal {
    background: linear-gradient(45deg, #ff416c, #ff4b2b);
    color: #ffffff;
    padding: 12px;
    border-radius: 8px;
    margin: 8px 0;
    text-align: center;
    font-weight: bold;
    animation: pulse 2s infinite;
}
.trend-bullish {
    background-color: #d4edda;
    color: #155724;
    padding: 10px 15px;
    border-radius: 8px;
    font-weight: bold;
    margin: 5px 0;
    border-left: 4px solid #28a745;
}
.trend-bearish {
    background-color: #f8d7da;
    color: #721c24;
    padding: 10px 15px;
    border-radius: 8px;
    font-weight: bold;
    margin: 5px 0;
    border-left: 4px solid #dc3545;
}
.trend-volatile {
    background-color: #fff3cd;
    color: #856404;
    padding: 10px 15px;
    border-radius: 8px;
    font-weight: bold;
    margin: 5px 0;
    border-left: 4px solid #ffc107;
}
.sector-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: #ffffff;
    padding: 15px;
    border-radius: 10px;
    margin: 15px 0;
    text-align: center;
}
.sector-price-card {
    background: linear-gradient(135deg, #f8f9fa, #ffffff);
    padding: 20px;
    border-radius: 12px;
    border: 3px solid #007bff;
    margin: 15px 0;
    text-align: center;
    box-shadow: 0 6px 20px rgba(0,0,0,0.1);
}
.stock-card {
    background: #ffffff;
    padding: 12px;
    border-radius: 8px;
    border: 2px solid #dee2e6;
    margin: 8px 0;
    transition: all 0.3s ease;
}
.stock-card:hover {
    border-color: #007bff;
    transform: translateY(-1px);
}
.calendar-day {
    background: #ffffff;
    border: 2px solid #dee2e6;
    border-radius: 8px;
    padding: 10px;
    margin: 3px;
    text-align: center;
    min-height: 120px;
    transition: all 0.3s ease;
}
.calendar-bullish {
    background: linear-gradient(135deg, #d4edda, #c3e6cb);
    border-color: #28a745;
    color: #155724;
}
.calendar-bearish {
    background: linear-gradient(135deg, #f8d7da, #f1c3c6);
    border-color: #dc3545;
    color: #721c24;
}
.calendar-volatile {
    background: linear-gradient(135deg, #fff3cd, #ffeeba);
    border-color: #ffc107;
    color: #856404;
}
.calendar-neutral {
    background: linear-gradient(135deg, #f8f9fa, #e9ecef);
    border-color: #6c757d;
    color: #495057;
}
.performance-card {
    padding: 12px;
    border-radius: 8px;
    margin: 5px 0;
    border-left: 4px solid #007bff;
}
.performance-strong-buy {
    background: #d4edda;
    color: #155724;
    border-left-color: #28a745;
}
.performance-buy {
    background: #d1ecf1;
    color: #0c5460;
    border-left-color: #17a2b8;
}
.performance-hold {
    background: #fff3cd;
    color: #856404;
    border-left-color: #ffc107;
}
.performance-sell {
    background: #f8d7da;
    color: #721c24;
    border-left-color: #dc3545;
}
.timeframe-header {
    background: linear-gradient(135deg, #6f42c1, #e83e8c);
    color: white;
    padding: 12px;
    border-radius: 8px;
    text-align: center;
    margin: 10px 0;
}
.planetary-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 20px;
    border-radius: 12px;
    margin: 15px 0;
    text-align: center;
    box-shadow: 0 8px 25px rgba(0,0,0,0.3);
}
.transit-effect {
    background: #ffffff;
    padding: 15px;
    border-radius: 10px;
    margin: 10px 0;
    border: 2px solid #dee2e6;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}
@keyframes pulse {
    0% { opacity: 1; }
    50% { opacity: 0.7; }
    100% { opacity: 1; }
}
</style>
""", unsafe_allow_html=True)

# Initialize comprehensive session state
try:
    if 'market_data' not in st.session_state:
        st.session_state.market_data = {
            # Main Indices
            'NIFTY': {'price': 24780.50, 'change': -0.50, 'high': 24920, 'low': 24750},
            'BANKNIFTY': {'price': 52435.75, 'change': 0.60, 'high': 52580, 'low': 52120},
            'SENSEX': {'price': 81342.15, 'change': -0.35, 'high': 81650, 'low': 81250},
            
            # Sector Indices
            'NIFTY_AUTO': {'price': 25380, 'change': -0.25, 'high': 25550, 'low': 25200},
            'NIFTY_PHARMA': {'price': 18925, 'change': 0.84, 'high': 19050, 'low': 18750},
            'NIFTY_PSU_BANK': {'price': 4250, 'change': 0.35, 'high': 4320, 'low': 4180},
            'NIFTY_PVT_BANK': {'price': 26780, 'change': 0.45, 'high': 26950, 'low': 26650},
            'NIFTY_METAL': {'price': 8965, 'change': -1.15, 'high': 9100, 'low': 8850},
            'NIFTY_OIL_GAS': {'price': 11890, 'change': -0.85, 'high': 12050, 'low': 11820},
            'NIFTY_IT': {'price': 32156, 'change': -1.31, 'high': 32600, 'low': 32100},
            'NIFTY_FMCG': {'price': 58920, 'change': 0.65, 'high': 59200, 'low': 58650},
            
            # Commodities
            'GOLD': {'price': 71850, 'change': 0.55, 'high': 72100, 'low': 71500},
            'SILVER': {'price': 91250, 'change': 1.20, 'high': 91800, 'low': 90200},
            'CRUDE': {'price': 6845, 'change': -1.49, 'high': 6920, 'low': 6800},
            'BITCOIN': {'price': 97850.50, 'change': 2.57, 'high': 98500, 'low': 95200},
            
            # Global Markets
            'DOWJONES': {'price': 44565, 'change': 0.85, 'high': 44750, 'low': 44200},
            'SP500': {'price': 6090.27, 'change': 1.15, 'high': 6120, 'low': 6050},
            'NASDAQ': {'price': 20173, 'change': 1.25, 'high': 20350, 'low': 19850},
            
            # Forex
            'USDINR': {'price': 83.45, 'change': -0.14, 'high': 83.58, 'low': 83.42},
            'EURINR': {'price': 88.25, 'change': 0.35, 'high': 88.50, 'low': 87.90},
            'GBPINR': {'price': 106.75, 'change': 0.28, 'high': 107.20, 'low': 106.50},
            'DXY': {'price': 103.25, 'change': 0.15, 'high': 103.45, 'low': 102.95}
        }
    
    if 'sector_data' not in st.session_state:
        st.session_state.sector_data = {
            'NIFTY 50': {
                'index_key': 'NIFTY',
                'stocks': ['RELIANCE', 'TCS', 'HDFC BANK', 'BHARTI AIRTEL', 'INFOSYS', 'ICICI BANK', 'SBI', 'HINDUNILVR', 'LT', 'ITC']
            },
            'BANKNIFTY': {
                'index_key': 'BANKNIFTY',
                'stocks': ['HDFC BANK', 'ICICI BANK', 'SBI', 'KOTAK BANK', 'AXIS BANK', 'INDUSIND BANK', 'PNB', 'BANK OF BARODA', 'CANARA BANK', 'IDFCFIRSTB']
            },
            'PSU BANK': {
                'index_key': 'NIFTY_PSU_BANK',
                'stocks': ['SBI', 'PNB', 'BANK OF BARODA', 'CANARA BANK', 'UNION BANK', 'INDIAN BANK', 'CENTRAL BANK', 'UCO BANK', 'BANK OF INDIA', 'PUNJAB & SIND BANK']
            },
            'AUTO': {
                'index_key': 'NIFTY_AUTO',
                'stocks': ['TATA MOTORS', 'MARUTI SUZUKI', 'MAHINDRA', 'BAJAJ AUTO', 'HERO MOTOCORP', 'TVS MOTOR', 'ASHOK LEYLAND', 'EICHER MOTORS', 'FORCE MOTORS', 'ESCORTS']
            },
            'PHARMA': {
                'index_key': 'NIFTY_PHARMA',
                'stocks': ['SUN PHARMA', 'DR REDDY', 'CIPLA', 'DIVIS LAB', 'BIOCON', 'LUPIN', 'CADILA HEALTH', 'GLENMARK', 'TORRENT PHARMA', 'ALKEM LAB']
            },
            'PVT BANK': {
                'index_key': 'NIFTY_PVT_BANK',
                'stocks': ['HDFC BANK', 'ICICI BANK', 'KOTAK BANK', 'AXIS BANK', 'INDUSIND BANK', 'FEDERAL BANK', 'RBL BANK', 'CITY UNION BANK', 'KARUR VYSYA', 'DCB BANK']
            },
            'METAL': {
                'index_key': 'NIFTY_METAL',
                'stocks': ['TATA STEEL', 'JSW STEEL', 'HINDALCO', 'VEDANTA', 'SAIL', 'JINDAL STEEL', 'NMDC', 'MOIL', 'RATNAMANI', 'APL APOLLO']
            },
            'OIL & GAS': {
                'index_key': 'NIFTY_OIL_GAS',
                'stocks': ['RELIANCE', 'ONGC', 'IOC', 'BPCL', 'HPCL', 'GAIL', 'OIL INDIA', 'PETRONET LNG', 'INDRAPRASTHA GAS', 'GUJARAT GAS']
            },
            'IT': {
                'index_key': 'NIFTY_IT',
                'stocks': ['TCS', 'INFOSYS', 'WIPRO', 'HCL TECH', 'TECH MAHINDRA', 'MPHASIS', 'MINDTREE', 'L&T INFOTECH', 'COFORGE', 'PERSISTENT']
            },
            'FMCG': {
                'index_key': 'NIFTY_FMCG',
                'stocks': ['HINDUNILVR', 'ITC', 'NESTLE', 'BRITANNIA', 'DABUR', 'MARICO', 'GODREJ CONSUMER', 'COLGATE', 'EMAMI', 'VBL']
            }
        }
    
    if 'last_update' not in st.session_state:
        st.session_state.last_update = current_date

except Exception as e:
    st.error(f"Error initializing data: {e}")

# Helper functions
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
        
        # Use IST timezone for last update
        ist_tz = pytz.timezone('Asia/Kolkata')
        st.session_state.last_update = datetime.now(ist_tz)
        return True
    except Exception as e:
        st.error(f"Error updating market data: {e}")
        return False

def get_planetary_influence(hour):
    planetary_hours = {
        9: ("Venus", "♀", "Banking, luxury goods favorable"),
        10: ("Sun", "☀️", "Energy, pharma sectors strong"),
        11: ("Mercury", "☿", "IT, communication mixed"),
        12: ("Saturn", "♄", "Metals, mining cautious"),
        13: ("Mars", "♂️", "Energy, defense volatile"),
        14: ("Rahu", "☊", "Tech under pressure"),
        15: ("Jupiter", "♃", "Banking recovery")
    }
    return planetary_hours.get(hour, ("Mixed", "🌟", "Multiple planetary influences"))

def create_sample_signals():
    """Create sample planetary signals for demonstration"""
    return [
        {'time': '09:00-10:00', 'signal': 'BUY', 'target': '+1.2%', 'strength': 'Strong'},
        {'time': '11:00-12:00', 'signal': 'HOLD', 'target': '+0.5%', 'strength': 'Medium'},
        {'time': '14:00-15:00', 'signal': 'SELL', 'target': '-0.8%', 'strength': 'Weak'},
    ]

def get_market_trend(change):
    """Determine market trend based on change percentage"""
    if change > 1:
        return "trend-bullish", "Bullish"
    elif change < -1:
        return "trend-bearish", "Bearish"
    else:
        return "trend-volatile", "Volatile"

def get_stock_recommendation(change):
    """Get stock recommendation based on change"""
    if change > 2:
        return "performance-strong-buy", "Strong Buy"
    elif change > 0.5:
        return "performance-buy", "Buy"
    elif change > -0.5:
        return "performance-hold", "Hold"
    else:
        return "performance-sell", "Sell"

# Main Application
def main():
    # Header
    st.markdown(f"""
    <div class="main-header">
        <h1>🕉️ VEDIC MARKET INTELLIGENCE</h1>
        <h3>Ancient Wisdom • Modern Markets • Precise Predictions</h3>
        <p>Planetary Transit Analysis for Financial Markets</p>
    </div>
    """, unsafe_allow_html=True)

    # Current Date and Time Display
    st.markdown(f"""
    <div class="date-display">
        <h2>📅 {current_date_str} • {current_day}</h2>
        <h3>⏰ Current Time: {current_time_str} IST</h3>
        <p>🌅 Tomorrow: {tomorrow_date} • {tomorrow_day}</p>
    </div>
    """, unsafe_allow_html=True)

    # Auto-refresh toggle
    auto_refresh = st.sidebar.checkbox("🔄 Auto Refresh (30 seconds)", value=False)
    
    if auto_refresh:
        time.sleep(30)
        update_market_data()
        st.rerun()

    # Manual refresh button
    if st.sidebar.button("🔄 Refresh Market Data"):
        if update_market_data():
            st.sidebar.success("✅ Data Updated Successfully!")
        else:
            st.sidebar.error("❌ Failed to update data")

    # Current planetary influence
    planet, symbol, influence = get_planetary_influence(current_hour)
    st.markdown(f"""
    <div class="planet-info">
        <h4>🌟 Current Planetary Hour: {planet} {symbol}</h4>
        <p>{influence}</p>
    </div>
    """, unsafe_allow_html=True)

    # Main navigation
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📈 EQUITY MARKETS", 
        "🥇 COMMODITIES", 
        "💱 FOREX & CRYPTO", 
        "🌍 GLOBAL MARKETS",
        "🔮 PLANETARY TRANSITS",
        "📊 DETAILED ANALYSIS"
    ])

    with tab1:
        display_equity_markets()
    
    with tab2:
        display_commodities()
    
    with tab3:
        display_forex_crypto()
    
    with tab4:
        display_global_markets()
    
    with tab5:
        display_planetary_transits()
    
    with tab6:
        display_detailed_analysis()

def display_equity_markets():
    st.markdown('<div class="section-header"><h2>📈 INDIAN EQUITY MARKETS</h2></div>', unsafe_allow_html=True)
    
    # Quick market overview
    col1, col2, col3 = st.columns(3)
    
    with col1:
        nifty_data = st.session_state.market_data['NIFTY']
        color_class = "positive" if nifty_data['change'] >= 0 else "negative"
        arrow = "▲" if nifty_data['change'] >= 0 else "▼"
        
        st.markdown(f"""
        <div class="market-card">
            <h4>📈 NIFTY 50</h4>
            <h2>{nifty_data['price']:,.2f}</h2>
            <h4 class="{color_class}">{arrow} {abs(nifty_data['change']):.2f}%</h4>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        banknifty_data = st.session_state.market_data['BANKNIFTY']
        color_class = "positive" if banknifty_data['change'] >= 0 else "negative"
        arrow = "▲" if banknifty_data['change'] >= 0 else "▼"
        
        st.markdown(f"""
        <div class="market-card">
            <h4>🏦 BANKNIFTY</h4>
            <h2>{banknifty_data['price']:,.2f}</h2>
            <h4 class="{color_class}">{arrow} {abs(banknifty_data['change']):.2f}%</h4>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        sensex_data = st.session_state.market_data['SENSEX']
        color_class = "positive" if sensex_data['change'] >= 0 else "negative"
        arrow = "▲" if sensex_data['change'] >= 0 else "▼"
        
        st.markdown(f"""
        <div class="market-card">
            <h4>📊 SENSEX</h4>
            <h2>{sensex_data['price']:,.2f}</h2>
            <h4 class="{color_class}">{arrow} {abs(sensex_data['change']):.2f}%</h4>
        </div>
        """, unsafe_allow_html=True)

    # Sector wise analysis
    st.markdown("### 🏭 Sector Analysis")
    
    sectors = ['AUTO', 'PHARMA', 'IT', 'METAL', 'FMCG']
    sector_cols = st.columns(len(sectors))
    
    for idx, sector in enumerate(sectors):
        sector_key = f'NIFTY_{sector}'
        if sector_key in st.session_state.market_data:
            sector_data = st.session_state.market_data[sector_key]
            color_class = "positive" if sector_data['change'] >= 0 else "negative"
            arrow = "▲" if sector_data['change'] >= 0 else "▼"
            trend_class, trend_text = get_market_trend(sector_data['change'])
            
            with sector_cols[idx]:
                st.markdown(f"""
                <div class="stock-card">
                    <h5>{sector}</h5>
                    <p>{sector_data['price']:,.0f}</p>
                    <p class="{color_class}">{arrow} {abs(sector_data['change']):.2f}%</p>
                    <div class="{trend_class}">{trend_text}</div>
                </div>
                """, unsafe_allow_html=True)

    # Live market ticker
    st.markdown("### 📊 Live Market Ticker")
    
    ticker_text = " | ".join([
        f"{market}: {data['price']:,.2f} ({'+' if data['change'] >= 0 else ''}{data['change']:.2f}%)"
        for market, data in list(st.session_state.market_data.items())[:6]
    ])
    
    st.markdown(f"""
    <div class="ticker-box">
        📈 LIVE: {ticker_text}
    </div>
    """, unsafe_allow_html=True)

def display_commodities():
    st.markdown('<div class="section-header"><h2>🥇 COMMODITIES & PRECIOUS METALS</h2></div>', unsafe_allow_html=True)
    
    # Commodities overview
    col1, col2, col3, col4 = st.columns(4)
    
    commodities = [
        ('GOLD', 'GOLD (₹/10g)', col1),
        ('SILVER', 'SILVER (₹/kg)', col2),
        ('CRUDE', 'CRUDE OIL', col3),
        ('BITCOIN', 'BITCOIN ($)', col4)
    ]
    
    for key, name, col in commodities:
        if key in st.session_state.market_data:
            data = st.session_state.market_data[key]
            color_class = "positive" if data['change'] >= 0 else "negative"
            arrow = "▲" if data['change'] >= 0 else "▼"
            
            with col:
                st.markdown(f"""
                <div class="market-card">
                    <h4>{name}</h4>
                    <h3>{data['price']:,.2f}</h3>
                    <h4 class="{color_class}">{arrow} {abs(data['change']):.2f}%</h4>
                </div>
                """, unsafe_allow_html=True)

    # Sample signals display
    st.markdown("### 📊 Today's Commodity Signals")
    signals = create_sample_signals()
    
    for signal in signals:
        signal_class = "live-signal" if signal['signal'] == 'BUY' else "warning-signal" if signal['signal'] == 'SELL' else "trend-volatile"
        st.markdown(f"""
        <div class="{signal_class}">
            <strong>{signal['time']}: {signal['signal']}</strong> - Target: {signal['target']} | Strength: {signal['strength']}
        </div>
        """, unsafe_allow_html=True)

    # Commodity trends analysis
    st.markdown("### 📈 Commodity Trends Analysis")
    
    trend_data = [
        ("Gold", "Bullish due to Venus transit", "Strong support at ₹71,500"),
        ("Silver", "Volatile with Mars influence", "Resistance at ₹92,000"),
        ("Crude Oil", "Bearish on Saturn aspect", "Key level at ₹6,800"),
        ("Bitcoin", "Highly volatile on Rahu transit", "Support at $95,000")
    ]
    
    for commodity, trend, level in trend_data:
        st.markdown(f"""
        <div class="transit-effect">
            <h4>{commodity}</h4>
            <p><strong>Trend:</strong> {trend}</p>
            <p><strong>Key Level:</strong> {level}</p>
        </div>
        """, unsafe_allow_html=True)

def display_forex_crypto():
    st.markdown('<div class="section-header"><h2>💱 FOREX & CRYPTOCURRENCY</h2></div>', unsafe_allow_html=True)
    
    # Forex pairs
    col1, col2, col3, col4 = st.columns(4)
    
    forex_pairs = [
        ('USDINR', 'USD/INR', col1),
        ('EURINR', 'EUR/INR', col2),
        ('GBPINR', 'GBP/INR', col3),
        ('DXY', 'Dollar Index', col4)
    ]
    
    for key, name, col in forex_pairs:
        if key in st.session_state.market_data:
            data = st.session_state.market_data[key]
            color_class = "positive" if data['change'] >= 0 else "negative"
            arrow = "▲" if data['change'] >= 0 else "▼"
            
            with col:
                st.markdown(f"""
                <div class="market-card">
                    <h4>{name}</h4>
                    <h3>{data['price']:.2f}</h3>
                    <h4 class="{color_class}">{arrow} {abs(data['change']):.2f}%</h4>
                </div>
                """, unsafe_allow_html=True)

    # Currency analysis
    st.markdown("### 💰 Currency Analysis")
    
    currency_analysis = [
        ("USD/INR", "Mercury influence suggests range-bound movement", "83.40-83.60"),
        ("EUR/INR", "Jupiter aspect favors strength", "88.00-88.50"),
        ("GBP/INR", "Venus transit supports upward bias", "106.50-107.20"),
        ("DXY", "Saturn influence indicates consolidation", "102.80-103.50")
    ]
    
    for pair, analysis, range_val in currency_analysis:
        st.markdown(f"""
        <div class="planet-info">
            <h4>{pair}</h4>
            <p><strong>Analysis:</strong> {analysis}</p>
            <p><strong>Expected Range:</strong> {range_val}</p>
        </div>
        """, unsafe_allow_html=True)

def display_global_markets():
    st.markdown('<div class="section-header"><h2>🌍 GLOBAL MARKETS</h2></div>', unsafe_allow_html=True)
    
    # Global indices
    col1, col2, col3 = st.columns(3)
    
    global_markets = [
        ('DOWJONES', 'DOW JONES', col1),
        ('SP500', 'S&P 500', col2),
        ('NASDAQ', 'NASDAQ', col3)
    ]
    
    for key, name, col in global_markets:
        if key in st.session_state.market_data:
            data = st.session_state.market_data[key]
            color_class = "positive" if data['change'] >= 0 else "negative"
            arrow = "▲" if data['change'] >= 0 else "▼"
            
            with col:
                st.markdown(f"""
                <div class="market-card">
                    <h4>{name}</h4>
                    <h3>{data['price']:,.2f}</h3>
                    <h4 class="{color_class}">{arrow} {abs(data['change']):.2f}%</h4>
                </div>
                """, unsafe_allow_html=True)

    # Global market sentiment
    st.markdown("### 🌐 Global Market Sentiment")
    
    sentiment_data = [
        ("US Markets", "Positive momentum on Jupiter transit", "Tech and Healthcare leading"),
        ("Asian Markets", "Mixed signals from Mars aspect", "Banking sector under pressure"),
        ("European Markets", "Cautious due to Saturn influence", "Energy sector volatility expected"),
        ("Emerging Markets", "Venus support for commodities", "Currency fluctuations likely")
    ]
    
    for market, sentiment, details in sentiment_data:
        st.markdown(f"""
        <div class="transit-effect">
            <h4>{market}</h4>
            <p><strong>Sentiment:</strong> {sentiment}</p>
            <p><strong>Details:</strong> {details}</p>
        </div>
        """, unsafe_allow_html=True)

def display_planetary_transits():
    st.markdown('<div class="section-header"><h2>🔮 PLANETARY TRANSITS & MARKET INFLUENCE</h2></div>', unsafe_allow_html=True)
    
    # Current planetary positions
    st.markdown("### 🌟 Current Planetary Positions")
    
    planets = [
        ('Sun', 'Cancer', 'FMCG, Banking positive', '☀️'),
        ('Moon', 'Libra', 'Auto, Luxury bullish', '🌙'),
        ('Mars', 'Virgo', 'IT, Healthcare mixed', '♂️'),
        ('Mercury', 'Cancer', 'Communication strong', '☿'),
        ('Jupiter', 'Gemini', 'Banking expansion', '♃'),
        ('Venus', 'Gemini', 'Luxury goods favorable', '♀'),
        ('Saturn', 'Pisces', 'Pharma caution', '♄')
    ]
    
    col1, col2 = st.columns(2)
    
    for idx, (planet, sign, effect, symbol) in enumerate(planets):
        col = col1 if idx % 2 == 0 else col2
        
        with col:
            st.markdown(f"""
            <div class="transit-effect">
                <h4>{planet} {symbol} in {sign}</h4>
                <p>{effect}</p>
            </div>
            """, unsafe_allow_html=True)

    # Daily predictions
    st.markdown("### 🔮 Today's Market Predictions")
    
    predictions = [
        "Banking sector shows strong planetary support from Jupiter transit",
        "IT stocks under Mercury influence - expect volatility",
        "Gold and Silver favored by Venus - good for precious metals",
        "Mars aspect suggests energy sector momentum",
        "Saturn's influence advises caution in speculative trades"
    ]
    
    for prediction in predictions:
        st.markdown(f"""
        <div class="planet-info">
            <p>• {prediction}</p>
        </div>
        """, unsafe_allow_html=True)

    # Hourly planetary influence
    st.markdown("### ⏰ Hourly Planetary Influence")
    
    hourly_influence = [
        ("09:00-10:00", "Venus Hour", "Banking stocks favorable"),
        ("10:00-11:00", "Sun Hour", "Energy and pharma strong"),
        ("11:00-12:00", "Mercury Hour", "IT sector mixed signals"),
        ("12:00-13:00", "Saturn Hour", "Metals under pressure"),
        ("13:00-14:00", "Mars Hour", "Defense and energy volatile"),
        ("14:00-15:00", "Rahu Hour", "Tech stocks caution advised"),
        ("15:00-15:30", "Jupiter Hour", "Banking recovery expected")
    ]
    
    for time_range, planet_hour, influence in hourly_influence:
        st.markdown(f"""
        <div class="planetary-card">
            <h4>{time_range} - {planet_hour}</h4>
            <p>{influence}</p>
        </div>
        """, unsafe_allow_html=True)

def display_detailed_analysis():
    st.markdown('<div class="section-header"><h2>📊 DETAILED MARKET ANALYSIS</h2></div>', unsafe_allow_html=True)
    
    # Stock recommendations based on planetary analysis
    st.markdown("### 📈 Stock Recommendations")
    
    # Sample stock data with recommendations
    stock_recommendations = [
        ("RELIANCE", 2850.50, 1.25, "Strong Buy", "Jupiter aspect favorable"),
        ("TCS", 4125.75, -0.85, "Hold", "Mercury influence mixed"),
        ("HDFC BANK", 1685.25, 0.65, "Buy", "Venus transit positive"),
        ("INFOSYS", 1825.40, -1.15, "Sell", "Rahu aspect negative"),
        ("SBI", 825.60, 2.15, "Strong Buy", "Jupiter support strong")
    ]
    
    for stock, price, change, recommendation, reason in stock_recommendations:
        color_class = "positive" if change >= 0 else "negative"
        arrow = "▲" if change >= 0 else "▼"
        rec_class, _ = get_stock_recommendation(change)
        
        st.markdown(f"""
        <div class="{rec_class}">
            <h4>{stock} - ₹{price:.2f} <span class="{color_class}">({arrow} {abs(change):.2f}%)</span></h4>
            <p><strong>Recommendation:</strong> {recommendation}</p>
            <p><strong>Reason:</strong> {reason}</p>
        </div>
        """, unsafe_allow_html=True)

    # Weekly market calendar
    st.markdown("### 📅 Weekly Market Calendar")
    
    # Sample weekly data
    weekly_data = [
        ("Monday", "Bullish", "Jupiter influence strong", "+0.8%"),
        ("Tuesday", "Volatile", "Mars aspect active", "-0.3%"),
        ("Wednesday", "Neutral", "Mercury mixed signals", "+0.1%"),
        ("Thursday", "Bearish", "Saturn pressure", "-1.2%"),
        ("Friday", "Bullish", "Venus support", "+1.5%"),
        ("Saturday", "Closed", "Market holiday", "—"),
        ("Sunday", "Closed", "Market holiday", "—")
    ]
    
    week_cols = st.columns(7)
    
    for idx, (day, trend, reason, expected) in enumerate(weekly_data):
        if trend == "Bullish":
            trend_class = "calendar-bullish"
        elif trend == "Bearish":
            trend_class = "calendar-bearish"
        elif trend == "Volatile":
            trend_class = "calendar-volatile"
        else:
            trend_class = "calendar-neutral"
        
        with week_cols[idx]:
            st.markdown(f"""
            <div class="calendar-day {trend_class}">
                <h5>{day}</h5>
                <p><strong>{trend}</strong></p>
                <p>{reason}</p>
                <p><strong>{expected}</strong></p>
            </div>
            """, unsafe_allow_html=True)

    # Performance metrics
    st.markdown("### 📊 Performance Metrics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="performance-card performance-strong-buy">
            <h4>Strong Buy Signals</h4>
            <h2>12</h2>
            <p>Stocks with Jupiter support</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="performance-card performance-hold">
            <h4>Hold Signals</h4>
            <h2>18</h2>
            <p>Mixed planetary influences</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="performance-card performance-sell">
            <h4>Sell Signals</h4>
            <h2>8</h2>
            <p>Negative planetary aspects</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
