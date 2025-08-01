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
            'NASDAQ': {'price': 20173, 'change': 1.25, 'high': 20350, 'low': 19850},
            
            # Forex
            'USDINR': {'price': 83.45, 'change': -0.14, 'high': 83.58, 'low': 83.42},
            'EURINR': {'price': 88.25, 'change': 0.35, 'high': 88.50, 'low': 87.90},
            'GBPINR': {'price': 106.75, 'change': 0.28, 'high': 107.20, 'low': 106.50}
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

def create_intraday_signals(market_name):
    """Generate intraday hourly signals for any market"""
    base_signals = [
        {'time': '09:15-10:00', 'planet': 'Venus ♀', 'signal': 'BUY', 'target': '+0.8%', 'sl': '-0.3%', 'trend': 'Bullish'},
        {'time': '10:00-11:00', 'planet': 'Sun ☀️', 'signal': 'HOLD', 'target': '+0.5%', 'sl': '-0.2%', 'trend': 'Neutral'},
        {'time': '11:00-12:00', 'planet': 'Mercury ☿', 'signal': 'BUY', 'target': '+1.2%', 'sl': '-0.4%', 'trend': 'Bullish'},
        {'time': '12:00-13:00', 'planet': 'Saturn ♄', 'signal': 'SELL', 'target': '-0.9%', 'sl': '+0.3%', 'trend': 'Bearish'},
        {'time': '13:00-14:00', 'planet': 'Mars ♂️', 'signal': 'CAUTION', 'target': '±1.5%', 'sl': '±0.5%', 'trend': 'Volatile'},
        {'time': '14:00-15:00', 'planet': 'Rahu ☊', 'signal': 'SELL', 'target': '-1.1%', 'sl': '+0.4%', 'trend': 'Bearish'},
        {'time': '15:00-15:30', 'planet': 'Jupiter ♃', 'signal': 'BUY', 'target': '+0.6%', 'sl': '-0.2%', 'trend': 'Bullish'}
    ]
    
    # Customize signals based on market type
    if 'BANK' in market_name.upper():
        for signal in base_signals:
            if signal['planet'] == 'Jupiter ♃':
                signal['target'] = '+1.5%'
                signal['trend'] = 'Strong Bullish'
    elif 'IT' in market_name.upper():
        for signal in base_signals:
            if signal['planet'] == 'Mercury ☿':
                signal['target'] = '-0.8%'
                signal['trend'] = 'Bearish'
    
    return base_signals

def generate_weekly_calendar(market_name):
    """Generate weekly planetary calendar"""
    today = datetime.now()
    week_start = today - timedelta(days=today.weekday())
    
    weekly_data = []
    planets = ['Sun ☀️', 'Moon 🌙', 'Mars ♂️', 'Mercury ☿', 'Jupiter ♃', 'Venus ♀', 'Saturn ♄']
    trends = ['Bullish', 'Volatile', 'Bearish', 'Neutral', 'Bullish', 'Bullish', 'Bearish']
    
    for i in range(7):
        current_date = week_start + timedelta(days=i)
        weekly_data.append({
            'date': current_date.strftime('%Y-%m-%d'),
            'day': current_date.strftime('%A'),
            'short_day': current_date.strftime('%a'),
            'day_num': current_date.strftime('%d'),
            'month': current_date.strftime('%m'),
            'planet': planets[i],
            'trend': trends[i],
            'target': f"{'+' if trends[i] == 'Bullish' else '-' if trends[i] == 'Bearish' else '±'}{random.uniform(0.5, 2.5):.1f}%",
            'is_today': current_date.date() == today.date()
        })
    
    return weekly_data

def generate_monthly_calendar(market_name):
    """Generate monthly planetary calendar"""
    today = datetime.now()
    month_start = today.replace(day=1)
    
    if month_start.month == 12:
        next_month = month_start.replace(year=month_start.year + 1, month=1)
    else:
        next_month = month_start.replace(month=month_start.month + 1)
    month_end = next_month - timedelta(days=1)
    
    monthly_data = []
    planets = ['Sun ☀️', 'Moon 🌙', 'Mars ♂️', 'Mercury ☿', 'Jupiter ♃', 'Venus ♀', 'Saturn ♄', 'Rahu ☊', 'Ketu ☋']
    trends = ['Bullish', 'Volatile', 'Bearish', 'Neutral', 'Bullish', 'Bullish', 'Bearish', 'Volatile', 'Bearish']
    
    current_date = month_start
    while current_date <= month_end:
        planet_idx = (current_date.day - 1) % len(planets)
        trend_idx = (current_date.day - 1) % len(trends)
        
        monthly_data.append({
            'date': current_date.strftime('%Y-%m-%d'),
            'day': current_date.strftime('%a'),
            'day_num': current_date.strftime('%d'),
            'month': current_date.strftime('%m'),
            'planet': planets[planet_idx],
            'trend': trends[trend_idx],
            'target': f"{'+' if trends[trend_idx] == 'Bullish' else '-' if trends[trend_idx] == 'Bearish' else '±'}{random.uniform(0.3, 1.8):.1f}%",
            'is_today': current_date.date() == today.date()
        })
        current_date += timedelta(days=1)
    
    return monthly_data

def display_calendar_grid(calendar_data, columns=7):
    """Display calendar data in a grid format"""
    for i in range(0, len(calendar_data), columns):
        week_data = calendar_data[i:i+columns]
        cols = st.columns(columns)
        
        for idx, day_data in enumerate(week_data):
            if idx < len(cols):
                css_class = f"calendar-{day_data['trend'].lower()}"
                border_style = "border: 3px solid #ff6b35;" if day_data.get('is_today', False) else ""
                
                with cols[idx]:
                    st.markdown(f"""
                    <div class="{css_class} calendar-day" style="{border_style}">
                        <h6 style="margin: 0 0 5px 0; font-weight: bold;">{day_data['day'] if 'day' in day_data else day_data['short_day']}</h6>
                        <p style="margin: 0; font-size: 0.9em; font-weight: bold;">{day_data['day_num']}/{day_data['month']}</p>
                        <p style="margin: 8px 0; font-size: 0.85em; font-weight: bold;">{day_data['planet']}</p>
                        <p style="margin: 0; font-size: 0.9em; font-weight: bold;">{day_data['trend']}</p>
                        <p style="margin: 3px 0 0 0; font-size: 0.85em; font-weight: bold;">{day_data['target']}</p>
                        {'<p style="margin: 3px 0 0 0; font-size: 0.7em; color: #ff6b35; font-weight: bold;">TODAY</p>' if day_data.get('is_today', False) else ''}
                    </div>
                    """, unsafe_allow_html=True)

def create_timeframe_tabs(market_name, market_type=""):
    """Create consistent timeframe tabs for any market"""
    tab1, tab2, tab3 = st.tabs(["⚡ INTRADAY", "📊 WEEKLY", "📅 MONTHLY"])
    
    with tab1:
        st.markdown(f'<div class="timeframe-header"><h4>⚡ {market_name} - Today\'s Intraday Signals</h4></div>', unsafe_allow_html=True)
        
        signals = create_intraday_signals(market_name)
        current_hour = datetime.now().hour
        
        # Split signals into morning and afternoon
        morning_signals = signals[:4]
        afternoon_signals = signals[4:]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🌅 Morning Session (9:15 AM - 1:00 PM)")
            for signal in morning_signals:
                is_active = current_hour >= int(signal['time'].split('-')[0].split(':')[0]) and current_hour < int(signal['time'].split('-')[1].split(':')[0])
                
                if signal['trend'] == 'Bullish':
                    css_class = 'live-signal' if is_active else 'trend-bullish'
                elif signal['trend'] == 'Bearish':
                    css_class = 'warning-signal' if is_active else 'trend-bearish'
                else:
                    css_class = 'trend-volatile'
                
                active_text = " 🔥 LIVE NOW" if is_active else ""
                
                st.markdown(f"""
                <div class="{css_class}">
                    <strong>{signal['time']}{active_text}</strong><br>
                    Planet: {signal['planet']} | Signal: <strong>{signal['signal']}</strong><br>
                    Target: {signal['target']} | SL: {signal['sl']}
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("#### 🌇 Afternoon Session (1:00 PM - 3:30 PM)")
            for signal in afternoon_signals:
                is_active = current_hour >= int(signal['time'].split('-')[0].split(':')[0]) and current_hour < int(signal['time'].split('-')[1].split(':')[0])
                
                if signal['trend'] == 'Bullish':
                    css_class = 'live-signal' if is_active else 'trend-bullish'
                elif signal['trend'] == 'Bearish':
                    css_class = 'warning-signal' if is_active else 'trend-bearish'
                else:
                    css_class = 'trend-volatile'
                
                active_text = " 🔥 LIVE NOW" if is_active else ""
                
                st.markdown(f"""
                <div class="{css_class}">
                    <strong>{signal['time']}{active_text}</strong><br>
                    Planet: {signal['planet']} | Signal: <strong>{signal['signal']}</strong><br>
                    Target: {signal['target']} | SL: {signal['sl']}
                </div>
                """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown(f'<div class="timeframe-header"><h4>📊 {market_name} - This Week\'s Calendar</h4></div>', unsafe_allow_html=True)
        
        weekly_data = generate_weekly_calendar(market_name)
        display_calendar_grid(weekly_data, 7)
        
        # Weekly Summary
        st.markdown("### 📈 Weekly Trading Summary")
        summary_col1, summary_col2 = st.columns(2)
        
        bullish_days = [day for day in weekly_data if day['trend'] == 'Bullish']
        bearish_days = [day for day in weekly_data if day['trend'] == 'Bearish']
        
        with summary_col1:
            st.markdown("""
            <div class="report-section" style="background: #d4edda; border-left: 5px solid #28a745;">
                <h4 style="color: #155724;">🟢 Long Opportunities</h4>
            """, unsafe_allow_html=True)
            
            for day in bullish_days:
                st.markdown(f"**{day['day']}:** {day['planet']} - Target {day['target']}")
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        with summary_col2:
            st.markdown("""
            <div class="report-section" style="background: #f8d7da; border-left: 5px solid #dc3545;">
                <h4 style="color: #721c24;">🔴 Short Opportunities</h4>
            """, unsafe_allow_html=True)
            
            for day in bearish_days:
                st.markdown(f"**{day['day']}:** {day['planet']} - Target {day['target']}")
            
            st.markdown("</div>", unsafe_allow_html=True)
    
    with tab3:
        st.markdown(f'<div class="timeframe-header"><h4>📅 {market_name} - Monthly Calendar</h4></div>', unsafe_allow_html=True)
        
        monthly_data = generate_monthly_calendar(market_name)
        
        # Display monthly calendar in weeks
        st.markdown("#### 📆 Complete Monthly Timeline")
        
        # Group data by weeks
        weeks = []
        current_week = []
        
        for day_data in monthly_data:
            current_week.append(day_data)
            if len(current_week) == 7:
                weeks.append(current_week)
                current_week = []
        
        if current_week:
            weeks.append(current_week)
        
        # Display first 4 weeks
        for week_idx, week in enumerate(weeks[:4]):
            st.markdown(f"**Week {week_idx + 1}**")
            display_calendar_grid(week, 7)
        
        # Monthly summary
        st.markdown("### 📊 Monthly Strategy Summary")
        
        bullish_count = sum(1 for day in monthly_data if day['trend'] == 'Bullish')
        bearish_count = sum(1 for day in monthly_data if day['trend'] == 'Bearish')
        volatile_count = sum(1 for day in monthly_data if day['trend'] == 'Volatile')
        
        month_col1, month_col2, month_col3 = st.columns(3)
        
        with month_col1:
            st.markdown(f"""
            <div class="report-section" style="background: #d4edda;">
                <h4 style="color: #155724;">🟢 Bullish Days: {bullish_count}</h4>
                <p>Best for long positions and accumulation</p>
            </div>
            """, unsafe_allow_html=True)
        
        with month_col2:
            st.markdown(f"""
            <div class="report-section" style="background: #f8d7da;">
                <h4 style="color: #721c24;">🔴 Bearish Days: {bearish_count}</h4>
                <p>Ideal for profit booking and shorts</p>
            </div>
            """, unsafe_allow_html=True)
        
        with month_col3:
            st.markdown(f"""
            <div class="report-section" style="background: #fff3cd;">
                <h4 style="color: #856404;">⚡ Volatile Days: {volatile_count}</h4>
                <p>High-risk intraday trading only</p>
            </div>
            """, unsafe_allow_html=True)

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
    <p style="margin: 0; font-size: 1.1em;">Live Astrological Market Timing for Equity • Commodity • Forex • Global • Sectorwise Analysis</p>
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
    
    # All Market Types - Including NEW SECTORWISE and PLANETARY TRANSIT
    equity_tab, commodity_tab, forex_tab, global_tab, sectorwise_tab, planetary_tab = st.tabs([
        "📈 EQUITY", 
        "🏭 COMMODITIES", 
        "💱 FOREX", 
        "🌍 GLOBAL", 
        "🏢 SECTORWISE",
        "🪐 PLANETARY TRANSIT"
    ])
    
    with equity_tab:
        st.markdown('<div class="sector-header"><h3 style="margin: 0;">📈 EQUITY MARKETS - Complete Analysis</h3></div>', unsafe_allow_html=True)
        create_timeframe_tabs("EQUITY MARKETS", "equity")
    
    with commodity_tab:
        st.markdown('<div class="sector-header"><h3 style="margin: 0;">🏭 COMMODITIES - Complete Analysis</h3></div>', unsafe_allow_html=True)
        create_timeframe_tabs("COMMODITIES", "commodity")
    
    with forex_tab:
        st.markdown('<div class="sector-header"><h3 style="margin: 0;">💱 FOREX - Complete Analysis</h3></div>', unsafe_allow_html=True)
        create_timeframe_tabs("FOREX MARKETS", "forex")
    
    with global_tab:
        st.markdown('<div class="sector-header"><h3 style="margin: 0;">🌍 GLOBAL MARKETS - Complete Analysis</h3></div>', unsafe_allow_html=True)
        create_timeframe_tabs("GLOBAL MARKETS", "global")
    
    with sectorwise_tab:
        st.markdown('<div class="sector-header"><h3 style="margin: 0;">🏢 SECTORWISE ANALYSIS - All Indian Sectors</h3></div>', unsafe_allow_html=True)
        
        # Sector Selection Interface
        sector_col1, sector_col2, sector_col3 = st.columns([3, 3, 2])
        
        with sector_col1:
            selected_sector = st.selectbox(
                "🎯 Select Indian Sector:",
                list(st.session_state.sector_data.keys()),
                help="Choose any Indian sector for detailed planetary analysis"
            )
        
        with sector_col2:
            custom_symbol = st.text_input(
                "📊 Or Enter Custom Symbol:",
                placeholder="e.g., RELIANCE, TATAMOTORS, ADANIGREEN",
                help="Enter any stock symbol for personalized analysis"
            )
        
        with sector_col3:
            st.markdown("**Currently Analyzing:**")
            analysis_target = custom_symbol.upper() if custom_symbol else selected_sector
            st.markdown(f"<h4 style='color: #007bff;'>{analysis_target}</h4>", unsafe_allow_html=True)
        
        # Display Sector Price (if available)
        if not custom_symbol and selected_sector in st.session_state.sector_data:
            sector_info = st.session_state.sector_data[selected_sector]
            index_key = sector_info['index_key']
            
            if index_key in st.session_state.market_data:
                data = st.session_state.market_data[index_key]
                color_class = "positive" if data['change'] >= 0 else "negative"
                arrow = "▲" if data['change'] >= 0 else "▼"
                
                st.markdown(f"""
                <div class="sector-price-card">
                    <h2 style="margin: 0 0 10px 0; color: #333;">{selected_sector} INDEX</h2>
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <h1 style="margin: 0; color: #007bff;">{data['price']:,.2f}</h1>
                            <h3 class="{color_class}" style="margin: 5px 0;">
                                {arrow} {abs(data['change']):.2f}%
                            </h3>
                        </div>
                        <div style="text-align: right;">
                            <p style="margin: 0; font-size: 1.1em;"><strong>High:</strong> {data['high']:,.2f}</p>
                            <p style="margin: 0; font-size: 1.1em;"><strong>Low:</strong> {data['low']:,.2f}</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Sector/Symbol Analysis with Timeframes
        st.markdown(f"### 📊 {analysis_target} - Complete Planetary Analysis")
        
        sector_tab1, sector_tab2, sector_tab3 = st.tabs(["⚡ INTRADAY", "📊 WEEKLY", "📅 MONTHLY"])
        
        with sector_tab1:
            st.markdown(f'<div class="timeframe-header"><h4>⚡ {analysis_target} - Today\'s Intraday Planetary Signals</h4></div>', unsafe_allow_html=True)
            
            # Generate sector-specific signals
            signals = create_intraday_signals(analysis_target)
            
            # Morning and Afternoon sessions
            morning_col, afternoon_col = st.columns(2)
            
            with morning_col:
                st.markdown("#### 🌅 Morning Session (9:15 AM - 1:00 PM)")
                for signal in signals[:4]:
                    is_active = current_hour >= int(signal['time'].split('-')[0].split(':')[0]) and current_hour < int(signal['time'].split('-')[1].split(':')[0])
                    
                    if signal['trend'] == 'Bullish':
                        css_class = 'live-signal' if is_active else 'trend-bullish'
                    elif signal['trend'] == 'Bearish':
                        css_class = 'warning-signal' if is_active else 'trend-bearish'
                    else:
                        css_class = 'trend-volatile'
                    
                    active_text = " 🔥 LIVE NOW" if is_active else ""
                    
                    st.markdown(f"""
                    <div class="{css_class}">
                        <strong>{signal['time']}{active_text}</strong><br>
                        Planet: {signal['planet']} | Signal: <strong>{signal['signal']}</strong><br>
                        Target: {signal['target']} | SL: {signal['sl']}
                    </div>
                    """, unsafe_allow_html=True)
            
            with afternoon_col:
                st.markdown("#### 🌇 Afternoon Session (1:00 PM - 3:30 PM)")
                for signal in signals[4:]:
                    is_active = current_hour >= int(signal['time'].split('-')[0].split(':')[0]) and current_hour < int(signal['time'].split('-')[1].split(':')[0])
                    
                    if signal['trend'] == 'Bullish':
                        css_class = 'live-signal' if is_active else 'trend-bullish'
                    elif signal['trend'] == 'Bearish':
                        css_class = 'warning-signal' if is_active else 'trend-bearish'
                    else:
                        css_class = 'trend-volatile'
                    
                    active_text = " 🔥 LIVE NOW" if is_active else ""
                    
                    st.markdown(f"""
                    <div class="{css_class}">
                        <strong>{signal['time']}{active_text}</strong><br>
                        Planet: {signal['planet']} | Signal: <strong>{signal['signal']}</strong><br>
                        Target: {signal['target']} | SL: {signal['sl']}
                    </div>
                    """, unsafe_allow_html=True)
            
            # Show individual stocks for selected sector (not custom symbol)
            if not custom_symbol and selected_sector in st.session_state.sector_data:
                st.markdown(f"### 📈 Top Stocks in {selected_sector} Sector")
                
                stocks = st.session_state.sector_data[selected_sector]['stocks']
                
                # Create stock grid
                stock_cols = st.columns(5)
                
                for idx, stock in enumerate(stocks):
                    col_idx = idx % 5
                    
                    # Generate random data for demonstration
                    stock_price = random.uniform(100, 3000)
                    stock_change = random.uniform(-4, 4)
                    
                    color_class = "positive" if stock_change >= 0 else "negative"
                    arrow = "▲" if stock_change >= 0 else "▼"
                    
                    with stock_cols[col_idx]:
                        st.markdown(f"""
                        <div class="stock-card">
                            <h6 style="margin: 0 0 8px 0; font-weight: bold; color: #333;">{stock}</h6>
                            <h4 style="margin: 0; color: #007bff;">₹{stock_price:.1f}</h4>
                            <p class="{color_class}" style="margin: 5px 0 0 0; font-weight: bold;">
                                {arrow} {abs(stock_change):.2f}%
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
        
        with sector_tab2:
            st.markdown(f'<div class="timeframe-header"><h4>📊 {analysis_target} - Weekly Planetary Calendar</h4></div>', unsafe_allow_html=True)
            
            weekly_data = generate_weekly_calendar(analysis_target)
            display_calendar_grid(weekly_data, 7)
            
            # Weekly Long/Short Analysis
            st.markdown("### 🎯 Weekly Trading Opportunities")
            
            weekly_opp_col1, weekly_opp_col2 = st.columns(2)
            
            bullish_days = [day for day in weekly_data if day['trend'] == 'Bullish']
            bearish_days = [day for day in weekly_data if day['trend'] == 'Bearish']
            
            with weekly_opp_col1:
                st.markdown("""
                <div class="report-section" style="background: #d4edda; border-left: 5px solid #28a745;">
                    <h4 style="color: #155724;">🟢 LONG Opportunities This Week</h4>
                """, unsafe_allow_html=True)
                
                for day in bullish_days:
                    st.markdown(f"**{day['day']}:** {day['planet']} | Target: {day['target']}")
                
                st.markdown("<p><strong>Strategy:</strong> Accumulate on dips during bullish days</p></div>", unsafe_allow_html=True)
            
            with weekly_opp_col2:
                st.markdown("""
                <div class="report-section" style="background: #f8d7da; border-left: 5px solid #dc3545;">
                    <h4 style="color: #721c24;">🔴 SHORT Opportunities This Week</h4>
                """, unsafe_allow_html=True)
                
                for day in bearish_days:
                    st.markdown(f"**{day['day']}:** {day['planet']} | Target: {day['target']}")
                
                st.markdown("<p><strong>Strategy:</strong> Short on rallies during bearish days</p></div>", unsafe_allow_html=True)
            
            # Individual Stock Weekly Performance (for sectors)
            if not custom_symbol and selected_sector in st.session_state.sector_data:
                st.markdown(f"### 📊 {selected_sector} Stocks - Weekly Outlook")
                
                stocks = st.session_state.sector_data[selected_sector]['stocks'][:8]  # Top 8 stocks
                perf_cols = st.columns(4)
                
                for idx, stock in enumerate(stocks):
                    col_idx = idx % 4
                    
                    # Generate weekly performance
                    weekly_outlook = random.choice(['Strong Buy', 'Buy', 'Hold', 'Sell'])
                    weekly_target = random.uniform(-10, 15)
                    
                    if weekly_outlook == 'Strong Buy':
                        css_class = 'performance-strong-buy'
                    elif weekly_outlook == 'Buy':
                        css_class = 'performance-buy'
                    elif weekly_outlook == 'Sell':
                        css_class = 'performance-sell'
                    else:
                        css_class = 'performance-hold'
                    
                    with perf_cols[col_idx]:
                        st.markdown(f"""
                        <div class="{css_class} performance-card">
                            <h6 style="margin: 0 0 5px 0; font-weight: bold;">{stock}</h6>
                            <p style="margin: 0; font-size: 0.9em;"><strong>{weekly_outlook}</strong></p>
                            <p style="margin: 0; font-size: 0.9em;">Target: {weekly_target:+.1f}%</p>
                        </div>
                        """, unsafe_allow_html=True)
        
        with sector_tab3:
            st.markdown(f'<div class="timeframe-header"><h4>📅 {analysis_target} - Monthly Planetary Calendar</h4></div>', unsafe_allow_html=True)
            
            monthly_data = generate_monthly_calendar(analysis_target)
            
            # Monthly calendar display
            st.markdown("#### 📆 Complete Monthly Timeline")
            
            # Group by weeks
            weeks = []
            current_week = []
            
            for day_data in monthly_data:
                current_week.append(day_data)
                if len(current_week) == 7:
                    weeks.append(current_week)
                    current_week = []
            
            if current_week:
                weeks.append(current_week)
            
            # Display weeks
            for week_idx, week in enumerate(weeks[:4]):  # First 4 weeks
                st.markdown(f"**Week {week_idx + 1}**")
                display_calendar_grid(week, 7)
            
            # Monthly Performance Summary
            st.markdown(f"### 📈 {analysis_target} - Monthly Performance Forecast")
            
            bullish_count = sum(1 for day in monthly_data if day['trend'] == 'Bullish')
            bearish_count = sum(1 for day in monthly_data if day['trend'] == 'Bearish')
            volatile_count = sum(1 for day in monthly_data if day['trend'] == 'Volatile')
            neutral_count = sum(1 for day in monthly_data if day['trend'] == 'Neutral')
            
            monthly_summary_col1, monthly_summary_col2, monthly_summary_col3 = st.columns(3)
            
            with monthly_summary_col1:
                st.markdown(f"""
                <div class="report-section" style="background: #d4edda; border-left: 5px solid #28a745;">
                    <h4 style="color: #155724;">🟢 Bullish Period</h4>
                    <h2 style="color: #155724;">{bullish_count} Days</h2>
                    <p>Best for accumulation and long-term positions</p>
                    <p><strong>Strategy:</strong> Buy on dips, hold positions</p>
                </div>
                """, unsafe_allow_html=True)
            
            with monthly_summary_col2:
                st.markdown(f"""
                <div class="report-section" style="background: #f8d7da; border-left: 5px solid #dc3545;">
                    <h4 style="color: #721c24;">🔴 Bearish Period</h4>
                    <h2 style="color: #721c24;">{bearish_count} Days</h2>
                    <p>Ideal for profit booking and shorts</p>
                    <p><strong>Strategy:</strong> Book profits, consider shorts</p>
                </div>
                """, unsafe_allow_html=True)
            
            with monthly_summary_col3:
                st.markdown(f"""
                <div class="report-section" style="background: #fff3cd; border-left: 5px solid #ffc107;">
                    <h4 style="color: #856404;">⚡ Volatile Period</h4>
                    <h2 style="color: #856404;">{volatile_count} Days</h2>
                    <p>High-risk intraday trading only</p>
                    <p><strong>Strategy:</strong> Use tight stops, scalp trades</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Detailed Stock Monthly Performance (for sectors)
            if not custom_symbol and selected_sector in st.session_state.sector_data:
                st.markdown(f"### 📊 {selected_sector} Stocks - Monthly Performance Forecast")
                
                stocks = st.session_state.sector_data[selected_sector]['stocks']
                
                # Create detailed performance table
                st.markdown("#### Individual Stock Monthly Outlook")
                
                stock_perf_cols = st.columns(2)
                
                for idx, stock in enumerate(stocks):
                    col_idx = idx % 2
                    
                    # Generate comprehensive monthly data
                    monthly_rating = random.choice(['Strong Buy', 'Buy', 'Hold', 'Sell', 'Strong Sell'])
                    target_return = random.uniform(-20, 30)
                    risk_level = random.choice(['Low', 'Medium', 'High'])
                    best_week = random.choice(['Week 1', 'Week 2', 'Week 3', 'Week 4'])
                    worst_week = random.choice(['Week 1', 'Week 2', 'Week 3', 'Week 4'])
                    
                    if monthly_rating in ['Strong Buy', 'Buy']:
                        card_style = 'background: #d4edda; color: #155724; border-left: 5px solid #28a745;'
                    elif monthly_rating in ['Strong Sell', 'Sell']:
                        card_style = 'background: #f8d7da; color: #721c24; border-left: 5px solid #dc3545;'
                    else:
                        card_style = 'background: #fff3cd; color: #856404; border-left: 5px solid #ffc107;'
                    
                    with stock_perf_cols[col_idx]:
                        st.markdown(f"""
                        <div style="{card_style} padding: 15px; border-radius: 8px; margin: 8px 0;">
                            <h5 style="margin: 0 0 10px 0;">{stock}</h5>
                            <p style="margin: 0; font-size: 0.9em;"><strong>Monthly Rating:</strong> {monthly_rating}</p>
                            <p style="margin: 0; font-size: 0.9em;"><strong>Target Return:</strong> {target_return:+.1f}%</p>
                            <p style="margin: 0; font-size: 0.9em;"><strong>Risk Level:</strong> {risk_level}</p>
                            <p style="margin: 0; font-size: 0.9em;"><strong>Best Week:</strong> {best_week}</p>
                            <p style="margin: 0; font-size: 0.9em;"><strong>Avoid Week:</strong> {worst_week}</p>
                        </div>
                        """, unsafe_allow_html=True)

with main_tab2:
    st.markdown(f"""
    <div class="section-header">
        <h2 style="margin: 0 0 10px 0;">🔮 TOMORROW'S COMPLETE PLANETARY TRANSIT FORECAST</h2>
        <h3 style="margin: 0; opacity: 0.9;">{tomorrow_day}, {tomorrow_date} • Detailed Predictions</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Tomorrow's Analysis with same structure
    tomorrow_equity_tab, tomorrow_commodity_tab, tomorrow_forex_tab, tomorrow_global_tab, tomorrow_sectorwise_tab = st.tabs([
        "📈 EQUITY FORECAST", 
        "🏭 COMMODITIES FORECAST", 
        "💱 FOREX FORECAST", 
        "🌍 GLOBAL FORECAST", 
        "🏢 SECTORWISE FORECAST"
    ])
    
    with tomorrow_equity_tab:
        st.markdown('<div class="sector-header"><h3 style="margin: 0;">📈 TOMORROW\'S EQUITY FORECAST</h3></div>', unsafe_allow_html=True)
        
        # Tomorrow's key opportunities
        st.markdown("### 🌟 Tomorrow's Best Trading Opportunities")
        
        tomorrow_opportunities = [
            {'time': '12:15-13:15', 'sector': 'Banking', 'planet': 'Jupiter ♃', 'signal': 'STRONG BUY', 'target': '+2.1%'},
            {'time': '09:15-10:15', 'sector': 'FMCG', 'planet': 'Moon 🌙', 'signal': 'BUY', 'target': '+1.5%'},
            {'time': '13:15-14:15', 'sector': 'Auto', 'planet': 'Venus ♀', 'signal': 'BUY', 'target': '+1.8%'},
            {'time': '11:15-12:15', 'sector': 'IT', 'planet': 'Mercury ☿', 'signal': 'SELL', 'target': '-1.5%'},
        ]
        
        opp_cols = st.columns(2)
        
        for idx, opp in enumerate(tomorrow_opportunities):
            col_idx = idx % 2
            
            if 'BUY' in opp['signal']:
                bg_color = '#d4edda'
                text_color = '#155724'
                icon = '🟢'
            else:
                bg_color = '#f8d7da'
                text_color = '#721c24'
                icon = '🔴'
            
            with opp_cols[col_idx]:
                st.markdown(f"""
                <div style="background: {bg_color}; color: {text_color}; padding: 15px; border-radius: 10px; margin: 10px 0; border: 2px solid {text_color};">
                    <h4 style="margin: 0 0 10px 0; color: {text_color};">{icon} {opp['sector']} Sector</h4>
                    <p style="margin: 0; font-size: 1em;"><strong>Time:</strong> {opp['time']}</p>
                    <p style="margin: 0; font-size: 1em;"><strong>Planet:</strong> {opp['planet']}</p>
                    <p style="margin: 0; font-size: 1.1em;"><strong>Signal:</strong> <span style="background: {text_color}; color: white; padding: 4px 8px; border-radius: 4px;">{opp['signal']}</span></p>
                    <p style="margin: 5px 0 0 0; font-size: 1em;"><strong>Expected:</strong> {opp['target']}</p>
                </div>
                """, unsafe_allow_html=True)
    
    with tomorrow_commodity_tab:
        st.markdown('<div class="sector-header"><h3 style="margin: 0;">🏭 TOMORROW\'S COMMODITIES FORECAST</h3></div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="report-section" style="background: #d4edda; border-left: 5px solid #28a745;">
            <h4 style="color: #155724;">⭐ PEAK OPPORTUNITY: 18:00-21:00 (Jupiter ♃)</h4>
            <p style="font-size: 1.1em;"><strong>🥇 GOLD:</strong> <span style="background: #28a745; color: white; padding: 4px 8px; border-radius: 4px; font-weight: bold;">STRONG BUY +2.2%</span></p>
            <p style="font-size: 1.1em;"><strong>🥈 SILVER:</strong> <span style="background: #28a745; color: white; padding: 4px 8px; border-radius: 4px; font-weight: bold;">STRONG BUY +3.5%</span></p>
            <p style="font-size: 1.1em;"><strong>₿ BITCOIN:</strong> <span style="background: #28a745; color: white; padding: 4px 8px; border-radius: 4px; font-weight: bold;">STRONG BUY +5.2%</span></p>
            <p style="margin: 15px 0 0 0; font-weight: bold; font-size: 1.2em; color: #155724;">🌟 This is the best commodity trading window of the week!</p>
        </div>
        """, unsafe_allow_html=True)
    
    with tomorrow_forex_tab:
        st.markdown('<div class="sector-header"><h3 style="margin: 0;">💱 TOMORROW\'S FOREX FORECAST</h3></div>', unsafe_allow_html=True)
        
        forex_forecast = [
            {'pair': 'USD/INR', 'trend': 'Bearish', 'range': '83.15 - 83.45', 'strategy': 'Sell on rallies above 83.35'},
            {'pair': 'EUR/INR', 'trend': 'Bullish', 'range': '88.10 - 88.80', 'strategy': 'Buy on dips below 88.20'},
            {'pair': 'GBP/INR', 'trend': 'Volatile', 'range': '106.00 - 108.00', 'strategy': 'Avoid or use very tight stops'},
        ]
        
        for forecast in forex_forecast:
            if forecast['trend'] == 'Bullish':
                bg_color = '#d4edda'
                text_color = '#155724'
            elif forecast['trend'] == 'Bearish':
                bg_color = '#f8d7da'
                text_color = '#721c24'
            else:
                bg_color = '#fff3cd'
                text_color = '#856404'
            
            st.markdown(f"""
            <div style="background: {bg_color}; color: {text_color}; padding: 15px; border-radius: 8px; margin: 10px 0; border-left: 5px solid {text_color};">
                <h4 style="margin: 0 0 10px 0; color: {text_color};">{forecast['pair']}: {forecast['trend']}</h4>
                <p style="margin: 0;"><strong>Range:</strong> {forecast['range']}</p>
                <p style="margin: 0;"><strong>Strategy:</strong> {forecast['strategy']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    with tomorrow_global_tab:
        st.markdown('<div class="sector-header"><h3 style="margin: 0;">🌍 TOMORROW\'S GLOBAL FORECAST</h3></div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="report-section">
            <h4>🇺🇸 US MARKETS: Strong Evening Rally Expected</h4>
            <p><strong>DOW JONES:</strong> Jupiter hour (21:00-23:00 IST) brings +1.5% rally</p>
            <p><strong>NASDAQ:</strong> Tech strength continues, target +2.0%</p>
            
            <h4>₿ CRYPTOCURRENCY: Exceptional Day</h4>
            <p><strong>BITCOIN:</strong> Jupiter peak (18:00-21:00) could trigger +5%+ move</p>
            <p><strong>Target:</strong> $103,000 - $105,000</p>
        </div>
        """, unsafe_allow_html=True)
    
    with tomorrow_sectorwise_tab:
        st.markdown('<div class="sector-header"><h3 style="margin: 0;">🏢 TOMORROW\'S SECTORWISE FORECAST</h3></div>', unsafe_allow_html=True)
        
        st.markdown("### 🎯 Tomorrow's Sector Opportunities")
        
        tomorrow_sector_forecast = [
            {'sector': 'Banking', 'trend': 'Strong Bullish', 'best_time': '12:15-13:15', 'target': '+2.1%', 'planet': 'Jupiter ♃'},
            {'sector': 'FMCG', 'trend': 'Bullish', 'best_time': '09:15-10:15', 'target': '+1.5%', 'planet': 'Moon 🌙'},
            {'sector': 'Auto', 'trend': 'Bullish', 'best_time': '13:15-14:15', 'target': '+1.8%', 'planet': 'Venus ♀'},
            {'sector': 'IT', 'trend': 'Bearish', 'best_time': '11:15-12:15', 'target': '-1.5%', 'planet': 'Mercury ☿'},
            {'sector': 'Metal', 'trend': 'Bearish', 'best_time': '14:15-15:15', 'target': '-1.2%', 'planet': 'Saturn ♄'},
            {'sector': 'Energy', 'trend': 'Volatile', 'best_time': '10:15-11:15', 'target': '±2.0%', 'planet': 'Mars ♂️'}
        ]
        
        sector_forecast_cols = st.columns(3)
        
        for idx, forecast in enumerate(tomorrow_sector_forecast):
            col_idx = idx % 3
            
            if forecast['trend'] in ['Strong Bullish', 'Bullish']:
                bg_color = '#d4edda'
                text_color = '#155724'
                icon = '🟢'
            elif forecast['trend'] == 'Bearish':
                bg_color = '#f8d7da'
                text_color = '#721c24'
                icon = '🔴'
            else:
                bg_color = '#fff3cd'
                text_color = '#856404'
                icon = '⚡'
            
            with sector_forecast_cols[col_idx]:
                st.markdown(f"""
                <div style="background: {bg_color}; color: {text_color}; padding: 12px; border-radius: 8px; margin: 8px 0; border: 2px solid {text_color};">
                    <h5 style="margin: 0 0 8px 0; color: {text_color};">{icon} {forecast['sector']}</h5>
                    <p style="margin: 0; font-size: 0.9em;"><strong>Trend:</strong> {forecast['trend']}</p>
                    <p style="margin: 0; font-size: 0.9em;"><strong>Best Time:</strong> {forecast['best_time']}</p>
                    <p style="margin: 0; font-size: 0.9em;"><strong>Target:</strong> {forecast['target']}</p>
                    <p style="margin: 0; font-size: 0.9em;"><strong>Planet:</strong> {forecast['planet']}</p>
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
