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

# Enhanced CSS with new styles for astro timing section
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
.astro-timing-box {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 20px;
    border-radius: 15px;
    margin: 20px 0;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
}
.time-slot {
    background: rgba(255,255,255,0.1);
    padding: 12px;
    border-radius: 8px;
    margin: 8px 0;
    border-left: 4px solid #ffd700;
}
.planetary-hour {
    background: linear-gradient(45deg, #ff9a56, #ff6b35);
    color: white;
    padding: 15px;
    border-radius: 10px;
    margin: 10px 0;
    text-align: center;
}
.sector-timeline {
    background: #f8f9fa;
    padding: 15px;
    border-radius: 10px;
    margin: 10px 0;
    border: 1px solid #dee2e6;
}
.live-signal {
    background: linear-gradient(45deg, #11998e, #38ef7d);
    color: white;
    padding: 12px;
    border-radius: 8px;
    margin: 8px 0;
    text-align: center;
    font-weight: bold;
}
.warning-signal {
    background: linear-gradient(45deg, #ff416c, #ff4b2b);
    color: white;
    padding: 12px;
    border-radius: 8px;
    margin: 8px 0;
    text-align: center;
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
    
    # Enhanced astrological predictions with detailed timing
    if 'astro_predictions' not in st.session_state:
        st.session_state.astro_predictions = {}
    
    # Set astro data update date
    if 'astro_data_date' not in st.session_state:
        st.session_state.astro_data_date = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    # Initialize NIFTY and BANKNIFTY signals
    if 'nifty_banknifty' not in st.session_state.astro_predictions:
        st.session_state.astro_predictions['nifty_banknifty'] = {
            'NIFTY': {
                'hourly_signals': [
                    {'time': '09:15-10:00', 'trend': 'Bullish', 'planet': 'Venus ♀', 'signal': 'LONG', 'target': '+0.8%', 'sl': '-0.3%'},
                    {'time': '10:00-11:00', 'trend': 'Neutral', 'planet': 'Mercury ☿', 'signal': 'WAIT', 'target': '±0.2%', 'sl': ''},
                    {'time': '11:00-12:00', 'trend': 'Bullish', 'planet': 'Sun ☀️', 'signal': 'LONG', 'target': '+1.2%', 'sl': '-0.4%'},
                    {'time': '12:00-13:00', 'trend': 'Bearish', 'planet': 'Saturn ♄', 'signal': 'SHORT', 'target': '-0.9%', 'sl': '+0.3%'},
                    {'time': '13:00-14:00', 'trend': 'Volatile', 'planet': 'Mars ♂️', 'signal': 'CAUTION', 'target': '±1.5%', 'sl': '±0.5%'},
                    {'time': '14:00-15:00', 'trend': 'Bearish', 'planet': 'Rahu ☊', 'signal': 'SHORT', 'target': '-1.1%', 'sl': '+0.4%'},
                    {'time': '15:00-15:30', 'trend': 'Bullish', 'planet': 'Jupiter ♃', 'signal': 'LONG', 'target': '+0.6%', 'sl': '-0.2%'}
                ]
            },
            'BANKNIFTY': {
                'hourly_signals': [
                    {'time': '09:15-10:00', 'trend': 'Bullish', 'planet': 'Jupiter ♃', 'signal': 'LONG', 'target': '+1.5%', 'sl': '-0.5%'},
                    {'time': '10:00-11:00', 'trend': 'Bullish', 'planet': 'Sun ☀️', 'signal': 'LONG', 'target': '+1.8%', 'sl': '-0.6%'},
                    {'time': '11:00-12:00', 'trend': 'Neutral', 'planet': 'Mercury ☿', 'signal': 'HOLD', 'target': '±0.4%', 'sl': ''},
                    {'time': '12:00-13:00', 'trend': 'Bearish', 'planet': 'Saturn ♄', 'signal': 'SHORT', 'target': '-1.3%', 'sl': '+0.4%'},
                    {'time': '13:00-14:00', 'trend': 'Bearish', 'planet': 'Mars ♂️', 'signal': 'SHORT', 'target': '-1.6%', 'sl': '+0.5%'},
                    {'time': '14:00-15:00', 'trend': 'Volatile', 'planet': 'Rahu ☊', 'signal': 'CAUTION', 'target': '±2.0%', 'sl': '±0.7%'},
                    {'time': '15:00-15:30', 'trend': 'Bullish', 'planet': 'Venus ♀', 'signal': 'LONG', 'target': '+1.0%', 'sl': '-0.3%'}
                ]
            }
        }
    
    # Initialize COMMODITIES and GLOBAL MARKETS signals
    if 'commodities_global' not in st.session_state.astro_predictions:
        st.session_state.astro_predictions['commodities_global'] = {
            'GOLD': {
                'hourly_signals': [
                    {'time': '09:00-10:30', 'trend': 'Bullish', 'planet': 'Sun ☀️', 'signal': 'BUY', 'target': '+0.6%', 'sl': '-0.2%'},
                    {'time': '10:30-12:00', 'trend': 'Neutral', 'planet': 'Mercury ☿', 'signal': 'HOLD', 'target': '±0.3%', 'sl': ''},
                    {'time': '14:00-16:00', 'trend': 'Volatile', 'planet': 'Mars ♂️', 'signal': 'CAUTION', 'target': '±1.2%', 'sl': '±0.4%'},
                    {'time': '18:00-20:00', 'trend': 'Bullish', 'planet': 'Venus ♀', 'signal': 'BUY', 'target': '+0.9%', 'sl': '-0.3%'},
                    {'time': '20:00-23:30', 'trend': 'Strong Bullish', 'planet': 'Jupiter ♃', 'signal': 'STRONG BUY', 'target': '+1.8%', 'sl': '-0.5%'}
                ]
            },
            'SILVER': {
                'hourly_signals': [
                    {'time': '09:00-10:30', 'trend': 'Neutral', 'planet': 'Moon 🌙', 'signal': 'WAIT', 'target': '±0.4%', 'sl': ''},
                    {'time': '10:30-12:00', 'trend': 'Bullish', 'planet': 'Sun ☀️', 'signal': 'BUY', 'target': '+1.2%', 'sl': '-0.4%'},
                    {'time': '14:00-16:00', 'trend': 'Strong Bullish', 'planet': 'Jupiter ♃', 'signal': 'STRONG BUY', 'target': '+2.1%', 'sl': '-0.6%'},
                    {'time': '18:00-20:00', 'trend': 'Volatile', 'planet': 'Mars ♂️', 'signal': 'CAUTION', 'target': '±1.8%', 'sl': '±0.6%'},
                    {'time': '20:00-23:30', 'trend': 'Bullish', 'planet': 'Venus ♀', 'signal': 'BUY', 'target': '+1.5%', 'sl': '-0.5%'}
                ]
            },
            'CRUDE': {
                'hourly_signals': [
                    {'time': '10:00-12:00', 'trend': 'Bearish', 'planet': 'Saturn ♄', 'signal': 'SELL', 'target': '-1.2%', 'sl': '+0.4%'},
                    {'time': '14:30-17:00', 'trend': 'Volatile', 'planet': 'Mars ♂️', 'signal': 'CAUTION', 'target': '±2.5%', 'sl': '±0.8%'},
                    {'time': '19:00-21:00', 'trend': 'Bearish', 'planet': 'Rahu ☊', 'signal': 'SELL', 'target': '-1.8%', 'sl': '+0.6%'},
                    {'time': '21:00-23:30', 'trend': 'Volatile', 'planet': 'Ketu ☋', 'signal': 'AVOID', 'target': '±3.0%', 'sl': '±1.0%'}
                ]
            },
            'BITCOIN': {
                'hourly_signals': [
                    {'time': '09:00-12:00', 'trend': 'Volatile', 'planet': 'Rahu ☊', 'signal': 'CAUTION', 'target': '±3.5%', 'sl': '±1.2%'},
                    {'time': '14:00-18:00', 'trend': 'Bullish', 'planet': 'Mercury ☿', 'signal': 'BUY', 'target': '+2.8%', 'sl': '-1.0%'},
                    {'time': '20:00-02:00', 'trend': 'Strong Bullish', 'planet': 'Jupiter ♃', 'signal': 'STRONG BUY', 'target': '+4.2%', 'sl': '-1.5%'},
                    {'time': '02:00-06:00', 'trend': 'Bearish', 'planet': 'Saturn ♄', 'signal': 'SELL', 'target': '-2.1%', 'sl': '+0.8%'}
                ]
            },
            'DOWJONES': {
                'hourly_signals': [
                    {'time': '19:00-21:00', 'trend': 'Bullish', 'planet': 'Sun ☀️', 'signal': 'BUY', 'target': '+0.9%', 'sl': '-0.3%'},
                    {'time': '21:00-23:00', 'trend': 'Bullish', 'planet': 'Jupiter ♃', 'signal': 'BUY', 'target': '+1.2%', 'sl': '-0.4%'},
                    {'time': '23:00-01:30', 'trend': 'Neutral', 'planet': 'Venus ♀', 'signal': 'HOLD', 'target': '±0.5%', 'sl': ''},
                    {'time': '01:30-03:00', 'trend': 'Bearish', 'planet': 'Saturn ♄', 'signal': 'SELL', 'target': '-0.8%', 'sl': '+0.3%'}
                ]
            }
        }
    
    # Initialize planetary transits
    if 'planetary_transits' not in st.session_state.astro_predictions:
        st.session_state.astro_predictions['planetary_transits'] = [
            {'time': '09:15-10:15', 'planet': 'Venus ♀', 'effect': 'Positive', 'influence': 'Banking, Auto sectors strong', 'markets': 'NIFTY +, BANKNIFTY ++'},
            {'time': '10:15-11:15', 'planet': 'Sun ☀️', 'effect': 'Positive', 'influence': 'Energy, Pharma boost', 'markets': 'Both indices bullish'},
            {'time': '11:15-12:15', 'planet': 'Mercury ☿', 'effect': 'Neutral', 'influence': 'IT sector mixed signals', 'markets': 'Consolidation phase'},
            {'time': '12:15-13:15', 'planet': 'Saturn ♄', 'effect': 'Negative', 'influence': 'Metals, Mining weak', 'markets': 'Profit booking expected'},
            {'time': '13:15-14:15', 'planet': 'Mars ♂️', 'effect': 'Volatile', 'influence': 'Defense up, Energy volatile', 'markets': 'High volatility'},
            {'time': '14:15-15:15', 'planet': 'Rahu ☊', 'effect': 'Negative', 'influence': 'Tech stocks under pressure', 'markets': 'Final hour weakness'},
            {'time': '15:15-15:30', 'planet': 'Jupiter ♃', 'effect': 'Positive', 'influence': 'Financial close strong', 'markets': 'Recovery rally'}
        ]
    
    # Initialize sector timeline
    if 'sector_timeline' not in st.session_state.astro_predictions:
        st.session_state.astro_predictions['sector_timeline'] = {
            '09:15-10:00': {'Banking': 'Bullish', 'IT': 'Neutral', 'Pharma': 'Bullish', 'Auto': 'Bullish', 'Metal': 'Bearish', 'FMCG': 'Bullish', 'Energy': 'Neutral', 'Realty': 'Bearish'},
            '10:00-11:00': {'Banking': 'Bullish', 'IT': 'Bearish', 'Pharma': 'Bullish', 'Auto': 'Neutral', 'Metal': 'Bearish', 'FMCG': 'Bullish', 'Energy': 'Bullish', 'Realty': 'Bearish'},
            '11:00-12:00': {'Banking': 'Neutral', 'IT': 'Bearish', 'Pharma': 'Bullish', 'Auto': 'Bullish', 'Metal': 'Neutral', 'FMCG': 'Neutral', 'Energy': 'Bullish', 'Realty': 'Bearish'},
            '12:00-13:00': {'Banking': 'Bearish', 'IT': 'Neutral', 'Pharma': 'Neutral', 'Auto': 'Bearish', 'Metal': 'Bearish', 'FMCG': 'Neutral', 'Energy': 'Volatile', 'Realty': 'Bearish'},
            '13:00-14:00': {'Banking': 'Bearish', 'IT': 'Bearish', 'Pharma': 'Bearish', 'Auto': 'Neutral', 'Metal': 'Bearish', 'FMCG': 'Bearish', 'Energy': 'Volatile', 'Realty': 'Bearish'},
            '14:00-15:00': {'Banking': 'Volatile', 'IT': 'Bearish', 'Pharma': 'Bearish', 'Auto': 'Bearish', 'Metal': 'Bearish', 'FMCG': 'Bearish', 'Energy': 'Bearish', 'Realty': 'Bearish'},
            '15:00-15:30': {'Banking': 'Bullish', 'IT': 'Neutral', 'Pharma': 'Bullish', 'Auto': 'Bullish', 'Metal': 'Neutral', 'FMCG': 'Bullish', 'Energy': 'Bullish', 'Realty': 'Neutral'}
        }

except Exception as e:
    st.error(f"Error initializing data: {e}")

# Helper functions
def get_planetary_influence(current_time):
    hour = current_time.hour
    minute = current_time.minute
    
    planetary_hours = {
        (9, 10): ("Venus", "♀", "Banking, luxury goods favorable"),
        (10, 11): ("Sun", "☀️", "Energy, pharma sectors strong"),
        (11, 12): ("Mercury", "☿", "IT, communication mixed"),
        (12, 13): ("Saturn", "♄", "Metals, mining cautious"),
        (13, 14): ("Mars", "♂️", "Energy, defense volatile"),
        (14, 15): ("Rahu", "☊", "Tech under pressure"),
        (15, 16): ("Jupiter", "♃", "Banking recovery")
    }
    
    for (start, end), (planet, symbol, influence) in planetary_hours.items():
        if start <= hour < end:
            return planet, symbol, influence
    
    return "Mixed", "🌟", "Multiple planetary influences"

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

# Header
st.markdown("""
<div class="main-header">
    <h1>🕉️ Vedic Market Intelligence Dashboard</h1>
    <p>Live Astrological Market Analysis with Planetary Transit Timing</p>
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
    refresh_rate = st.selectbox("Rate (sec)", [5, 10, 30], index=1)
with col4:
    view_mode = st.selectbox("View", ["Live Signals", "All Timing", "Bullish Only", "Bearish Only"])

# Ticker
try:
    ticker_items = []
    for market, data in list(st.session_state.market_data.items())[:6]:
        arrow = '▲' if data['change'] >= 0 else '▼'
        ticker_items.append(f"{market}: {data['price']:.1f} {arrow} {abs(data['change']):.2f}%")
    
    ticker_text = " | ".join(ticker_items)
    st.markdown(f'<div class="ticker-box">📡 LIVE: {ticker_text}</div>', unsafe_allow_html=True)
except Exception as e:
    st.error(f"Error creating ticker: {e}")

# Global Markets (keeping original structure)
st.subheader("🌍 Global Markets")
global_col1, global_col2, global_col3 = st.columns(3)

with global_col1:
    data = st.session_state.market_data['DOWJONES']
    color_class = "positive" if data['change'] >= 0 else "negative"
    arrow = "▲" if data['change'] >= 0 else "▼"
    st.markdown(f"""
    <div class="market-card">
        <h4>DOWJONES</h4>
        <h2>{data['price']:.2f}</h2>
        <p class="{color_class}">
            {arrow} {abs(data['change']):.2f}%
        </p>
        <small>H: {data['high']:.0f} | L: {data['low']:.0f}</small>
    </div>
    """, unsafe_allow_html=True)

with global_col2:
    data = st.session_state.market_data['NASDAQ']
    color_class = "positive" if data['change'] >= 0 else "negative"
    arrow = "▲" if data['change'] >= 0 else "▼"
    st.markdown(f"""
    <div class="market-card">
        <h4>NASDAQ</h4>
        <h2>{data['price']:.2f}</h2>
        <p class="{color_class}">
            {arrow} {abs(data['change']):.2f}%
        </p>
        <small>H: {data['high']:.0f} | L: {data['low']:.0f}</small>
    </div>
    """, unsafe_allow_html=True)

with global_col3:
    data = st.session_state.market_data['USDINR']
    color_class = "positive" if data['change'] >= 0 else "negative"
    arrow = "▲" if data['change'] >= 0 else "▼"
    st.markdown(f"""
    <div class="market-card">
        <h4>USDINR</h4>
        <h2>{data['price']:.2f}</h2>
        <p class="{color_class}">
            {arrow} {abs(data['change']):.2f}%
        </p>
        <small>H: {data['high']:.2f} | L: {data['low']:.2f}</small>
    </div>
    """, unsafe_allow_html=True)

# NEW ENHANCED ASTRO TIMING SECTION
st.markdown(f"""
<div class="astro-timing-box">
    <h2>🔮 Live Astrological Market Timing Analysis</h2>
    <p>Real-time planetary transit effects on NIFTY, BANKNIFTY, Commodities & Global Markets</p>
    <p style="text-align: right; font-size: 0.9em;">📅 Astro Data Updated: {st.session_state.astro_data_date}</p>
</div>
""", unsafe_allow_html=True)

# Current planetary hour
current_time = datetime.now()
current_planet, current_symbol, current_influence = get_planetary_influence(current_time)
current_time_str = current_time.strftime('%H:%M')

st.markdown(f"""
<div class="planetary-hour">
    <h3>{current_symbol} Current Planetary Hour: {current_planet}</h3>
    <p>🌟 {current_influence}</p>
    <p>⏰ Time: {current_time_str} | Market Effect: <strong>Active Now</strong></p>
</div>
""", unsafe_allow_html=True)

# NIFTY and BANKNIFTY Astro Timing
st.subheader("📊 NIFTY & BANKNIFTY Hourly Astrological Signals")

nifty_banknifty_col1, nifty_banknifty_col2 = st.columns(2)

with nifty_banknifty_col1:
    st.markdown("### 🎯 NIFTY Signals")
    try:
        nifty_signals = st.session_state.astro_predictions['nifty_banknifty']['NIFTY']['hourly_signals']
    except KeyError:
        st.error("NIFTY signals data not available")
        nifty_signals = []
    
    for signal in nifty_signals:
        is_active = is_time_in_range(current_time_str, signal['time'])
        
        if signal['trend'] == 'Bullish':
            trend_class = 'live-signal' if is_active else 'trend-bullish'
            signal_icon = '🟢'
        elif signal['trend'] == 'Bearish':
            trend_class = 'warning-signal' if is_active else 'trend-bearish'
            signal_icon = '🔴'
        elif signal['trend'] == 'Volatile':
            trend_class = 'warning-signal' if is_active else 'trend-volatile'
            signal_icon = '🟡'
        else:
            trend_class = 'trend-neutral'
            signal_icon = '🟡'
        
        active_text = " 🔥 ACTIVE NOW" if is_active else ""
        
        st.markdown(f"""
        <div class="{trend_class}">
            <strong>{signal_icon} {signal['time']}{active_text}</strong><br>
            Planet: {signal['planet']} | Signal: <strong>{signal['signal']}</strong><br>
            Target: {signal['target']} | SL: {signal['sl']}
        </div>
        """, unsafe_allow_html=True)

# COMMODITIES & GLOBAL MARKETS Astro Timing
st.subheader("🏭 Commodities & Global Markets Astrological Signals")

# Create tabs for different market types
commodity_tab1, commodity_tab2, commodity_tab3 = st.tabs(["🥇 Precious Metals", "🛢️ Energy & Crypto", "🌍 Global Indices"])

with commodity_tab1:
    gold_col, silver_col = st.columns(2)
    
    with gold_col:
        st.markdown("### 🥇 GOLD Signals")
        try:
            gold_signals = st.session_state.astro_predictions['commodities_global']['GOLD']['hourly_signals']
        except KeyError:
            st.error("GOLD signals data not available")
            gold_signals = []
        
        for signal in gold_signals:
            is_active = is_time_in_range(current_time_str, signal['time'])
            
            if signal['trend'] == 'Bullish' or signal['trend'] == 'Strong Bullish':
                trend_class = 'live-signal' if is_active else 'trend-bullish'
                signal_icon = '🟢'
            elif signal['trend'] == 'Bearish':
                trend_class = 'warning-signal' if is_active else 'trend-bearish'
                signal_icon = '🔴'
            elif signal['trend'] == 'Volatile':
                trend_class = 'warning-signal' if is_active else 'trend-volatile'
                signal_icon = '🟡'
            else:
                trend_class = 'trend-neutral'
                signal_icon = '🟡'
            
            active_text = " 🔥 ACTIVE NOW" if is_active else ""
            
            st.markdown(f"""
            <div class="{trend_class}">
                <strong>{signal_icon} {signal['time']}{active_text}</strong><br>
                Planet: {signal['planet']} | Signal: <strong>{signal['signal']}</strong><br>
                Target: {signal['target']} | SL: {signal['sl']}
            </div>
            """, unsafe_allow_html=True)
    
    with silver_col:
        st.markdown("### 🥈 SILVER Signals")
        try:
            silver_signals = st.session_state.astro_predictions['commodities_global']['SILVER']['hourly_signals']
        except KeyError:
            st.error("SILVER signals data not available")
            silver_signals = []
        
        for signal in silver_signals:
            is_active = is_time_in_range(current_time_str, signal['time'])
            
            if signal['trend'] == 'Bullish' or signal['trend'] == 'Strong Bullish':
                trend_class = 'live-signal' if is_active else 'trend-bullish'
                signal_icon = '🟢'
            elif signal['trend'] == 'Bearish':
                trend_class = 'warning-signal' if is_active else 'trend-bearish'
                signal_icon = '🔴'
            elif signal['trend'] == 'Volatile':
                trend_class = 'warning-signal' if is_active else 'trend-volatile'
                signal_icon = '🟡'
            else:
                trend_class = 'trend-neutral'
                signal_icon = '🟡'
            
            active_text = " 🔥 ACTIVE NOW" if is_active else ""
            
            st.markdown(f"""
            <div class="{trend_class}">
                <strong>{signal_icon} {signal['time']}{active_text}</strong><br>
                Planet: {signal['planet']} | Signal: <strong>{signal['signal']}</strong><br>
                Target: {signal['target']} | SL: {signal['sl']}
            </div>
            """, unsafe_allow_html=True)

with commodity_tab2:
    crude_col, btc_col = st.columns(2)
    
    with crude_col:
        st.markdown("### 🛢️ CRUDE OIL Signals")
        try:
            crude_signals = st.session_state.astro_predictions['commodities_global']['CRUDE']['hourly_signals']
        except KeyError:
            st.error("CRUDE signals data not available")
            crude_signals = []
        
        for signal in crude_signals:
            is_active = is_time_in_range(current_time_str, signal['time'])
            
            if signal['trend'] == 'Bullish':
                trend_class = 'live-signal' if is_active else 'trend-bullish'
                signal_icon = '🟢'
            elif signal['trend'] == 'Bearish':
                trend_class = 'warning-signal' if is_active else 'trend-bearish'
                signal_icon = '🔴'
            elif signal['trend'] == 'Volatile':
                trend_class = 'warning-signal' if is_active else 'trend-volatile'
                signal_icon = '🟡'
            else:
                trend_class = 'trend-neutral'
                signal_icon = '🟡'
            
            active_text = " 🔥 ACTIVE NOW" if is_active else ""
            
            st.markdown(f"""
            <div class="{trend_class}">
                <strong>{signal_icon} {signal['time']}{active_text}</strong><br>
                Planet: {signal['planet']} | Signal: <strong>{signal['signal']}</strong><br>
                Target: {signal['target']} | SL: {signal['sl']}
            </div>
            """, unsafe_allow_html=True)
    
    with btc_col:
        st.markdown("### ₿ BITCOIN Signals")
        try:
            btc_signals = st.session_state.astro_predictions['commodities_global']['BITCOIN']['hourly_signals']
        except KeyError:
            st.error("BITCOIN signals data not available")
            btc_signals = []
        
        for signal in btc_signals:
            is_active = is_time_in_range(current_time_str, signal['time'])
            
            if signal['trend'] == 'Bullish' or signal['trend'] == 'Strong Bullish':
                trend_class = 'live-signal' if is_active else 'trend-bullish'
                signal_icon = '🟢'
            elif signal['trend'] == 'Bearish':
                trend_class = 'warning-signal' if is_active else 'trend-bearish'
                signal_icon = '🔴'
            elif signal['trend'] == 'Volatile':
                trend_class = 'warning-signal' if is_active else 'trend-volatile'
                signal_icon = '🟡'
            else:
                trend_class = 'trend-neutral'
                signal_icon = '🟡'
            
            active_text = " 🔥 ACTIVE NOW" if is_active else ""
            
            st.markdown(f"""
            <div class="{trend_class}">
                <strong>{signal_icon} {signal['time']}{active_text}</strong><br>
                Planet: {signal['planet']} | Signal: <strong>{signal['signal']}</strong><br>
                Target: {signal['target']} | SL: {signal['sl']}
            </div>
            """, unsafe_allow_html=True)

with commodity_tab3:
    st.markdown("### 🇺🇸 DOW JONES Signals")
    try:
        dow_signals = st.session_state.astro_predictions['commodities_global']['DOWJONES']['hourly_signals']
    except KeyError:
        st.error("DOW JONES signals data not available")
        dow_signals = []
    
    for signal in dow_signals:
        is_active = is_time_in_range(current_time_str, signal['time'])
        
        if signal['trend'] == 'Bullish':
            trend_class = 'live-signal' if is_active else 'trend-bullish'
            signal_icon = '🟢'
        elif signal['trend'] == 'Bearish':
            trend_class = 'warning-signal' if is_active else 'trend-bearish'
            signal_icon = '🔴'
        elif signal['trend'] == 'Volatile':
            trend_class = 'warning-signal' if is_active else 'trend-volatile'
            signal_icon = '🟡'
        else:
            trend_class = 'trend-neutral'
            signal_icon = '🟡'
        
        active_text = " 🔥 ACTIVE NOW" if is_active else ""
        
        st.markdown(f"""
        <div class="{trend_class}">
            <strong>{signal_icon} {signal['time']}{active_text}</strong><br>
            Planet: {signal['planet']} | Signal: <strong>{signal['signal']}</strong><br>
            Target: {signal['target']} | SL: {signal['sl']}
        </div>
        """, unsafe_allow_html=True)
    
    # Add current prices for global market
    st.markdown("### 📊 Current Global Market Status")
    current_hour = datetime.now().hour
    
    if 19 <= current_hour <= 23 or 0 <= current_hour <= 2:
        st.success("🟢 US Markets ACTIVE - Prime trading time for DOW JONES")
    elif 2 <= current_hour <= 6:
        st.warning("🟡 Asian Pre-market - Low volume period")
    elif 6 <= current_hour <= 12:
        st.info("🔵 Asian Markets Active - Prepare for US session")
    else:
        st.info("⏳ Waiting for US market opening at 7:00 PM IST")

# Show all currently active opportunities across all markets
st.subheader("🎯 All Active Trading Opportunities RIGHT NOW")

# Collect all active signals
all_active_signals = []

try:
    # Check NIFTY signals
    nifty_signals = st.session_state.astro_predictions['nifty_banknifty']['NIFTY']['hourly_signals']
    for signal in nifty_signals:
        if is_time_in_range(current_time_str, signal['time']):
            all_active_signals.append({
                'Market': 'NIFTY',
                'Signal': signal['signal'],
                'Trend': signal['trend'],
                'Target': signal['target'],
                'SL': signal['sl'],
                'Planet': signal['planet'],
                'Time': signal['time']
            })
    
    # Check BANKNIFTY signals
    banknifty_signals = st.session_state.astro_predictions['nifty_banknifty']['BANKNIFTY']['hourly_signals']
    for signal in banknifty_signals:
        if is_time_in_range(current_time_str, signal['time']):
            all_active_signals.append({
                'Market': 'BANKNIFTY',
                'Signal': signal['signal'],
                'Trend': signal['trend'],
                'Target': signal['target'],
                'SL': signal['sl'],
                'Planet': signal['planet'],
                'Time': signal['time']
            })
    
    # Check commodity and global signals
    for market in ['GOLD', 'SILVER', 'CRUDE', 'BITCOIN', 'DOWJONES']:
        try:
            market_signals = st.session_state.astro_predictions['commodities_global'][market]['hourly_signals']
            for signal in market_signals:
                if is_time_in_range(current_time_str, signal['time']):
                    all_active_signals.append({
                        'Market': market,
                        'Signal': signal['signal'],
                        'Trend': signal['trend'],
                        'Target': signal['target'],
                        'SL': signal['sl'],
                        'Planet': signal['planet'],
                        'Time': signal['time']
                    })
        except KeyError:
            continue

except KeyError:
    st.info("Signal data is loading...")

if all_active_signals:
    st.markdown("### 🔥 LIVE TRADING SIGNALS")
    
    # Display in a more compact format
    signal_cols = st.columns(min(len(all_active_signals), 4))
    
    for idx, signal in enumerate(all_active_signals[:4]):  # Show max 4 active signals
        col_idx = idx % 4
        
        with signal_cols[col_idx]:
            if signal['Signal'] in ['LONG', 'BUY', 'STRONG BUY']:
                signal_class = 'live-signal'
                signal_emoji = '🟢'
            elif signal['Signal'] in ['SHORT', 'SELL']:
                signal_class = 'warning-signal'
                signal_emoji = '🔴'
            else:
                signal_class = 'planetary-hour'
                signal_emoji = '🟡'
            
            st.markdown(f"""
            <div class="{signal_class}">
                <h4>{signal_emoji} {signal['Market']}</h4>
                <strong>{signal['Signal']}</strong><br>
                Target: {signal['Target']}<br>
                SL: {signal['SL']}<br>
                {signal['Planet']}
            </div>
            """, unsafe_allow_html=True)
    
    if len(all_active_signals) > 4:
        st.info(f"📈 +{len(all_active_signals) - 4} more active signals. Check individual market sections above.")
else:
    st.markdown("""
    <div class="timing-alert">
        <h4>🕐 No Active Signals Currently</h4>
        <p>Market is in transition period. Check upcoming planetary hours below.</p>
    </div>
    """, unsafe_allow_html=True)

with nifty_banknifty_col2:
    st.markdown("### 🏦 BANKNIFTY Signals")
    try:
        banknifty_signals = st.session_state.astro_predictions['nifty_banknifty']['BANKNIFTY']['hourly_signals']
    except KeyError:
        st.error("BANKNIFTY signals data not available")
        banknifty_signals = []
    
    for signal in banknifty_signals:
        is_active = is_time_in_range(current_time_str, signal['time'])
        
        if signal['trend'] == 'Bullish':
            trend_class = 'live-signal' if is_active else 'trend-bullish'
            signal_icon = '🟢'
        elif signal['trend'] == 'Bearish':
            trend_class = 'warning-signal' if is_active else 'trend-bearish'
            signal_icon = '🔴'
        elif signal['trend'] == 'Volatile':
            trend_class = 'warning-signal' if is_active else 'trend-volatile'
            signal_icon = '🟡'
        else:
            trend_class = 'trend-neutral'
            signal_icon = '🟡'
        
        active_text = " 🔥 ACTIVE NOW" if is_active else ""
        
        st.markdown(f"""
        <div class="{trend_class}">
            <strong>{signal_icon} {signal['time']}{active_text}</strong><br>
            Planet: {signal['planet']} | Signal: <strong>{signal['signal']}</strong><br>
            Target: {signal['target']} | SL: {signal['sl']}
        </div>
        """, unsafe_allow_html=True)

# Planetary Transit Schedule
st.subheader("🪐 Planetary Transit Schedule & Market Impact")

transit_col1, transit_col2 = st.columns([1, 1])

with transit_col1:
    st.markdown("### ⏰ Hourly Planetary Transits")
    try:
        transits = st.session_state.astro_predictions['planetary_transits']
    except KeyError:
        st.error("Transit data not available")
        transits = []
    
    for transit in transits:
        is_active = is_time_in_range(current_time_str, transit['time'])
        
        if transit['effect'] == 'Positive':
            effect_class = 'live-signal' if is_active else 'trend-bullish'
            effect_icon = '✅'
        elif transit['effect'] == 'Negative':
            effect_class = 'warning-signal' if is_active else 'trend-bearish'
            effect_icon = '❌'
        else:
            effect_class = 'trend-volatile'
            effect_icon = '⚡'
        
        active_text = " 🌟 ACTIVE" if is_active else ""
        
        st.markdown(f"""
        <div class="{effect_class}">
            <strong>{effect_icon} {transit['time']}{active_text}</strong><br>
            Planet: {transit['planet']} | Effect: <strong>{transit['effect']}</strong><br>
            Impact: {transit['influence']}<br>
            Markets: {transit['markets']}
        </div>
        """, unsafe_allow_html=True)

with transit_col2:
    st.markdown("### 🎯 Current Active Signals")
    
    # Find current active signals
    try:
        nifty_signals = st.session_state.astro_predictions['nifty_banknifty']['NIFTY']['hourly_signals']
        banknifty_signals = st.session_state.astro_predictions['nifty_banknifty']['BANKNIFTY']['hourly_signals']
        transits = st.session_state.astro_predictions['planetary_transits']
    except KeyError:
        nifty_signals = []
        banknifty_signals = []
        transits = []
    
    active_nifty = [s for s in nifty_signals if is_time_in_range(current_time_str, s['time'])]
    active_banknifty = [s for s in banknifty_signals if is_time_in_range(current_time_str, s['time'])]
    active_transits = [t for t in transits if is_time_in_range(current_time_str, t['time'])]
    
    if active_nifty:
        signal = active_nifty[0]
        st.markdown(f"""
        <div class="live-signal">
            🎯 NIFTY: {signal['signal']}<br>
            Target: {signal['target']} | SL: {signal['sl']}<br>
            Planet: {signal['planet']}
        </div>
        """, unsafe_allow_html=True)
    
    if active_banknifty:
        signal = active_banknifty[0]
        st.markdown(f"""
        <div class="live-signal">
            🏦 BANKNIFTY: {signal['signal']}<br>
            Target: {signal['target']} | SL: {signal['sl']}<br>
            Planet: {signal['planet']}
        </div>
        """, unsafe_allow_html=True)
    
    if active_transits:
        transit = active_transits[0]
        st.markdown(f"""
        <div class="planetary-hour">
            🪐 Active Transit: {transit['planet']}<br>
            Effect: {transit['effect']}<br>
            {transit['influence']}
        </div>
        """, unsafe_allow_html=True)
    
    if not (active_nifty or active_banknifty or active_transits):
        st.info("🕐 No active signals at current time. Check upcoming timing above.")

# Sector-wise Timeline
st.subheader("🏭 Sector-wise Hourly Timeline (9:15 AM - 3:30 PM)")

sectors = ['Banking', 'IT', 'Pharma', 'Auto', 'Metal', 'FMCG', 'Energy', 'Realty']

try:
    time_slots = list(st.session_state.astro_predictions['sector_timeline'].keys())
    sector_data_available = True
except KeyError:
    st.error("Sector timeline data not available")
    time_slots = []
    sector_data_available = False

if sector_data_available:

    # Create sector timeline table
    st.markdown("### 📈 Complete Sector Timeline")

    # Header
    col_header = st.columns([2] + [1] * len(time_slots))
    col_header[0].markdown("**Sector**")
    for i, time_slot in enumerate(time_slots):
        col_header[i+1].markdown(f"**{time_slot}**")

    # Sector rows
    for sector in sectors:
        cols = st.columns([2] + [1] * len(time_slots))
        cols[0].markdown(f"**{sector}**")
        
        for i, time_slot in enumerate(time_slots):
            try:
                trend = st.session_state.astro_predictions['sector_timeline'][time_slot][sector]
                is_active = is_time_in_range(current_time_str, time_slot)
                
                if trend == 'Bullish':
                    if is_active:
                        cols[i+1].markdown('<div class="live-signal">🟢 BULL</div>', unsafe_allow_html=True)
                    else:
                        cols[i+1].markdown('<span class="bullish-text">🟢 Bull</span>', unsafe_allow_html=True)
                elif trend == 'Bearish':
                    if is_active:
                        cols[i+1].markdown('<div class="warning-signal">🔴 BEAR</div>', unsafe_allow_html=True)
                    else:
                        cols[i+1].markdown('<span class="bearish-text">🔴 Bear</span>', unsafe_allow_html=True)
                elif trend == 'Volatile':
                    if is_active:
                        cols[i+1].markdown('<div class="warning-signal">⚡ VOL</div>', unsafe_allow_html=True)
                    else:
                        cols[i+1].markdown('<span class="volatile-text">⚡ Vol</span>', unsafe_allow_html=True)
                else:
                    cols[i+1].markdown('<span class="neutral-text">🟡 Neut</span>', unsafe_allow_html=True)
            except KeyError:
                cols[i+1].markdown('<span class="neutral-text">N/A</span>', unsafe_allow_html=True)

    # Current sector status
    st.markdown("### 🔥 Currently Active Sectors")
    current_sectors = []
    try:
        for time_slot, sectors_data in st.session_state.astro_predictions['sector_timeline'].items():
            if is_time_in_range(current_time_str, time_slot):
                for sector, trend in sectors_data.items():
                    if trend in ['Bullish', 'Bearish', 'Volatile']:
                        current_sectors.append(f"{sector}: {trend}")
    except KeyError:
        pass

    if current_sectors:
        active_col1, active_col2, active_col3 = st.columns(3)
        
        with active_col1:
            bullish_sectors = [s for s in current_sectors if 'Bullish' in s]
            if bullish_sectors:
                st.markdown("**🟢 Bullish Now:**")
                for sector in bullish_sectors:
                    st.markdown(f'<span class="bullish-text">• {sector.split(":")[0]}</span>', unsafe_allow_html=True)
        
        with active_col2:
            bearish_sectors = [s for s in current_sectors if 'Bearish' in s]
            if bearish_sectors:
                st.markdown("**🔴 Bearish Now:**")
                for sector in bearish_sectors:
                    st.markdown(f'<span class="bearish-text">• {sector.split(":")[0]}</span>', unsafe_allow_html=True)
        
        with active_col3:
            volatile_sectors = [s for s in current_sectors if 'Volatile' in s]
            if volatile_sectors:
                st.markdown("**⚡ Volatile Now:**")
                for sector in volatile_sectors:
                    st.markdown(f'<span class="volatile-text">• {sector.split(":")[0]}</span>', unsafe_allow_html=True)
    else:
        st.info("🕐 Market transitioning between planetary hours")
else:
    st.info("Sector timeline data is being initialized...")

# Summary & Recommendations
st.subheader("💡 Today's Trading Recommendations")

summary_col1, summary_col2, summary_col3 = st.columns(3)

with summary_col1:
    st.markdown("""
    <div class="live-signal">
        <h4>🟢 Best Long Opportunities</h4>
        <strong>Morning (9:15-11:00):</strong><br>
        • NIFTY, BANKNIFTY<br>
        • Banking, FMCG, Pharma<br>
        <strong>Evening (20:00-23:30):</strong><br>
        • GOLD, SILVER strong<br>
        • BITCOIN bullish<br>
        <strong>US Hours (19:00-23:00):</strong><br>
        • DOW JONES positive
    </div>
    """, unsafe_allow_html=True)

with summary_col2:
    st.markdown("""
    <div class="warning-signal">
        <h4>🔴 Short Opportunities</h4>
        <strong>Midday (12:00-14:00):</strong><br>
        • NIFTY, BANKNIFTY profit booking<br>
        • IT, Metals weak<br>
        <strong>Crude Oil:</strong><br>
        • Bearish 10:00-12:00<br>
        • Volatile during inventory<br>
        <strong>Late night (02:00-06:00):</strong><br>
        • BITCOIN bearish
    </div>
    """, unsafe_allow_html=True)

with summary_col3:
    st.markdown("""
    <div class="planetary-hour">
        <h4>⚡ High Risk Periods</h4>
        <strong>13:00-14:00 (Mars Hour):</strong><br>
        • All indices volatile<br>
        • Energy sector swings<br>
        <strong>Crude Inventory (20:00):</strong><br>
        • Extreme volatility<br>
        <strong>Rahu Hours (14:00-15:00):</strong><br>
        • Tech stocks pressure<br>
        • BITCOIN caution
    </div>
    """, unsafe_allow_html=True)

# Astro Data Management
st.subheader("📅 Astrological Data Management")

astro_mgmt_col1, astro_mgmt_col2, astro_mgmt_col3 = st.columns(3)

with astro_mgmt_col1:
    st.info(f"📅 **Current Astro Data Date:** {st.session_state.astro_data_date}")

with astro_mgmt_col2:
    if st.button("🔄 Update Astro Data", help="Recalculate planetary positions and market timing"):
        st.session_state.astro_data_date = datetime.now().strftime('%Y-%m-%d %H:%M')
        st.success("✅ Astrological data updated!")
        st.rerun()

with astro_mgmt_col3:
    # Show data freshness
    try:
        data_date = datetime.strptime(st.session_state.astro_data_date, '%Y-%m-%d %H:%M')
        hours_old = (datetime.now() - data_date).total_seconds() / 3600
        
        if hours_old < 1:
            st.success("🟢 Data: Fresh")
        elif hours_old < 6:
            st.warning("🟡 Data: Recent")
        else:
            st.error("🔴 Data: Update needed")
    except:
        st.info("🔵 Data: Unknown age")

# Current Market Prices for New Markets
st.subheader("💰 Live Prices - Commodities & Global")

price_col1, price_col2, price_col3, price_col4, price_col5 = st.columns(5)

markets_to_show = ['GOLD', 'SILVER', 'CRUDE', 'BITCOIN', 'DOWJONES']

for idx, market in enumerate(markets_to_show):
    if market in st.session_state.market_data:
        data = st.session_state.market_data[market]
        color_class = "positive" if data['change'] >= 0 else "negative"
        arrow = "▲" if data['change'] >= 0 else "▼"
        
        # Format price based on market
        if market in ['GOLD', 'SILVER']:
            price_str = f"₹{data['price']:,.0f}"
        elif market == 'CRUDE':
            price_str = f"₹{data['price']:,.0f}"
        elif market == 'BITCOIN':
            price_str = f"${data['price']:,.0f}"
        else:  # DOWJONES
            price_str = f"{data['price']:,.0f}"
        
        with [price_col1, price_col2, price_col3, price_col4, price_col5][idx]:
            st.markdown(f"""
            <div class="market-card">
                <h5>{market}</h5>
                <h3>{price_str}</h3>
                <p class="{color_class}">
                    {arrow} {abs(data['change']):.2f}%
                </p>
            </div>
            """, unsafe_allow_html=True)

# Auto-refresh
if auto_refresh:
    time.sleep(refresh_rate)
    update_market_data()
    st.rerun()

# Footer
st.write("---")
footer_col1, footer_col2, footer_col3, footer_col4, footer_col5 = st.columns(5)

with footer_col1:
    st.caption(f"🕐 Last Updated: {st.session_state.last_update.strftime('%H:%M:%S')}")

with footer_col2:
    st.caption(f"{current_symbol} Current Planet: {current_planet}")

with footer_col3:
    try:
        # Get signals data for overall sentiment calculation
        nifty_signals = st.session_state.astro_predictions['nifty_banknifty']['NIFTY']['hourly_signals']
        banknifty_signals = st.session_state.astro_predictions['nifty_banknifty']['BANKNIFTY']['hourly_signals']
        
        bullish_count = sum(1 for s in nifty_signals + banknifty_signals if s['trend'] == 'Bullish')
        bearish_count = sum(1 for s in nifty_signals + banknifty_signals if s['trend'] == 'Bearish')
        
        if bullish_count > bearish_count:
            st.caption("📈 Indices: BULLISH")
        elif bearish_count > bullish_count:
            st.caption("📉 Indices: BEARISH")
        else:
            st.caption("➡️ Indices: MIXED")
    except KeyError:
        st.caption("📊 Indices: LOADING...")

with footer_col4:
    # Count active opportunities
    try:
        active_count = len(all_active_signals)
        st.caption(f"🎯 Active Signals: {active_count}")
    except:
        st.caption("🎯 Active Signals: 0")

with footer_col5:
    st.caption(f"📅 Astro: {st.session_state.astro_data_date}")

st.caption("🕉️ Vedic Market Intelligence - Complete Astrological Trading Analysis")
