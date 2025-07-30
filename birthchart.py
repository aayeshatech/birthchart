import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta
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
.transit-box {
    background: #f0f8ff;
    padding: 15px;
    border-radius: 8px;
    margin: 10px 0;
    border: 1px solid #87ceeb;
}
.timing-alert {
    background: #fff3cd;
    padding: 10px;
    border-radius: 5px;
    margin: 5px 0;
    border-left: 4px solid #ffc107;
}
.bullish-text {
    color: #28a745;
    font-weight: bold;
}
.bearish-text {
    color: #dc3545;
    font-weight: bold;
}
.neutral-text {
    color: #ffc107;
    font-weight: bold;
}
.volatile-text {
    color: #ff6b35;
    font-weight: bold;
}
.trend-bullish {
    background-color: #d4edda;
    color: #155724;
    padding: 4px 8px;
    border-radius: 4px;
    font-weight: bold;
}
.trend-bearish {
    background-color: #f8d7da;
    color: #721c24;
    padding: 4px 8px;
    border-radius: 4px;
    font-weight: bold;
}
.trend-neutral {
    background-color: #fff3cd;
    color: #856404;
    padding: 4px 8px;
    border-radius: 4px;
    font-weight: bold;
}
.trend-volatile {
    background-color: #ffe5d4;
    color: #a04000;
    padding: 4px 8px;
    border-radius: 4px;
    font-weight: bold;
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
            'GOLD': {'price': 71850, 'change': 0.55, 'high': 72100, 'low': 71500},
            'SILVER': {'price': 91250, 'change': 1.20, 'high': 91800, 'low': 90200},
            'BITCOIN': {'price': 97850.50, 'change': 2.57, 'high': 98500, 'low': 95200},
            'CRUDE': {'price': 6845, 'change': -1.49, 'high': 6920, 'low': 6800},
            'DOWJONES': {'price': 44565, 'change': 0.85, 'high': 44750, 'low': 44200},
            'NASDAQ': {'price': 20173, 'change': 1.25, 'high': 20350, 'low': 19850},
            'USDINR': {'price': 83.45, 'change': -0.14, 'high': 83.58, 'low': 83.42},
            'EURINR': {'price': 88.25, 'change': 0.35, 'high': 88.50, 'low': 87.90},
            'NIFTY_IT': {'price': 32156, 'change': -1.31, 'high': 32600, 'low': 32100},
            'NIFTY_PHARMA': {'price': 18925, 'change': 0.84, 'high': 19050, 'low': 18750},
            'NIFTY_BANK': {'price': 52435, 'change': 0.60, 'high': 52580, 'low': 52120},
            'NIFTY_AUTO': {'price': 25380, 'change': -0.25, 'high': 25550, 'low': 25200}
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
    
    # Initialize astrological predictions
    if 'astro_predictions' not in st.session_state:
        st.session_state.astro_predictions = {
            'sectors': {
                'Banking': {'trend': 'Bullish', 'planet': 'Mars in 6th', 'timing': '10:30-12:00'},
                'IT': {'trend': 'Bearish', 'planet': 'Mercury in 4th', 'timing': '14:00-15:15'},
                'Pharma': {'trend': 'Bullish', 'planet': 'Jupiter aspect', 'timing': '09:30-11:00'},
                'Auto': {'trend': 'Neutral', 'planet': 'Venus in 3rd', 'timing': '11:30-13:00'},
                'Metal': {'trend': 'Bearish', 'planet': 'Saturn in 12th', 'timing': '13:30-15:00'},
                'FMCG': {'trend': 'Bullish', 'planet': 'Moon in 6th', 'timing': '09:15-10:45'},
                'Energy': {'trend': 'Volatile', 'planet': 'Rahu in 1st', 'timing': '12:00-14:30'},
                'Realty': {'trend': 'Bearish', 'planet': 'Ketu in 7th', 'timing': '14:30-15:30'}
            },
            'commodities': {
                'GOLD': {'trend': 'Bullish', 'planet': 'Sun in Cancer', 'timing': '20:00-23:00'},
                'SILVER': {'trend': 'Strong Bullish', 'planet': 'Moon favorable', 'timing': '20:30-23:30'},
                'CRUDE': {'trend': 'Bearish', 'planet': 'Mars afflicted', 'timing': '19:00-22:00'},
                'NATURALGAS': {'trend': 'Volatile', 'planet': 'Mercury combust', 'timing': '18:30-21:30'},
                'COPPER': {'trend': 'Neutral', 'planet': 'Venus aspect', 'timing': '21:00-23:00'}
            },
            'global': {
                'DOWJONES': {'trend': 'Bullish', 'planet': 'Jupiter in Gemini', 'timing': '19:00-22:30'},
                'NASDAQ': {'trend': 'Strong Bullish', 'planet': 'Mercury tech', 'timing': '19:00-02:00'},
                'S&P500': {'trend': 'Bullish', 'planet': 'Venus favorable', 'timing': '19:00-22:30'},
                'FTSE': {'trend': 'Neutral', 'planet': 'Saturn aspect', 'timing': '13:30-20:00'},
                'NIKKEI': {'trend': 'Bearish', 'planet': 'Rahu influence', 'timing': '05:30-11:30'},
                'HANGSENG': {'trend': 'Volatile', 'planet': 'Ketu in 7th', 'timing': '06:30-13:00'}
            }
        }

except Exception as e:
    st.error(f"Error initializing data: {e}")

# Helper function to get planetary influence for time
def get_planetary_influence(current_time):
    hour = current_time.hour
    minute = current_time.minute
    
    # Planetary hours (simplified)
    planetary_hours = {
        (6, 7): ("Sun", "☀️", "Strong energy, leadership sectors"),
        (7, 9): ("Venus", "♀", "Banking, luxury goods favorable"),
        (9, 10): ("Mercury", "☿", "IT, communication sectors active"),
        (10, 12): ("Moon", "🌙", "FMCG, consumer goods strong"),
        (12, 13): ("Saturn", "♄", "Metals, mining cautious"),
        (13, 15): ("Jupiter", "♃", "Banking, finance positive"),
        (15, 16): ("Mars", "♂️", "Energy, defense volatile"),
        (16, 18): ("Sun", "☀️", "Power, energy sectors"),
        (18, 20): ("Venus", "♀", "Entertainment, luxury"),
        (20, 22): ("Mercury", "☿", "Global tech markets"),
        (22, 24): ("Moon", "🌙", "Commodities active"),
        (0, 3): ("Saturn", "♄", "Crypto, global markets"),
        (3, 6): ("Jupiter", "♃", "Asian markets opening")
    }
    
    for (start, end), (planet, symbol, influence) in planetary_hours.items():
        if start <= hour < end:
            return planet, symbol, influence
    
    return "Mixed", "🌟", "Multiple planetary influences"

# Helper function to check if current time is in range
def is_time_in_range(current_time_str, time_range):
    try:
        start_str, end_str = time_range.split('-')
        current = datetime.strptime(current_time_str, '%H:%M').time()
        start = datetime.strptime(start_str, '%H:%M').time()
        end = datetime.strptime(end_str, '%H:%M').time()
        
        if start <= end:
            return start <= current <= end
        else:
            return current >= start or current <= end
    except:
        return False

# Function to format market timings based on selected market type
def get_market_timing(market_type, selected_item):
    current_time = datetime.now()
    timings = []
    
    if market_type == "Sector":
        sector_stocks = {
            'Banking': ['HDFC Bank', 'ICICI Bank', 'SBI', 'Axis Bank', 'Kotak Bank'],
            'IT': ['TCS', 'Infosys', 'Wipro', 'HCL Tech', 'Tech Mahindra'],
            'Pharma': ['Sun Pharma', 'Dr Reddy', 'Cipla', 'Divis Lab', 'Biocon'],
            'Auto': ['Maruti', 'Tata Motors', 'M&M', 'Bajaj Auto', 'Hero Motor'],
            'Metal': ['Tata Steel', 'JSW Steel', 'Hindalco', 'Vedanta', 'SAIL'],
            'FMCG': ['HUL', 'ITC', 'Nestle', 'Britannia', 'Dabur']
        }
        
        if selected_item in sector_stocks:
            stocks = sector_stocks[selected_item]
            
            # Predefined timing patterns based on sector
            sector_timings = {
                'Banking': [
                    ('10:30-11:15', 'Bullish'),
                    ('11:00-12:00', 'Bullish'),
                    ('13:00-14:00', 'Neutral'),
                    ('14:30-15:15', 'Bearish'),
                    ('09:30-10:30', 'Bullish')
                ],
                'IT': [
                    ('14:00-15:00', 'Bearish'),
                    ('14:15-15:15', 'Bearish'),
                    ('11:30-12:30', 'Neutral'),
                    ('13:45-14:45', 'Bearish'),
                    ('14:00-15:00', 'Bearish')
                ],
                'Pharma': [
                    ('09:30-10:30', 'Bullish'),
                    ('10:00-11:00', 'Bullish'),
                    ('11:30-12:30', 'Neutral'),
                    ('09:45-10:45', 'Bullish'),
                    ('14:00-15:00', 'Bearish')
                ],
                'Auto': [
                    ('11:30-12:30', 'Neutral'),
                    ('12:00-13:00', 'Bullish'),
                    ('11:45-12:45', 'Neutral'),
                    ('13:30-14:30', 'Bearish'),
                    ('11:00-12:00', 'Neutral')
                ],
                'Metal': [
                    ('13:30-14:30', 'Bearish'),
                    ('13:45-14:45', 'Bearish'),
                    ('14:00-15:00', 'Bearish'),
                    ('12:00-13:00', 'Neutral'),
                    ('13:30-14:30', 'Bearish')
                ],
                'FMCG': [
                    ('09:15-10:15', 'Bullish'),
                    ('09:30-10:30', 'Bullish'),
                    ('11:00-12:00', 'Neutral'),
                    ('10:00-11:00', 'Bullish'),
                    ('09:45-10:45', 'Bullish')
                ]
            }
            
            stock_timings = sector_timings.get(selected_item, [])
            
            for i, stock in enumerate(stocks):
                if i < len(stock_timings):
                    time_range, trend = stock_timings[i]
                    start_time, end_time = time_range.split('-')
                else:
                    # Default timing if not enough predefined
                    start_time = f"{9 + i}:00"
                    end_time = f"{10 + i}:00"
                    trend = "Neutral"
                
                planet = list(st.session_state.planetary_data.keys())[i % 9]
                
                timings.append({
                    'Stock': stock,
                    'Trend': trend,
                    'Start': start_time,
                    'End': end_time,
                    'Planet': st.session_state.planetary_data[planet]['symbol'] + ' ' + planet,
                    'Target': f"+{1.5 + (i*0.2):.1f}%" if trend == "Bullish" else f"-{1.2 + (i*0.2):.1f}%" if trend == "Bearish" else f"±{0.5:.1f}%"
                })
    
    elif market_type == "Commodity":
        # Commodity specific timings
        commodity_sessions = {
            'GOLD': [
                ('09:00', '12:00', 'Asian Session', 'Accumulation'),
                ('14:00', '17:00', 'European Session', 'Volatility'),
                ('20:00', '23:30', 'US Session', 'Trending')
            ],
            'SILVER': [
                ('09:00', '12:00', 'Asian Session', 'Range Bound'),
                ('14:00', '17:00', 'European Session', 'Breakout'),
                ('20:00', '23:30', 'US Session', 'Strong Trend')
            ],
            'CRUDE': [
                ('10:00', '14:30', 'Asian Session', 'Low Volume'),
                ('14:30', '19:00', 'European Session', 'Inventory Data'),
                ('19:00', '23:30', 'US Session', 'High Volatility')
            ]
        }
        
        if selected_item in commodity_sessions:
            for start, end, session, nature in commodity_sessions[selected_item]:
                planet, symbol, _ = get_planetary_influence(datetime.strptime(start, '%H:%M').time())
                timings.append({
                    'Session': session,
                    'Time': f"{start} - {end}",
                    'Nature': nature,
                    'Planet': f"{symbol} {planet}",
                    'Strategy': 'Buy' if 'Trend' in nature else 'Wait'
                })
    
    elif market_type == "Global":
        # Global market timings
        global_timings = {
            'DOWJONES': ('19:00', '01:30', 'NYSE Session'),
            'NASDAQ': ('19:00', '01:30', 'NASDAQ Session'),
            'FTSE': ('13:30', '20:00', 'London Session'),
            'NIKKEI': ('05:30', '11:30', 'Tokyo Session'),
            'HANGSENG': ('06:30', '13:00', 'Hong Kong Session')
        }
        
        if selected_item in global_timings:
            start, end, session = global_timings[selected_item]
            timings.append({
                'Market': selected_item,
                'Session': session,
                'Timing': f"{start} - {end} IST",
                'Current Status': 'Open' if is_market_open(start, end) else 'Closed',
                'Planetary Hour': get_planetary_influence(current_time)[1] + ' ' + get_planetary_influence(current_time)[0]
            })
    
    return timings

# Function to check if market is open
def is_market_open(start_str, end_str):
    current_time = datetime.now().time()
    start_time = datetime.strptime(start_str, '%H:%M').time()
    end_time = datetime.strptime(end_str, '%H:%M').time()
    
    if start_time <= end_time:
        return start_time <= current_time <= end_time
    else:  # Handles overnight sessions
        return current_time >= start_time or current_time <= end_time

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

# Header
st.markdown("""
<div class="main-header">
    <h1>Vedic Birth Chart & Live Market Intelligence</h1>
    <p>Real-time Kundali Analysis with Live Market Data & Astrological Predictions</p>
</div>
""", unsafe_allow_html=True)

# Controls
col1, col2, col3, col4 = st.columns(4)

with col1:
    auto_refresh = st.checkbox("🔄 Auto-Refresh", value=False)

with col2:
    if st.button("📈 Update Now", type="primary"):
        if update_market_data():
            st.success("Data updated!")
        st.rerun()

with col3:
    refresh_rate = st.selectbox("Rate (sec)", [5, 10, 30], index=0)

with col4:
    # Quick view buttons
    view_mode = st.selectbox("Quick View", ["Overview", "Bullish Only", "Bearish Only", "Active Now"])

# Apply quick view filter
if view_mode == "Bullish Only":
    st.markdown("<p style='color: #28a745; font-weight: bold'>🟢 Showing only Bullish markets/sectors</p>", unsafe_allow_html=True)
elif view_mode == "Bearish Only":
    st.markdown("<p style='color: #dc3545; font-weight: bold'>🔴 Showing only Bearish markets/sectors</p>", unsafe_allow_html=True)
elif view_mode == "Active Now":
    st.markdown("<p style='color: #ff6b35; font-weight: bold'>🔥 Showing only active trading opportunities</p>", unsafe_allow_html=True)

# Show current time and planetary hour
current_time = datetime.now()
planet, symbol, influence = get_planetary_influence(current_time)

# Quick Alerts Section
if st.session_state.get('show_alerts', True):
    current_hour = datetime.now().hour
    current_minute = datetime.now().minute
    
    # Morning alerts (9:00 - 10:30)
    if 9 <= current_hour < 10 or (current_hour == 10 and current_minute <= 30):
        st.markdown("""
        <div style='background-color: #d4edda; padding: 10px; border-radius: 5px; margin: 10px 0;'>
            <strong>🌅 Morning Session Alert:</strong>
            <span class='bullish-text'>FMCG & Pharma sectors favorable</span> | 
            <span class='bearish-text'>Avoid Metal stocks</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Noon alerts (12:00 - 13:30)
    elif 12 <= current_hour < 13 or (current_hour == 13 and current_minute <= 30):
        st.markdown("""
        <div style='background-color: #fff3cd; padding: 10px; border-radius: 5px; margin: 10px 0;'>
            <strong>🌞 Midday Alert:</strong>
            <span class='volatile-text'>Energy sector volatile</span> | 
            <span class='neutral-text'>Auto sector ranging</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Closing alerts (14:00 - 15:30)
    elif 14 <= current_hour < 15 or (current_hour == 15 and current_minute <= 30):
        st.markdown("""
        <div style='background-color: #f8d7da; padding: 10px; border-radius: 5px; margin: 10px 0;'>
            <strong>🌆 Closing Session Alert:</strong>
            <span class='bearish-text'>IT & Metal sectors weak</span> | 
            <span class='bullish-text'>Book profits in morning trades</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Evening/Global alerts (19:00 - 23:30)
    elif 19 <= current_hour <= 23:
        st.markdown("""
        <div style='background-color: #d1ecf1; padding: 10px; border-radius: 5px; margin: 10px 0;'>
            <strong>🌙 Global Session Alert:</strong>
            <span class='bullish-text'>Gold & Silver active</span> | 
            <span class='volatile-text'>Watch US market opening</span>
        </div>
        """, unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.write(f"🕐 **Current Time:** {current_time.strftime('%H:%M:%S')}")
with col2:
    st.write(f"{symbol} **Planetary Hour:** {planet}")
with col3:
    st.write(f"📊 **Influence:** {influence}")

# Market Sentiment Summary
st.write("---")
sentiment_col1, sentiment_col2, sentiment_col3, sentiment_col4 = st.columns(4)

with sentiment_col1:
    bullish_count = sum(1 for _, data in st.session_state.astro_predictions['sectors'].items() if 'Bullish' in data['trend'])
    st.markdown(f"<div style='text-align: center'><h3 style='color: #28a745'>🟢 {bullish_count}</h3><p>Bullish Sectors</p></div>", unsafe_allow_html=True)

with sentiment_col2:
    bearish_count = sum(1 for _, data in st.session_state.astro_predictions['sectors'].items() if 'Bearish' in data['trend'])
    st.markdown(f"<div style='text-align: center'><h3 style='color: #dc3545'>🔴 {bearish_count}</h3><p>Bearish Sectors</p></div>", unsafe_allow_html=True)

with sentiment_col3:
    neutral_count = sum(1 for _, data in st.session_state.astro_predictions['sectors'].items() if 'Neutral' in data['trend'] or 'Volatile' in data['trend'])
    st.markdown(f"<div style='text-align: center'><h3 style='color: #ffc107'>🟡 {neutral_count}</h3><p>Neutral/Volatile</p></div>", unsafe_allow_html=True)

with sentiment_col4:
    # Overall market sentiment based on planetary hour
    if planet in ['Sun', 'Jupiter', 'Venus']:
        st.markdown("<div style='text-align: center'><h3 style='color: #28a745'>BULLISH</h3><p>Overall Sentiment</p></div>", unsafe_allow_html=True)
    elif planet in ['Saturn', 'Mars']:
        st.markdown("<div style='text-align: center'><h3 style='color: #dc3545'>BEARISH</h3><p>Overall Sentiment</p></div>", unsafe_allow_html=True)
    else:
        st.markdown("<div style='text-align: center'><h3 style='color: #ffc107'>MIXED</h3><p>Overall Sentiment</p></div>", unsafe_allow_html=True)

st.write("---")

# Auto-refresh logic
if auto_refresh:
    time.sleep(refresh_rate)
    update_market_data()
    st.rerun()

# Ticker display
try:
    ticker_items = []
    for market, data in list(st.session_state.market_data.items())[:5]:
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
        st.balloons()
    
    # Simple birth chart representation
    st.write("### 📊 Birth Chart (North Indian Style)")
    
    # Create a simple 4x4 grid for the chart
    chart_data = [
        ['12♓', '1♈', '2♉', '3♊'],
        ['11♒', '🕉️', 'Rasi', '4♋'],
        ['10♑', 'Chart', '⭐', '5♌'],
        ['9♐', '8♏', '7♎', '6♍']
    ]
    
    chart_df = pd.DataFrame(chart_data, columns=['Col1', 'Col2', 'Col3', 'Col4'])
    st.dataframe(chart_df, hide_index=True, use_container_width=True, 
                 column_config={
                     "Col1": st.column_config.TextColumn(label=""),
                     "Col2": st.column_config.TextColumn(label=""),
                     "Col3": st.column_config.TextColumn(label=""),
                     "Col4": st.column_config.TextColumn(label="")
                 })
    
    # Show planetary placements with market predictions
    st.write("### 🏠 Planetary Positions & Market Impact")
    
    # Planetary market influences
    planetary_market = {
        'Sun': {'sectors': 'Power, Energy, Pharma', 'trend': 'Bullish'},
        'Moon': {'sectors': 'FMCG, Dairy, Hotels', 'trend': 'Volatile'},
        'Mars': {'sectors': 'Defense, Metal, Energy', 'trend': 'Aggressive'},
        'Mercury': {'sectors': 'IT, Telecom, Media', 'trend': 'Mixed'},
        'Jupiter': {'sectors': 'Banking, Finance, Gold', 'trend': 'Positive'},
        'Venus': {'sectors': 'Auto, Luxury, Entertainment', 'trend': 'Stable'},
        'Saturn': {'sectors': 'Mining, Cement, Oil', 'trend': 'Bearish'},
        'Rahu': {'sectors': 'Tech, Crypto, Airlines', 'trend': 'Volatile'},
        'Ketu': {'sectors': 'Pharma, Spiritual, Research', 'trend': 'Uncertain'}
    }
    
    for planet, data in st.session_state.planetary_data.items():
        market_info = planetary_market.get(planet, {})
        trend = market_info.get('trend', 'N/A')
        
        # Apply color based on trend
        if trend in ['Bullish', 'Positive']:
            trend_class = 'bullish-text'
        elif trend in ['Bearish', 'Negative']:
            trend_class = 'bearish-text'
        elif trend in ['Volatile', 'Aggressive']:
            trend_class = 'volatile-text'
        else:
            trend_class = 'neutral-text'
            
        st.markdown(f"""
        <div class="planet-info">
            <strong>{data['symbol']} {planet}</strong> - {data['sign']} {data['degree']}<br>
            Nakshatra: {data['nakshatra']} | House: {data['house']}<br>
            <strong>Market Impact:</strong> {market_info.get('sectors', 'N/A')} - <span class="{trend_class}">{trend}</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

with main_col2:
    st.markdown('<div class="chart-box">', unsafe_allow_html=True)
    st.subheader("📊 Live Market Dashboard")
    
    # Market type selector
    market_type = st.selectbox(
        "Select Market Type",
        ["Overview", "Sector", "Commodity", "Global"],
        help="Choose market type for detailed analysis"
    )
    
    if market_type == "Overview":
        # Display market cards
        try:
            # Show indices
            st.write("#### 📊 Indices")
            indices = ['NIFTY', 'BANKNIFTY', 'SENSEX']
            cols = st.columns(3)
            
            for idx, market in enumerate(indices):
                if market in st.session_state.market_data:
                    data = st.session_state.market_data[market]
                    color_class = "positive" if data['change'] >= 0 else "negative"
                    arrow = "▲" if data['change'] >= 0 else "▼"
                    
                    cols[idx].markdown(f"""
                    <div class="market-card">
                        <h4>{market}</h4>
                        <h2>{data['price']:.2f}</h2>
                        <p class="{color_class}">
                            {arrow} {abs(data['change']):.2f}%
                        </p>
                        <small>H: {data['high']:.1f} | L: {data['low']:.1f}</small>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Show commodities
            st.write("#### 🏭 Commodities")
            commodities = ['GOLD', 'SILVER', 'CRUDE']
            cols = st.columns(3)
            
            for idx, market in enumerate(commodities):
                if market in st.session_state.market_data:
                    data = st.session_state.market_data[market]
                    color_class = "positive" if data['change'] >= 0 else "negative"
                    arrow = "▲" if data['change'] >= 0 else "▼"
                    
                    # Format price based on commodity
                    if market == 'GOLD':
                        price_str = f"₹{data['price']:,.0f}"
                    elif market == 'SILVER':
                        price_str = f"₹{data['price']:,.0f}"
                    elif market == 'CRUDE':
                        price_str = f"₹{data['price']:,.0f}"
                    else:
                        price_str = f"{data['price']:.2f}"
                    
                    cols[idx].markdown(f"""
                    <div class="market-card">
                        <h4>{market}</h4>
                        <h3>{price_str}</h3>
                        <p class="{color_class}">
                            {arrow} {abs(data['change']):.2f}%
                        </p>
                        <small>H: {data['high']:,.0f} | L: {data['low']:,.0f}</small>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Show global markets
            st.write("#### 🌍 Global Markets")
            global_markets = ['DOWJONES', 'NASDAQ', 'USDINR']
            cols = st.columns(3)
            
            for idx, market in enumerate(global_markets):
                if market in st.session_state.market_data:
                    data = st.session_state.market_data[market]
                    color_class = "positive" if data['change'] >= 0 else "negative"
                    arrow = "▲" if data['change'] >= 0 else "▼"
                    
                    cols[idx].markdown(f"""
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
    
    elif market_type == "Sector":
        selected_sector = st.selectbox(
            "Select Sector",
            list(st.session_state.astro_predictions['sectors'].keys())
        )
        
        sector_data = st.session_state.astro_predictions['sectors'][selected_sector]
        
        # Enhanced sector display with timing
        col1, col2 = st.columns(2)
        with col1:
            trend_color = "🟢" if "Bullish" in sector_data['trend'] else "🔴" if "Bearish" in sector_data['trend'] else "🟡"
            
            # Apply colored styling to trend
            if "Bullish" in sector_data['trend']:
                trend_html = f'<span class="trend-bullish">{sector_data["trend"]}</span>'
            elif "Bearish" in sector_data['trend']:
                trend_html = f'<span class="trend-bearish">{sector_data["trend"]}</span>'
            else:
                trend_html = f'<span class="trend-neutral">{sector_data["trend"]}</span>'
            
            st.markdown(f'{trend_color} **Trend:** {trend_html}', unsafe_allow_html=True)
            st.info(f"🪐 **Planetary Influence:** {sector_data['planet']}")
        with col2:
            st.info(f"⏰ **Best Trading Time:** {sector_data['timing']}")
            current_time_str = datetime.now().strftime('%H:%M')
            if is_time_in_range(current_time_str, sector_data['timing']):
                st.success("🔥 ACTIVE NOW - Good time to trade!")
        
        # Show sector stocks with timing
        st.write("### 📈 Intraday Stock Timings")
        timings = get_market_timing("Sector", selected_sector)
        if timings:
            # Create custom display for colored trends
            for timing in timings:
                col1, col2, col3, col4, col5, col6 = st.columns([2, 1.5, 1, 1, 1.5, 1])
                
                with col1:
                    st.write(f"**{timing['Stock']}**")
                
                with col2:
                    if timing['Trend'] == 'Bullish':
                        st.markdown('<span class="trend-bullish">Bullish</span>', unsafe_allow_html=True)
                    elif timing['Trend'] == 'Bearish':
                        st.markdown('<span class="trend-bearish">Bearish</span>', unsafe_allow_html=True)
                    else:
                        st.markdown('<span class="trend-neutral">Neutral</span>', unsafe_allow_html=True)
                
                with col3:
                    st.write(timing['Start'])
                
                with col4:
                    st.write(timing['End'])
                
                with col5:
                    st.write(timing['Planet'])
                
                with col6:
                    if timing['Trend'] == 'Bullish':
                        st.markdown(f'<span class="bullish-text">{timing["Target"]}</span>', unsafe_allow_html=True)
                    elif timing['Trend'] == 'Bearish':
                        st.markdown(f'<span class="bearish-text">{timing["Target"]}</span>', unsafe_allow_html=True)
                    else:
                        st.write(timing['Target'])
    
    elif market_type == "Commodity":
        selected_commodity = st.selectbox(
            "Select Commodity",
            ['GOLD', 'SILVER', 'CRUDE', 'NATURALGAS', 'COPPER']
        )
        
        if selected_commodity in st.session_state.astro_predictions['commodities']:
            comm_data = st.session_state.astro_predictions['commodities'][selected_commodity]
            
            # Apply colored styling to trend
            if "Bullish" in comm_data['trend']:
                trend_html = f'<span class="trend-bullish">{comm_data["trend"]}</span>'
            elif "Bearish" in comm_data['trend']:
                trend_html = f'<span class="trend-bearish">{comm_data["trend"]}</span>'
            elif "Volatile" in comm_data['trend']:
                trend_html = f'<span class="trend-volatile">{comm_data["trend"]}</span>'
            else:
                trend_html = f'<span class="trend-neutral">{comm_data["trend"]}</span>'
            
            st.markdown(f'**{selected_commodity}:** {trend_html} | {comm_data["planet"]} | Active: {comm_data["timing"]}', unsafe_allow_html=True)
        
        # Show commodity current price if available
        if selected_commodity in st.session_state.market_data:
            price_data = st.session_state.market_data[selected_commodity]
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Current Price", f"₹{price_data['price']:,.2f}")
            with col2:
                st.metric("Change", f"{price_data['change']:+.2f}%")
            with col3:
                st.metric("Day High", f"₹{price_data['high']:,.2f}")
            with col4:
                st.metric("Day Low", f"₹{price_data['low']:,.2f}")
        
        # Show commodity session timings
        st.write("### ⏰ Session-wise Analysis")
        timings = get_market_timing("Commodity", selected_commodity)
        if timings:
            for timing in timings:
                st.markdown(f"""
                <div class="timing-alert">
                    <strong>{timing['Session']}</strong> ({timing['Time']})<br>
                    Nature: {timing['Nature']} | Planet: {timing['Planet']}<br>
                    Strategy: {timing['Strategy']}
                </div>
                """, unsafe_allow_html=True)
    
    elif market_type == "Global":
        selected_global = st.selectbox(
            "Select Global Market",
            list(st.session_state.astro_predictions['global'].keys())
        )
        
        global_data = st.session_state.astro_predictions['global'][selected_global]
        
        # Apply colored styling to trend
        if "Bullish" in global_data['trend']:
            trend_html = f'<span class="trend-bullish">{global_data["trend"]}</span>'
        elif "Bearish" in global_data['trend']:
            trend_html = f'<span class="trend-bearish">{global_data["trend"]}</span>'
        elif "Volatile" in global_data['trend']:
            trend_html = f'<span class="trend-volatile">{global_data["trend"]}</span>'
        else:
            trend_html = f'<span class="trend-neutral">{global_data["trend"]}</span>'
        
        st.markdown(f'**{selected_global}:** {trend_html} | {global_data["planet"]} | Trading Hours: {global_data["timing"]} IST', unsafe_allow_html=True)
        
        # Show global market status
        timings = get_market_timing("Global", selected_global)
        if timings:
            for timing in timings:
                status_color = "🟢" if timing['Current Status'] == 'Open' else "🔴"
                st.write(f"{status_color} **{timing['Market']}** - {timing['Session']}")
                st.write(f"Trading Hours: {timing['Timing']}")
                st.write(f"Planetary Hour: {timing['Planetary Hour']}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Live Planetary Transit Section
st.write("---")
st.subheader("🌌 Live Planetary Transits & Market Impact")

# Add current active opportunities
st.write("### 🎯 Active Trading Opportunities Right Now")
current_time_str = datetime.now().strftime('%H:%M')
current_hour = datetime.now().hour

active_opportunities = []

# Check sectors
sector_stocks_quick = {
    'Banking': [
        {'stock': 'HDFC Bank', 'trend': 'Bullish', 'time': '10:30-11:15'},
        {'stock': 'ICICI Bank', 'trend': 'Bullish', 'time': '11:00-12:00'},
        {'stock': 'Kotak Bank', 'trend': 'Bullish', 'time': '09:30-10:30'}
    ],
    'IT': [
        {'stock': 'TCS', 'trend': 'Bearish', 'time': '14:00-15:00'},
        {'stock': 'Infosys', 'trend': 'Bearish', 'time': '14:15-15:15'}
    ],
    'Pharma': [
        {'stock': 'Sun Pharma', 'trend': 'Bullish', 'time': '09:30-10:30'},
        {'stock': 'Dr Reddy', 'trend': 'Bullish', 'time': '10:00-11:00'}
    ]
}

for sector, stocks in sector_stocks_quick.items():
    for stock_info in stocks:
        if is_time_in_range(current_time_str, stock_info['time']):
            active_opportunities.append({
                'Type': 'Stock',
                'Name': stock_info['stock'],
                'Sector': sector,
                'Trend': stock_info['trend'],
                'Signal': 'BUY' if stock_info['trend'] == 'Bullish' else 'SELL',
                'Active Till': stock_info['time'].split('-')[1]
            })

# Check commodities
if 20 <= current_hour <= 23:
    active_opportunities.append({
        'Type': 'Commodity',
        'Name': 'GOLD',
        'Sector': 'Precious Metal',
        'Trend': 'Bullish',
        'Signal': 'BUY',
        'Active Till': '23:30'
    })
    active_opportunities.append({
        'Type': 'Commodity',
        'Name': 'SILVER',
        'Sector': 'Precious Metal',
        'Trend': 'Strong Bullish',
        'Signal': 'BUY',
        'Active Till': '23:30'
    })

if active_opportunities:
    # Display opportunities with custom formatting
    for opp in active_opportunities:
        col1, col2, col3, col4, col5, col6 = st.columns([1, 1.5, 1.5, 1, 1, 1])
        
        with col1:
            st.write(opp['Type'])
        
        with col2:
            st.write(f"**{opp['Name']}**")
        
        with col3:
            st.write(opp['Sector'])
        
        with col4:
            if 'Bullish' in opp['Trend']:
                st.markdown(f'<span class="trend-bullish">{opp["Trend"]}</span>', unsafe_allow_html=True)
            elif 'Bearish' in opp['Trend']:
                st.markdown(f'<span class="trend-bearish">{opp["Trend"]}</span>', unsafe_allow_html=True)
            else:
                st.markdown(f'<span class="trend-neutral">{opp["Trend"]}</span>', unsafe_allow_html=True)
        
        with col5:
            if opp['Signal'] == 'BUY':
                st.markdown('<span class="bullish-text">🟢 BUY</span>', unsafe_allow_html=True)
            else:
                st.markdown('<span class="bearish-text">🔴 SELL</span>', unsafe_allow_html=True)
        
        with col6:
            st.write(f"Till {opp['Active Till']}")
else:
    st.info("No active opportunities at current time. Check sector/commodity tabs for upcoming timings.")

transit_col1, transit_col2 = st.columns(2)

with transit_col1:
    st.markdown("""
    <div class="transit-box">
        <h4>📍 Current Transits</h4>
    </div>
    """, unsafe_allow_html=True)
    
    # Show current planetary transits with colored predictions
    current_hour = datetime.now().hour
    if 9 <= current_hour < 15:
        st.write("**🌞 Day Trading Hours**")
        st.markdown("- Moon in Virgo: <span class='bullish-text'>Technical stocks favorable</span>", unsafe_allow_html=True)
        st.markdown("- Mercury direct: <span class='neutral-text'>IT sector clarity</span>", unsafe_allow_html=True)
        st.markdown("- Mars aspect: <span class='volatile-text'>Energy sector volatile</span>", unsafe_allow_html=True)
    elif 15 <= current_hour < 20:
        st.write("**🌅 Evening Session**")
        st.markdown("- Venus active: <span class='bullish-text'>Auto sector positive</span>", unsafe_allow_html=True)
        st.markdown("- Jupiter aspect: <span class='bullish-text'>Banking stable</span>", unsafe_allow_html=True)
        st.markdown("- Saturn influence: <span class='bearish-text'>Metals cautious</span>", unsafe_allow_html=True)
    else:
        st.write("**🌙 Global Market Hours**")
        st.markdown("- Moon aspects: <span class='bullish-text'>Commodities active</span>", unsafe_allow_html=True)
        st.markdown("- Rahu influence: <span class='volatile-text'>Crypto volatile</span>", unsafe_allow_html=True)
        st.markdown("- Mercury in tech: <span class='bullish-text'>NASDAQ positive</span>", unsafe_allow_html=True)

with transit_col2:
    st.markdown("""
    <div class="transit-box">
        <h4>⏰ Upcoming Market Timings</h4>
    </div>
    """, unsafe_allow_html=True)
    
    # Show upcoming important timings with trend indicators
    upcoming_times = []
    current = datetime.now()
    
    timing_predictions = [
        (1, "Bullish", "Banking, FMCG strong"),
        (2, "Neutral", "Range-bound movement"),
        (3, "Bearish", "Profit booking likely"),
        (4, "Volatile", "News-based moves")
    ]
    
    for i, (hours_ahead, trend, desc) in enumerate(timing_predictions):
        future_time = current + timedelta(hours=hours_ahead)
        planet, symbol, _ = get_planetary_influence(future_time)
        
        time_str = future_time.strftime('%H:%M')
        
        if trend == "Bullish":
            trend_html = f'<span class="bullish-text">{desc}</span>'
        elif trend == "Bearish":
            trend_html = f'<span class="bearish-text">{desc}</span>'
        elif trend == "Volatile":
            trend_html = f'<span class="volatile-text">{desc}</span>'
        else:
            trend_html = f'<span class="neutral-text">{desc}</span>'
        
        st.markdown(f"• {time_str} - {symbol} {planet}: {trend_html}", unsafe_allow_html=True)

# Detailed analysis tabs
tab1, tab2, tab3, tab4 = st.tabs(["📈 Sector Analysis", "🏭 Commodities", "🌍 Global Markets", "⚡ Intraday Signals"])

with tab1:
    st.subheader("📈 Detailed Sector Analysis")
    
    # Show currently active sectors
    current_time_str = datetime.now().strftime('%H:%M')
    active_sectors = []
    
    for sector, data in st.session_state.astro_predictions['sectors'].items():
        if is_time_in_range(current_time_str, data['timing']):
            trend_icon = "🟢" if "Bullish" in data['trend'] else "🔴" if "Bearish" in data['trend'] else "🟡"
            if "Bullish" in data['trend']:
                trend_html = f'<span class="trend-bullish">{data["trend"]}</span>'
            elif "Bearish" in data['trend']:
                trend_html = f'<span class="trend-bearish">{data["trend"]}</span>'
            else:
                trend_html = f'<span class="trend-neutral">{data["trend"]}</span>'
            active_sectors.append(f"{trend_icon} **{sector}** ({trend_html})")
    
    if active_sectors:
        st.markdown(f"🔥 **Currently Active Sectors:** {', '.join(active_sectors)}", unsafe_allow_html=True)
    else:
        st.info("💤 No sectors in their optimal trading window currently")
    
    st.write("---")
    
    # Define sector stocks with detailed predictions
    sector_stocks_detail = {
        'Banking': [
            {'stock': 'HDFC Bank', 'trend': 'Bullish', 'time': '10:30-11:15', 'target': '+1.2%'},
            {'stock': 'ICICI Bank', 'trend': 'Bullish', 'time': '11:00-12:00', 'target': '+0.8%'},
            {'stock': 'SBI', 'trend': 'Neutral', 'time': '13:00-14:00', 'target': '±0.3%'},
            {'stock': 'Axis Bank', 'trend': 'Bearish', 'time': '14:30-15:15', 'target': '-0.6%'},
            {'stock': 'Kotak Bank', 'trend': 'Bullish', 'time': '09:30-10:30', 'target': '+0.9%'}
        ],
        'IT': [
            {'stock': 'TCS', 'trend': 'Bearish', 'time': '14:00-15:00', 'target': '-0.8%'},
            {'stock': 'Infosys', 'trend': 'Bearish', 'time': '14:15-15:15', 'target': '-1.1%'},
            {'stock': 'Wipro', 'trend': 'Neutral', 'time': '11:30-12:30', 'target': '±0.4%'},
            {'stock': 'HCL Tech', 'trend': 'Bearish', 'time': '13:45-14:45', 'target': '-0.9%'},
            {'stock': 'Tech Mahindra', 'trend': 'Bearish', 'time': '14:00-15:00', 'target': '-1.3%'}
        ],
        'Pharma': [
            {'stock': 'Sun Pharma', 'trend': 'Bullish', 'time': '09:30-10:30', 'target': '+1.5%'},
            {'stock': 'Dr Reddy', 'trend': 'Bullish', 'time': '10:00-11:00', 'target': '+1.2%'},
            {'stock': 'Cipla', 'trend': 'Neutral', 'time': '11:30-12:30', 'target': '±0.5%'},
            {'stock': 'Divis Lab', 'trend': 'Bullish', 'time': '09:45-10:45', 'target': '+0.9%'},
            {'stock': 'Biocon', 'trend': 'Bearish', 'time': '14:00-15:00', 'target': '-0.7%'}
        ],
        'Auto': [
            {'stock': 'Maruti', 'trend': 'Neutral', 'time': '11:30-12:30', 'target': '±0.3%'},
            {'stock': 'Tata Motors', 'trend': 'Bullish', 'time': '12:00-13:00', 'target': '+0.8%'},
            {'stock': 'M&M', 'trend': 'Neutral', 'time': '11:45-12:45', 'target': '±0.4%'},
            {'stock': 'Bajaj Auto', 'trend': 'Bearish', 'time': '13:30-14:30', 'target': '-0.6%'},
            {'stock': 'Hero Motor', 'trend': 'Neutral', 'time': '11:00-12:00', 'target': '±0.2%'}
        ],
        'Metal': [
            {'stock': 'Tata Steel', 'trend': 'Bearish', 'time': '13:30-14:30', 'target': '-1.8%'},
            {'stock': 'JSW Steel', 'trend': 'Bearish', 'time': '13:45-14:45', 'target': '-1.5%'},
            {'stock': 'Hindalco', 'trend': 'Bearish', 'time': '14:00-15:00', 'target': '-1.3%'},
            {'stock': 'Vedanta', 'trend': 'Neutral', 'time': '12:00-13:00', 'target': '±0.5%'},
            {'stock': 'SAIL', 'trend': 'Bearish', 'time': '13:30-14:30', 'target': '-2.1%'}
        ],
        'FMCG': [
            {'stock': 'HUL', 'trend': 'Bullish', 'time': '09:15-10:15', 'target': '+0.6%'},
            {'stock': 'ITC', 'trend': 'Bullish', 'time': '09:30-10:30', 'target': '+0.8%'},
            {'stock': 'Nestle', 'trend': 'Neutral', 'time': '11:00-12:00', 'target': '±0.3%'},
            {'stock': 'Britannia', 'trend': 'Bullish', 'time': '10:00-11:00', 'target': '+0.7%'},
            {'stock': 'Dabur', 'trend': 'Bullish', 'time': '09:45-10:45', 'target': '+0.5%'}
        ],
        'Energy': [
            {'stock': 'Reliance', 'trend': 'Volatile', 'time': '12:00-13:30', 'target': '±1.5%'},
            {'stock': 'ONGC', 'trend': 'Bearish', 'time': '13:00-14:00', 'target': '-0.9%'},
            {'stock': 'IOC', 'trend': 'Bearish', 'time': '13:30-14:30', 'target': '-0.7%'},
            {'stock': 'BPCL', 'trend': 'Neutral', 'time': '12:30-13:30', 'target': '±0.4%'},
            {'stock': 'GAIL', 'trend': 'Volatile', 'time': '12:15-13:45', 'target': '±1.2%'}
        ],
        'Realty': [
            {'stock': 'DLF', 'trend': 'Bearish', 'time': '14:30-15:15', 'target': '-1.2%'},
            {'stock': 'Godrej Prop', 'trend': 'Bearish', 'time': '14:15-15:15', 'target': '-0.9%'},
            {'stock': 'Oberoi Realty', 'trend': 'Neutral', 'time': '13:00-14:00', 'target': '±0.5%'},
            {'stock': 'Brigade', 'trend': 'Bearish', 'time': '14:00-15:00', 'target': '-0.8%'},
            {'stock': 'Sobha', 'trend': 'Bearish', 'time': '14:30-15:30', 'target': '-1.0%'}
        ]
    }
    
    # Create expandable sections for each sector
    for sector, stocks in sector_stocks_detail.items():
        with st.expander(f"📊 {sector} Sector Analysis", expanded=False):
            # Get sector-level prediction
            sector_pred = st.session_state.astro_predictions['sectors'].get(
                sector, 
                {'trend': 'Neutral', 'planet': 'Mixed', 'timing': '09:15-15:30'}
            )
            
            # Show sector overview with colored trend
            col1, col2, col3 = st.columns(3)
            with col1:
                if "Bullish" in sector_pred['trend']:
                    trend_display = '<span class="trend-bullish">Bullish</span>'
                elif "Bearish" in sector_pred['trend']:
                    trend_display = '<span class="trend-bearish">Bearish</span>'
                else:
                    trend_display = '<span class="trend-neutral">Neutral</span>'
                st.markdown(f"**Overall Trend:** {trend_display}", unsafe_allow_html=True)
            with col2:
                st.write(f"**Planetary Influence:** {sector_pred['planet']}")
            with col3:
                st.write(f"**Best Hours:** {sector_pred['timing']}")
            
            st.write("---")
            
            # Show individual stocks with colored trends
            stock_data = []
            for stock_info in stocks:
                stock_data.append({
                    'Stock': stock_info['stock'],
                    'Trend': stock_info['trend'],
                    'Best Time': stock_info['time'],
                    'Expected Move': stock_info['target'],
                    'Signal': '🟢 BUY' if stock_info['trend'] == 'Bullish' else '🔴 SELL' if stock_info['trend'] == 'Bearish' else '🟡 CAUTION' if stock_info['trend'] == 'Volatile' else '🟡 HOLD'
                })
            
            # Create custom styled dataframe
            stock_df = pd.DataFrame(stock_data)
            
            # Apply custom styling
            def style_trend(val):
                if val == 'Bullish':
                    return 'background-color: #d4edda; color: #155724; font-weight: bold'
                elif val == 'Bearish':
                    return 'background-color: #f8d7da; color: #721c24; font-weight: bold'
                elif val == 'Volatile':
                    return 'background-color: #ffe5d4; color: #a04000; font-weight: bold'
                else:
                    return 'background-color: #fff3cd; color: #856404; font-weight: bold'
            
            def style_target(val):
                if val.startswith('+'):
                    return 'color: #28a745; font-weight: bold'
                elif val.startswith('-'):
                    return 'color: #dc3545; font-weight: bold'
                else:
                    return 'color: #ffc107; font-weight: bold'
            
            styled_df = stock_df.style.applymap(style_trend, subset=['Trend']).applymap(style_target, subset=['Expected Move'])
            st.dataframe(styled_df, use_container_width=True, hide_index=True)
            
            # Add timing note
            current_hour = datetime.now().hour
            current_min = datetime.now().minute
            current_time_str = f"{current_hour:02d}:{current_min:02d}"
            
            active_stocks = [s for s in stocks if is_time_in_range(current_time_str, s['time'])]
            if active_stocks:
                st.success(f"🔔 Active Now: {', '.join([s['stock'] for s in active_stocks])}")
            
    # Add legend at the bottom
    st.write("---")
    st.write("### 📌 Signal Legend")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.write("🟢 **BUY** - Strong bullish signal")
    with col2:
        st.write("🔴 **SELL** - Strong bearish signal")
    with col3:
        st.write("🟡 **HOLD** - Neutral, wait for clarity")
    with col4:
        st.write("🟡 **CAUTION** - High volatility expected")

with tab2:
    st.subheader("🏭 Commodity Trading Windows")
    
    # Define detailed commodity timings
    commodity_details = {
        'GOLD': {
            'sessions': [
                {'session': 'Asian Opening', 'time': '09:00-10:30', 'trend': 'Accumulation', 'action': 'BUY dips'},
                {'session': 'Indian Morning', 'time': '10:30-12:00', 'trend': 'Range Bound', 'action': 'WAIT'},
                {'session': 'European Open', 'time': '14:00-16:00', 'trend': 'Volatile', 'action': 'SCALP'},
                {'session': 'US Pre-Open', 'time': '18:00-20:00', 'trend': 'Trending', 'action': 'FOLLOW trend'},
                {'session': 'US Session', 'time': '20:00-23:30', 'trend': 'Strong Moves', 'action': 'POSITION'}
            ],
            'key_levels': {'support': 71500, 'resistance': 72200, 'pivot': 71850}
        },
        'SILVER': {
            'sessions': [
                {'session': 'Asian Opening', 'time': '09:00-10:30', 'trend': 'Quiet', 'action': 'WAIT'},
                {'session': 'Indian Morning', 'time': '10:30-12:00', 'trend': 'Building', 'action': 'ACCUMULATE'},
                {'session': 'European Open', 'time': '14:00-16:00', 'trend': 'Breakout', 'action': 'BUY breakouts'},
                {'session': 'US Pre-Open', 'time': '18:00-20:00', 'trend': 'Volatile', 'action': 'TIGHT stops'},
                {'session': 'US Session', 'time': '20:00-23:30', 'trend': 'Trending Strong', 'action': 'RIDE trend'}
            ],
            'key_levels': {'support': 90500, 'resistance': 92000, 'pivot': 91250}
        },
        'CRUDE': {
            'sessions': [
                {'session': 'Asian Session', 'time': '06:30-10:00', 'trend': 'Low Volume', 'action': 'AVOID'},
                {'session': 'Indian Session', 'time': '10:00-14:30', 'trend': 'Range Trade', 'action': 'SCALP'},
                {'session': 'Inventory Time', 'time': '20:00-21:00', 'trend': 'High Volatility', 'action': 'CAUTION'},
                {'session': 'US Session', 'time': '19:00-23:30', 'trend': 'Trending', 'action': 'POSITION'}
            ],
            'key_levels': {'support': 6800, 'resistance': 6920, 'pivot': 6845}
        },
        'NATURALGAS': {
            'sessions': [
                {'session': 'Morning', 'time': '09:00-12:00', 'trend': 'Quiet', 'action': 'WAIT'},
                {'session': 'Afternoon', 'time': '14:00-17:00', 'trend': 'Building', 'action': 'WATCH'},
                {'session': 'US Open', 'time': '19:00-21:00', 'trend': 'Volatile', 'action': 'SCALP'},
                {'session': 'Inventory', 'time': '20:00-20:30', 'trend': 'Spike', 'action': 'AVOID'}
            ],
            'key_levels': {'support': 220, 'resistance': 245, 'pivot': 232}
        },
        'COPPER': {
            'sessions': [
                {'session': 'Asian Trade', 'time': '06:30-10:00', 'trend': 'Active', 'action': 'TRADE'},
                {'session': 'London Open', 'time': '13:30-16:00', 'trend': 'Trending', 'action': 'FOLLOW'},
                {'session': 'US Session', 'time': '19:00-22:00', 'trend': 'Volatile', 'action': 'CAUTIOUS'}
            ],
            'key_levels': {'support': 745, 'resistance': 765, 'pivot': 755}
        }
    }
    
    # Create expandable sections for each commodity
    for commodity, details in commodity_details.items():
        with st.expander(f"📊 {commodity} Detailed Analysis", expanded=False):
            # Get commodity prediction
            comm_pred = st.session_state.astro_predictions['commodities'].get(
                commodity,
                {'trend': 'Neutral', 'planet': 'Mixed', 'timing': '09:00-23:30'}
            )
            
            # Overview with colored trend
            col1, col2, col3 = st.columns(3)
            with col1:
                if "Bullish" in comm_pred['trend']:
                    trend_display = '<span class="trend-bullish">Strong Bullish</span>' if "Strong" in comm_pred['trend'] else '<span class="trend-bullish">Bullish</span>'
                elif "Bearish" in comm_pred['trend']:
                    trend_display = '<span class="trend-bearish">Bearish</span>'
                elif "Volatile" in comm_pred['trend']:
                    trend_display = '<span class="trend-volatile">Volatile</span>'
                else:
                    trend_display = '<span class="trend-neutral">Neutral</span>'
                st.markdown(f"**Overall Trend:** {trend_display}", unsafe_allow_html=True)
            with col2:
                st.write(f"**Planetary Rule:** {comm_pred['planet']}")
            with col3:
                st.write(f"**Best Hours:** {comm_pred['timing']}")
            
            # Key levels
            if 'key_levels' in details:
                st.write("### 📍 Key Levels")
                levels = details['key_levels']
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Support", f"₹{levels['support']:,}")
                with col2:
                    st.metric("Pivot", f"₹{levels['pivot']:,}")
                with col3:
                    st.metric("Resistance", f"₹{levels['resistance']:,}")
            
            # Session-wise breakdown
            st.write("### ⏰ Session Breakdown")
            session_data = []
            current_time_str = datetime.now().strftime('%H:%M')
            
            for session in details['sessions']:
                # Check if session is active
                is_active = is_time_in_range(current_time_str, session['time'])
                
                # Determine action color
                if 'BUY' in session['action'] or 'ACCUMULATE' in session['action'] or 'POSITION' in session['action']:
                    action_style = 'bullish-text'
                elif 'AVOID' in session['action'] or 'CAUTION' in session['action']:
                    action_style = 'bearish-text'
                elif 'WAIT' in session['action'] or 'WATCH' in session['action']:
                    action_style = 'neutral-text'
                else:
                    action_style = 'volatile-text'
                
                session_data.append({
                    'Session': session['session'],
                    'Timing': session['time'],
                    'Market Nature': session['trend'],
                    'Action': session['action'],
                    'Action_Style': action_style,
                    'Status': '🟢 ACTIVE' if is_active else '⏸️ Inactive'
                })
            
            # Display session table with styled actions
            for idx, session in enumerate(session_data):
                col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 1])
                with col1:
                    st.write(session['Session'])
                with col2:
                    st.write(session['Timing'])
                with col3:
                    st.write(session['Market Nature'])
                with col4:
                    st.markdown(f'<span class="{session["Action_Style"]}">{session["Action"]}</span>', unsafe_allow_html=True)
                with col5:
                    st.write(session['Status'])
                
                if idx < len(session_data) - 1:
                    st.write("---")
            
            # Current recommendation
            active_sessions = [s for s in details['sessions'] if is_time_in_range(current_time_str, s['time'])]
            if active_sessions:
                action = active_sessions[0]['action']
                if 'BUY' in action or 'ACCUMULATE' in action:
                    st.success(f"🔔 Current Action: {action} ({active_sessions[0]['session']})")
                elif 'AVOID' in action or 'CAUTION' in action:
                    st.error(f"⚠️ Current Action: {action} ({active_sessions[0]['session']})")
                else:
                    st.info(f"💡 Current Action: {action} ({active_sessions[0]['session']})")
            else:
                st.info("💤 No active session currently")
    
    # Add commodity trading tips
    st.write("---")
    st.write("### 💡 Commodity Trading Tips")
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Best Trading Times:**")
        st.markdown("• Gold: <span class='bullish-text'>US Session (20:00-23:30)</span>", unsafe_allow_html=True)
        st.markdown("• Silver: <span class='bullish-text'>European Open (14:00-16:00)</span>", unsafe_allow_html=True)
        st.markdown("• Crude: <span class='bearish-text'>Avoid Inventory (20:00)</span>", unsafe_allow_html=True)
    with col2:
        st.write("**Risk Management:**")
        st.write("• Use 1% risk per trade")
        st.write("• Avoid inventory announcements")
        st.write("• Follow planetary hours")

with tab3:
    st.subheader("🌍 Global Market Outlook")
    
    # Show current global market status
    current_hour = datetime.now().hour
    if 19 <= current_hour <= 23 or 0 <= current_hour <= 2:
        st.success("🟢 US Markets are OPEN")
    elif 13 <= current_hour <= 20:
        st.success("🟢 European Markets are OPEN")
    elif 5 <= current_hour <= 11:
        st.success("🟢 Asian Markets are OPEN")
    else:
        st.info("💤 Major global markets in transition period")
    
    st.write("---")
    
    global_outlook = []
    for market, data in st.session_state.astro_predictions['global'].items():
        global_outlook.append({
            'Market': market,
            'Trend': data['trend'],
            'Astrological Factor': data['planet'],
            'Trading Hours (IST)': data['timing'],
            'Expected Move': f"{'+' if 'Bullish' in data['trend'] else '-' if 'Bearish' in data['trend'] else '±'}{random.uniform(0.3, 1.8):.1f}%"
        })
    
    # Display with custom formatting
    st.write("### 📊 Market-wise Analysis")
    for market_data in global_outlook:
        with st.expander(f"🌐 {market_data['Market']}", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                # Colored trend display
                if "Bullish" in market_data['Trend']:
                    st.markdown(f"**Trend:** <span class='trend-bullish'>{market_data['Trend']}</span>", unsafe_allow_html=True)
                elif "Bearish" in market_data['Trend']:
                    st.markdown(f"**Trend:** <span class='trend-bearish'>{market_data['Trend']}</span>", unsafe_allow_html=True)
                elif "Volatile" in market_data['Trend']:
                    st.markdown(f"**Trend:** <span class='trend-volatile'>{market_data['Trend']}</span>", unsafe_allow_html=True)
                else:
                    st.markdown(f"**Trend:** <span class='trend-neutral'>{market_data['Trend']}</span>", unsafe_allow_html=True)
                
                st.write(f"**Planetary Factor:** {market_data['Astrological Factor']}")
            
            with col2:
                st.write(f"**Trading Hours:** {market_data['Trading Hours (IST)']}")
                
                # Colored expected move
                if market_data['Expected Move'].startswith('+'):
                    st.markdown(f"**Expected Move:** <span class='bullish-text'>{market_data['Expected Move']}</span>", unsafe_allow_html=True)
                elif market_data['Expected Move'].startswith('-'):
                    st.markdown(f"**Expected Move:** <span class='bearish-text'>{market_data['Expected Move']}</span>", unsafe_allow_html=True)
                else:
                    st.markdown(f"**Expected Move:** <span class='neutral-text'>{market_data['Expected Move']}</span>", unsafe_allow_html=True)
            
            # Check if market is currently open
            start, end = market_data['Trading Hours (IST)'].split('-')
            if is_market_open(start, end):
                st.success("🟢 Market is OPEN NOW")
            else:
                st.info("🔴 Market is CLOSED")
    
    # Global market correlation
    st.write("---")
    st.write("### 🔗 Market Correlations & Impact")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Positive Correlations:**")
        st.markdown("• <span class='bullish-text'>NASDAQ ↑</span> → <span class='bullish-text'>IT Stocks ↑</span>", unsafe_allow_html=True)
        st.markdown("• <span class='bullish-text'>DOWJONES ↑</span> → <span class='bullish-text'>Banking ↑</span>", unsafe_allow_html=True)
        st.markdown("• <span class='bullish-text'>Crude ↑</span> → <span class='bullish-text'>Energy Stocks ↑</span>", unsafe_allow_html=True)
    
    with col2:
        st.write("**Inverse Correlations:**")
        st.markdown("• <span class='bearish-text'>Dollar ↑</span> → <span class='bearish-text'>Gold ↓</span>", unsafe_allow_html=True)
        st.markdown("• <span class='bearish-text'>VIX ↑</span> → <span class='bearish-text'>Markets ↓</span>", unsafe_allow_html=True)
        st.markdown("• <span class='bullish-text'>Gold ↑</span> → <span class='bearish-text'>Banking ↓</span>", unsafe_allow_html=True)

with tab4:
    st.subheader("⚡ Live Intraday Signals")
    
    # Generate intraday signals based on current planetary positions
    signals = []
    markets = ['NIFTY', 'BANKNIFTY', 'GOLD', 'CRUDE', 'USDINR']
    
    for market in markets:
        planet, symbol, _ = get_planetary_influence(datetime.now())
        signal_type = random.choice(['BUY', 'SELL', 'HOLD'])
        
        signals.append({
            'Time': datetime.now().strftime('%H:%M:%S'),
            'Market': market,
            'Signal': signal_type,
            'Entry': st.session_state.market_data[market]['price'],
            'Target': st.session_state.market_data[market]['price'] * (1.01 if signal_type == 'BUY' else 0.99),
            'SL': st.session_state.market_data[market]['price'] * (0.995 if signal_type == 'BUY' else 1.005),
            'Planet': f"{symbol} {planet}"
        })
    
    # Create DataFrame
    signals_df = pd.DataFrame(signals)
    
    # Custom styling function
    def style_signal(val):
        if val == 'BUY':
            return 'background-color: #d4edda; color: #155724; font-weight: bold'
        elif val == 'SELL':
            return 'background-color: #f8d7da; color: #721c24; font-weight: bold'
        else:
            return 'background-color: #fff3cd; color: #856404; font-weight: bold'
    
    # Apply styling
    styled_signals = signals_df.style.applymap(style_signal, subset=['Signal'])
    
    # Display with icons
    st.write("### 📊 Current Trading Signals")
    for idx, signal in signals_df.iterrows():
        col1, col2, col3, col4, col5, col6, col7 = st.columns([1.5, 1.5, 1, 1.5, 1.5, 1.5, 1.5])
        
        with col1:
            st.write(f"⏰ {signal['Time']}")
        
        with col2:
            st.write(f"**{signal['Market']}**")
        
        with col3:
            if signal['Signal'] == 'BUY':
                st.markdown('<span class="trend-bullish">🟢 BUY</span>', unsafe_allow_html=True)
            elif signal['Signal'] == 'SELL':
                st.markdown('<span class="trend-bearish">🔴 SELL</span>', unsafe_allow_html=True)
            else:
                st.markdown('<span class="trend-neutral">🟡 HOLD</span>', unsafe_allow_html=True)
        
        with col4:
            st.write(f"₹{signal['Entry']:.2f}")
        
        with col5:
            if signal['Signal'] == 'BUY':
                st.markdown(f'<span class="bullish-text">₹{signal["Target"]:.2f}</span>', unsafe_allow_html=True)
            else:
                st.markdown(f'<span class="bearish-text">₹{signal["Target"]:.2f}</span>', unsafe_allow_html=True)
        
        with col6:
            st.write(f"₹{signal['SL']:.2f}")
        
        with col7:
            st.write(signal['Planet'])
    
    st.write("---")
    
    # Add risk-reward info
    st.write("### 📈 Signal Performance")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        buy_signals = len([s for s in signals if s['Signal'] == 'BUY'])
        st.metric("Buy Signals", buy_signals, f"{(buy_signals/len(signals)*100):.0f}%")
    
    with col2:
        sell_signals = len([s for s in signals if s['Signal'] == 'SELL'])
        st.metric("Sell Signals", sell_signals, f"{(sell_signals/len(signals)*100):.0f}%")
    
    with col3:
        hold_signals = len([s for s in signals if s['Signal'] == 'HOLD'])
        st.metric("Hold Signals", hold_signals, f"{(hold_signals/len(signals)*100):.0f}%")
    
    # Trading tips based on planetary hour
    planet, symbol, influence = get_planetary_influence(datetime.now())
    st.write("---")
    st.write(f"### {symbol} Current Planetary Hour: {planet}")
    st.info(f"💡 {influence}")
    
    # Suggested actions based on planetary hour
    if planet in ['Sun', 'Jupiter']:
        st.success("✅ Favorable time for long positions in index and banking stocks")
    elif planet in ['Venus']:
        st.success("✅ Good time for auto and luxury sector trades")
    elif planet in ['Mercury']:
        st.warning("⚡ High volatility expected in IT and communication stocks")
    elif planet in ['Saturn', 'Mars']:
        st.error("⚠️ Exercise caution - favorable for short positions in metals")
    else:
        st.info("💡 Mixed influences - trade with smaller positions")

# Help/Legend Section (Add before footer)
with st.expander("📚 Color Guide & Trading Legend", expanded=False):
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.write("### 🎨 Trend Colors")
        st.markdown('<span class="trend-bullish">BULLISH</span> - Upward trend expected', unsafe_allow_html=True)
        st.markdown('<span class="trend-bearish">BEARISH</span> - Downward trend expected', unsafe_allow_html=True)
        st.markdown('<span class="trend-neutral">NEUTRAL</span> - Sideways movement', unsafe_allow_html=True)
        st.markdown('<span class="trend-volatile">VOLATILE</span> - High fluctuation', unsafe_allow_html=True)
    
    with col2:
        st.write("### 📊 Signal Meanings")
        st.write("🟢 **BUY** - Enter long position")
        st.write("🔴 **SELL** - Enter short position")
        st.write("🟡 **HOLD** - Wait for clarity")
        st.write("🟡 **CAUTION** - Trade carefully")
    
    with col3:
        st.write("### ⏰ Time Indicators")
        st.write("🔥 **ACTIVE NOW** - In trading window")
        st.write("⏸️ **Inactive** - Outside window")
        st.write("🟢 **Market Open** - Trading hours")
        st.write("🔴 **Market Closed** - Non-trading")
    
    with col4:
        st.write("### 🪐 Planetary Effects")
        st.write("☀️ **Sun** - Leadership stocks")
        st.write("🌙 **Moon** - FMCG, Consumer")
        st.write("♃ **Jupiter** - Banking, Finance")
        st.write("♄ **Saturn** - Metals, Mining")

# Footer
st.write("---")
footer_col1, footer_col2, footer_col3, footer_col4 = st.columns(4)

with footer_col1:
    st.caption(f"🕐 Last Updated: {st.session_state.last_update.strftime('%H:%M:%S')}")

with footer_col2:
    current_planet, current_symbol, _ = get_planetary_influence(datetime.now())
    st.caption(f"{current_symbol} Current Planetary Hour: {current_planet}")

with footer_col3:
    # Show overall market direction
    bullish_markets = sum(1 for _, data in st.session_state.market_data.items() if data['change'] > 0)
    bearish_markets = sum(1 for _, data in st.session_state.market_data.items() if data['change'] < 0)
    
    if bullish_markets > bearish_markets:
        st.caption("📈 Market Direction: BULLISH")
    elif bearish_markets > bullish_markets:
        st.caption("📉 Market Direction: BEARISH")
    else:
        st.caption("➡️ Market Direction: SIDEWAYS")

with footer_col4:
    st.caption("🕉️ Vedic Market Intelligence - Live Predictions")
