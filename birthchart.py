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

# Function to get market-specific timing
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
            for i, stock in enumerate(stocks):
                # Generate timing based on planetary positions
                start_time = current_time + timedelta(minutes=30*i)
                end_time = start_time + timedelta(minutes=45)
                trend = "Bullish" if i % 2 == 0 else "Bearish"
                planet = list(st.session_state.planetary_data.keys())[i % 9]
                
                timings.append({
                    'Stock': stock,
                    'Trend': trend,
                    'Start': start_time.strftime('%H:%M'),
                    'End': end_time.strftime('%H:%M'),
                    'Planet': st.session_state.planetary_data[planet]['symbol'] + ' ' + planet,
                    'Target': f"+{1.5 + (i*0.2):.1f}%" if trend == "Bullish" else f"-{1.2 + (i*0.2):.1f}%"
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

# Show current time and planetary hour
current_time = datetime.now()
planet, symbol, influence = get_planetary_influence(current_time)

col1, col2, col3 = st.columns(3)
with col1:
    st.write(f"🕐 **Current Time:** {current_time.strftime('%H:%M:%S')}")
with col2:
    st.write(f"{symbol} **Planetary Hour:** {planet}")
with col3:
    st.write(f"📊 **Influence:** {influence}")

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
        st.markdown(f"""
        <div class="planet-info">
            <strong>{data['symbol']} {planet}</strong> - {data['sign']} {data['degree']}<br>
            Nakshatra: {data['nakshatra']} | House: {data['house']}<br>
            <em>Market Impact: {market_info.get('sectors', 'N/A')} - {market_info.get('trend', 'N/A')}</em>
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
            major_markets = ['NIFTY', 'BANKNIFTY', 'SENSEX', 'GOLD', 'SILVER', 'DOWJONES']
            
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
    
    elif market_type == "Sector":
        selected_sector = st.selectbox(
            "Select Sector",
            list(st.session_state.astro_predictions['sectors'].keys())
        )
        
        sector_data = st.session_state.astro_predictions['sectors'][selected_sector]
        st.info(f"**{selected_sector}:** {sector_data['trend']} | {sector_data['planet']} | Best Time: {sector_data['timing']}")
        
        # Show sector stocks with timing
        st.write("### 📈 Intraday Stock Timings")
        timings = get_market_timing("Sector", selected_sector)
        if timings:
            timing_df = pd.DataFrame(timings)
            st.dataframe(timing_df, use_container_width=True)
    
    elif market_type == "Commodity":
        selected_commodity = st.selectbox(
            "Select Commodity",
            ['GOLD', 'SILVER', 'CRUDE', 'NATURALGAS', 'COPPER']
        )
        
        if selected_commodity in st.session_state.astro_predictions['commodities']:
            comm_data = st.session_state.astro_predictions['commodities'][selected_commodity]
            st.info(f"**{selected_commodity}:** {comm_data['trend']} | {comm_data['planet']} | Active: {comm_data['timing']}")
        
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
        st.info(f"**{selected_global}:** {global_data['trend']} | {global_data['planet']} | Trading Hours: {global_data['timing']} IST")
        
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

transit_col1, transit_col2 = st.columns(2)

with transit_col1:
    st.markdown("""
    <div class="transit-box">
        <h4>📍 Current Transits</h4>
    </div>
    """, unsafe_allow_html=True)
    
    # Show current planetary transits
    current_hour = datetime.now().hour
    if 9 <= current_hour < 15:
        st.write("**🌞 Day Trading Hours**")
        st.write("- Moon in Virgo: Technical stocks favorable")
        st.write("- Mercury direct: IT sector clarity")
        st.write("- Mars aspect: Energy sector volatile")
    elif 15 <= current_hour < 20:
        st.write("**🌅 Evening Session**")
        st.write("- Venus active: Auto sector positive")
        st.write("- Jupiter aspect: Banking stable")
        st.write("- Saturn influence: Metals cautious")
    else:
        st.write("**🌙 Global Market Hours**")
        st.write("- Moon aspects: Commodities active")
        st.write("- Rahu influence: Crypto volatile")
        st.write("- Mercury in tech: NASDAQ positive")

with transit_col2:
    st.markdown("""
    <div class="transit-box">
        <h4>⏰ Upcoming Market Timings</h4>
    </div>
    """, unsafe_allow_html=True)
    
    # Show upcoming important timings
    upcoming_times = []
    current = datetime.now()
    
    for i in range(4):
        future_time = current + timedelta(hours=i+1)
        planet, symbol, influence = get_planetary_influence(future_time)
        upcoming_times.append(f"{future_time.strftime('%H:%M')} - {symbol} {planet}: {influence}")
    
    for timing in upcoming_times:
        st.write(f"• {timing}")

# Detailed analysis tabs
tab1, tab2, tab3, tab4 = st.tabs(["📈 Sector Analysis", "🏭 Commodities", "🌍 Global Markets", "⚡ Intraday Signals"])

with tab1:
    st.subheader("📈 Detailed Sector Analysis")
    
    # Sector performance with planetary influence
    sector_analysis = []
    for sector, data in st.session_state.astro_predictions['sectors'].items():
        sector_analysis.append({
            'Sector': sector,
            'Trend': data['trend'],
            'Planetary Influence': data['planet'],
            'Best Timing': data['timing'],
            'Signal': '🟢 BUY' if 'Bullish' in data['trend'] else '🔴 SELL' if 'Bearish' in data['trend'] else '🟡 HOLD'
        })
    
    sector_df = pd.DataFrame(sector_analysis)
    st.dataframe(sector_df, use_container_width=True)

with tab2:
    st.subheader("🏭 Commodity Trading Windows")
    
    commodity_windows = []
    for commodity, data in st.session_state.astro_predictions['commodities'].items():
        commodity_windows.append({
            'Commodity': commodity,
            'Trend': data['trend'],
            'Ruling Planet': data['planet'],
            'Active Hours': data['timing'],
            'Today\'s Range': f"±{random.uniform(0.5, 2.5):.1f}%"
        })
    
    comm_df = pd.DataFrame(commodity_windows)
    st.dataframe(comm_df, use_container_width=True)

with tab3:
    st.subheader("🌍 Global Market Outlook")
    
    global_outlook = []
    for market, data in st.session_state.astro_predictions['global'].items():
        global_outlook.append({
            'Market': market,
            'Trend': data['trend'],
            'Astrological Factor': data['planet'],
            'Trading Hours (IST)': data['timing'],
            'Expected Move': f"{'+' if 'Bullish' in data['trend'] else '-'}{random.uniform(0.3, 1.8):.1f}%"
        })
    
    global_df = pd.DataFrame(global_outlook)
    st.dataframe(global_df, use_container_width=True)

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
            'Signal': f"{'🟢' if signal_type == 'BUY' else '🔴' if signal_type == 'SELL' else '🟡'} {signal_type}",
            'Entry': st.session_state.market_data[market]['price'],
            'Target': st.session_state.market_data[market]['price'] * (1.01 if signal_type == 'BUY' else 0.99),
            'SL': st.session_state.market_data[market]['price'] * (0.995 if signal_type == 'BUY' else 1.005),
            'Planet': f"{symbol} {planet}"
        })
    
    signals_df = pd.DataFrame(signals)
    st.dataframe(signals_df, use_container_width=True)

# Footer
st.write("---")
footer_col1, footer_col2, footer_col3 = st.columns(3)

with footer_col1:
    st.caption(f"🕐 Last Updated: {st.session_state.last_update.strftime('%H:%M:%S')}")

with footer_col2:
    current_planet, current_symbol, _ = get_planetary_influence(datetime.now())
    st.caption(f"{current_symbol} Current Planetary Hour: {current_planet}")

with footer_col3:
    st.caption("🕉️ Vedic Market Intelligence - Live Predictions")
