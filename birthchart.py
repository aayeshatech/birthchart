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

# Enhanced CSS with compact and dynamic styles
st.markdown("""
<style>
.main-header {
    background: linear-gradient(45deg, #ff6b35, #f7931e);
    color: white;
    padding: 10px;
    text-align: center;
    border-radius: 8px;
    margin-bottom: 10px;
}
.market-card {
    background: #f8f9fa;
    padding: 8px;
    border-radius: 6px;
    text-align: center;
    margin: 4px 0;
    border: 1px solid #dee2e6;
    font-size: 0.9em;
}
.positive { color: #28a745; font-weight: bold; }
.negative { color: #dc3545; font-weight: bold; }
.ticker-box {
    background: #000;
    color: #00ff00;
    padding: 6px;
    font-family: monospace;
    border-radius: 4px;
    margin: 6px 0;
    font-size: 0.85em;
}
.compact-card {
    background: white;
    padding: 8px;
    border-radius: 6px;
    border: 1px solid #ddd;
    margin: 4px 0;
    font-size: 0.85em;
}
.market-status {
    padding: 4px 8px;
    border-radius: 12px;
    font-weight: bold;
    font-size: 0.75em;
    display: inline-block;
    margin: 2px;
}
.market-open { background: #d4edda; color: #155724; }
.market-closed { background: #f8d7da; color: #721c24; }
.market-preopen { background: #fff3cd; color: #856404; }
.signal-box {
    padding: 6px;
    border-radius: 4px;
    margin: 2px 0;
    text-align: center;
    font-weight: bold;
    font-size: 0.8em;
}
.signal-buy { background: #d4edda; color: #155724; }
.signal-sell { background: #f8d7da; color: #721c24; }
.signal-hold { background: #fff3cd; color: #856404; }
.signal-caution { background: #ffeaa7; color: #6c757d; }
.active-signal {
    background: linear-gradient(45deg, #11998e, #38ef7d) !important;
    color: white !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.3);
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.05); }
    100% { transform: scale(1); }
}
.time-slot-compact {
    background: #f8f9fa;
    padding: 4px 6px;
    border-radius: 4px;
    margin: 1px;
    border-left: 3px solid #007bff;
    font-size: 0.75em;
}
.planetary-compact {
    background: linear-gradient(45deg, #667eea, #764ba2);
    color: white;
    padding: 8px;
    border-radius: 6px;
    margin: 4px 0;
    text-align: center;
    font-size: 0.8em;
}
.sector-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
    gap: 4px;
    margin: 8px 0;
}
.sector-cell {
    padding: 4px;
    border-radius: 4px;
    text-align: center;
    font-size: 0.75em;
    font-weight: bold;
    border: 1px solid;
}
.trending-up { background: #d4edda; color: #155724; border-color: #28a745; }
.trending-down { background: #f8d7da; color: #721c24; border-color: #dc3545; }
.trending-sideways { background: #fff3cd; color: #856404; border-color: #ffc107; }
.trending-volatile { background: #ffeaa7; color: #e17055; border-color: #fd79a8; }
</style>
""", unsafe_allow_html=True)

# Helper functions
def get_market_status(current_time):
    hour = current_time.hour
    minute = current_time.minute
    
    # Indian Markets: 9:15 AM - 3:30 PM
    indian_start = 9 * 60 + 15  # 9:15 AM in minutes
    indian_end = 15 * 60 + 30   # 3:30 PM in minutes
    
    # Global/Commodity Markets: 5:00 AM - 11:55 PM
    global_start = 5 * 60       # 5:00 AM in minutes
    global_end = 23 * 60 + 55   # 11:55 PM in minutes
    
    current_minutes = hour * 60 + minute
    
    indian_open = indian_start <= current_minutes <= indian_end
    global_open = global_start <= current_minutes <= global_end
    
    return {
        'indian_open': indian_open,
        'global_open': global_open,
        'current_time': current_time.strftime('%H:%M'),
        'indian_status': 'OPEN' if indian_open else 'CLOSED',
        'global_status': 'OPEN' if global_open else 'CLOSED'
    }

def get_planetary_influence_dynamic(current_time):
    hour = current_time.hour
    
    # Extended planetary hours for global markets (5 AM - 11:55 PM)
    planetary_hours_extended = {
        (5, 6): ("Saturn", "♄", "Pre-market caution", "global"),
        (6, 7): ("Jupiter", "♃", "Early morning strength", "global"),
        (7, 8): ("Mars", "♂️", "Volatile pre-market", "global"),
        (8, 9): ("Sun", "☀️", "Pre-Indian market energy", "global"),
        (9, 10): ("Venus", "♀", "Indian market opening", "indian"),
        (10, 11): ("Mercury", "☿", "IT, communication focus", "indian"),
        (11, 12): ("Moon", "🌙", "Emotional trading", "indian"),
        (12, 13): ("Saturn", "♄", "Midday resistance", "indian"),
        (13, 14): ("Jupiter", "♃", "Afternoon strength", "indian"),
        (14, 15): ("Mars", "♂️", "High volatility hour", "indian"),
        (15, 16): ("Sun", "☀️", "Closing energy", "indian"),
        (16, 17): ("Venus", "♀", "Post-market analysis", "global"),
        (17, 18): ("Mercury", "☿", "Evening news impact", "global"),
        (18, 19): ("Moon", "🌙", "Evening emotional phase", "global"),
        (19, 20): ("Saturn", "♄", "US pre-market caution", "global"),
        (20, 21): ("Jupiter", "♃", "US market strength", "global"),
        (21, 22): ("Mars", "♂️", "US volatility", "global"),
        (22, 23): ("Sun", "☀️", "Late night energy", "global"),
        (23, 24): ("Venus", "♀", "Overnight stability", "global")
    }
    
    for (start, end), (planet, symbol, influence, market_type) in planetary_hours_extended.items():
        if start <= hour < end:
            return planet, symbol, influence, market_type
    
    return "Mixed", "🌟", "Multiple influences", "global"

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

# Initialize session state with error handling
try:
    if 'market_data' not in st.session_state:
        st.session_state.market_data = {
            # Indian Markets
            'NIFTY': {'price': 24780.50, 'change': -0.50, 'high': 24920, 'low': 24750, 'type': 'indian'},
            'BANKNIFTY': {'price': 52435.75, 'change': 0.60, 'high': 52580, 'low': 52120, 'type': 'indian'},
            'SENSEX': {'price': 81342.15, 'change': -0.35, 'high': 81650, 'low': 81250, 'type': 'indian'},
            'NIFTY_IT': {'price': 32156, 'change': -1.31, 'high': 32600, 'low': 32100, 'type': 'indian'},
            'NIFTY_PHARMA': {'price': 18925, 'change': 0.84, 'high': 19050, 'low': 18750, 'type': 'indian'},
            'NIFTY_BANK': {'price': 52435, 'change': 0.60, 'high': 52580, 'low': 52120, 'type': 'indian'},
            'NIFTY_AUTO': {'price': 25380, 'change': -0.25, 'high': 25550, 'low': 25200, 'type': 'indian'},
            
            # Global & Commodities
            'GOLD': {'price': 71850, 'change': 0.55, 'high': 72100, 'low': 71500, 'type': 'global'},
            'SILVER': {'price': 91250, 'change': 1.20, 'high': 91800, 'low': 90200, 'type': 'global'},
            'BITCOIN': {'price': 97850.50, 'change': 2.57, 'high': 98500, 'low': 95200, 'type': 'global'},
            'CRUDE': {'price': 6845, 'change': -1.49, 'high': 6920, 'low': 6800, 'type': 'global'},
            'DOWJONES': {'price': 44565, 'change': 0.85, 'high': 44750, 'low': 44200, 'type': 'global'},
            'NASDAQ': {'price': 20173, 'change': 1.25, 'high': 20350, 'low': 19850, 'type': 'global'},
            'USDINR': {'price': 83.45, 'change': -0.14, 'high': 83.58, 'low': 83.42, 'type': 'global'},
            'EURINR': {'price': 88.25, 'change': 0.35, 'high': 88.50, 'low': 87.90, 'type': 'global'},
        }
    
    if 'last_update' not in st.session_state:
        st.session_state.last_update = datetime.now()
        
    # Initialize timing data for different market types
    if 'timing_data' not in st.session_state:
        st.session_state.timing_data = {
            'indian_signals': {
                'NIFTY': [
                    {'time': '09:15-10:00', 'planet': 'Venus ♀', 'signal': 'BUY', 'target': '+0.8%'},
                    {'time': '10:00-11:00', 'planet': 'Mercury ☿', 'signal': 'HOLD', 'target': '±0.2%'},
                    {'time': '11:00-12:00', 'planet': 'Moon 🌙', 'signal': 'BUY', 'target': '+1.2%'},
                    {'time': '12:00-13:00', 'planet': 'Saturn ♄', 'signal': 'SELL', 'target': '-0.9%'},
                    {'time': '13:00-14:00', 'planet': 'Jupiter ♃', 'signal': 'BUY', 'target': '+1.1%'},
                    {'time': '14:00-15:00', 'planet': 'Mars ♂️', 'signal': 'CAUTION', 'target': '±1.5%'},
                    {'time': '15:00-15:30', 'planet': 'Sun ☀️', 'signal': 'BUY', 'target': '+0.6%'}
                ],
                'BANKNIFTY': [
                    {'time': '09:15-10:00', 'planet': 'Jupiter ♃', 'signal': 'BUY', 'target': '+1.5%'},
                    {'time': '10:00-11:00', 'planet': 'Sun ☀️', 'signal': 'BUY', 'target': '+1.8%'},
                    {'time': '11:00-12:00', 'planet': 'Venus ♀', 'signal': 'HOLD', 'target': '±0.4%'},
                    {'time': '12:00-13:00', 'planet': 'Saturn ♄', 'signal': 'SELL', 'target': '-1.3%'},
                    {'time': '13:00-14:00', 'planet': 'Mars ♂️', 'signal': 'SELL', 'target': '-1.6%'},
                    {'time': '14:00-15:00', 'planet': 'Mercury ☿', 'signal': 'CAUTION', 'target': '±2.0%'},
                    {'time': '15:00-15:30', 'planet': 'Moon 🌙', 'signal': 'BUY', 'target': '+1.0%'}
                ]
            },
            'global_signals': {
                'GOLD': [
                    {'time': '05:00-07:00', 'planet': 'Saturn ♄', 'signal': 'HOLD', 'target': '±0.3%'},
                    {'time': '07:00-09:00', 'planet': 'Jupiter ♃', 'signal': 'BUY', 'target': '+0.8%'},
                    {'time': '16:00-18:00', 'planet': 'Venus ♀', 'signal': 'BUY', 'target': '+0.9%'},
                    {'time': '20:00-22:00', 'planet': 'Moon 🌙', 'signal': 'BUY', 'target': '+1.2%'},
                    {'time': '22:00-23:55', 'planet': 'Mercury ☿', 'signal': 'HOLD', 'target': '±0.4%'}
                ],
                'SILVER': [
                    {'time': '05:00-07:00', 'planet': 'Mars ♂️', 'signal': 'CAUTION', 'target': '±1.5%'},
                    {'time': '07:00-09:00', 'planet': 'Sun ☀️', 'signal': 'BUY', 'target': '+1.1%'},
                    {'time': '16:00-18:00', 'planet': 'Jupiter ♃', 'signal': 'BUY', 'target': '+1.8%'},
                    {'time': '20:00-22:00', 'planet': 'Venus ♀', 'signal': 'BUY', 'target': '+1.5%'},
                    {'time': '22:00-23:55', 'planet': 'Saturn ♄', 'signal': 'SELL', 'target': '-0.8%'}
                ],
                'CRUDE': [
                    {'time': '05:00-07:00', 'planet': 'Mercury ☿', 'signal': 'HOLD', 'target': '±0.8%'},
                    {'time': '16:00-18:00', 'planet': 'Mars ♂️', 'signal': 'CAUTION', 'target': '±2.5%'},
                    {'time': '20:00-22:00', 'planet': 'Saturn ♄', 'signal': 'SELL', 'target': '-1.8%'},
                    {'time': '22:00-23:55', 'planet': 'Rahu ☊', 'signal': 'AVOID', 'target': '±3.0%'}
                ],
                'BITCOIN': [
                    {'time': '05:00-09:00', 'planet': 'Rahu ☊', 'signal': 'CAUTION', 'target': '±3.5%'},
                    {'time': '16:00-20:00', 'planet': 'Mercury ☿', 'signal': 'BUY', 'target': '+2.8%'},
                    {'time': '20:00-23:55', 'planet': 'Jupiter ♃', 'signal': 'BUY', 'target': '+4.2%'}
                ],
                'DOWJONES': [
                    {'time': '19:00-21:00', 'planet': 'Sun ☀️', 'signal': 'BUY', 'target': '+0.9%'},
                    {'time': '21:00-23:00', 'planet': 'Jupiter ♃', 'signal': 'BUY', 'target': '+1.2%'},
                    {'time': '23:00-23:55', 'planet': 'Venus ♀', 'signal': 'HOLD', 'target': '±0.5%'}
                ]
            }
        }

except Exception as e:
    st.error(f"Error initializing data: {e}")

# Get current market status
current_time = datetime.now()
market_status = get_market_status(current_time)
current_planet, current_symbol, current_influence, market_type = get_planetary_influence_dynamic(current_time)

# Compact Header with Market Status
st.markdown(f"""
<div class="main-header">
    <h1 style="margin: 0 0 3px 0; font-size: 1.8em;">🕉️ Vedic Market Intelligence</h1>
    <div style="display: flex; justify-content: center; gap: 15px; margin-top: 5px;">
        <span class="market-status {'market-open' if market_status['indian_open'] else 'market-closed'}">
            🇮🇳 Indian: {market_status['indian_status']}
        </span>
        <span class="market-status {'market-open' if market_status['global_open'] else 'market-closed'}">
            🌍 Global: {market_status['global_status']}
        </span>
        <span class="market-status market-preopen">
            ⏰ {market_status['current_time']}
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

# Current Planetary Status - Compact
st.markdown(f"""
<div class="planetary-compact">
    <strong>{current_symbol} {current_planet} Hour</strong> | {current_influence} | 📊 {market_type.upper()} Market Focus
</div>
""", unsafe_allow_html=True)

# Compact Controls
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    auto_refresh = st.checkbox("🔄 Auto", value=False)
with col2:
    if st.button("📈", help="Update Now"):
        st.session_state.last_update = datetime.now()
        st.rerun()
with col3:
    refresh_rate = st.selectbox("Rate", [5, 10, 30], index=1)
with col4:
    market_filter = st.selectbox("Markets", ["All", "Indian Only", "Global Only"])
with col5:
    view_compact = st.checkbox("Compact View", value=True)

# Dynamic Market Display based on current status and filter
if market_filter in ["All", "Indian Only"] and (market_status['indian_open'] or market_filter == "All"):
    st.subheader("🇮🇳 Indian Markets (9:15 AM - 3:30 PM)")
    
    indian_markets = {k: v for k, v in st.session_state.market_data.items() if v.get('type') == 'indian'}
    
    if view_compact:
        # Compact grid layout
        indian_cols = st.columns(4)
        for idx, (market, data) in enumerate(indian_markets.items()):
            color_class = "positive" if data['change'] >= 0 else "negative"
            arrow = "▲" if data['change'] >= 0 else "▼"
            
            with indian_cols[idx % 4]:
                st.markdown(f"""
                <div class="market-card">
                    <h5 style="margin: 0 0 2px 0; font-size: 0.9em;">{market}</h5>
                    <h3 style="margin: 0 0 2px 0; font-size: 1.1em;">{data['price']:.1f}</h3>
                    <p class="{color_class}" style="margin: 0; font-size: 0.8em;">
                        {arrow} {abs(data['change']):.2f}%
                    </p>
                </div>
                """, unsafe_allow_html=True)
    else:
        # Regular layout for Indian markets
        indian_grid_cols = st.columns(3)
        for idx, (market, data) in enumerate(list(indian_markets.items())[:6]):
            color_class = "positive" if data['change'] >= 0 else "negative"
            arrow = "▲" if data['change'] >= 0 else "▼"
            
            with indian_grid_cols[idx % 3]:
                st.markdown(f"""
                <div class="compact-card">
                    <h4 style="margin: 0 0 5px 0;">{market}</h4>
                    <h2 style="margin: 0 0 5px 0;">{data['price']:.2f}</h2>
                    <p class="{color_class}" style="margin: 0 0 3px 0;">
                        {arrow} {abs(data['change']):.2f}%
                    </p>
                    <small>H: {data['high']:.0f} | L: {data['low']:.0f}</small>
                </div>
                """, unsafe_allow_html=True)

if market_filter in ["All", "Global Only"]:
    st.subheader("🌍 Global & Commodities (5:00 AM - 11:55 PM)")
    
    global_markets = {k: v for k, v in st.session_state.market_data.items() if v.get('type') == 'global'}
    
    if view_compact:
        # Compact grid for global markets
        global_cols = st.columns(4)
        for idx, (market, data) in enumerate(global_markets.items()):
            color_class = "positive" if data['change'] >= 0 else "negative"
            arrow = "▲" if data['change'] >= 0 else "▼"
            
            # Format price based on market type
            if market in ['GOLD', 'SILVER', 'CRUDE']:
                price_str = f"₹{data['price']:,.0f}"
            elif market == 'BITCOIN':
                price_str = f"${data['price']:,.0f}"
            elif market in ['USDINR', 'EURINR']:
                price_str = f"{data['price']:.2f}"
            else:
                price_str = f"{data['price']:,.0f}"
            
            with global_cols[idx % 4]:
                st.markdown(f"""
                <div class="market-card">
                    <h5 style="margin: 0 0 2px 0; font-size: 0.9em;">{market}</h5>
                    <h3 style="margin: 0 0 2px 0; font-size: 1.1em;">{price_str}</h3>
                    <p class="{color_class}" style="margin: 0; font-size: 0.8em;">
                        {arrow} {abs(data['change']):.2f}%
                    </p>
                </div>
                """, unsafe_allow_html=True)
    else:
        # Regular grid for global markets
        global_grid_cols = st.columns(3)
        for idx, (market, data) in enumerate(list(global_markets.items())[:6]):
            color_class = "positive" if data['change'] >= 0 else "negative"
            arrow = "▲" if data['change'] >= 0 else "▼"
            
            if market in ['GOLD', 'SILVER', 'CRUDE']:
                price_str = f"₹{data['price']:,.0f}"
            elif market == 'BITCOIN':
                price_str = f"${data['price']:,.0f}"
            elif market in ['USDINR', 'EURINR']:
                price_str = f"{data['price']:.2f}"
            else:
                price_str = f"{data['price']:,.0f}"
            
            with global_grid_cols[idx % 3]:
                st.markdown(f"""
                <div class="compact-card">
                    <h4 style="margin: 0 0 5px 0;">{market}</h4>
                    <h2 style="margin: 0 0 5px 0;">{price_str}</h2>
                    <p class="{color_class}" style="margin: 0 0 3px 0;">
                        {arrow} {abs(data['change']):.2f}%
                    </p>
                    <small>H: {data['high']:.0f} | L: {data['low']:.0f}</small>
                </div>
                """, unsafe_allow_html=True)

# Active Signals Section - Dynamic based on market hours
active_signals = []
current_time_str = current_time.strftime('%H:%M')

# Check Indian market signals if market is open or for reference
if market_filter in ["All", "Indian Only"]:
    for market in ['NIFTY', 'BANKNIFTY']:
        if market in st.session_state.timing_data['indian_signals']:
            for signal in st.session_state.timing_data['indian_signals'][market]:
                if is_time_in_range(current_time_str, signal['time']):
                    active_signals.append({
                        'Market': market,
                        'Signal': signal['signal'],
                        'Target': signal['target'],
                        'Planet': signal['planet'],
                        'Type': 'Indian',
                        'Time': signal['time']
                    })

# Check Global market signals
if market_filter in ["All", "Global Only"]:
    for market in ['GOLD', 'SILVER', 'CRUDE', 'BITCOIN', 'DOWJONES']:
        if market in st.session_state.timing_data['global_signals']:
            for signal in st.session_state.timing_data['global_signals'][market]:
                if is_time_in_range(current_time_str, signal['time']):
                    active_signals.append({
                        'Market': market,
                        'Signal': signal['signal'],
                        'Target': signal['target'],
                        'Planet': signal['planet'],
                        'Type': 'Global',
                        'Time': signal['time']
                    })

# Display Active Signals
if active_signals:
    st.subheader("🔥 LIVE TRADING SIGNALS")
    
    if len(active_signals) <= 4:
        signal_cols = st.columns(len(active_signals))
    else:
        signal_cols = st.columns(4)
    
    for idx, signal in enumerate(active_signals[:4]):
        col_idx = idx % len(signal_cols)
        
        signal_class = "signal-buy" if signal['Signal'] in ['BUY', 'STRONG BUY'] else \
                      "signal-sell" if signal['Signal'] in ['SELL', 'SHORT'] else \
                      "signal-caution" if signal['Signal'] == 'CAUTION' else "signal-hold"
        
        signal_emoji = '🟢' if signal['Signal'] in ['BUY', 'STRONG BUY'] else \
                      '🔴' if signal['Signal'] in ['SELL', 'SHORT'] else \
                      '🟡' if signal['Signal'] == 'CAUTION' else '🟡'
        
        with signal_cols[col_idx]:
            st.markdown(f"""
            <div class="signal-box {signal_class} active-signal">
                <div style="font-weight: bold; font-size: 0.9em;">{signal_emoji} {signal['Market']}</div>
                <div style="font-size: 1.1em; margin: 2px 0;">{signal['Signal']}</div>
                <div style="font-size: 0.75em;">
                    {signal['Target']} | {signal['Planet']}<br>
                    <span style="opacity: 0.8;">{signal['Type']} | {signal['Time']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    if len(active_signals) > 4:
        st.info(f"📈 +{len(active_signals) - 4} more signals available")
else:
    st.markdown("""
    <div class="signal-box signal-hold">
        <div style="font-weight: bold;">🕐 No Active Signals</div>
        <div style="font-size: 0.8em;">Markets in transition or closed</div>
    </div>
    """, unsafe_allow_html=True)

# Compact Market Timing Tables
timing_tab1, timing_tab2 = st.tabs(["🇮🇳 Indian Markets Timing", "🌍 Global Markets Timing"])

with timing_tab1:
    if market_status['indian_open']:
        st.success("🟢 Indian Markets are OPEN")
    else:
        st.error("🔴 Indian Markets are CLOSED")
    
    indian_timing_col1, indian_timing_col2 = st.columns(2)
    
    with indian_timing_col1:
        st.markdown("#### 📊 NIFTY Hourly Signals")
        for signal in st.session_state.timing_data['indian_signals']['NIFTY']:
            is_active = is_time_in_range(current_time_str, signal['time'])
            
            signal_class = "signal-buy" if signal['signal'] in ['BUY'] else \
                          "signal-sell" if signal['signal'] in ['SELL'] else \
                          "signal-caution" if signal['signal'] == 'CAUTION' else "signal-hold"
            
            if is_active:
                signal_class += " active-signal"
            
            active_text = " 🔥" if is_active else ""
            
            st.markdown(f"""
            <div class="signal-box {signal_class}">
                <strong>{signal['time']}{active_text}</strong><br>
                {signal['planet']} | {signal['signal']} | {signal['target']}
            </div>
            """, unsafe_allow_html=True)
    
    with indian_timing_col2:
        st.markdown("#### 🏦 BANKNIFTY Hourly Signals")
        for signal in st.session_state.timing_data['indian_signals']['BANKNIFTY']:
            is_active = is_time_in_range(current_time_str, signal['time'])
            
            signal_class = "signal-buy" if signal['signal'] in ['BUY'] else \
                          "signal-sell" if signal['signal'] in ['SELL'] else \
                          "signal-caution" if signal['signal'] == 'CAUTION' else "signal-hold"
            
            if is_active:
                signal_class += " active-signal"
            
            active_text = " 🔥" if is_active else ""
            
            st.markdown(f"""
            <div class="signal-box {signal_class}">
                <strong>{signal['time']}{active_text}</strong><br>
                {signal['planet']} | {signal['signal']} | {signal['target']}
            </div>
            """, unsafe_allow_html=True)

with timing_tab2:
    if market_status['global_open']:
        st.success("🟢 Global Markets are OPEN")
    else:
        st.error("🔴 Global Markets are CLOSED")
    
    # Global markets in tabs for better organization
    global_sub_tab1, global_sub_tab2, global_sub_tab3 = st.tabs(["🥇 Metals", "🛢️ Energy & Crypto", "📈 Indices"])
    
    with global_sub_tab1:
        metals_col1, metals_col2 = st.columns(2)
        
        with metals_col1:
            st.markdown("##### 🥇 GOLD")
            for signal in st.session_state.timing_data['global_signals']['GOLD']:
                is_active = is_time_in_range(current_time_str, signal['time'])
                
                signal_class = "signal-buy" if signal['signal'] in ['BUY'] else \
                              "signal-sell" if signal['signal'] in ['SELL'] else \
                              "signal-caution" if signal['signal'] == 'CAUTION' else "signal-hold"
                
                if is_active:
                    signal_class += " active-signal"
                
                active_text = " 🔥" if is_active else ""
                
                st.markdown(f"""
                <div class="signal-box {signal_class}" style="margin: 1px 0; padding: 4px;">
                    <strong style="font-size: 0.8em;">{signal['time']}{active_text}</strong><br>
                    <span style="font-size: 0.7em;">{signal['planet']} | {signal['signal']} | {signal['target']}</span>
                </div>
                """, unsafe_allow_html=True)
        
        with metals_col2:
            st.markdown("##### 🥈 SILVER")
            for signal in st.session_state.timing_data['global_signals']['SILVER']:
                is_active = is_time_in_range(current_time_str, signal['time'])
                
                signal_class = "signal-buy" if signal['signal'] in ['BUY'] else \
                              "signal-sell" if signal['signal'] in ['SELL'] else \
                              "signal-caution" if signal['signal'] == 'CAUTION' else "signal-hold"
                
                if is_active:
                    signal_class += " active-signal"
                
                active_text = " 🔥" if is_active else ""
                
                st.markdown(f"""
                <div class="signal-box {signal_class}" style="margin: 1px 0; padding: 4px;">
                    <strong style="font-size: 0.8em;">{signal['time']}{active_text}</strong><br>
                    <span style="font-size: 0.7em;">{signal['planet']} | {signal['signal']} | {signal['target']}</span>
                </div>
                """, unsafe_allow_html=True)
    
    with global_sub_tab2:
        energy_col1, energy_col2 = st.columns(2)
        
        with energy_col1:
            st.markdown("##### 🛢️ CRUDE OIL")
            for signal in st.session_state.timing_data['global_signals']['CRUDE']:
                is_active = is_time_in_range(current_time_str, signal['time'])
                
                signal_class = "signal-buy" if signal['signal'] in ['BUY'] else \
                              "signal-sell" if signal['signal'] in ['SELL', 'AVOID'] else \
                              "signal-caution" if signal['signal'] == 'CAUTION' else "signal-hold"
                
                if is_active:
                    signal_class += " active-signal"
                
                active_text = " 🔥" if is_active else ""
                
                st.markdown(f"""
                <div class="signal-box {signal_class}" style="margin: 1px 0; padding: 4px;">
                    <strong style="font-size: 0.8em;">{signal['time']}{active_text}</strong><br>
                    <span style="font-size: 0.7em;">{signal['planet']} | {signal['signal']} | {signal['target']}</span>
                </div>
                """, unsafe_allow_html=True)
        
        with energy_col2:
            st.markdown("##### ₿ BITCOIN")
            for signal in st.session_state.timing_data['global_signals']['BITCOIN']:
                is_active = is_time_in_range(current_time_str, signal['time'])
                
                signal_class = "signal-buy" if signal['signal'] in ['BUY'] else \
                              "signal-sell" if signal['signal'] in ['SELL'] else \
                              "signal-caution" if signal['signal'] == 'CAUTION' else "signal-hold"
                
                if is_active:
                    signal_class += " active-signal"
                
                active_text = " 🔥" if is_active else ""
                
                st.markdown(f"""
                <div class="signal-box {signal_class}" style="margin: 1px 0; padding: 4px;">
                    <strong style="font-size: 0.8em;">{signal['time']}{active_text}</strong><br>
                    <span style="font-size: 0.7em;">{signal['planet']} | {signal['signal']} | {signal['target']}</span>
                </div>
                """, unsafe_allow_html=True)
    
    with global_sub_tab3:
        st.markdown("##### 🇺🇸 DOW JONES (US Market Hours)")
        for signal in st.session_state.timing_data['global_signals']['DOWJONES']:
            is_active = is_time_in_range(current_time_str, signal['time'])
            
            signal_class = "signal-buy" if signal['signal'] in ['BUY'] else \
                          "signal-sell" if signal['signal'] in ['SELL'] else \
                          "signal-caution" if signal['signal'] == 'CAUTION' else "signal-hold"
            
            if is_active:
                signal_class += " active-signal"
            
            active_text = " 🔥" if is_active else ""
            
            st.markdown(f"""
            <div class="signal-box {signal_class}" style="margin: 1px 0; padding: 4px;">
                <strong style="font-size: 0.8em;">{signal['time']}{active_text}</strong><br>
                <span style="font-size: 0.7em;">{signal['planet']} | {signal['signal']} | {signal['target']}</span>
            </div>
            """, unsafe_allow_html=True)

# Market Hours Information
st.markdown("### ⏰ Market Trading Hours")

hours_col1, hours_col2 = st.columns(2)

with hours_col1:
    indian_status_color = "#d4edda" if market_status['indian_open'] else "#f8d7da"
    indian_text_color = "#155724" if market_status['indian_open'] else "#721c24"
    
    st.markdown(f"""
    <div style="background: {indian_status_color}; color: {indian_text_color}; padding: 8px; border-radius: 6px; border: 2px solid {indian_text_color};">
        <h5 style="margin: 0 0 3px 0;">🇮🇳 Indian Markets</h5>
        <div style="font-size: 0.85em;">
        <strong>Trading Hours:</strong> 9:15 AM - 3:30 PM<br>
        <strong>Status:</strong> {market_status['indian_status']}<br>
        <strong>Markets:</strong> NIFTY, BANKNIFTY, SENSEX, Sector Indices
        </div>
    </div>
    """, unsafe_allow_html=True)

with hours_col2:
    global_status_color = "#d4edda" if market_status['global_open'] else "#f8d7da"
    global_text_color = "#155724" if market_status['global_open'] else "#721c24"
    
    st.markdown(f"""
    <div style="background: {global_status_color}; color: {global_text_color}; padding: 8px; border-radius: 6px; border: 2px solid {global_text_color};">
        <h5 style="margin: 0 0 3px 0;">🌍 Global & Commodities</h5>
        <div style="font-size: 0.85em;">
        <strong>Trading Hours:</strong> 5:00 AM - 11:55 PM<br>
        <strong>Status:</strong> {market_status['global_status']}<br>
        <strong>Markets:</strong> Gold, Silver, Crude, Bitcoin, US Indices
        </div>
    </div>
    """, unsafe_allow_html=True)

# Next Hour Predictions - Compact
st.subheader("⏭️ Next Hour Planetary Forecast")

next_hour = current_time + timedelta(hours=1)
next_planet, next_symbol, next_influence, next_market_type = get_planetary_influence_dynamic(next_hour)

next_col1, next_col2, next_col3 = st.columns(3)

with next_col1:
    st.markdown(f"""
    <div class="planetary-compact">
        <strong>{next_symbol} Next Hour: {next_planet}</strong><br>
        <span style="font-size: 0.8em;">{next_influence}</span>
    </div>
    """, unsafe_allow_html=True)

with next_col2:
    # Determine if next hour is favorable
    favorable_planets = ['Sun', 'Moon', 'Jupiter', 'Venus']
    if next_planet in favorable_planets:
        st.success("🟢 Favorable Next Hour")
    else:
        st.warning("🟡 Caution Next Hour")

with next_col3:
    market_focus = "Indian Markets" if next_market_type == "indian" else "Global Markets"
    st.info(f"🎯 Focus: {market_focus}")

# Sector Quick View - Ultra Compact
if market_filter in ["All", "Indian Only"]:
    st.subheader("🏭 Sector Quick Status")
    
    # Define current sector trends (simplified)
    current_sectors = {
        'Banking': 'Bullish', 'IT': 'Bearish', 'Pharma': 'Bullish', 'Auto': 'Neutral',
        'Metal': 'Bearish', 'FMCG': 'Bullish', 'Energy': 'Volatile', 'Realty': 'Bearish'
    }
    
    st.markdown('<div class="sector-grid">', unsafe_allow_html=True)
    
    for sector, trend in current_sectors.items():
        if trend == 'Bullish':
            cell_class = "trending-up"
            emoji = "🟢"
        elif trend == 'Bearish':
            cell_class = "trending-down"
            emoji = "🔴"
        elif trend == 'Volatile':
            cell_class = "trending-volatile"
            emoji = "⚡"
        else:
            cell_class = "trending-sideways"
            emoji = "🟡"
        
        st.markdown(f"""
        <div class="sector-cell {cell_class}">
            {emoji} {sector}<br>{trend}
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Tomorrow's Quick Preview
st.subheader("📅 Tomorrow's Key Opportunities")

tomorrow_preview_col1, tomorrow_preview_col2, tomorrow_preview_col3 = st.columns(3)

with tomorrow_preview_col1:
    st.markdown("""
    <div class="signal-box signal-buy">
        <strong>🌟 Best Opportunity</strong><br>
        <span style="font-size: 0.9em;">12:15-13:15 (Jupiter ♃)</span><br>
        <span style="font-size: 0.8em;">STRONG BUY Banking +2.1%</span>
    </div>
    """, unsafe_allow_html=True)

with tomorrow_preview_col2:
    st.markdown("""
    <div class="signal-box signal-sell">
        <strong>⚠️ Avoid Period</strong><br>
        <span style="font-size: 0.9em;">14:15-15:15 (Saturn ♄)</span><br>
        <span style="font-size: 0.8em;">BOOK PROFITS All Sectors</span>
    </div>
    """, unsafe_allow_html=True)

with tomorrow_preview_col3:
    st.markdown("""
    <div class="signal-box signal-caution">
        <strong>⚡ High Volatility</strong><br>
        <span style="font-size: 0.9em;">10:15-11:15 (Mars ♂️)</span><br>
        <span style="font-size: 0.8em;">Use Tight Stops ±2%</span>
    </div>
    """, unsafe_allow_html=True)

# Quick Action Panel
st.subheader("⚡ Quick Actions")

action_col1, action_col2, action_col3, action_col4 = st.columns(4)

with action_col1:
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.session_state.last_update = datetime.now()
        st.success("Data refreshed!")
        st.rerun()

with action_col2:
    if st.button("📊 Show All Signals", use_container_width=True):
        st.info("All signals displayed above")

with action_col3:
    if st.button("🎯 Best Trades Now", use_container_width=True):
        if active_signals:
            st.success(f"Found {len(active_signals)} active signals!")
        else:
            st.warning("No active signals currently")

with action_col4:
    if st.button("📅 Tomorrow Forecast", use_container_width=True):
        st.info("Tomorrow's forecast shown above")

# Compact Footer
st.markdown("---")
footer_col1, footer_col2, footer_col3, footer_col4, footer_col5 = st.columns(5)

with footer_col1:
    st.caption(f"⏰ Updated: {st.session_state.last_update.strftime('%H:%M')}")

with footer_col2:
    st.caption(f"{current_symbol} {current_planet}")

with footer_col3:
    indian_status_short = "🟢 IND" if market_status['indian_open'] else "🔴 IND"
    st.caption(indian_status_short)

with footer_col4:
    global_status_short = "🟢 GLB" if market_status['global_open'] else "🔴 GLB"
    st.caption(global_status_short)

with footer_col5:
    active_count = len(active_signals)
    st.caption(f"🎯 Signals: {active_count}")

# Auto-refresh functionality
if auto_refresh:
    time.sleep(refresh_rate)
    st.rerun()

# Extended Trading Schedule Information
with st.expander("📋 Complete Trading Schedule", expanded=False):
    schedule_col1, schedule_col2 = st.columns(2)
    
    with schedule_col1:
        st.markdown("""
        #### 🇮🇳 Indian Markets Schedule
        - **Pre-Market:** 9:00 - 9:15 AM
        - **Opening:** 9:15 AM
        - **Regular Trading:** 9:15 AM - 3:30 PM
        - **Closing:** 3:30 PM
        - **Post-Market Analysis:** 3:30 - 4:00 PM
        
        **Key Planetary Hours:**
        - Morning Strength: 9:15-11:00 AM
        - Midday Caution: 12:00-14:00 PM
        - Closing Rally: 15:00-15:30 PM
        """)
    
    with schedule_col2:
        st.markdown("""
        #### 🌍 Global Markets Schedule
        - **Early Asian:** 5:00 - 9:00 AM
        - **Indian Overlap:** 9:15 AM - 3:30 PM
        - **European:** 1:30 - 10:00 PM
        - **US Markets:** 7:00 PM - 1:30 AM
        - **Overnight:** 1:30 - 5:00 AM (Closed)
        
        **Key Global Hours:**
        - Asian Session: 5:00-9:00 AM
        - European: 1:30-7:00 PM
        - US Prime: 7:00-11:55 PM
        """)

# Performance Tips
with st.expander("💡 Trading Tips Based on Market Hours", expanded=False):
    tips_col1, tips_col2 = st.columns(2)
    
    with tips_col1:
        st.markdown("""
        #### 🇮🇳 Indian Market Tips
        - **Best Entry:** 9:15-10:00 AM (Venus hour)
        - **Avoid:** 12:00-13:00 PM (Saturn resistance)
        - **Best Exit:** 15:00-15:30 PM (Sun closing)
        - **Volatile Time:** 13:00-14:00 PM (Mars hour)
        """)
    
    with tips_col2:
        st.markdown("""
        #### 🌍 Global Market Tips
        - **Gold/Silver Best:** 7:00-9:00 AM, 20:00-22:00 PM
        - **Bitcoin Volatile:** 5:00-9:00 AM
        - **US Indices:** 19:00-23:00 PM
        - **Avoid Crude:** 22:00-23:55 PM (high volatility)
        """)
