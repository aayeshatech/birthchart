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
    padding: 15px;
    text-align: center;
    border-radius: 10px;
    margin-bottom: 15px;
}
.market-card {
    background: #f8f9fa;
    padding: 12px;
    border-radius: 8px;
    text-align: center;
    margin: 8px 0;
    border: 2px solid #dee2e6;
}
.positive { color: #28a745; font-weight: bold; }
.negative { color: #dc3545; font-weight: bold; }
.ticker-box {
    background: #000;
    color: #00ff00;
    padding: 8px;
    font-family: monospace;
    border-radius: 5px;
    margin: 8px 0;
}
.chart-box {
    background: white;
    padding: 15px;
    border-radius: 8px;
    border: 2px solid #ddd;
    margin: 8px 0;
}
.planet-info {
    background: #e3f2fd;
    color: #1565c0;
    padding: 8px;
    border-radius: 5px;
    margin: 5px 0;
    border-left: 3px solid #2196f3;
    font-weight: 500;
}
.transit-box {
    background: #f0f8ff;
    color: #1e3a8a;
    padding: 12px;
    border-radius: 6px;
    margin: 8px 0;
    border: 1px solid #87ceeb;
    font-weight: 500;
}
.timing-alert {
    background: #fff3cd;
    color: #856404;
    padding: 8px;
    border-radius: 5px;
    margin: 5px 0;
    border-left: 4px solid #ffc107;
    font-weight: 500;
}
.bullish-text {
    color: #155724;
    font-weight: bold;
}
.bearish-text {
    color: #721c24;
    font-weight: bold;
}
.neutral-text {
    color: #856404;
    font-weight: bold;
}
.volatile-text {
    color: #d84315;
    font-weight: bold;
}
.trend-bullish {
    background-color: #d4edda;
    color: #155724;
    padding: 3px 6px;
    border-radius: 4px;
    font-weight: bold;
    font-size: 0.9em;
}
.trend-bearish {
    background-color: #f8d7da;
    color: #721c24;
    padding: 3px 6px;
    border-radius: 4px;
    font-weight: bold;
    font-size: 0.9em;
}
.trend-neutral {
    background-color: #fff3cd;
    color: #856404;
    padding: 3px 6px;
    border-radius: 4px;
    font-weight: bold;
    font-size: 0.9em;
}
.trend-volatile {
    background-color: #ffe5d4;
    color: #d84315;
    padding: 3px 6px;
    border-radius: 4px;
    font-weight: bold;
    font-size: 0.9em;
}
.astro-timing-box {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: #ffffff;
    padding: 15px;
    border-radius: 10px;
    margin: 15px 0;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
}
.time-slot {
    background: rgba(255,255,255,0.95);
    color: #212529;
    padding: 10px;
    border-radius: 6px;
    margin: 5px 0;
    border-left: 4px solid #ffd700;
    font-weight: 500;
}
.planetary-hour {
    background: linear-gradient(45deg, #ff9a56, #ff6b35);
    color: #ffffff;
    padding: 12px;
    border-radius: 8px;
    margin: 8px 0;
    text-align: center;
    font-weight: bold;
}
.sector-timeline {
    background: #f8f9fa;
    color: #212529;
    padding: 12px;
    border-radius: 8px;
    margin: 8px 0;
    border: 1px solid #dee2e6;
}
.live-signal {
    background: linear-gradient(45deg, #11998e, #38ef7d);
    color: #ffffff;
    padding: 10px;
    border-radius: 6px;
    margin: 5px 0;
    text-align: center;
    font-weight: bold;
    font-size: 0.95em;
}
.warning-signal {
    background: linear-gradient(45deg, #ff416c, #ff4b2b);
    color: #ffffff;
    padding: 10px;
    border-radius: 6px;
    margin: 5px 0;
    text-align: center;
    font-weight: bold;
    font-size: 0.95em;
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
    <h1 style="margin: 0 0 5px 0;">🕉️ Vedic Market Intelligence Dashboard</h1>
    <p style="margin: 0;">Live Astrological Market Analysis with Planetary Transit Timing</p>
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

# CURRENT SECTOR SIGNALS BOX
st.markdown("""
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: #ffffff; padding: 15px; border-radius: 10px; margin: 15px 0;">
    <h2 style="margin: 0 0 5px 0; color: #ffffff;">🎯 Current Sector Signals & Stock Recommendations</h2>
    <p style="margin: 0; color: #ffffff; opacity: 0.9;">Based on live planetary transit - Specific stocks to trade RIGHT NOW</p>
</div>
""", unsafe_allow_html=True)

# Get current planetary influence
current_hour = datetime.now().hour
current_minute = datetime.now().minute

# Define current sector recommendations based on time and planetary transit
current_sector_signals = {}

if 9 <= current_hour < 10:
    current_sector_signals = {
        'LONG_SECTORS': {
            'Banking': {'stocks': ['HDFC Bank', 'ICICI Bank', 'Kotak Bank'], 'planet': 'Venus ♀', 'reason': 'Venus hora - luxury banking strong'},
            'FMCG': {'stocks': ['HUL', 'ITC', 'Nestle'], 'planet': 'Venus ♀', 'reason': 'Consumer goods favorable'},
            'Pharma': {'stocks': ['Sun Pharma', 'Dr Reddy'], 'planet': 'Sun ☀️', 'reason': 'Health sector blessed'}
        },
        'SHORT_SECTORS': {
            'Metal': {'stocks': ['Tata Steel', 'JSW Steel'], 'planet': 'Saturn ♄', 'reason': 'Heavy industries weak'},
            'Realty': {'stocks': ['DLF', 'Godrej Prop'], 'planet': 'Saturn ♄', 'reason': 'Real estate under pressure'}
        }
    }
elif 10 <= current_hour < 11:
    current_sector_signals = {
        'LONG_SECTORS': {
            'Banking': {'stocks': ['HDFC Bank', 'SBI', 'Axis Bank'], 'planet': 'Sun ☀️', 'reason': 'Solar energy in finance'},
            'Energy': {'stocks': ['Reliance', 'ONGC'], 'planet': 'Sun ☀️', 'reason': 'Sun rules energy sector'},
            'Pharma': {'stocks': ['Cipla', 'Divis Lab'], 'planet': 'Sun ☀️', 'reason': 'Healing energy strong'}
        },
        'SHORT_SECTORS': {
            'IT': {'stocks': ['TCS', 'Infosys'], 'planet': 'Mercury ☿', 'reason': 'Tech sector retrograde effect'},
            'Metal': {'stocks': ['Hindalco', 'Vedanta'], 'planet': 'Saturn ♄', 'reason': 'Heavy metals suppressed'}
        }
    }
elif 11 <= current_hour < 12:
    current_sector_signals = {
        'LONG_SECTORS': {
            'Auto': {'stocks': ['Maruti', 'Tata Motors'], 'planet': 'Mercury ☿', 'reason': 'Transport sector active'},
            'Pharma': {'stocks': ['Biocon', 'Lupin'], 'planet': 'Jupiter ♃', 'reason': 'Jupiter aspect on health'}
        },
        'SHORT_SECTORS': {
            'IT': {'stocks': ['Wipro', 'HCL Tech'], 'planet': 'Mercury ☿', 'reason': 'Mercury combust effect'},
            'Realty': {'stocks': ['Brigade', 'Sobha'], 'planet': 'Ketu ☋', 'reason': 'Property market uncertain'}
        }
    }
elif 12 <= current_hour < 13:
    current_sector_signals = {
        'LONG_SECTORS': {},
        'SHORT_SECTORS': {
            'Banking': {'stocks': ['ICICI Bank', 'Axis Bank'], 'planet': 'Saturn ♄', 'reason': 'Financial sector profit booking'},
            'Auto': {'stocks': ['Bajaj Auto', 'Hero Motor'], 'planet': 'Saturn ♄', 'reason': 'Transport sector decline'},
            'IT': {'stocks': ['Tech Mahindra', 'Mphasis'], 'planet': 'Saturn ♄', 'reason': 'Technology under pressure'}
        }
    }
elif 13 <= current_hour < 14:
    current_sector_signals = {
        'LONG_SECTORS': {},
        'SHORT_SECTORS': {
            'Banking': {'stocks': ['SBI', 'PNB'], 'planet': 'Mars ♂️', 'reason': 'Aggressive selling in finance'},
            'IT': {'stocks': ['Infosys', 'TCS'], 'planet': 'Mars ♂️', 'reason': 'Tech sector volatility'},
            'Metal': {'stocks': ['SAIL', 'JSW Steel'], 'planet': 'Mars ♂️', 'reason': 'Industrial metals weak'},
            'FMCG': {'stocks': ['Dabur', 'Marico'], 'planet': 'Mars ♂️', 'reason': 'Consumer goods selling'}
        }
    }
elif 14 <= current_hour < 15:
    current_sector_signals = {
        'LONG_SECTORS': {},
        'SHORT_SECTORS': {
            'IT': {'stocks': ['TCS', 'Wipro', 'HCL Tech'], 'planet': 'Rahu ☊', 'reason': 'Technology crisis, global IT pressure'},
            'Metal': {'stocks': ['Tata Steel', 'Vedanta'], 'planet': 'Rahu ☊', 'reason': 'Mining sector confusion'},
            'Energy': {'stocks': ['BPCL', 'IOC'], 'planet': 'Rahu ☊', 'reason': 'Energy uncertainty'}
        }
    }
elif 15 <= current_hour < 16:
    current_sector_signals = {
        'LONG_SECTORS': {
            'Banking': {'stocks': ['HDFC Bank', 'Kotak Bank'], 'planet': 'Jupiter ♃', 'reason': 'Financial recovery rally'},
            'FMCG': {'stocks': ['HUL', 'ITC'], 'planet': 'Venus ♀', 'reason': 'Consumer comeback'},
            'Auto': {'stocks': ['Maruti', 'M&M'], 'planet': 'Venus ♀', 'reason': 'Transport sector revival'}
        },
        'SHORT_SECTORS': {}
    }
else:
    # After market hours or early morning
    current_sector_signals = {
        'LONG_SECTORS': {},
        'SHORT_SECTORS': {}
    }

# Display Current Sector Signals
sector_signal_col1, sector_signal_col2 = st.columns(2)

with sector_signal_col1:
    st.markdown("### 🟢 SECTORS TO GO LONG")
    
    if current_sector_signals['LONG_SECTORS']:
        for sector, data in current_sector_signals['LONG_SECTORS'].items():
            stocks_text = ", ".join(data['stocks'])
            
            st.markdown(f"""
            <div style="background: #c8e6c9; color: #1b5e20; padding: 10px; border-radius: 6px; margin: 3px 0; text-align: center; font-weight: bold; border: 2px solid #388e3c;">
                <h5 style="margin: 0 0 5px 0; color: #1b5e20;">📈 {sector} Sector</h5>
                <div style="color: #1b5e20; font-size: 0.9em;">
                <span style="background: #2e7d32; color: white; padding: 3px 8px; border-radius: 4px; font-weight: bold; font-size: 1.1em;">🟢 BUY: {stocks_text}</span><br>
                <small>Planet: {data['planet']} | {data['reason']}</small>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: #fff8e1; color: #e65100; padding: 10px; border-radius: 6px; margin: 3px 0; border: 2px solid #f57c00;">
            <h5 style="margin: 0 0 5px 0; color: #e65100;">⏳ No Long Opportunities</h5>
            <p style="margin: 0; color: #e65100; font-size: 0.85em;">Current planetary hour not favorable for long positions</p>
        </div>
        """, unsafe_allow_html=True)

with sector_signal_col2:
    st.markdown("### 🔴 SECTORS TO GO SHORT")
    
    if current_sector_signals['SHORT_SECTORS']:
        for sector, data in current_sector_signals['SHORT_SECTORS'].items():
            stocks_text = ", ".join(data['stocks'])
            
            st.markdown(f"""
            <div style="background: #ffcdd2; color: #b71c1c; padding: 10px; border-radius: 6px; margin: 3px 0; text-align: center; font-weight: bold; border: 2px solid #d32f2f;">
                <h5 style="margin: 0 0 5px 0; color: #b71c1c;">📉 {sector} Sector</h5>
                <div style="color: #b71c1c; font-size: 0.9em;">
                <span style="background: #c62828; color: white; padding: 3px 8px; border-radius: 4px; font-weight: bold; font-size: 1.1em;">🔴 SELL: {stocks_text}</span><br>
                <small>Planet: {data['planet']} | {data['reason']}</small>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: #fff8e1; color: #e65100; padding: 10px; border-radius: 6px; margin: 3px 0; border: 2px solid #f57c00;">
            <h5 style="margin: 0 0 5px 0; color: #e65100;">⏳ No Short Opportunities</h5>
            <p style="margin: 0; color: #e65100; font-size: 0.85em;">Current planetary hour not showing strong bearish signals</p>
        </div>
        """, unsafe_allow_html=True)

# TOMORROW'S PLANETARY TRANSIT PREDICTIONS
st.markdown("""
<div style="background: linear-gradient(135deg, #ff9a56 0%, #ff6b35 100%); color: #ffffff; padding: 15px; border-radius: 10px; margin: 15px 0;">
    <h2 style="margin: 0 0 5px 0; color: #ffffff;">🔮 Tomorrow's Planetary Transit Forecast</h2>
    <p style="margin: 0; color: #ffffff; opacity: 0.9;">Next day detailed astrological predictions with timing</p>
</div>
""", unsafe_allow_html=True)

# Calculate tomorrow's date
tomorrow = datetime.now() + timedelta(days=1)
tomorrow_date = tomorrow.strftime('%B %d, %Y (%A)')

forecast_header_col1, forecast_header_col2 = st.columns([3, 1])

with forecast_header_col1:
    st.markdown(f"### 📅 Forecast for {tomorrow_date}")

with forecast_header_col2:
    if st.session_state.get('show_commodity_forecast', False):
        if st.button("🏭 Hide Commodity Forecast", help="Hide commodity forecast section"):
            st.session_state.show_commodity_forecast = False
            st.rerun()
    else:
        if st.button("🏭 View Commodity Forecast", help="Jump to tomorrow's commodity-specific planetary forecast"):
            st.session_state.show_commodity_forecast = True
            st.rerun()

# Tomorrow's planetary transit schedule
tomorrow_transits = [
    {
        'time': '09:15-10:15',
        'planet': 'Moon 🌙',
        'trend': 'Bullish',
        'effect': 'Positive',
        'sectors': 'FMCG, Consumer goods strong',
        'indices': 'NIFTY: +0.7%, BANKNIFTY: +1.2%',
        'action': 'BUY consumer stocks at opening'
    },
    {
        'time': '10:15-11:15', 
        'planet': 'Mars ♂️',
        'trend': 'Volatile',
        'effect': 'Mixed',
        'sectors': 'Energy up, Defense strong, IT weak',
        'indices': 'NIFTY: ±1.5%, BANKNIFTY: ±1.8%',
        'action': 'Trade energy stocks with tight stops'
    },
    {
        'time': '11:15-12:15',
        'planet': 'Mercury ☿',
        'trend': 'Bearish',
        'effect': 'Negative',
        'sectors': 'IT, Telecom under pressure',
        'indices': 'NIFTY: -0.8%, BANKNIFTY: -0.5%',
        'action': 'SHORT tech stocks'
    },
    {
        'time': '12:15-13:15',
        'planet': 'Jupiter ♃',
        'trend': 'Bullish',
        'effect': 'Positive',
        'sectors': 'Banking, Finance, Gold bullish',
        'indices': 'NIFTY: +1.3%, BANKNIFTY: +2.1%',
        'action': 'STRONG BUY banking stocks'
    },
    {
        'time': '13:15-14:15',
        'planet': 'Venus ♀',
        'trend': 'Bullish',
        'effect': 'Positive',
        'sectors': 'Auto, Luxury, Entertainment up',
        'indices': 'NIFTY: +0.9%, BANKNIFTY: +0.6%',
        'action': 'BUY auto and consumer durables'
    },
    {
        'time': '14:15-15:15',
        'planet': 'Saturn ♄',
        'trend': 'Bearish',
        'effect': 'Negative',
        'sectors': 'All sectors weak, profit booking',
        'indices': 'NIFTY: -1.2%, BANKNIFTY: -1.8%',
        'action': 'BOOK PROFITS, avoid fresh longs'
    },
    {
        'time': '15:15-15:30',
        'planet': 'Sun ☀️',
        'trend': 'Bullish',
        'effect': 'Positive',
        'sectors': 'Power, Energy, Pharma recovery',
        'indices': 'NIFTY: +0.8%, BANKNIFTY: +0.4%',
        'action': 'Closing rally - BUY energy stocks'
    }
]

# Display tomorrow's predictions in compact timeline format
forecast_col1, forecast_col2 = st.columns(2)

for idx, transit in enumerate(tomorrow_transits):
    col = forecast_col1 if idx % 2 == 0 else forecast_col2
    
    # Determine styling based on trend with darker colors
    if transit['trend'] == 'Bullish':
        bg_color = '#c8e6c9'
        text_color = '#1b5e20'
        trend_icon = '🟢'
        badge_color = '#2e7d32'
    elif transit['trend'] == 'Bearish':
        bg_color = '#ffcdd2'
        text_color = '#b71c1c'
        trend_icon = '🔴'
        badge_color = '#c62828'
    else:
        bg_color = '#fff8e1'
        text_color = '#e65100'
        trend_icon = '🟡'
        badge_color = '#f57c00'
    
    with col:
        st.markdown(f"""
        <div style="background: {bg_color}; color: {text_color}; padding: 8px; border-radius: 6px; margin: 3px 0; border-left: 4px solid {badge_color};">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                <h5 style="margin: 0; color: {text_color}; font-size: 0.95em;">{trend_icon} {transit['time']} - {transit['planet']}</h5>
                <span style="background: {badge_color}; color: white; padding: 2px 6px; border-radius: 8px; font-weight: bold; font-size: 0.7em;">
                    {transit['trend'].upper()}
                </span>
            </div>
            <div style="line-height: 1.2; font-size: 0.8em;">
                <strong style="color: {text_color};">📊</strong> {transit['sectors']}<br>
                <strong style="color: {text_color};">📈</strong> {transit['indices']}<br>
                <strong style="color: {text_color}; font-size: 1.1em;">💡 ACTION:</strong> <span style="font-weight: bold; color: {badge_color}; font-size: 1.1em; background: rgba(255,255,255,0.8); padding: 2px 4px; border-radius: 4px;">{transit['action']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Tomorrow's Key Highlights - More Compact
tomorrow_col1, tomorrow_col2, tomorrow_col3 = st.columns(3)

with tomorrow_col1:
    st.markdown("""
    <div style="background: #c8e6c9; color: #1b5e20; padding: 10px; border-radius: 6px; margin: 3px 0; font-weight: 600; border: 2px solid #388e3c;">
        <h5 style="margin: 0 0 5px 0; color: #1b5e20;">🌟 Best Opportunities</h5>
        <div style="font-size: 0.85em; line-height: 1.3; color: #1b5e20;">
        <strong>12:15-13:15 (Jupiter ♃):</strong><br>
        <span style="background: #2e7d32; color: white; padding: 2px 4px; border-radius: 4px; font-weight: bold; font-size: 0.9em;">STRONG BUY Banking</span><br>
        BANKNIFTY: +2.1%<br><br>
        <strong>09:15-10:15 (Moon 🌙):</strong><br>
        <span style="background: #388e3c; color: white; padding: 2px 4px; border-radius: 4px; font-weight: bold; font-size: 0.9em;">BUY FMCG</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with tomorrow_col2:
    st.markdown("""
    <div style="background: #ffcdd2; color: #b71c1c; padding: 10px; border-radius: 6px; margin: 3px 0; font-weight: 600; border: 2px solid #d32f2f;">
        <h5 style="margin: 0 0 5px 0; color: #b71c1c;">⚠️ Avoid These Times</h5>
        <div style="font-size: 0.85em; line-height: 1.3; color: #b71c1c;">
        <strong>11:15-12:15 (Mercury ☿):</strong><br>
        <span style="background: #c62828; color: white; padding: 2px 4px; border-radius: 4px; font-weight: bold; font-size: 0.9em;">SHORT IT Stocks</span><br><br>
        <strong>14:15-15:15 (Saturn ♄):</strong><br>
        <span style="background: #d32f2f; color: white; padding: 2px 4px; border-radius: 4px; font-weight: bold; font-size: 0.9em;">BOOK PROFITS</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with tomorrow_col3:
    st.markdown("""
    <div style="background: #fff8e1; color: #e65100; padding: 10px; border-radius: 6px; margin: 3px 0; font-weight: 600; border: 2px solid #f57c00;">
        <h5 style="margin: 0 0 5px 0; color: #e65100;">🎯 Special Alerts</h5>
        <div style="font-size: 0.85em; line-height: 1.3; color: #e65100;">
        <strong>10:15-11:15 (Mars ♂️):</strong><br>
        <span style="background: #ef6c00; color: white; padding: 2px 4px; border-radius: 4px; font-weight: bold; font-size: 0.9em;">HIGH VOLATILITY</span><br><br>
        <strong>15:15-15:30 (Sun ☀️):</strong><br>
        <span style="background: #f57c00; color: white; padding: 2px 4px; border-radius: 4px; font-weight: bold; font-size: 0.9em;">BUY Energy Rally</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Tomorrow's Sector-wise Timeline - Compact
st.markdown("### 📊 Tomorrow's Sector Timeline (Compact View)")

tomorrow_sectors = {
    '09:15': {'Banking': 'Neutral', 'IT': 'Neutral', 'Pharma': 'Bullish', 'Auto': 'Bullish', 'Metal': 'Bearish', 'FMCG': 'Strong Bullish', 'Energy': 'Neutral', 'Realty': 'Bearish'},
    '10:15': {'Banking': 'Neutral', 'IT': 'Bearish', 'Pharma': 'Bullish', 'Auto': 'Volatile', 'Metal': 'Volatile', 'FMCG': 'Neutral', 'Energy': 'Strong Bullish', 'Realty': 'Bearish'},
    '11:15': {'Banking': 'Bearish', 'IT': 'Strong Bearish', 'Pharma': 'Bearish', 'Auto': 'Bearish', 'Metal': 'Bearish', 'FMCG': 'Bearish', 'Energy': 'Bearish', 'Realty': 'Bearish'},
    '12:15': {'Banking': 'Strong Bullish', 'IT': 'Neutral', 'Pharma': 'Bullish', 'Auto': 'Bullish', 'Metal': 'Neutral', 'FMCG': 'Bullish', 'Energy': 'Bullish', 'Realty': 'Neutral'},
    '13:15': {'Banking': 'Bullish', 'IT': 'Neutral', 'Pharma': 'Bullish', 'Auto': 'Strong Bullish', 'Metal': 'Neutral', 'FMCG': 'Bullish', 'Energy': 'Bullish', 'Realty': 'Neutral'},
    '14:15': {'Banking': 'Bearish', 'IT': 'Bearish', 'Pharma': 'Bearish', 'Auto': 'Bearish', 'Metal': 'Bearish', 'FMCG': 'Bearish', 'Energy': 'Bearish', 'Realty': 'Bearish'},
    '15:15': {'Banking': 'Bullish', 'IT': 'Neutral', 'Pharma': 'Strong Bullish', 'Auto': 'Bullish', 'Metal': 'Neutral', 'FMCG': 'Bullish', 'Energy': 'Strong Bullish', 'Realty': 'Neutral'}
}

tomorrow_time_slots = list(tomorrow_sectors.keys())
sectors = ['Banking', 'IT', 'Pharma', 'Auto', 'Metal', 'FMCG', 'Energy', 'Realty']

# Create a more compact grid
sector_grid_html = """
<div style="background: white; padding: 8px; border-radius: 6px; border: 1px solid #dee2e6; overflow-x: auto;">
<table style="width: 100%; font-size: 0.8em; border-collapse: collapse;">
<tr style="background: #f8f9fa;">
<th style="padding: 4px; border: 1px solid #dee2e6; color: #495057; font-weight: bold;">Sector</th>
"""

for time_slot in tomorrow_time_slots:
    sector_grid_html += f'<th style="padding: 4px; border: 1px solid #dee2e6; color: #495057; font-weight: bold; font-size: 0.75em;">{time_slot}</th>'

sector_grid_html += "</tr>"

for sector in sectors:
    sector_grid_html += f'<tr><td style="padding: 4px; border: 1px solid #dee2e6; font-weight: bold; color: #212529;">{sector}</td>'
    
    for time_slot in tomorrow_time_slots:
        trend = tomorrow_sectors[time_slot][sector]
        
        if trend == 'Strong Bullish':
            cell_style = 'background: #2e7d32; color: white; font-weight: bold;'
            cell_text = '🟢🟢'
        elif trend == 'Bullish':
            cell_style = 'background: #c8e6c9; color: #1b5e20; font-weight: bold;'
            cell_text = '🟢'
        elif trend == 'Strong Bearish':
            cell_style = 'background: #c62828; color: white; font-weight: bold;'
            cell_text = '🔴🔴'
        elif trend == 'Bearish':
            cell_style = 'background: #ffcdd2; color: #b71c1c; font-weight: bold;'
            cell_text = '🔴'
        elif trend == 'Volatile':
            cell_style = 'background: #fff8e1; color: #e65100; font-weight: bold;'
            cell_text = '⚡'
        else:
            cell_style = 'background: #f5f5f5; color: #616161; font-weight: bold;'
            cell_text = '🟡'
        
        sector_grid_html += f'<td style="padding: 4px; border: 1px solid #dee2e6; text-align: center; {cell_style}">{cell_text}</td>'
    
    sector_grid_html += '</tr>'

sector_grid_html += '</table></div>'

st.markdown(sector_grid_html, unsafe_allow_html=True)

# Tomorrow's Best Trading Plan - Compact
plan_col1, plan_col2 = st.columns(2)

with plan_col1:
    st.markdown("""
    <div style="background: #e1f5fe; color: #0277bd; padding: 10px; border-radius: 6px; margin: 3px 0; border: 2px solid #0288d1;">
        <h5 style="margin: 0 0 5px 0; color: #01579b;">⏰ Time-based Strategy</h5>
        <div style="font-size: 0.85em; line-height: 1.3; color: #0277bd;">
        <strong>09:15-10:15:</strong> <span style="background: #2e7d32; color: white; padding: 2px 4px; border-radius: 3px; font-weight: bold;">BUY FMCG</span><br>
        <strong>12:15-13:15:</strong> <span style="background: #1b5e20; color: white; padding: 2px 4px; border-radius: 3px; font-weight: bold;">STRONG BUY Banking</span><br>
        <strong>13:15-14:15:</strong> <span style="background: #388e3c; color: white; padding: 2px 4px; border-radius: 3px; font-weight: bold;">BUY Auto</span><br>
        <strong>15:15-15:30:</strong> <span style="background: #43a047; color: white; padding: 2px 4px; border-radius: 3px; font-weight: bold;">BUY Energy</span><br><br>
        <span style="background: #c62828; color: white; padding: 3px 6px; border-radius: 4px; font-weight: bold; font-size: 0.9em;">⚠️ AVOID 11:15-12:15 & 14:15-15:15</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with plan_col2:
    st.markdown("""
    <div style="background: #e8f5e8; color: #1b5e20; padding: 10px; border-radius: 6px; margin: 3px 0; border: 2px solid #2e7d32;">
        <h5 style="margin: 0 0 5px 0; color: #1b5e20;">🎯 Key Targets Tomorrow</h5>
        <div style="font-size: 0.85em; line-height: 1.3; color: #1b5e20;">
        <strong>Best Long:</strong> <span style="background: #2e7d32; color: white; padding: 2px 4px; border-radius: 3px; font-weight: bold;">Banking +2.1%</span><br>
        <strong>Best Short:</strong> <span style="background: #c62828; color: white; padding: 2px 4px; border-radius: 3px; font-weight: bold;">IT -1.5%</span><br>
        <strong>Highest Vol:</strong> 10:15-11:15 (Mars)<br>
        <strong>Safest Entry:</strong> 09:15-10:15 (Moon)<br><br>
        <span style="background: #1b5e20; color: white; padding: 3px 6px; border-radius: 4px; font-weight: bold; font-size: 0.9em;">📈 Overall: BULLISH BIAS</span>
        </div>
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
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: #ffffff; padding: 15px; border-radius: 10px; margin: 15px 0;">
    <h2 style="margin: 0 0 5px 0; color: #ffffff;">🔮 Live Astrological Market Timing Analysis</h2>
    <p style="margin: 0 0 5px 0; color: #ffffff; opacity: 0.9;">Real-time planetary transit effects on NIFTY, BANKNIFTY, Commodities & Global Markets</p>
    <p style="text-align: right; font-size: 0.85em; margin: 0; color: #ffffff; opacity: 0.8;">📅 Astro Data Updated: {st.session_state.astro_data_date}</p>
</div>
""", unsafe_allow_html=True)

# Current planetary hour
current_time = datetime.now()
current_planet, current_symbol, current_influence = get_planetary_influence(current_time)
current_time_str = current_time.strftime('%H:%M')

st.markdown(f"""
<div style="background: linear-gradient(45deg, #ff9a56, #ff6b35); color: #ffffff; padding: 12px; border-radius: 8px; margin: 8px 0; text-align: center;">
    <h3 style="margin: 0 0 5px 0; color: #ffffff;">{current_symbol} Current Planetary Hour: {current_planet}</h3>
    <p style="margin: 0 0 3px 0; color: #ffffff; font-weight: 500;">🌟 {current_influence}</p>
    <p style="margin: 0; color: #ffffff; font-size: 0.9em;">⏰ Time: {current_time_str} | Market Effect: <strong>Active Now</strong></p>
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
commodity_header_col1, commodity_header_col2 = st.columns([3, 1])

with commodity_header_col1:
    st.subheader("🏭 Commodities & Global Markets Astrological Signals")

with commodity_header_col2:
    show_commodity_forecast = st.checkbox("📅 Tomorrow's Commodity Forecast", value=st.session_state.get('show_commodity_forecast', False), help="Show detailed commodity planetary transits for tomorrow")
    if show_commodity_forecast:
        st.session_state.show_commodity_forecast = True
    else:
        st.session_state.show_commodity_forecast = False

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

# TOMORROW'S COMMODITY FORECAST (Conditional Display)
if st.session_state.get('show_commodity_forecast', False):
    commodity_forecast_col1, commodity_forecast_col2 = st.columns([4, 1])
    
    with commodity_forecast_col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #ff6b35 0%, #f7931e 100%); color: #ffffff; padding: 15px; border-radius: 10px; margin: 15px 0;">
            <h3 style="margin: 0 0 5px 0; color: #ffffff;">🔮 Tomorrow's Commodity Planetary Forecast</h3>
            <p style="margin: 0; color: #ffffff; opacity: 0.9;">Detailed commodity timing with planetary transits for next trading day</p>
        </div>
        """, unsafe_allow_html=True)
    
    with commodity_forecast_col2:
        if st.button("❌ Close", help="Close commodity forecast"):
            st.session_state.show_commodity_forecast = False
            st.rerun()
    
    # Tomorrow's commodity predictions with enhanced planetary timing
    tomorrow_commodity_forecast = [
        {
            'time': '06:00-09:00',
            'planet': 'Saturn ♄',
            'planetary_effect': 'Restrictive & Slow',
            'commodities': {
                'GOLD': {'trend': 'Neutral', 'signal': 'WAIT', 'target': '±0.3%', 'reasoning': 'Early morning consolidation'},
                'SILVER': {'trend': 'Bearish', 'signal': 'AVOID', 'target': '-0.8%', 'reasoning': 'Industrial metal weakness'},
                'CRUDE': {'trend': 'Volatile', 'signal': 'CAUTION', 'target': '±2.1%', 'reasoning': 'Asian pre-market uncertainty'},
                'BITCOIN': {'trend': 'Bearish', 'signal': 'SELL', 'target': '-3.2%', 'reasoning': 'Crypto night session decline'}
            },
            'description': 'Pre-market Asian session - Saturn restricts growth, low liquidity'
        },
        {
            'time': '09:00-12:00',
            'planet': 'Moon 🌙',
            'planetary_effect': 'Emotional & Nurturing',
            'commodities': {
                'GOLD': {'trend': 'Bullish', 'signal': 'BUY', 'target': '+1.2%', 'reasoning': 'Safe haven demand strong'},
                'SILVER': {'trend': 'Strong Bullish', 'signal': 'STRONG BUY', 'target': '+2.5%', 'reasoning': 'Industrial + safe haven combo'},
                'CRUDE': {'trend': 'Bearish', 'signal': 'SELL', 'target': '-1.8%', 'reasoning': 'Risk-off sentiment hurts energy'},
                'BITCOIN': {'trend': 'Volatile', 'signal': 'CAUTION', 'target': '±4.5%', 'reasoning': 'Emotional trading in crypto'}
            },
            'description': 'Asian session - Moon favors precious metals, hurts risk assets'
        },
        {
            'time': '12:00-15:00',
            'planet': 'Mercury ☿',
            'planetary_effect': 'Communicative & Technical',
            'commodities': {
                'GOLD': {'trend': 'Neutral', 'signal': 'HOLD', 'target': '±0.5%', 'reasoning': 'Technical consolidation'},
                'SILVER': {'trend': 'Bullish', 'signal': 'BUY', 'target': '+1.8%', 'reasoning': 'Industrial demand recovery'},
                'CRUDE': {'trend': 'Volatile', 'signal': 'SCALP', 'target': '±2.8%', 'reasoning': 'News-driven moves'},
                'BITCOIN': {'trend': 'Bullish', 'signal': 'BUY', 'target': '+3.1%', 'reasoning': 'Tech adoption news positive'}
            },
            'description': 'Midday session - Mercury brings technical analysis focus'
        },
        {
            'time': '15:00-18:00',
            'planet': 'Venus ♀',
            'planetary_effect': 'Harmonious & Luxurious',
            'commodities': {
                'GOLD': {'trend': 'Bullish', 'signal': 'BUY', 'target': '+1.0%', 'reasoning': 'Luxury demand increases'},
                'SILVER': {'trend': 'Strong Bullish', 'signal': 'STRONG BUY', 'target': '+2.8%', 'reasoning': 'Jewelry & industrial demand'},
                'CRUDE': {'trend': 'Bullish', 'signal': 'BUY', 'target': '+1.5%', 'reasoning': 'Economic activity pickup'},
                'BITCOIN': {'trend': 'Bullish', 'signal': 'BUY', 'target': '+2.7%', 'reasoning': 'Digital luxury asset appeal'}
            },
            'description': 'European session - Venus harmonizes all commodity markets'
        },
        {
            'time': '18:00-21:00',
            'planet': 'Jupiter ♃',
            'planetary_effect': 'Expansive & Prosperous',
            'commodities': {
                'GOLD': {'trend': 'Strong Bullish', 'signal': 'STRONG BUY', 'target': '+2.2%', 'reasoning': 'Jupiter expands precious metal value'},
                'SILVER': {'trend': 'Strong Bullish', 'signal': 'STRONG BUY', 'target': '+3.5%', 'reasoning': 'Peak prosperity phase'},
                'CRUDE': {'trend': 'Volatile', 'signal': 'CAUTION', 'target': '±3.0%', 'reasoning': 'Expansion vs inventory concerns'},
                'BITCOIN': {'trend': 'Strong Bullish', 'signal': 'STRONG BUY', 'target': '+5.2%', 'reasoning': 'Jupiter rules digital expansion'}
            },
            'description': '🌟 PRIME TIME - Jupiter\'s expansion benefits all stores of value'
        },
        {
            'time': '21:00-00:00',
            'planet': 'Mars ♂️',
            'planetary_effect': 'Aggressive & Volatile',
            'commodities': {
                'GOLD': {'trend': 'Bullish', 'signal': 'BUY', 'target': '+1.5%', 'reasoning': 'Safe haven in volatile times'},
                'SILVER': {'trend': 'Volatile', 'signal': 'CAUTION', 'target': '±2.2%', 'reasoning': 'Industrial uncertainty'},
                'CRUDE': {'trend': 'Bearish', 'signal': 'SELL', 'target': '-2.1%', 'reasoning': 'Aggressive selling pressure'},
                'BITCOIN': {'trend': 'Volatile', 'signal': 'TIGHT STOPS', 'target': '±4.8%', 'reasoning': 'Mars brings extreme swings'}
            },
            'description': 'Late US session - Mars creates volatility, gold remains defensive'
        }
    ]
    
    # Display tomorrow's commodity forecast
    for forecast in tomorrow_commodity_forecast:
        st.markdown(f"""
        <div style="background: #f5f5f5; color: #333; padding: 10px; border-radius: 6px; margin: 5px 0; border-left: 4px solid #ff6b35;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;">
                <h6 style="margin: 0; color: #333; font-weight: bold;">{forecast['planet']} {forecast['time']}</h6>
                <small style="color: #666; font-style: italic;">Effect: {forecast['planetary_effect']}</small>
            </div>
            <small style="color: #555; font-size: 0.8em;">{forecast['description']}</small>
        </div>
        """, unsafe_allow_html=True)
        
        # Display commodity signals in a compact grid
        commodity_cols = st.columns(4)
        commodities = ['GOLD', 'SILVER', 'CRUDE', 'BITCOIN']
        
        for idx, commodity in enumerate(commodities):
            if commodity in forecast['commodities']:
                comm_data = forecast['commodities'][commodity]
                
                # Determine colors based on trend
                if 'Strong Bullish' in comm_data['trend']:
                    bg_color = '#2e7d32'
                    text_color = '#ffffff'
                    signal_icon = '🟢🟢'
                elif 'Bullish' in comm_data['trend']:
                    bg_color = '#c8e6c9'
                    text_color = '#1b5e20'
                    signal_icon = '🟢'
                elif 'Bearish' in comm_data['trend']:
                    bg_color = '#ffcdd2'
                    text_color = '#b71c1c'
                    signal_icon = '🔴'
                elif 'Volatile' in comm_data['trend']:
                    bg_color = '#fff8e1'
                    text_color = '#e65100'
                    signal_icon = '⚡'
                else:
                    bg_color = '#f5f5f5'
                    text_color = '#616161'
                    signal_icon = '🟡'
                
                with commodity_cols[idx]:
                    st.markdown(f"""
                    <div style="background: {bg_color}; color: {text_color}; padding: 8px; border-radius: 5px; margin: 2px; text-align: center; border: 1px solid {text_color};">
                        <h6 style="margin: 0 0 3px 0; color: {text_color}; font-size: 0.9em;">{signal_icon} {commodity}</h6>
                        <div style="font-size: 0.8em;">
                        <span style="background: rgba(0,0,0,0.3); color: white; padding: 2px 4px; border-radius: 3px; font-weight: bold; font-size: 0.85em;">{comm_data['signal']}</span><br>
                        <small style="color: {text_color}; font-weight: bold;">{comm_data['target']}</small><br>
                        <small style="color: {text_color}; opacity: 0.8; font-size: 0.75em;">{comm_data['reasoning']}</small>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
    
    # Tomorrow's commodity highlights
    st.markdown("### 🎯 Tomorrow's Commodity Highlights")
    
    commodity_highlight_col1, commodity_highlight_col2, commodity_highlight_col3 = st.columns(3)
    
    with commodity_highlight_col1:
        st.markdown("""
        <div style="background: #c8e6c9; color: #1b5e20; padding: 10px; border-radius: 6px; border: 2px solid #388e3c;">
            <h6 style="margin: 0 0 5px 0; color: #1b5e20;">🥇 Best Commodity Opportunities</h6>
            <div style="font-size: 0.85em; line-height: 1.3; color: #1b5e20;">
            <strong>18:00-21:00 (Jupiter ♃):</strong><br>
            <span style="background: #2e7d32; color: white; padding: 2px 4px; border-radius: 3px; font-weight: bold;">GOLD +2.2%</span><br>
            <span style="background: #388e3c; color: white; padding: 2px 4px; border-radius: 3px; font-weight: bold;">SILVER +3.5%</span><br>
            <span style="background: #43a047; color: white; padding: 2px 4px; border-radius: 3px; font-weight: bold;">BITCOIN +5.2%</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with commodity_highlight_col2:
        st.markdown("""
        <div style="background: #ffcdd2; color: #b71c1c; padding: 10px; border-radius: 6px; border: 2px solid #d32f2f;">
            <h6 style="margin: 0 0 5px 0; color: #b71c1c;">🛢️ Commodity Warnings</h6>
            <div style="font-size: 0.85em; line-height: 1.3; color: #b71c1c;">
            <strong>09:00-12:00:</strong><br>
            <span style="background: #c62828; color: white; padding: 2px 4px; border-radius: 3px; font-weight: bold;">CRUDE SELL -1.8%</span><br><br>
            <strong>21:00-00:00:</strong><br>
            <span style="background: #d32f2f; color: white; padding: 2px 4px; border-radius: 3px; font-weight: bold;">CRUDE SELL -2.1%</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with commodity_highlight_col3:
        st.markdown("""
        <div style="background: #fff8e1; color: #e65100; padding: 10px; border-radius: 6px; border: 2px solid #f57c00;">
            <h6 style="margin: 0 0 5px 0; color: #e65100;">⚡ High Volatility Windows</h6>
            <div style="font-size: 0.85em; line-height: 1.3; color: #e65100;">
            <strong>06:00-09:00 (Saturn ♄):</strong><br>
            <span style="background: #ef6c00; color: white; padding: 2px 4px; border-radius: 3px; font-weight: bold;">BITCOIN VOLATILE ±3.2%</span><br><br>
            <strong>21:00-00:00 (Mars ♂️):</strong><br>
            <span style="background: #f57c00; color: white; padding: 2px 4px; border-radius: 3px; font-weight: bold;">ALL COMMODITIES RISK</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick commodity trading plan for tomorrow
    st.markdown("### 📋 Tomorrow's Commodity Trading Plan")
    
    plan_col1, plan_col2 = st.columns(2)
    
    with plan_col1:
        st.markdown("""
        <div style="background: #e8f5e8; color: #1b5e20; padding: 10px; border-radius: 6px; border: 2px solid #2e7d32;">
            <h6 style="margin: 0 0 5px 0; color: #1b5e20;">✅ Recommended Actions</h6>
            <div style="font-size: 0.85em; line-height: 1.3; color: #1b5e20;">
            <strong>09:00-12:00:</strong> <span style="background: #2e7d32; color: white; padding: 2px 4px; border-radius: 3px; font-weight: bold;">BUY GOLD & SILVER</span><br>
            <strong>15:00-18:00:</strong> <span style="background: #388e3c; color: white; padding: 2px 4px; border-radius: 3px; font-weight: bold;">BUY ALL COMMODITIES</span><br>
            <strong>18:00-21:00:</strong> <span style="background: #1b5e20; color: white; padding: 2px 4px; border-radius: 3px; font-weight: bold;">PEAK BUY TIME</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with plan_col2:
        st.markdown("""
        <div style="background: #ffebee; color: #b71c1c; padding: 10px; border-radius: 6px; border: 2px solid #c62828;">
            <h6 style="margin: 0 0 5px 0; color: #b71c1c;">❌ Avoid These Periods</h6>
            <div style="font-size: 0.85em; line-height: 1.3; color: #b71c1c;">
            <strong>06:00-09:00:</strong> <span style="background: #c62828; color: white; padding: 2px 4px; border-radius: 3px; font-weight: bold;">AVOID BITCOIN</span><br>
            <strong>09:00-12:00:</strong> <span style="background: #d32f2f; color: white; padding: 2px 4px; border-radius: 3px; font-weight: bold;">SHORT CRUDE</span><br>
            <strong>21:00-00:00:</strong> <span style="background: #f44336; color: white; padding: 2px 4px; border-radius: 3px; font-weight: bold;">HIGH RISK ALL</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

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
                bg_color = '#c8e6c9'
                text_color = '#1b5e20'
                signal_emoji = '🟢'
                action_bg = '#2e7d32'
            elif signal['Signal'] in ['SHORT', 'SELL']:
                bg_color = '#ffcdd2'
                text_color = '#b71c1c'
                signal_emoji = '🔴'
                action_bg = '#c62828'
            else:
                bg_color = '#fff8e1'
                text_color = '#e65100'
                signal_emoji = '🟡'
                action_bg = '#f57c00'
            
            st.markdown(f"""
            <div style="background: {bg_color}; color: {text_color}; padding: 8px; border-radius: 6px; margin: 3px 0; text-align: center; font-weight: bold; border: 2px solid {action_bg};">
                <h5 style="margin: 0 0 3px 0; color: {text_color};">{signal_emoji} {signal['Market']}</h5>
                <div style="font-size: 0.85em; color: {text_color};">
                <span style="background: {action_bg}; color: white; padding: 3px 6px; border-radius: 4px; font-weight: bold; font-size: 1.1em;">{signal['Signal']}</span><br>
                <small>Target: {signal['Target']} | SL: {signal['SL']}</small><br>
                <small>{signal['Planet']}</small>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    if len(all_active_signals) > 4:
        st.info(f"📈 +{len(all_active_signals) - 4} more active signals. Check individual market sections above.")
else:
    st.markdown("""
    <div style="background: #fff8e1; color: #e65100; padding: 10px; border-radius: 6px; margin: 5px 0; border: 2px solid #f57c00;">
        <h5 style="margin: 0 0 3px 0; color: #e65100;">🕐 No Active Signals Currently</h5>
        <p style="margin: 0; color: #e65100; font-size: 0.85em;">Market is in transition period. Check upcoming planetary hours below.</p>
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
    <div style="background: #d4edda; color: #155724; padding: 12px; border-radius: 8px; margin: 5px 0; text-align: center; font-weight: bold; border: 1px solid #c3e6cb;">
        <h4 style="margin: 0 0 8px 0; color: #155724;">🟢 Best Long Opportunities</h4>
        <div style="text-align: left; font-size: 0.9em; line-height: 1.4; color: #155724;">
        <strong>Morning (9:15-11:00):</strong><br>
        • NIFTY, BANKNIFTY<br>
        • Banking, FMCG, Pharma<br>
        <strong>Evening (20:00-23:30):</strong><br>
        • GOLD, SILVER strong<br>
        • BITCOIN bullish<br>
        <strong>US Hours (19:00-23:00):</strong><br>
        • DOW JONES positive
        </div>
    </div>
    """, unsafe_allow_html=True)

with summary_col2:
    st.markdown("""
    <div style="background: #f8d7da; color: #721c24; padding: 12px; border-radius: 8px; margin: 5px 0; text-align: center; font-weight: bold; border: 1px solid #f5c6cb;">
        <h4 style="margin: 0 0 8px 0; color: #721c24;">🔴 Short Opportunities</h4>
        <div style="text-align: left; font-size: 0.9em; line-height: 1.4; color: #721c24;">
        <strong>Midday (12:00-14:00):</strong><br>
        • NIFTY, BANKNIFTY profit booking<br>
        • IT, Metals weak<br>
        <strong>Crude Oil:</strong><br>
        • Bearish 10:00-12:00<br>
        • Volatile during inventory<br>
        <strong>Late night (02:00-06:00):</strong><br>
        • BITCOIN bearish
        </div>
    </div>
    """, unsafe_allow_html=True)

# Summary & Recommendations - Compact
summary_col1, summary_col2, summary_col3 = st.columns(3)

with summary_col1:
    st.markdown("""
    <div style="background: #c8e6c9; color: #1b5e20; padding: 10px; border-radius: 6px; margin: 3px 0; text-align: center; font-weight: bold; border: 2px solid #388e3c;">
        <h5 style="margin: 0 0 5px 0; color: #1b5e20;">🟢 Best Long Opportunities</h5>
        <div style="text-align: left; font-size: 0.85em; line-height: 1.3; color: #1b5e20;">
        <strong>Morning (9:15-11:00):</strong><br>
        <span style="background: #2e7d32; color: white; padding: 2px 4px; border-radius: 3px; font-weight: bold; font-size: 1em;">BUY NIFTY, BANKNIFTY</span><br>
        <span style="background: #388e3c; color: white; padding: 2px 4px; border-radius: 3px; font-weight: bold; font-size: 1em;">BUY Banking, FMCG</span><br><br>
        <strong>Evening (20:00-23:30):</strong><br>
        <span style="background: #43a047; color: white; padding: 2px 4px; border-radius: 3px; font-weight: bold; font-size: 1em;">BUY GOLD, SILVER</span><br>
        <span style="background: #4caf50; color: white; padding: 2px 4px; border-radius: 3px; font-weight: bold; font-size: 1em;">BUY BITCOIN</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with summary_col2:
    st.markdown("""
    <div style="background: #ffcdd2; color: #b71c1c; padding: 10px; border-radius: 6px; margin: 3px 0; text-align: center; font-weight: bold; border: 2px solid #d32f2f;">
        <h5 style="margin: 0 0 5px 0; color: #b71c1c;">🔴 Short Opportunities</h5>
        <div style="text-align: left; font-size: 0.85em; line-height: 1.3; color: #b71c1c;">
        <strong>Midday (12:00-14:00):</strong><br>
        <span style="background: #c62828; color: white; padding: 2px 4px; border-radius: 3px; font-weight: bold; font-size: 1em;">SELL NIFTY, BANKNIFTY</span><br>
        <span style="background: #d32f2f; color: white; padding: 2px 4px; border-radius: 3px; font-weight: bold; font-size: 1em;">SHORT IT, Metals</span><br><br>
        <strong>Crude Oil:</strong><br>
        <span style="background: #f44336; color: white; padding: 2px 4px; border-radius: 3px; font-weight: bold; font-size: 1em;">SELL 10:00-12:00</span><br>
        <span style="background: #e53935; color: white; padding: 2px 4px; border-radius: 3px; font-weight: bold; font-size: 1em;">SHORT BITCOIN 02:00-06:00</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with summary_col3:
    st.markdown("""
    <div style="background: #fff8e1; color: #e65100; padding: 10px; border-radius: 6px; margin: 3px 0; text-align: center; font-weight: bold; border: 2px solid #f57c00;">
        <h5 style="margin: 0 0 5px 0; color: #e65100;">⚡ High Risk Periods</h5>
        <div style="text-align: left; font-size: 0.85em; line-height: 1.3; color: #e65100;">
        <strong>13:00-14:00 (Mars):</strong><br>
        <span style="background: #ef6c00; color: white; padding: 2px 4px; border-radius: 3px; font-weight: bold; font-size: 1em;">⚠️ ALL VOLATILE</span><br><br>
        <strong>Crude Inventory (20:00):</strong><br>
        <span style="background: #f57c00; color: white; padding: 2px 4px; border-radius: 3px; font-weight: bold; font-size: 1em;">AVOID TRADING</span><br><br>
        <strong>Rahu (14:00-15:00):</strong><br>
        <span style="background: #ff9800; color: white; padding: 2px 4px; border-radius: 3px; font-weight: bold; font-size: 1em;">TECH PRESSURE</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Astro Data Management
st.subheader("📅 Astrological Data Management")

astro_mgmt_col1, astro_mgmt_col2, astro_mgmt_col3 = st.columns(3)

with astro_mgmt_col1:
    st.markdown(f"""
    <div style="background: #e3f2fd; color: #1565c0; padding: 10px; border-radius: 6px; border: 1px solid #2196f3;">
        <strong style="color: #1565c0;">📅 Current Astro Data Date:</strong><br>
        <span style="color: #0d47a1; font-weight: bold;">{st.session_state.astro_data_date}</span>
    </div>
    """, unsafe_allow_html=True)

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
            st.markdown('<div style="background: #d4edda; color: #155724; padding: 8px; border-radius: 6px; text-align: center; font-weight: bold;">🟢 Data: Fresh</div>', unsafe_allow_html=True)
        elif hours_old < 6:
            st.markdown('<div style="background: #fff3cd; color: #856404; padding: 8px; border-radius: 6px; text-align: center; font-weight: bold;">🟡 Data: Recent</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="background: #f8d7da; color: #721c24; padding: 8px; border-radius: 6px; text-align: center; font-weight: bold;">🔴 Data: Update needed</div>', unsafe_allow_html=True)
    except:
        st.markdown('<div style="background: #e3f2fd; color: #1565c0; padding: 8px; border-radius: 6px; text-align: center; font-weight: bold;">🔵 Data: Unknown age</div>', unsafe_allow_html=True)

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
            <div style="background: #f8f9fa; padding: 10px; border-radius: 6px; text-align: center; margin: 5px 0; border: 1px solid #dee2e6;">
                <h5 style="margin: 0 0 3px 0; color: #495057;">{market}</h5>
                <h3 style="margin: 0 0 3px 0; color: #212529;">{price_str}</h3>
                <p class="{color_class}" style="margin: 0; font-size: 0.9em;">
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
