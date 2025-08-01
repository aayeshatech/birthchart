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

# Enhanced CSS with new styles
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
    animation: scroll-text 30s linear infinite;
}
.planet-info {
    background: linear-gradient(45deg, #e3f2fd, #bbdefb);
    color: #1565c0;
    padding: 12px;
    border-radius: 8px;
    margin: 8px 0;
    border-left: 4px solid #2196f3;
    font-weight: 500;
}
.timing-alert {
    background: #fff3cd;
    color: #856404;
    padding: 12px;
    border-radius: 8px;
    margin: 8px 0;
    border-left: 4px solid #ffc107;
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
    padding: 8px 12px;
    border-radius: 6px;
    font-weight: bold;
    margin: 4px 0;
}
.trend-bearish {
    background-color: #f8d7da;
    color: #721c24;
    padding: 8px 12px;
    border-radius: 6px;
    font-weight: bold;
    margin: 4px 0;
}
.trend-volatile {
    background-color: #fff3cd;
    color: #856404;
    padding: 8px 12px;
    border-radius: 6px;
    font-weight: bold;
    margin: 4px 0;
}
@keyframes pulse {
    0% { opacity: 1; }
    50% { opacity: 0.7; }
    100% { opacity: 1; }
}
@keyframes scroll-text {
    0% { transform: translateX(100%); }
    100% { transform: translateX(-100%); }
}
.timeframe-tab {
    background: #f8f9fa;
    padding: 15px;
    border-radius: 8px;
    margin: 10px 0;
    border: 1px solid #dee2e6;
}
.market-type-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: #ffffff;
    padding: 15px;
    border-radius: 10px;
    margin: 15px 0;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
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
            'GBPINR': {'price': 106.75, 'change': 0.28, 'high': 107.20, 'low': 106.50}
        }
    
    if 'last_update' not in st.session_state:
        st.session_state.last_update = datetime.now()

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
        
        st.session_state.last_update = datetime.now()
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

# Get current date and time
current_date = datetime.now()
current_date_str = current_date.strftime('%d %B %Y')
current_day = current_date.strftime('%A')
tomorrow_date = (current_date + timedelta(days=1)).strftime('%d %B %Y')
tomorrow_day = (current_date + timedelta(days=1)).strftime('%A')

# Header
st.markdown("""
<div class="main-header">
    <h1 style="margin: 0 0 10px 0;">🕉️ Vedic Market Intelligence Dashboard</h1>
    <h2 style="margin: 0 0 5px 0;">Complete Planetary Transit Analysis</h2>
    <p style="margin: 0; font-size: 1.1em;">Live Astrological Market Timing for Equity • Commodity • Forex • Global Markets</p>
</div>
""", unsafe_allow_html=True)

# Prominent Date Display
st.markdown(f"""
<div class="date-display">
    <h1 style="margin: 0 0 10px 0; font-size: 2.5em;">📅 Today: {current_day}, {current_date_str}</h1>
    <h3 style="margin: 0; opacity: 0.9;">Live Planetary Transit Analysis • Real-time Market Intelligence</h3>
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
    view_mode = st.selectbox("Analysis Depth", ["Complete", "Intraday Focus", "Positional Focus"])

# Live Ticker
try:
    ticker_items = []
    for market, data in list(st.session_state.market_data.items())[:8]:
        arrow = '▲' if data['change'] >= 0 else '▼'
        ticker_items.append(f"{market}: {data['price']:.1f} {arrow} {abs(data['change']):.2f}%")
    
    ticker_text = " | ".join(ticker_items)
    st.markdown(f'<div class="ticker-box">📡 LIVE MARKETS: {ticker_text}</div>', unsafe_allow_html=True)
except Exception as e:
    st.error(f"Error creating ticker: {e}")

# Current Planetary Hour
current_hour = current_date.hour
current_planet, current_symbol, current_influence = get_planetary_influence(current_hour)

st.markdown(f"""
<div class="planet-info">
    <h3 style="margin: 0 0 5px 0;">{current_symbol} Current Planetary Hour: {current_planet}</h3>
    <p style="margin: 0; font-size: 1.1em;">🌟 {current_influence}</p>
    <p style="margin: 5px 0 0 0; font-size: 0.9em;">⏰ Active Now: {current_date.strftime('%H:%M')} | Market Effect: <strong>Live</strong></p>
</div>
""", unsafe_allow_html=True)

# Main Content - Today and Tomorrow Sections
main_tab1, main_tab2 = st.tabs([f"🌟 TODAY - {current_day}, {current_date_str}", f"🔮 TOMORROW - {tomorrow_day}, {tomorrow_date}"])

with main_tab1:
    st.markdown(f"""
    <div class="section-header">
        <h2 style="margin: 0 0 10px 0;">📊 TODAY'S COMPLETE PLANETARY TRANSIT REPORT</h2>
        <h3 style="margin: 0; opacity: 0.9;">{current_day}, {current_date_str} • Full Market Analysis</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Today's Market Types Analysis
    equity_tab, commodity_tab, forex_tab, global_tab = st.tabs(["📈 EQUITY MARKETS", "🏭 COMMODITIES", "💱 FOREX", "🌍 GLOBAL MARKETS"])
    
    with equity_tab:
        st.markdown("""
        <div class="market-type-header">
            <h3 style="margin: 0;">📈 EQUITY MARKETS - Today's Planetary Analysis</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Timeframe analysis for Equity
        timeframe_tab1, timeframe_tab2, timeframe_tab3, timeframe_tab4 = st.tabs(["⚡ INTRADAY", "📅 DAILY", "📊 WEEKLY", "🎯 POSITIONAL"])
        
        with timeframe_tab1:
            st.markdown("### ⚡ Today's Intraday Equity Signals")
            
            # NIFTY Intraday
            nifty_col, banknifty_col = st.columns(2)
            
            with nifty_col:
                st.markdown("#### 🎯 NIFTY 50 - Hourly Signals")
                nifty_intraday = [
                    {'time': '09:15-10:00', 'planet': 'Venus ♀', 'signal': 'BUY', 'target': '+0.8%', 'sl': '-0.3%', 'trend': 'Bullish'},
                    {'time': '10:00-11:00', 'planet': 'Sun ☀️', 'signal': 'HOLD', 'target': '+0.5%', 'sl': '-0.2%', 'trend': 'Neutral'},
                    {'time': '11:00-12:00', 'planet': 'Mercury ☿', 'signal': 'BUY', 'target': '+1.2%', 'sl': '-0.4%', 'trend': 'Bullish'},
                    {'time': '12:00-13:00', 'planet': 'Saturn ♄', 'signal': 'SELL', 'target': '-0.9%', 'sl': '+0.3%', 'trend': 'Bearish'},
                    {'time': '13:00-14:00', 'planet': 'Mars ♂️', 'signal': 'CAUTION', 'target': '±1.5%', 'sl': '±0.5%', 'trend': 'Volatile'},
                    {'time': '14:00-15:00', 'planet': 'Rahu ☊', 'signal': 'SELL', 'target': '-1.1%', 'sl': '+0.4%', 'trend': 'Bearish'},
                    {'time': '15:00-15:30', 'planet': 'Jupiter ♃', 'signal': 'BUY', 'target': '+0.6%', 'sl': '-0.2%', 'trend': 'Bullish'}
                ]
                
                for signal in nifty_intraday:
                    is_active = current_hour >= int(signal['time'].split('-')[0].split(':')[0]) and current_hour < int(signal['time'].split('-')[1].split(':')[0])
                    
                    if signal['trend'] == 'Bullish':
                        css_class = 'live-signal' if is_active else 'trend-bullish'
                    elif signal['trend'] == 'Bearish':
                        css_class = 'warning-signal' if is_active else 'trend-bearish'
                    else:
                        css_class = 'trend-volatile'
                    
                    active_text = " 🔥 ACTIVE NOW" if is_active else ""
                    
                    st.markdown(f"""
                    <div class="{css_class}">
                        <strong>{signal['time']}{active_text}</strong><br>
                        Planet: {signal['planet']} | Signal: <strong>{signal['signal']}</strong><br>
                        Target: {signal['target']} | SL: {signal['sl']}
                    </div>
                    """, unsafe_allow_html=True)
            
            with banknifty_col:
                st.markdown("#### 🏦 BANKNIFTY - Hourly Signals")
                banknifty_intraday = [
                    {'time': '09:15-10:00', 'planet': 'Jupiter ♃', 'signal': 'BUY', 'target': '+1.5%', 'sl': '-0.5%', 'trend': 'Bullish'},
                    {'time': '10:00-11:00', 'planet': 'Sun ☀️', 'signal': 'BUY', 'target': '+1.8%', 'sl': '-0.6%', 'trend': 'Bullish'},
                    {'time': '11:00-12:00', 'planet': 'Mercury ☿', 'signal': 'HOLD', 'target': '±0.4%', 'sl': '', 'trend': 'Neutral'},
                    {'time': '12:00-13:00', 'planet': 'Saturn ♄', 'signal': 'SELL', 'target': '-1.3%', 'sl': '+0.4%', 'trend': 'Bearish'},
                    {'time': '13:00-14:00', 'planet': 'Mars ♂️', 'signal': 'SELL', 'target': '-1.6%', 'sl': '+0.5%', 'trend': 'Bearish'},
                    {'time': '14:00-15:00', 'planet': 'Rahu ☊', 'signal': 'CAUTION', 'target': '±2.0%', 'sl': '±0.7%', 'trend': 'Volatile'},
                    {'time': '15:00-15:30', 'planet': 'Venus ♀', 'signal': 'BUY', 'target': '+1.0%', 'sl': '-0.3%', 'trend': 'Bullish'}
                ]
                
                for signal in banknifty_intraday:
                    is_active = current_hour >= int(signal['time'].split('-')[0].split(':')[0]) and current_hour < int(signal['time'].split('-')[1].split(':')[0])
                    
                    if signal['trend'] == 'Bullish':
                        css_class = 'live-signal' if is_active else 'trend-bullish'
                    elif signal['trend'] == 'Bearish':
                        css_class = 'warning-signal' if is_active else 'trend-bearish'
                    else:
                        css_class = 'trend-volatile'
                    
                    active_text = " 🔥 ACTIVE NOW" if is_active else ""
                    
                    st.markdown(f"""
                    <div class="{css_class}">
                        <strong>{signal['time']}{active_text}</strong><br>
                        Planet: {signal['planet']} | Signal: <strong>{signal['signal']}</strong><br>
                        Target: {signal['target']} | SL: {signal['sl']}
                    </div>
                    """, unsafe_allow_html=True)
        
        with timeframe_tab2:
            st.markdown("### 📅 Daily Equity Analysis")
            
            daily_col1, daily_col2 = st.columns(2)
            
            with daily_col1:
                st.markdown("""
                <div class="report-section">
                    <h4>🎯 Today's Overall Equity Outlook</h4>
                    <p><strong>Dominant Planet:</strong> Jupiter ♃ (12:00-13:00)</p>
                    <p><strong>Market Bias:</strong> <span class="positive">Moderately Bullish</span></p>
                    <p><strong>Expected Range:</strong> NIFTY: 24650-24950, BANKNIFTY: 52200-52800</p>
                    <p><strong>Key Levels:</strong> Support at 24700, Resistance at 24900</p>
                    <p><strong>Sector Focus:</strong> Banking, Energy, Pharma positive</p>
                </div>
                """, unsafe_allow_html=True)
            
            with daily_col2:
                st.markdown("""
                <div class="report-section">
                    <h4>⚠️ Daily Risk Factors</h4>
                    <p><strong>High Risk Period:</strong> 13:00-15:00 (Mars & Rahu)</p>
                    <p><strong>Volatility Expected:</strong> Above normal due to Mars influence</p>
                    <p><strong>Sectors to Avoid:</strong> IT, Metals during 12:00-14:00</p>
                    <p><strong>Stop Loss:</strong> Wider than usual (0.8-1.0%)</p>
                    <p><strong>Position Sizing:</strong> Reduce by 20% during volatile hours</p>
                </div>
                """, unsafe_allow_html=True)
        
        with timeframe_tab3:
            st.markdown("### 📊 Weekly Equity Perspective")
            
            st.markdown("""
            <div class="report-section">
                <h4>📈 This Week's Equity Forecast</h4>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                    <div>
                        <h5>🟢 Bullish Factors</h5>
                        <ul>
                            <li>Jupiter dominant on Thu-Fri</li>
                            <li>Venus supporting auto sector</li>
                            <li>Banking sector strength continues</li>
                            <li>Energy sector revival expected</li>
                        </ul>
                    </div>
                    <div>
                        <h5>🔴 Bearish Factors</h5>
                        <ul>
                            <li>Mercury retrograde effect on IT</li>
                            <li>Saturn pressure on metals</li>
                            <li>Mid-week volatility (Mars)</li>
                            <li>Global cues uncertain</li>
                        </ul>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with timeframe_tab4:
            st.markdown("### 🎯 Positional Equity Strategy")
            
            positional_col1, positional_col2 = st.columns(2)
            
            with positional_col1:
                st.markdown("""
                <div class="report-section">
                    <h4>📈 Long-term Bullish Positions</h4>
                    <p><strong>Holding Period:</strong> 2-4 weeks</p>
                    <p><strong>Recommended Sectors:</strong></p>
                    <ul>
                        <li>Banking (Jupiter support till Aug 15)</li>
                        <li>Pharma (Sun-Jupiter conjunction)</li>
                        <li>Energy (Mars-Sun positive aspect)</li>
                        <li>FMCG (Venus blessing consumer goods)</li>
                    </ul>
                    <p><strong>Entry Strategy:</strong> Accumulate on 2-3% dips</p>
                    <p><strong>Target:</strong> 15-20% gains by month-end</p>
                </div>
                """, unsafe_allow_html=True)
            
            with positional_col2:
                st.markdown("""
                <div class="report-section">
                    <h4>🔴 Sectors to Avoid</h4>
                    <p><strong>Weak Period:</strong> Next 2-3 weeks</p>
                    <p><strong>Avoid/Reduce:</strong></p>
                    <ul>
                        <li>IT (Mercury retrograde till Aug 20)</li>
                        <li>Metals (Saturn opposition)</li>
                        <li>Real Estate (Ketu influence)</li>
                        <li>Telecom (Communication disruption)</li>
                    </ul>
                    <p><strong>Action:</strong> Book profits if holding</p>
                    <p><strong>Re-entry:</strong> Wait for planetary shift</p>
                </div>
                """, unsafe_allow_html=True)
    
    with commodity_tab:
        st.markdown("""
        <div class="market-type-header">
            <h3 style="margin: 0;">🏭 COMMODITIES - Today's Planetary Analysis</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Commodity timeframes
        comm_timeframe1, comm_timeframe2, comm_timeframe3, comm_timeframe4 = st.tabs(["⚡ INTRADAY", "📅 DAILY", "📊 WEEKLY", "🎯 POSITIONAL"])
        
        with comm_timeframe1:
            st.markdown("### ⚡ Today's Commodity Intraday Signals")
            
            gold_col, silver_col, crude_col = st.columns(3)
            
            with gold_col:
                st.markdown("#### 🥇 GOLD Hourly Signals")
                gold_signals = [
                    {'time': '09:00-10:30', 'planet': 'Sun ☀️', 'signal': 'BUY', 'target': '+0.6%', 'sl': '-0.2%'},
                    {'time': '10:30-12:00', 'planet': 'Mercury ☿', 'signal': 'HOLD', 'target': '±0.3%', 'sl': ''},
                    {'time': '14:00-16:00', 'planet': 'Mars ♂️', 'signal': 'CAUTION', 'target': '±1.2%', 'sl': '±0.4%'},
                    {'time': '18:00-20:00', 'planet': 'Venus ♀', 'signal': 'BUY', 'target': '+0.9%', 'sl': '-0.3%'},
                    {'time': '20:00-23:30', 'planet': 'Jupiter ♃', 'signal': 'STRONG BUY', 'target': '+1.8%', 'sl': '-0.5%'}
                ]
                
                for signal in gold_signals:
                    st.markdown(f"""
                    <div class="trend-bullish">
                        <strong>{signal['time']}</strong><br>
                        {signal['planet']} | <strong>{signal['signal']}</strong><br>
                        Target: {signal['target']} | SL: {signal['sl']}
                    </div>
                    """, unsafe_allow_html=True)
            
            with silver_col:
                st.markdown("#### 🥈 SILVER Hourly Signals")
                silver_signals = [
                    {'time': '09:00-10:30', 'planet': 'Moon 🌙', 'signal': 'WAIT', 'target': '±0.4%', 'sl': ''},
                    {'time': '10:30-12:00', 'planet': 'Sun ☀️', 'signal': 'BUY', 'target': '+1.2%', 'sl': '-0.4%'},
                    {'time': '14:00-16:00', 'planet': 'Jupiter ♃', 'signal': 'STRONG BUY', 'target': '+2.1%', 'sl': '-0.6%'},
                    {'time': '18:00-20:00', 'planet': 'Mars ♂️', 'signal': 'CAUTION', 'target': '±1.8%', 'sl': '±0.6%'},
                    {'time': '20:00-23:30', 'planet': 'Venus ♀', 'signal': 'BUY', 'target': '+1.5%', 'sl': '-0.5%'}
                ]
                
                for signal in silver_signals:
                    st.markdown(f"""
                    <div class="trend-bullish">
                        <strong>{signal['time']}</strong><br>
                        {signal['planet']} | <strong>{signal['signal']}</strong><br>
                        Target: {signal['target']} | SL: {signal['sl']}
                    </div>
                    """, unsafe_allow_html=True)
            
            with crude_col:
                st.markdown("#### 🛢️ CRUDE OIL Hourly Signals")
                crude_signals = [
                    {'time': '10:00-12:00', 'planet': 'Saturn ♄', 'signal': 'SELL', 'target': '-1.2%', 'sl': '+0.4%'},
                    {'time': '14:30-17:00', 'planet': 'Mars ♂️', 'signal': 'CAUTION', 'target': '±2.5%', 'sl': '±0.8%'},
                    {'time': '19:00-21:00', 'planet': 'Rahu ☊', 'signal': 'SELL', 'target': '-1.8%', 'sl': '+0.6%'},
                    {'time': '21:00-23:30', 'planet': 'Ketu ☋', 'signal': 'AVOID', 'target': '±3.0%', 'sl': '±1.0%'}
                ]
                
                for signal in crude_signals:
                    st.markdown(f"""
                    <div class="trend-bearish">
                        <strong>{signal['time']}</strong><br>
                        {signal['planet']} | <strong>{signal['signal']}</strong><br>
                        Target: {signal['target']} | SL: {signal['sl']}
                    </div>
                    """, unsafe_allow_html=True)
        
        with comm_timeframe2:
            st.markdown("### 📅 Daily Commodity Outlook")
            
            comm_daily_col1, comm_daily_col2 = st.columns(2)
            
            with comm_daily_col1:
                st.markdown("""
                <div class="report-section">
                    <h4>🥇 Precious Metals Daily Analysis</h4>
                    <p><strong>GOLD:</strong> <span class="positive">Bullish bias</span> - Jupiter support</p>
                    <p><strong>Expected Range:</strong> ₹71,500 - ₹72,200</p>
                    <p><strong>Key Level:</strong> Support at ₹71,750</p>
                    <p><strong>SILVER:</strong> <span class="positive">Very Bullish</span> - Strong planetary support</p>
                    <p><strong>Expected Range:</strong> ₹90,800 - ₹92,500</p>
                    <p><strong>Strategy:</strong> Buy on dips, Jupiter peak at 8-9 PM</p>
                </div>
                """, unsafe_allow_html=True)
            
            with comm_daily_col2:
                st.markdown("""
                <div class="report-section">
                    <h4>🛢️ Energy Commodities Daily Analysis</h4>
                    <p><strong>CRUDE OIL:</strong> <span class="negative">Bearish trend</span> - Saturn pressure</p>
                    <p><strong>Expected Range:</strong> ₹6,750 - ₹6,900</p>
                    <p><strong>Key Level:</strong> Resistance at ₹6,850</p>
                    <p><strong>Natural Gas:</strong> <span class="negative">Weak</span> - Avoid longs</p>
                    <p><strong>Strategy:</strong> Short on rallies, avoid during volatile hours</p>
                </div>
                """, unsafe_allow_html=True)
        
        with comm_timeframe3:
            st.markdown("### 📊 Weekly Commodity Forecast")
            
            st.markdown("""
            <div class="report-section">
                <h4>📈 This Week's Commodity Trends</h4>
                <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px;">
                    <div style="background: #d4edda; padding: 15px; border-radius: 8px;">
                        <h5>🥇 GOLD</h5>
                        <p><strong>Trend:</strong> <span class="positive">Bullish</span></p>
                        <p><strong>Target:</strong> ₹72,500</p>
                        <p><strong>Best Days:</strong> Thu-Fri</p>
                    </div>
                    <div style="background: #d4edda; padding: 15px; border-radius: 8px;">
                        <h5>🥈 SILVER</h5>
                        <p><strong>Trend:</strong> <span class="positive">Very Bullish</span></p>
                        <p><strong>Target:</strong> ₹94,000</p>
                        <p><strong>Best Days:</strong> Wed-Fri</p>
                    </div>
                    <div style="background: #f8d7da; padding: 15px; border-radius: 8px;">
                        <h5>🛢️ CRUDE</h5>
                        <p><strong>Trend:</strong> <span class="negative">Bearish</span></p>
                        <p><strong>Target:</strong> ₹6,650</p>
                        <p><strong>Weak Days:</strong> Mon-Wed</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with comm_timeframe4:
            st.markdown("### 🎯 Positional Commodity Strategy")
            
            st.markdown("""
            <div class="report-section">
                <h4>💎 Long-term Commodity Positions (2-6 weeks)</h4>
                
                <h5>🟢 STRONG BUY - Precious Metals</h5>
                <p><strong>GOLD:</strong> Jupiter-Venus conjunction supports 6-month bull run</p>
                <p><strong>Entry:</strong> Any dip below ₹71,800 | <strong>Target:</strong> ₹75,000 | <strong>SL:</strong> ₹70,500</p>
                
                <p><strong>SILVER:</strong> Exceptional planetary support till September</p>
                <p><strong>Entry:</strong> Current levels | <strong>Target:</strong> ₹98,000 | <strong>SL:</strong> ₹88,000</p>
                
                <h5>🔴 AVOID - Energy Complex</h5>
                <p><strong>CRUDE OIL:</strong> Saturn opposition continues till August end</p>
                <p><strong>Strategy:</strong> Short on rallies | <strong>Target:</strong> ₹6,400 | <strong>SL:</strong> ₹7,000</p>
                
                <h5>⚡ WATCH - Base Metals</h5>
                <p><strong>COPPER/ZINC:</strong> Mixed signals, trade range-bound</p>
                <p><strong>Strategy:</strong> Wait for clear planetary shift in September</p>
            </div>
            """, unsafe_allow_html=True)
    
    with forex_tab:
        st.markdown("""
        <div class="market-type-header">
            <h3 style="margin: 0;">💱 FOREX - Today's Planetary Analysis</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Current Forex Prices
        forex_price_col1, forex_price_col2, forex_price_col3 = st.columns(3)
        
        with forex_price_col1:
            data = st.session_state.market_data['USDINR']
            color_class = "positive" if data['change'] >= 0 else "negative"
            arrow = "▲" if data['change'] >= 0 else "▼"
            st.markdown(f"""
            <div class="market-card">
                <h4>USD/INR</h4>
                <h2>₹{data['price']:.2f}</h2>
                <p class="{color_class}">
                    {arrow} {abs(data['change']):.2f}%
                </p>
                <small>H: {data['high']:.2f} | L: {data['low']:.2f}</small>
            </div>
            """, unsafe_allow_html=True)
        
        with forex_price_col2:
            data = st.session_state.market_data['EURINR']
            color_class = "positive" if data['change'] >= 0 else "negative"
            arrow = "▲" if data['change'] >= 0 else "▼"
            st.markdown(f"""
            <div class="market-card">
                <h4>EUR/INR</h4>
                <h2>₹{data['price']:.2f}</h2>
                <p class="{color_class}">
                    {arrow} {abs(data['change']):.2f}%
                </p>
                <small>H: {data['high']:.2f} | L: {data['low']:.2f}</small>
            </div>
            """, unsafe_allow_html=True)
        
        with forex_price_col3:
            data = st.session_state.market_data['GBPINR']
            color_class = "positive" if data['change'] >= 0 else "negative"
            arrow = "▲" if data['change'] >= 0 else "▼"
            st.markdown(f"""
            <div class="market-card">
                <h4>GBP/INR</h4>
                <h2>₹{data['price']:.2f}</h2>
                <p class="{color_class}">
                    {arrow} {abs(data['change']):.2f}%
                </p>
                <small>H: {data['high']:.2f} | L: {data['low']:.2f}</small>
            </div>
            """, unsafe_allow_html=True)
        
        # Forex Analysis
        forex_timeframe1, forex_timeframe2, forex_timeframe3, forex_timeframe4 = st.tabs(["⚡ INTRADAY", "📅 DAILY", "📊 WEEKLY", "🎯 POSITIONAL"])
        
        with forex_timeframe1:
            st.markdown("### 💱 Today's Forex Intraday Analysis")
            
            forex_intra_col1, forex_intra_col2 = st.columns(2)
            
            with forex_intra_col1:
                st.markdown("""
                <div class="report-section">
                    <h4>💵 USD/INR Hourly Signals</h4>
                    <div class="trend-bearish">
                        <strong>09:00-11:00:</strong> Venus ♀ | SELL | Target: 83.25 | SL: 83.55
                    </div>
                    <div class="trend-volatile">
                        <strong>11:00-13:00:</strong> Mercury ☿ | RANGE | 83.35-83.50
                    </div>
                    <div class="trend-bearish">
                        <strong>13:00-15:00:</strong> Saturn ♄ | SELL | Target: 83.20 | SL: 83.45
                    </div>
                    <div class="trend-bullish">
                        <strong>15:00-17:00:</strong> Jupiter ♃ | BUY | Target: 83.60 | SL: 83.35
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with forex_intra_col2:
                st.markdown("""
                <div class="report-section">
                    <h4>💶 EUR/INR & 💷 GBP/INR Signals</h4>
                    <p><strong>EUR/INR:</strong></p>
                    <div class="trend-bullish">
                        <strong>Morning:</strong> Venus support | BUY | Target: 88.50
                    </div>
                    <div class="trend-bearish">
                        <strong>Afternoon:</strong> Saturn pressure | SELL | Target: 88.00
                    </div>
                    
                    <p><strong>GBP/INR:</strong></p>
                    <div class="trend-volatile">
                        <strong>All Day:</strong> Mars influence | High volatility | Range: 106.50-107.20
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        with forex_timeframe2:
            st.markdown("### 📅 Daily Forex Outlook")
            
            st.markdown("""
            <div class="report-section">
                <h4>💱 Today's Forex Summary</h4>
                
                <h5>💵 USD/INR: <span class="negative">Bearish Bias</span></h5>
                <p><strong>Range:</strong> 83.20 - 83.55 | <strong>Pivot:</strong> 83.40</p>
                <p><strong>Trend:</strong> Saturn creates selling pressure on USD</p>
                <p><strong>Strategy:</strong> Sell on rallies towards 83.50</p>
                
                <h5>💶 EUR/INR: <span class="positive">Mildly Bullish</span></h5>
                <p><strong>Range:</strong> 87.90 - 88.60 | <strong>Pivot:</strong> 88.25</p>
                <p><strong>Trend:</strong> Venus supports Euro strength</p>
                <p><strong>Strategy:</strong> Buy on dips below 88.00</p>
                
                <h5>💷 GBP/INR: <span style="color: #856404;">High Volatility</span></h5>
                <p><strong>Range:</strong> 106.30 - 107.50 | <strong>Pivot:</strong> 106.75</p>
                <p><strong>Trend:</strong> Mars creates unpredictable swings</p>
                <p><strong>Strategy:</strong> Avoid or use tight stops</p>
            </div>
            """, unsafe_allow_html=True)
        
        with forex_timeframe3:
            st.markdown("### 📊 Weekly Forex Perspective")
            
            st.markdown("""
            <div class="report-section">
                <h4>📈 This Week's Forex Forecast</h4>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px;">
                    <div style="background: #f8d7da; padding: 15px; border-radius: 8px;">
                        <h5>💵 USD/INR</h5>
                        <p><strong>Trend:</strong> <span class="negative">Bearish</span></p>
                        <p><strong>Target:</strong> 82.80-83.00</p>
                        <p><strong>Reason:</strong> Fed dovish, RBI hawkish</p>
                    </div>
                    <div style="background: #d4edda; padding: 15px; border-radius: 8px;">
                        <h5>💶 EUR/INR</h5>
                        <p><strong>Trend:</strong> <span class="positive">Bullish</span></p>
                        <p><strong>Target:</strong> 89.00-89.50</p>
                        <p><strong>Reason:</strong> ECB hawkish stance</p>
                    </div>
                    <div style="background: #fff3cd; padding: 15px; border-radius: 8px;">
                        <h5>💷 GBP/INR</h5>
                        <p><strong>Trend:</strong> <span style="color: #856404;">Sideways</span></p>
                        <p><strong>Range:</strong> 106-108</p>
                        <p><strong>Reason:</strong> BoE uncertainty</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with forex_timeframe4:
            st.markdown("### 🎯 Positional Forex Strategy")
            
            st.markdown("""
            <div class="report-section">
                <h4>💱 Long-term Forex Positions (1-3 months)</h4>
                
                <h5>🔴 SELL USD/INR - Strong Conviction</h5>
                <p><strong>Entry:</strong> 83.40-83.60 | <strong>Target:</strong> 82.20 | <strong>SL:</strong> 84.20</p>
                <p><strong>Reason:</strong> Saturn-Rahu conjunction weakens USD for 3 months</p>
                <p><strong>Time Frame:</strong> August-October 2025</p>
                
                <h5>🟢 BUY EUR/INR - Medium Conviction</h5>
                <p><strong>Entry:</strong> 87.80-88.20 | <strong>Target:</strong> 90.50 | <strong>SL:</strong> 87.00</p>
                <p><strong>Reason:</strong> Jupiter supports Euro strength till September</p>
                <p><strong>Time Frame:</strong> August-September 2025</p>
                
                <h5>⚡ AVOID GBP/INR - High Uncertainty</h5>
                <p><strong>Reason:</strong> Mars-Ketu conjunction creates extreme volatility</p>
                <p><strong>Strategy:</strong> Wait for October planetary shift</p>
                
                <h5>📊 Portfolio Allocation</h5>
                <p><strong>USD/INR Short:</strong> 50% | <strong>EUR/INR Long:</strong> 30% | <strong>Cash:</strong> 20%</p>
            </div>
            """, unsafe_allow_html=True)
    
    with global_tab:
        st.markdown("""
        <div class="market-type-header">
            <h3 style="margin: 0;">🌍 GLOBAL MARKETS - Today's Planetary Analysis</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Global Market Prices
        global_price_col1, global_price_col2, global_price_col3 = st.columns(3)
        
        with global_price_col1:
            data = st.session_state.market_data['DOWJONES']
            color_class = "positive" if data['change'] >= 0 else "negative"
            arrow = "▲" if data['change'] >= 0 else "▼"
            st.markdown(f"""
            <div class="market-card">
                <h4>DOW JONES</h4>
                <h2>{data['price']:,.0f}</h2>
                <p class="{color_class}">
                    {arrow} {abs(data['change']):.2f}%
                </p>
                <small>H: {data['high']:,.0f} | L: {data['low']:,.0f}</small>
            </div>
            """, unsafe_allow_html=True)
        
        with global_price_col2:
            data = st.session_state.market_data['NASDAQ']
            color_class = "positive" if data['change'] >= 0 else "negative"
            arrow = "▲" if data['change'] >= 0 else "▼"
            st.markdown(f"""
            <div class="market-card">
                <h4>NASDAQ</h4>
                <h2>{data['price']:,.0f}</h2>
                <p class="{color_class}">
                    {arrow} {abs(data['change']):.2f}%
                </p>
                <small>H: {data['high']:,.0f} | L: {data['low']:,.0f}</small>
            </div>
            """, unsafe_allow_html=True)
        
        with global_price_col3:
            data = st.session_state.market_data['BITCOIN']
            color_class = "positive" if data['change'] >= 0 else "negative"
            arrow = "▲" if data['change'] >= 0 else "▼"
            st.markdown(f"""
            <div class="market-card">
                <h4>BITCOIN</h4>
                <h2>${data['price']:,.0f}</h2>
                <p class="{color_class}">
                    {arrow} {abs(data['change']):.2f}%
                </p>
                <small>H: ${data['high']:,.0f} | L: ${data['low']:,.0f}</small>
            </div>
            """, unsafe_allow_html=True)
        
        # Global Markets Analysis
        global_timeframe1, global_timeframe2, global_timeframe3, global_timeframe4 = st.tabs(["⚡ INTRADAY", "📅 DAILY", "📊 WEEKLY", "🎯 POSITIONAL"])
        
        with global_timeframe1:
            st.markdown("### 🌍 Today's Global Markets Intraday")
            
            global_intra_col1, global_intra_col2 = st.columns(2)
            
            with global_intra_col1:
                st.markdown("""
                <div class="report-section">
                    <h4>🇺🇸 US MARKETS (IST 19:00-01:30)</h4>
                    <div class="trend-bullish">
                        <strong>19:00-21:00:</strong> Sun ☀️ | DOW JONES BUY | Target: +0.9%
                    </div>
                    <div class="trend-bullish">
                        <strong>21:00-23:00:</strong> Jupiter ♃ | Both indices BUY | Target: +1.2%
                    </div>
                    <div class="trend-volatile">
                        <strong>23:00-01:30:</strong> Venus ♀ | NASDAQ focus | Target: ±0.5%
                    </div>
                    <div class="trend-bearish">
                        <strong>01:30-03:00:</strong> Saturn ♄ | Profit booking | Target: -0.8%
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with global_intra_col2:
                st.markdown("""
                <div class="report-section">
                    <h4>₿ BITCOIN (24x7 Trading)</h4>
                    <div class="trend-volatile">
                        <strong>09:00-12:00:</strong> Rahu ☊ | High volatility | ±3.5%
                    </div>
                    <div class="trend-bullish">
                        <strong>14:00-18:00:</strong> Mercury ☿ | Tech buying | +2.8%
                    </div>
                    <div class="trend-bullish">
                        <strong>20:00-02:00:</strong> Jupiter ♃ | Strong rally | +4.2%
                    </div>
                    <div class="trend-bearish">
                        <strong>02:00-06:00:</strong> Saturn ♄ | Correction | -2.1%
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        with global_timeframe2:
            st.markdown("### 📅 Daily Global Markets Analysis")
            
            st.markdown("""
            <div class="report-section">
                <h4>🌍 Today's Global Markets Outlook</h4>
                
                <h5>🇺🇸 US MARKETS: <span class="positive">Bullish</span></h5>
                <p><strong>DOW JONES:</strong> Expected range 44,400-44,800 | Jupiter support in evening</p>
                <p><strong>NASDAQ:</strong> Tech sector strong | Target: 20,300-20,500</p>
                <p><strong>Best Trading Time:</strong> 21:00-23:00 IST (Jupiter hour)</p>
                
                <h5>₿ CRYPTO MARKETS: <span class="positive">Volatile Bullish</span></h5>
                <p><strong>BITCOIN:</strong> Range $95,000-$100,000 | Multiple planetary influences</p>
                <p><strong>Peak Time:</strong> 20:00-02:00 IST | <strong>Avoid:</strong> 02:00-06:00 IST</p>
                
                <h5>🌏 ASIAN MARKETS: <span style="color: #856404;">Mixed</span></h5>
                <p><strong>Nikkei/Hang Seng:</strong> Follow US lead with 1-day lag</p>
                <p><strong>Strategy:</strong> Wait for US direction, then follow</p>
            </div>
            """, unsafe_allow_html=True)
        
        with global_timeframe3:
            st.markdown("### 📊 Weekly Global Markets Forecast")
            
            st.markdown("""
            <div class="report-section">
                <h4>🌍 This Week's Global Trends</h4>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                    <div>
                        <h5>🇺🇸 US MARKETS</h5>
                        <p><strong>DOW JONES:</strong> <span class="positive">Bullish</span> - Infrastructure boost</p>
                        <p><strong>NASDAQ:</strong> <span class="positive">Tech Rally</span> - AI sector strength</p>
                        <p><strong>S&P 500:</strong> <span class="positive">Steady Rise</span> - Fed dovish</p>
                        <p><strong>Best Days:</strong> Thursday-Friday (Jupiter dominant)</p>
                    </div>
                    <div>
                        <h5>₿ CRYPTOCURRENCY</h5>
                        <p><strong>BITCOIN:</strong> <span class="positive">Strong Bullish</span> - $105K target</p>
                        <p><strong>ETHEREUM:</strong> <span class="positive">Bullish</span> - DeFi revival</p>
                        <p><strong>ALTCOINS:</strong> <span style="color: #856404;">Selective</span> - Pick leaders</p>
                        <p><strong>Risk:</strong> High volatility Wednesday (Mars)</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with global_timeframe4:
            st.markdown("### 🎯 Positional Global Strategy")
            
            st.markdown("""
            <div class="report-section">
                <h4>🌍 Long-term Global Positions (1-6 months)</h4>
                
                <h5>🟢 STRONG BUY - US TECH</h5>
                <p><strong>NASDAQ 100:</strong> Jupiter-Mercury conjunction supports tech boom</p>
                <p><strong>Entry:</strong> Current levels | <strong>Target:</strong> 22,500 | <strong>SL:</strong> 19,200</p>
                <p><strong>Time Frame:</strong> August-December 2025</p>
                
                <h5>🟢 BUY - CRYPTO MAJORS</h5>
                <p><strong>BITCOIN:</strong> Institutional adoption + planetary support</p>
                <p><strong>Entry:</strong> $95,000-$98,000 | <strong>Target:</strong> $120,000 | <strong>SL:</strong> $85,000</p>
                <p><strong>ETHEREUM:</strong> DeFi renaissance expected</p>
                <p><strong>Entry:</strong> Current levels | <strong>Target:</strong> $4,500 | <strong>SL:</strong> $3,000</p>
                
                <h5>⚠️ WATCH - TRADITIONAL MARKETS</h5>
                <p><strong>DOW JONES:</strong> Good for 3-6 months, then Saturn pressure</p>
                <p><strong>Strategy:</strong> Accumulate quality stocks, book profits by December</p>
                
                <h5>🔴 AVOID - EMERGING MARKETS</h5>
                <p><strong>Chinese Markets:</strong> Ketu influence creates uncertainty</p>
                <p><strong>Strategy:</strong> Wait for Q4 2025 for re-entry</p>
            </div>
            """, unsafe_allow_html=True)

with main_tab2:
    st.markdown(f"""
    <div class="section-header">
        <h2 style="margin: 0 0 10px 0;">🔮 TOMORROW'S COMPLETE PLANETARY TRANSIT FORECAST</h2>
        <h3 style="margin: 0; opacity: 0.9;">{tomorrow_day}, {tomorrow_date} • Detailed Predictions</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Tomorrow's Analysis - Same structure as today but with different data
    tomorrow_equity_tab, tomorrow_commodity_tab, tomorrow_forex_tab, tomorrow_global_tab = st.tabs(["📈 EQUITY FORECAST", "🏭 COMMODITIES FORECAST", "💱 FOREX FORECAST", "🌍 GLOBAL FORECAST"])
    
    with tomorrow_equity_tab:
        st.markdown("""
        <div class="market-type-header">
            <h3 style="margin: 0;">📈 TOMORROW'S EQUITY MARKETS FORECAST</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 🌟 Tomorrow's Key Planetary Events")
        
        tomorrow_events = [
            {'time': '09:15-10:15', 'planet': 'Moon 🌙', 'effect': 'Positive', 'impact': 'FMCG, Consumer goods strong opening'},
            {'time': '10:15-11:15', 'planet': 'Mars ♂️', 'effect': 'Volatile', 'impact': 'Energy up, Defense strong, IT weak'},
            {'time': '11:15-12:15', 'planet': 'Mercury ☿', 'effect': 'Negative', 'impact': 'IT, Telecom under pressure'},
            {'time': '12:15-13:15', 'planet': 'Jupiter ♃', 'effect': 'Positive', 'impact': 'Banking, Finance, Gold peak bullish'},
            {'time': '13:15-14:15', 'planet': 'Venus ♀', 'effect': 'Positive', 'impact': 'Auto, Luxury, Entertainment up'},
            {'time': '14:15-15:15', 'planet': 'Saturn ♄', 'effect': 'Negative', 'impact': 'All sectors weak, profit booking'},
            {'time': '15:15-15:30', 'planet': 'Sun ☀️', 'effect': 'Positive', 'impact': 'Power, Energy, Pharma recovery'}
        ]
        
        for event in tomorrow_events:
            if event['effect'] == 'Positive':
                bg_color = '#d4edda'
                text_color = '#155724'
                icon = '🟢'
            elif event['effect'] == 'Negative':
                bg_color = '#f8d7da'
                text_color = '#721c24'
                icon = '🔴'
            else:
                bg_color = '#fff3cd'
                text_color = '#856404'
                icon = '⚡'
            
            st.markdown(f"""
            <div style="background: {bg_color}; color: {text_color}; padding: 12px; border-radius: 8px; margin: 8px 0; border-left: 4px solid {text_color};">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h5 style="margin: 0; color: {text_color};">{icon} {event['time']} - {event['planet']}</h5>
                    <span style="background: {text_color}; color: white; padding: 3px 8px; border-radius: 12px; font-weight: bold; font-size: 0.8em;">{event['effect'].upper()}</span>
                </div>
                <p style="margin: 5px 0 0 0; color: {text_color}; font-weight: 500;">{event['impact']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Tomorrow's Best Opportunities
        st.markdown("### 🎯 Tomorrow's Top Trading Opportunities")
        
        tomorrow_opp_col1, tomorrow_opp_col2, tomorrow_opp_col3 = st.columns(3)
        
        with tomorrow_opp_col1:
            st.markdown("""
            <div style="background: #d4edda; color: #155724; padding: 15px; border-radius: 10px; border: 2px solid #28a745;">
                <h4 style="margin: 0 0 10px 0; color: #155724;">🌟 Best Long Opportunity</h4>
                <p style="margin: 0; color: #155724;"><strong>12:15-13:15 (Jupiter ♃)</strong></p>
                <p style="margin: 5px 0; color: #155724; font-weight: bold;">STRONG BUY Banking Stocks</p>
                <p style="margin: 0; color: #155724;">Expected: BANKNIFTY +2.1%</p>
                <p style="margin: 5px 0 0 0; color: #155724; font-size: 0.9em;">Target: HDFC Bank, ICICI Bank, SBI</p>
            </div>
            """, unsafe_allow_html=True)
        
        with tomorrow_opp_col2:
            st.markdown("""
            <div style="background: #f8d7da; color: #721c24; padding: 15px; border-radius: 10px; border: 2px solid #dc3545;">
                <h4 style="margin: 0 0 10px 0; color: #721c24;">⚠️ Biggest Risk</h4>
                <p style="margin: 0; color: #721c24;"><strong>11:15-12:15 (Mercury ☿)</strong></p>
                <p style="margin: 5px 0; color: #721c24; font-weight: bold;">SHORT IT Stocks</p>
                <p style="margin: 0; color: #721c24;">Expected: IT Index -1.5%</p>
                <p style="margin: 5px 0 0 0; color: #721c24; font-size: 0.9em;">Target: TCS, Infosys, Wipro</p>
            </div>
            """, unsafe_allow_html=True)
        
        with tomorrow_opp_col3:
            st.markdown("""
            <div style="background: #fff3cd; color: #856404; padding: 15px; border-radius: 10px; border: 2px solid #ffc107;">
                <h4 style="margin: 0 0 10px 0; color: #856404;">⚡ High Volatility</h4>
                <p style="margin: 0; color: #856404;"><strong>10:15-11:15 (Mars ♂️)</strong></p>
                <p style="margin: 5px 0; color: #856404; font-weight: bold;">Energy Stocks Swing</p>
                <p style="margin: 0; color: #856404;">Expected: ±1.8% moves</p>
                <p style="margin: 5px 0 0 0; color: #856404; font-size: 0.9em;">Use tight stops, scalping only</p>
            </div>
            """, unsafe_allow_html=True)
    
    with tomorrow_commodity_tab:
        st.markdown("""
        <div class="market-type-header">
            <h3 style="margin: 0;">🏭 TOMORROW'S COMMODITIES FORECAST</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 🥇 Tomorrow's Commodity Highlights")
        
        st.markdown("""
        <div class="report-section">
            <h4>⭐ PEAK OPPORTUNITY: 18:00-21:00 (Jupiter ♃)</h4>
            <div style="background: #d4edda; padding: 15px; border-radius: 8px; margin: 10px 0;">
                <p><strong>🥇 GOLD:</strong> <span style="background: #28a745; color: white; padding: 3px 8px; border-radius: 4px; font-weight: bold;">STRONG BUY +2.2%</span></p>
                <p><strong>🥈 SILVER:</strong> <span style="background: #28a745; color: white; padding: 3px 8px; border-radius: 4px; font-weight: bold;">STRONG BUY +3.5%</span></p>
                <p><strong>₿ BITCOIN:</strong> <span style="background: #28a745; color: white; padding: 3px 8px; border-radius: 4px; font-weight: bold;">STRONG BUY +5.2%</span></p>
                <p style="margin: 10px 0 0 0; font-weight: bold; color: #155724;">🌟 This is the best commodity trading window of the week!</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        tomorrow_comm_col1, tomorrow_comm_col2 = st.columns(2)
        
        with tomorrow_comm_col1:
            st.markdown("""
            <div class="report-section">
                <h4>🟢 Tomorrow's Bullish Commodities</h4>
                <p><strong>09:00-12:00 (Moon 🌙):</strong></p>
                <ul>
                    <li>GOLD: Safe haven demand +1.2%</li>
                    <li>SILVER: Industrial + safe haven +2.5%</li>
                </ul>
                <p><strong>15:00-18:00 (Venus ♀):</strong></p>
                <ul>
                    <li>All commodities harmonized</li>
                    <li>GOLD +1.0%, SILVER +2.8%</li>
                    <li>CRUDE recovers +1.5%</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with tomorrow_comm_col2:
            st.markdown("""
            <div class="report-section">
                <h4>🔴 Tomorrow's Weak Periods</h4>
                <p><strong>06:00-09:00 (Saturn ♄):</strong></p>
                <ul>
                    <li>SILVER weak -0.8%</li>
                    <li>BITCOIN decline -3.2%</li>
                </ul>
                <p><strong>21:00-00:00 (Mars ♂️):</strong></p>
                <ul>
                    <li>CRUDE selling pressure -2.1%</li>
                    <li>High volatility all commodities</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    with tomorrow_forex_tab:
        st.markdown("""
        <div class="market-type-header">
            <h3 style="margin: 0;">💱 TOMORROW'S FOREX FORECAST</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="report-section">
            <h4>💱 Tomorrow's Forex Key Levels & Strategies</h4>
            
            <h5>💵 USD/INR: <span class="negative">Continued Weakness</span></h5>
            <p><strong>Expected Range:</strong> 83.15 - 83.45</p>
            <p><strong>Strategy:</strong> Sell on any rally above 83.35</p>
            <p><strong>Best Selling Time:</strong> 12:15-13:15 (Jupiter strengthens INR)</p>
            
            <h5>💶 EUR/INR: <span class="positive">Morning Strength</span></h5>
            <p><strong>Expected Range:</strong> 88.10 - 88.80</p>
            <p><strong>Strategy:</strong> Buy on dips below 88.20</p>
            <p><strong>Best Buying Time:</strong> 09:15-10:15 (Moon supports Euro)</p>
            
            <h5>💷 GBP/INR: <span style="color: #856404;">Extreme Volatility</span></h5>
            <p><strong>Expected Range:</strong> 106.00 - 108.00</p>
            <p><strong>Strategy:</strong> Avoid or use very tight stops</p>
            <p><strong>Risk Period:</strong> 10:15-11:15 (Mars creates chaos)</p>
        </div>
        """, unsafe_allow_html=True)
    
    with tomorrow_global_tab:
        st.markdown("""
        <div class="market-type-header">
            <h3 style="margin: 0;">🌍 TOMORROW'S GLOBAL MARKETS FORECAST</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="report-section">
            <h4>🌍 Tomorrow's Global Markets Outlook</h4>
            
            <h5>🇺🇸 US MARKETS: <span class="positive">Strong Evening Rally Expected</span></h5>
            <p><strong>DOW JONES:</strong> Jupiter hour (21:00-23:00 IST) brings +1.5% rally</p>
            <p><strong>NASDAQ:</strong> Tech strength continues, target +2.0%</p>
            <p><strong>Opening:</strong> Flat to slightly positive</p>
            
            <h5>₿ CRYPTOCURRENCY: <span class="positive">Exceptional Day</span></h5>
            <p><strong>BITCOIN:</strong> Jupiter peak (18:00-21:00) could trigger +5%+ move</p>
            <p><strong>Strategy:</strong> Accumulate during Asian hours, hold through Jupiter peak</p>
            <p><strong>Target:</strong> $103,000 - $105,000</p>
            
            <h5>🌏 ASIAN MARKETS: <span style="color: #856404;">Follow US Lead</span></h5>
            <p><strong>Strategy:</strong> Wait for US direction, then trade Asian ETFs</p>
            <p><strong>Nikkei:</strong> Expected to follow US tech rally</p>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.write("---")
footer_col1, footer_col2, footer_col3, footer_col4 = st.columns(4)

with footer_col1:
    st.caption(f"🕐 Last Updated: {st.session_state.last_update.strftime('%H:%M:%S')}")

with footer_col2:
    st.caption(f"{current_symbol} Current Planet: {current_planet}")

with footer_col3:
    st.caption(f"📅 Analysis Date: {current_date_str}")

with footer_col4:
    st.caption("🕉️ Vedic Market Intelligence - Complete Analysis")

# Auto-refresh
if auto_refresh:
    time.sleep(refresh_rate)
    update_market_data()
    st.rerun()
