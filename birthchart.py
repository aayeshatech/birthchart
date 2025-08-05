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

def get_planetary_transits():
    """Get current planetary transit data - Based on Real Astronomical Positions for Aug 1, 2025"""
    ist_tz = pytz.timezone('Asia/Kolkata')
    current_date = datetime.now(ist_tz)
    current_time = current_date.strftime('%H:%M')
    
    # Real planetary positions for August 1, 2025 (based on astronomical ephemeris)
    transits = {
        'Sun': {
            'symbol': '☀️',
            'sign': 'Cancer',
            'degree': '15°01\'',
            'effect': 'Strong for FMCG, Dairy, Real Estate sectors',
            'strength': 'Friendly Sign',
            'markets_affected': ['FMCG', 'Dairy', 'Real Estate'],
            'trend': 'Bullish',
            'duration': '30 days',
            'vedic_time': '15:01',
            'modern_position': 'Cancer 15°01\''
        },
        'Moon': {
            'symbol': '🌙',
            'sign': 'Swati (Libra)',
            'degree': '11°47\'',
            'effect': 'Favorable for Luxury, Auto, Textiles, Trade',
            'strength': 'Moderate',
            'markets_affected': ['Auto', 'Textiles', 'Luxury Goods'],
            'trend': 'Bullish',
            'duration': '2.5 days',
            'vedic_time': '11:47',
            'modern_position': 'Libra 11°47\''
        },
        'Mars': {
            'symbol': '♂️',
            'sign': 'Uttara Phalguni (Virgo)',
            'degree': '02°13\'',
            'effect': 'Mixed for IT, Healthcare, Precision industries',
            'strength': 'Neutral',
            'markets_affected': ['IT', 'Healthcare', 'Precision Tools'],
            'trend': 'Volatile',
            'duration': '45 days',
            'vedic_time': '02:13',
            'modern_position': 'Virgo 02°13\''
        },
        'Mercury': {
            'symbol': '☿',
            'sign': 'Pushya (Cancer)',
            'degree': '14°36\'',
            'effect': 'Strong for Communication, FMCG, IT services',
            'strength': 'Friendly',
            'markets_affected': ['IT', 'Telecom', 'FMCG'],
            'trend': 'Bullish',
            'duration': '20 days',
            'vedic_time': '14:36',
            'modern_position': 'Cancer 14°36\''
        },
        'Jupiter': {
            'symbol': '♃',
            'sign': 'Ardra (Gemini)',
            'degree': '17°32\'',
            'effect': 'Moderate for Communication, Media, Education',
            'strength': 'Neutral',
            'markets_affected': ['Media', 'Education', 'Communication'],
            'trend': 'Neutral',
            'duration': '12 months',
            'vedic_time': '17:32',
            'modern_position': 'Gemini 17°32\''
        },
        'Venus': {
            'symbol': '♀',
            'sign': 'Ardra (Gemini)',
            'degree': '07°01\'',
            'effect': 'Good for Media, Communication, Luxury goods',
            'strength': 'Neutral',
            'markets_affected': ['Media', 'Luxury', 'Communication'],
            'trend': 'Bullish',
            'duration': '25 days',
            'vedic_time': '07:01',
            'modern_position': 'Gemini 07°01\''
        },
        'Saturn': {
            'symbol': '♄',
            'sign': 'Uttara Bhadrapada (Pisces)',
            'degree': '07°24\'',
            'effect': 'Cautious for Pharma, Chemicals, Spirituality',
            'strength': 'Friendly',
            'markets_affected': ['Pharma', 'Chemicals', 'Healthcare'],
            'trend': 'Cautious',
            'duration': '2.5 years',
            'vedic_time': '07:24',
            'modern_position': 'Pisces 07°24\''
        },
        'Rahu': {
            'symbol': '☊',
            'sign': 'Purvabhadrapada (Pisces)',
            'degree': '24°51\'',
            'effect': 'Volatile for Pharma, Chemicals, Foreign stocks',
            'strength': 'Strong',
            'markets_affected': ['Pharma', 'Chemicals', 'Foreign'],
            'trend': 'Volatile',
            'duration': '18 months',
            'vedic_time': '24:51',
            'modern_position': 'Pisces 24°51\''
        },
        'Ketu': {
            'symbol': '☋',
            'sign': 'Hasta (Virgo)',
            'degree': '24°51\'',
            'effect': 'Supportive for IT, Healthcare, Service sectors',
            'strength': 'Moderate',
            'markets_affected': ['IT Services', 'Healthcare', 'Analytics'],
            'trend': 'Supportive',
            'duration': '18 months',
            'vedic_time': '24:51',
            'modern_position': 'Virgo 24°51\''
        },
        'Uranus': {
            'symbol': '♅',
            'sign': 'Krittika (Taurus)',
            'degree': '06°42\'',
            'effect': 'Innovation in Finance, Energy, Technology',
            'strength': 'Moderate',
            'markets_affected': ['Fintech', 'Energy Tech', 'Innovation'],
            'trend': 'Disruptive',
            'duration': '7 years',
            'vedic_time': '06:42',
            'modern_position': 'Taurus 06°42\''
        }
    }
    
    return transits

def create_commodity_signals():
    """Generate commodity-specific planetary signals from 5 AM to 11:55 PM"""
    commodity_signals = [
        # Early Morning (5 AM - 9 AM)
        {'time': '05:00-06:00', 'planet': 'Saturn ♄', 'gold': 'SELL', 'silver': 'SELL', 'crude': 'BUY', 'trend': 'Bearish', 'strength': 'Moderate'},
        {'time': '06:00-07:00', 'planet': 'Jupiter ♃', 'gold': 'BUY', 'silver': 'BUY', 'crude': 'HOLD', 'trend': 'Bullish', 'strength': 'Strong'},
        {'time': '07:00-08:00', 'planet': 'Mars ♂️', 'gold': 'HOLD', 'silver': 'VOLATILE', 'crude': 'BUY', 'trend': 'Volatile', 'strength': 'High'},
        {'time': '08:00-09:00', 'planet': 'Sun ☀️', 'gold': 'BUY', 'silver': 'BUY', 'crude': 'STRONG BUY', 'trend': 'Bullish', 'strength': 'Very Strong'},
        
        # Market Hours (9 AM - 4 PM)
        {'time': '09:00-10:00', 'planet': 'Venus ♀', 'gold': 'STRONG BUY', 'silver': 'BUY', 'crude': 'SELL', 'trend': 'Bullish', 'strength': 'Strong'},
        {'time': '10:00-11:00', 'planet': 'Mercury ☿', 'gold': 'HOLD', 'silver': 'VOLATILE', 'crude': 'HOLD', 'trend': 'Neutral', 'strength': 'Moderate'},
        {'time': '11:00-12:00', 'planet': 'Moon 🌙', 'gold': 'BUY', 'silver': 'STRONG BUY', 'crude': 'SELL', 'trend': 'Bullish', 'strength': 'Strong'},
        {'time': '12:00-13:00', 'planet': 'Saturn ♄', 'gold': 'SELL', 'silver': 'SELL', 'crude': 'VOLATILE', 'trend': 'Bearish', 'strength': 'Weak'},
        {'time': '13:00-14:00', 'planet': 'Jupiter ♃', 'gold': 'STRONG BUY', 'silver': 'STRONG BUY', 'crude': 'BUY', 'trend': 'Strong Bullish', 'strength': 'Excellent'},
        {'time': '14:00-15:00', 'planet': 'Mars ♂️', 'gold': 'VOLATILE', 'silver': 'VOLATILE', 'crude': 'STRONG BUY', 'trend': 'Volatile', 'strength': 'High'},
        {'time': '15:00-16:00', 'planet': 'Sun ☀️', 'gold': 'BUY', 'silver': 'HOLD', 'crude': 'BUY', 'trend': 'Bullish', 'strength': 'Strong'},
        
        # Evening (4 PM - 11:55 PM)
        {'time': '16:00-17:00', 'planet': 'Venus ♀', 'gold': 'BUY', 'silver': 'BUY', 'crude': 'HOLD', 'trend': 'Bullish', 'strength': 'Strong'},
        {'time': '17:00-18:00', 'planet': 'Mercury ☿', 'gold': 'HOLD', 'silver': 'SELL', 'crude': 'SELL', 'trend': 'Bearish', 'strength': 'Weak'},
        {'time': '18:00-19:00', 'planet': 'Moon 🌙', 'gold': 'STRONG BUY', 'silver': 'STRONG BUY', 'crude': 'HOLD', 'trend': 'Strong Bullish', 'strength': 'Excellent'},
        {'time': '19:00-20:00', 'planet': 'Saturn ♄', 'gold': 'SELL', 'silver': 'VOLATILE', 'crude': 'SELL', 'trend': 'Bearish', 'strength': 'Weak'},
        {'time': '20:00-21:00', 'planet': 'Jupiter ♃', 'gold': 'PEAK BUY', 'silver': 'PEAK BUY', 'crude': 'BUY', 'trend': 'Peak Bullish', 'strength': 'Maximum'},
        {'time': '21:00-22:00', 'planet': 'Mars ♂️', 'gold': 'VOLATILE', 'silver': 'SELL', 'crude': 'STRONG BUY', 'trend': 'Volatile', 'strength': 'High'},
        {'time': '22:00-23:00', 'planet': 'Sun ☀️', 'gold': 'HOLD', 'silver': 'HOLD', 'crude': 'BUY', 'trend': 'Neutral', 'strength': 'Moderate'},
        {'time': '23:00-23:55', 'planet': 'Venus ♀', 'gold': 'BUY', 'silver': 'BUY', 'crude': 'HOLD', 'trend': 'Bullish', 'strength': 'Good'}
    ]
    return commodity_signals

def create_forex_signals():
    """Generate forex-specific planetary signals from 5 AM to 11:55 PM"""
    forex_signals = [
        # Early Morning (5 AM - 9 AM)
        {'time': '05:00-06:00', 'planet': 'Saturn ♄', 'usdinr': 'BUY', 'btc': 'SELL', 'dxy': 'STRONG BUY', 'trend': 'Bearish Crypto', 'strength': 'Strong'},
        {'time': '06:00-07:00', 'planet': 'Jupiter ♃', 'usdinr': 'SELL', 'btc': 'STRONG BUY', 'dxy': 'SELL', 'trend': 'Bullish Crypto', 'strength': 'Excellent'},
        {'time': '07:00-08:00', 'planet': 'Mars ♂️', 'usdinr': 'VOLATILE', 'btc': 'VOLATILE', 'dxy': 'VOLATILE', 'trend': 'High Volatility', 'strength': 'Extreme'},
        {'time': '08:00-09:00', 'planet': 'Sun ☀️', 'usdinr': 'BUY', 'btc': 'BUY', 'dxy': 'BUY', 'trend': 'Broad Bullish', 'strength': 'Strong'},
        
        # Active Trading (9 AM - 4 PM)
        {'time': '09:00-10:00', 'planet': 'Venus ♀', 'usdinr': 'SELL', 'btc': 'STRONG BUY', 'dxy': 'SELL', 'trend': 'Crypto Bullish', 'strength': 'Strong'},
        {'time': '10:00-11:00', 'planet': 'Mercury ☿', 'usdinr': 'VOLATILE', 'btc': 'SELL', 'dxy': 'BUY', 'trend': 'Dollar Strength', 'strength': 'Moderate'},
        {'time': '11:00-12:00', 'planet': 'Moon 🌙', 'usdinr': 'BUY', 'btc': 'BUY', 'dxy': 'HOLD', 'trend': 'Mixed Bullish', 'strength': 'Good'},
        {'time': '12:00-13:00', 'planet': 'Saturn ♄', 'usdinr': 'STRONG BUY', 'btc': 'SELL', 'dxy': 'STRONG BUY', 'trend': 'Dollar Bullish', 'strength': 'Strong'},
        {'time': '13:00-14:00', 'planet': 'Jupiter ♃', 'usdinr': 'SELL', 'btc': 'PEAK BUY', 'dxy': 'SELL', 'trend': 'Peak Crypto', 'strength': 'Maximum'},
        {'time': '14:00-15:00', 'planet': 'Mars ♂️', 'usdinr': 'VOLATILE', 'btc': 'VOLATILE', 'dxy': 'VOLATILE', 'trend': 'Extreme Volatility', 'strength': 'Extreme'},
        {'time': '15:00-16:00', 'planet': 'Sun ☀️', 'usdinr': 'BUY', 'btc': 'HOLD', 'dxy': 'BUY', 'trend': 'Dollar Strength', 'strength': 'Strong'},
        
        # Evening Trading (4 PM - 11:55 PM)
        {'time': '16:00-17:00', 'planet': 'Venus ♀', 'usdinr': 'SELL', 'btc': 'BUY', 'dxy': 'SELL', 'trend': 'Crypto Recovery', 'strength': 'Good'},
        {'time': '17:00-18:00', 'planet': 'Mercury ☿', 'usdinr': 'HOLD', 'btc': 'SELL', 'dxy': 'BUY', 'trend': 'Dollar Recovery', 'strength': 'Moderate'},
        {'time': '18:00-19:00', 'planet': 'Moon 🌙', 'usdinr': 'SELL', 'btc': 'STRONG BUY', 'dxy': 'SELL', 'trend': 'Crypto Surge', 'strength': 'Strong'},
        {'time': '19:00-20:00', 'planet': 'Saturn ♄', 'usdinr': 'BUY', 'btc': 'SELL', 'dxy': 'BUY', 'trend': 'Safe Haven', 'strength': 'Strong'},
        {'time': '20:00-21:00', 'planet': 'Jupiter ♃', 'usdinr': 'SELL', 'btc': 'PEAK BUY', 'dxy': 'VOLATILE', 'trend': 'Crypto Peak', 'strength': 'Maximum'},
        {'time': '21:00-22:00', 'planet': 'Mars ♂️', 'usdinr': 'VOLATILE', 'btc': 'VOLATILE', 'dxy': 'VOLATILE', 'trend': 'Night Volatility', 'strength': 'High'},
        {'time': '22:00-23:00', 'planet': 'Sun ☀️', 'usdinr': 'HOLD', 'btc': 'BUY', 'dxy': 'HOLD', 'trend': 'Consolidation', 'strength': 'Moderate'},
        {'time': '23:00-23:55', 'planet': 'Venus ♀', 'usdinr': 'SELL', 'btc': 'BUY', 'dxy': 'SELL', 'trend': 'Late Crypto Buy', 'strength': 'Good'}
    ]
    return forex_signals

def create_global_signals():
    """Generate global market planetary signals from 5 AM to 11:55 PM"""
    global_signals = [
        # Early Morning (5 AM - 9 AM)
        {'time': '05:00-06:00', 'planet': 'Saturn ♄', 'dow': 'SELL', 'nasdaq': 'SELL', 'sp500': 'SELL', 'trend': 'Pre-market Weakness', 'strength': 'Weak'},
        {'time': '06:00-07:00', 'planet': 'Jupiter ♃', 'dow': 'BUY', 'nasdaq': 'STRONG BUY', 'sp500': 'BUY', 'trend': 'Pre-market Strength', 'strength': 'Strong'},
        {'time': '07:00-08:00', 'planet': 'Mars ♂️', 'dow': 'VOLATILE', 'nasdaq': 'VOLATILE', 'sp500': 'VOLATILE', 'trend': 'Pre-market Volatility', 'strength': 'High'},
        {'time': '08:00-09:00', 'planet': 'Sun ☀️', 'dow': 'BUY', 'nasdaq': 'BUY', 'sp500': 'STRONG BUY', 'trend': 'Opening Strength', 'strength': 'Strong'},
        
        # US Market Open (9:30 PM IST = 12:00 PM EST) - Active Trading
        {'time': '09:00-10:00', 'planet': 'Venus ♀', 'dow': 'STRONG BUY', 'nasdaq': 'BUY', 'sp500': 'BUY', 'trend': 'Morning Rally', 'strength': 'Strong'},
        {'time': '10:00-11:00', 'planet': 'Mercury ☿', 'dow': 'HOLD', 'nasdaq': 'SELL', 'sp500': 'HOLD', 'trend': 'Tech Weakness', 'strength': 'Moderate'},
        {'time': '11:00-12:00', 'planet': 'Moon 🌙', 'dow': 'BUY', 'nasdaq': 'BUY', 'sp500': 'BUY', 'trend': 'Mid-day Strength', 'strength': 'Good'},
        {'time': '12:00-13:00', 'planet': 'Saturn ♄', 'dow': 'SELL', 'nasdaq': 'VOLATILE', 'sp500': 'SELL', 'trend': 'Afternoon Pressure', 'strength': 'Weak'},
        {'time': '13:00-14:00', 'planet': 'Jupiter ♃', 'dow': 'STRONG BUY', 'nasdaq': 'STRONG BUY', 'sp500': 'STRONG BUY', 'trend': 'Power Hour Prep', 'strength': 'Excellent'},
        {'time': '14:00-15:00', 'planet': 'Mars ♂️', 'dow': 'VOLATILE', 'nasdaq': 'VOLATILE', 'sp500': 'VOLATILE', 'trend': 'High Volatility', 'strength': 'Extreme'},
        {'time': '15:00-16:00', 'planet': 'Sun ☀️', 'dow': 'BUY', 'nasdaq': 'BUY', 'sp500': 'BUY', 'trend': 'Closing Strength', 'strength': 'Strong'},
        
        # After Hours & Evening (4 PM - 11:55 PM)
        {'time': '16:00-17:00', 'planet': 'Venus ♀', 'dow': 'HOLD', 'nasdaq': 'BUY', 'sp500': 'HOLD', 'trend': 'After Hours Tech', 'strength': 'Moderate'},
        {'time': '17:00-18:00', 'planet': 'Mercury ☿', 'dow': 'SELL', 'nasdaq': 'VOLATILE', 'sp500': 'SELL', 'trend': 'Evening Weakness', 'strength': 'Weak'},
        {'time': '18:00-19:00', 'planet': 'Moon 🌙', 'dow': 'BUY', 'nasdaq': 'BUY', 'sp500': 'BUY', 'trend': 'Evening Recovery', 'strength': 'Good'},
        {'time': '19:00-20:00', 'planet': 'Saturn ♄', 'dow': 'HOLD', 'nasdaq': 'SELL', 'sp500': 'HOLD', 'trend': 'Consolidation', 'strength': 'Neutral'},
        {'time': '20:00-21:00', 'planet': 'Jupiter ♃', 'dow': 'PEAK BUY', 'nasdaq': 'PEAK BUY', 'sp500': 'PEAK BUY', 'trend': 'Peak Evening Rally', 'strength': 'Maximum'},
        {'time': '21:00-22:00', 'planet': 'Mars ♂️', 'dow': 'VOLATILE', 'nasdaq': 'VOLATILE', 'sp500': 'VOLATILE', 'trend': 'Late Volatility', 'strength': 'High'},
        {'time': '22:00-23:00', 'planet': 'Sun ☀️', 'dow': 'HOLD', 'nasdaq': 'BUY', 'sp500': 'HOLD', 'trend': 'Late Tech Strength', 'strength': 'Moderate'},
        {'time': '23:00-23:55', 'planet': 'Venus ♀', 'dow': 'BUY', 'nasdaq': 'BUY', 'sp500': 'BUY', 'trend': 'End Day Strength', 'strength': 'Good'}
    ]
    return global_signals

def create_equity_signals():
    """Generate equity-specific planetary signals for Indian market hours (9:15 AM - 3:30 PM)"""
    equity_signals = [
        # Pre-opening (9:00-9:15)
        {'time': '09:00-09:15', 'planet': 'Venus ♀', 'nifty': 'WATCH', 'banknifty': 'WATCH', 'trend': 'Pre-Open Analysis', 'strength': 'Setup'},
        
        # Opening Hour (9:15-10:15)
        {'time': '09:15-10:15', 'planet': 'Venus ♀', 'nifty': 'STRONG BUY', 'banknifty': 'BUY', 'trend': 'Opening Bullish', 'strength': 'Strong'},
        
        # Mid Morning (10:15-11:15)
        {'time': '10:15-11:15', 'planet': 'Sun ☀️', 'nifty': 'BUY', 'banknifty': 'STRONG BUY', 'trend': 'Bank Strength', 'strength': 'Very Strong'},
        
        # Late Morning (11:15-12:15)
        {'time': '11:15-12:15', 'planet': 'Mercury ☿', 'nifty': 'VOLATILE', 'banknifty': 'SELL', 'trend': 'Tech Pressure', 'strength': 'Weak'},
        
        # Noon Hour (12:15-13:15)
        {'time': '12:15-13:15', 'planet': 'Saturn ♄', 'nifty': 'SELL', 'banknifty': 'VOLATILE', 'trend': 'Midday Weakness', 'strength': 'Weak'},
        
        # Early Afternoon (13:15-14:15)
        {'time': '13:15-14:15', 'planet': 'Jupiter ♃', 'nifty': 'PEAK BUY', 'banknifty': 'PEAK BUY', 'trend': 'Peak Banking Hour', 'strength': 'Maximum'},
        
        # Late Afternoon (14:15-15:15)
        {'time': '14:15-15:15', 'planet': 'Mars ♂️', 'nifty': 'VOLATILE', 'banknifty': 'VOLATILE', 'trend': 'High Volatility', 'strength': 'Extreme'},
        
        # Closing Hour (15:15-15:30)
        {'time': '15:15-15:30', 'planet': 'Sun ☀️', 'nifty': 'BUY', 'banknifty': 'BUY', 'trend': 'Closing Strength', 'strength': 'Strong'}
    ]
    return equity_signals

def display_detailed_signals(signals, market_type, current_hour):
    """Display detailed planetary signals for any market type"""
    
    if market_type == "commodity":
        st.markdown("### 🥇 GOLD • 🥈 SILVER • 🛢️ CRUDE - Complete Planetary Transit")
        
        # Group signals by time periods
        early_morning = [s for s in signals if int(s['time'].split('-')[0].split(':')[0]) < 9]
        market_hours = [s for s in signals if 9 <= int(s['time'].split('-')[0].split(':')[0]) < 16]
        evening_hours = [s for s in signals if int(s['time'].split('-')[0].split(':')[0]) >= 16]
        
        # Early Morning (5 AM - 9 AM)
        st.markdown("#### 🌅 Early Morning Session (5:00 AM - 9:00 AM)")
        early_cols = st.columns(2)
        
        for idx, signal in enumerate(early_morning):
            col_idx = idx % 2
            is_active = current_hour >= int(signal['time'].split('-')[0].split(':')[0]) and current_hour < int(signal['time'].split('-')[1].split(':')[0])
            
            if signal['trend'] in ['Bullish', 'Strong Bullish']:
                css_class = 'live-signal' if is_active else 'trend-bullish'
            elif 'Bearish' in signal['trend']:
                css_class = 'warning-signal' if is_active else 'trend-bearish'
            else:
                css_class = 'trend-volatile'
            
            active_text = " 🔥 LIVE NOW" if is_active else ""
            
            with early_cols[col_idx]:
                st.markdown(f"""
                <div class="{css_class}">
                    <strong>{signal['time']} - {signal['planet']}{active_text}</strong><br>
                    <strong>🥇 GOLD:</strong> {signal['gold']} | <strong>🥈 SILVER:</strong> {signal['silver']} | <strong>🛢️ CRUDE:</strong> {signal['crude']}<br>
                    <strong>Trend:</strong> {signal['trend']} | <strong>Strength:</strong> {signal['strength']}
                </div>
                """, unsafe_allow_html=True)
        
        # Market Hours (9 AM - 4 PM)
        st.markdown("#### 📈 Active Trading Session (9:00 AM - 4:00 PM)")
        market_cols = st.columns(2)
        
        for idx, signal in enumerate(market_hours):
            col_idx = idx % 2
            is_active = current_hour >= int(signal['time'].split('-')[0].split(':')[0]) and current_hour < int(signal['time'].split('-')[1].split(':')[0])
            
            if signal['trend'] in ['Bullish', 'Strong Bullish', 'Peak Bullish']:
                css_class = 'live-signal' if is_active else 'trend-bullish'
            elif 'Bearish' in signal['trend']:
                css_class = 'warning-signal' if is_active else 'trend-bearish'
            else:
                css_class = 'trend-volatile'
            
            active_text = " 🔥 LIVE NOW" if is_active else ""
            if signal['strength'] == 'Maximum':
                active_text += " ⭐ PEAK"
            
            with market_cols[col_idx]:
                st.markdown(f"""
                <div class="{css_class}">
                    <strong>{signal['time']} - {signal['planet']}{active_text}</strong><br>
                    <strong>🥇 GOLD:</strong> {signal['gold']} | <strong>🥈 SILVER:</strong> {signal['silver']} | <strong>🛢️ CRUDE:</strong> {signal['crude']}<br>
                    <strong>Trend:</strong> {signal['trend']} | <strong>Strength:</strong> {signal['strength']}
                </div>
                """, unsafe_allow_html=True)
        
        # Evening Hours (4 PM - 11:55 PM)
        st.markdown("#### 🌙 Evening Session (4:00 PM - 11:55 PM)")
        evening_cols = st.columns(2)
        
        for idx, signal in enumerate(evening_hours):
            col_idx = idx % 2
            is_active = current_hour >= int(signal['time'].split('-')[0].split(':')[0]) and current_hour < int(signal['time'].split('-')[1].split(':')[0])
            
            if signal['trend'] in ['Bullish', 'Strong Bullish', 'Peak Bullish']:
                css_class = 'live-signal' if is_active else 'trend-bullish'
            elif 'Bearish' in signal['trend']:
                css_class = 'warning-signal' if is_active else 'trend-bearish'
            else:
                css_class = 'trend-volatile'
            
            active_text = " 🔥 LIVE NOW" if is_active else ""
            if signal['strength'] == 'Maximum':
                active_text += " ⭐ PEAK"
            
            with evening_cols[col_idx]:
                st.markdown(f"""
                <div class="{css_class}">
                    <strong>{signal['time']} - {signal['planet']}{active_text}</strong><br>
                    <strong>🥇 GOLD:</strong> {signal['gold']} | <strong>🥈 SILVER:</strong> {signal['silver']} | <strong>🛢️ CRUDE:</strong> {signal['crude']}<br>
                    <strong>Trend:</strong> {signal['trend']} | <strong>Strength:</strong> {signal['strength']}
                </div>
                """, unsafe_allow_html=True)
    
    elif market_type == "forex":
        st.markdown("### 💵 USDINR • ₿ BITCOIN • 📊 DOLLAR INDEX - Complete Planetary Transit")
        
        # Group signals by time periods
        early_morning = [s for s in signals if int(s['time'].split('-')[0].split(':')[0]) < 9]
        active_hours = [s for s in signals if 9 <= int(s['time'].split('-')[0].split(':')[0]) < 16]
        evening_hours = [s for s in signals if int(s['time'].split('-')[0].split(':')[0]) >= 16]
        
        # Early Morning (5 AM - 9 AM)
        st.markdown("#### 🌅 Early Session (5:00 AM - 9:00 AM)")
        early_cols = st.columns(2)
        
        for idx, signal in enumerate(early_morning):
            col_idx = idx % 2
            is_active = current_hour >= int(signal['time'].split('-')[0].split(':')[0]) and current_hour < int(signal['time'].split('-')[1].split(':')[0])
            
            if 'Bullish' in signal['trend']:
                css_class = 'live-signal' if is_active else 'trend-bullish'
            elif 'Bearish' in signal['trend']:
                css_class = 'warning-signal' if is_active else 'trend-bearish'
            else:
                css_class = 'trend-volatile'
            
            active_text = " 🔥 LIVE NOW" if is_active else ""
            
            with early_cols[col_idx]:
                st.markdown(f"""
                <div class="{css_class}">
                    <strong>{signal['time']} - {signal['planet']}{active_text}</strong><br>
                    <strong>💵 USDINR:</strong> {signal['usdinr']} | <strong>₿ BTC:</strong> {signal['btc']} | <strong>📊 DXY:</strong> {signal['dxy']}<br>
                    <strong>Trend:</strong> {signal['trend']} | <strong>Strength:</strong> {signal['strength']}
                </div>
                """, unsafe_allow_html=True)
        
        # Active Hours (9 AM - 4 PM)
        st.markdown("#### ⚡ Active Trading Session (9:00 AM - 4:00 PM)")
        active_cols = st.columns(2)
        
        for idx, signal in enumerate(active_hours):
            col_idx = idx % 2
            is_active = current_hour >= int(signal['time'].split('-')[0].split(':')[0]) and current_hour < int(signal['time'].split('-')[1].split(':')[0])
            
            if 'Bullish' in signal['trend']:
                css_class = 'live-signal' if is_active else 'trend-bullish'
            elif 'Bearish' in signal['trend'] or 'Weakness' in signal['trend']:
                css_class = 'warning-signal' if is_active else 'trend-bearish'
            else:
                css_class = 'trend-volatile'
            
            active_text = " 🔥 LIVE NOW" if is_active else ""
            if signal['strength'] == 'Maximum':
                active_text += " ⭐ PEAK"
            
            with active_cols[col_idx]:
                st.markdown(f"""
                <div class="{css_class}">
                    <strong>{signal['time']} - {signal['planet']}{active_text}</strong><br>
                    <strong>💵 USDINR:</strong> {signal['usdinr']} | <strong>₿ BTC:</strong> {signal['btc']} | <strong>📊 DXY:</strong> {signal['dxy']}<br>
                    <strong>Trend:</strong> {signal['trend']} | <strong>Strength:</strong> {signal['strength']}
                </div>
                """, unsafe_allow_html=True)
        
        # Evening Hours (4 PM - 11:55 PM)
        st.markdown("#### 🌙 Evening Session (4:00 PM - 11:55 PM)")
        evening_cols = st.columns(2)
        
        for idx, signal in enumerate(evening_hours):
            col_idx = idx % 2
            is_active = current_hour >= int(signal['time'].split('-')[0].split(':')[0]) and current_hour < int(signal['time'].split('-')[1].split(':')[0])
            
            if 'Bullish' in signal['trend'] or 'Recovery' in signal['trend'] or 'Surge' in signal['trend']:
                css_class = 'live-signal' if is_active else 'trend-bullish'
            elif 'Bearish' in signal['trend'] or 'Weakness' in signal['trend']:
                css_class = 'warning-signal' if is_active else 'trend-bearish'
            else:
                css_class = 'trend-volatile'
            
            active_text = " 🔥 LIVE NOW" if is_active else ""
            if signal['strength'] == 'Maximum':
                active_text += " ⭐ PEAK"
            
            with evening_cols[col_idx]:
                st.markdown(f"""
                <div class="{css_class}">
                    <strong>{signal['time']} - {signal['planet']}{active_text}</strong><br>
                    <strong>💵 USDINR:</strong> {signal['usdinr']} | <strong>₿ BTC:</strong> {signal['btc']} | <strong>📊 DXY:</strong> {signal['dxy']}<br>
                    <strong>Trend:</strong> {signal['trend']} | <strong>Strength:</strong> {signal['strength']}
                </div>
                """, unsafe_allow_html=True)
    
    elif market_type == "global":
        st.markdown("### 📊 DOW JONES • 💻 NASDAQ • 📈 S&P 500 - Complete Planetary Transit")
        
        # Group signals by time periods
        early_morning = [s for s in signals if int(s['time'].split('-')[0].split(':')[0]) < 9]
        market_hours = [s for s in signals if 9 <= int(s['time'].split('-')[0].split(':')[0]) < 16]
        evening_hours = [s for s in signals if int(s['time'].split('-')[0].split(':')[0]) >= 16]
        
        # Early Morning (5 AM - 9 AM)
        st.markdown("#### 🌅 Pre-Market Session (5:00 AM - 9:00 AM)")
        early_cols = st.columns(2)
        
        for idx, signal in enumerate(early_morning):
            col_idx = idx % 2
            is_active = current_hour >= int(signal['time'].split('-')[0].split(':')[0]) and current_hour < int(signal['time'].split('-')[1].split(':')[0])
            
            if 'Strength' in signal['trend'] or 'Bullish' in signal['trend']:
                css_class = 'live-signal' if is_active else 'trend-bullish'
            elif 'Weakness' in signal['trend']:
                css_class = 'warning-signal' if is_active else 'trend-bearish'
            else:
                css_class = 'trend-volatile'
            
            active_text = " 🔥 LIVE NOW" if is_active else ""
            
            with early_cols[col_idx]:
                st.markdown(f"""
                <div class="{css_class}">
                    <strong>{signal['time']} - {signal['planet']}{active_text}</strong><br>
                    <strong>📊 DOW:</strong> {signal['dow']} | <strong>💻 NASDAQ:</strong> {signal['nasdaq']} | <strong>📈 S&P500:</strong> {signal['sp500']}<br>
                    <strong>Trend:</strong> {signal['trend']} | <strong>Strength:</strong> {signal['strength']}
                </div>
                """, unsafe_allow_html=True)
        
        # Market Hours (9 AM - 4 PM)
        st.markdown("#### 🇺🇸 US Market Hours (9:00 AM - 4:00 PM IST)")
        market_cols = st.columns(2)
        
        for idx, signal in enumerate(market_hours):
            col_idx = idx % 2
            is_active = current_hour >= int(signal['time'].split('-')[0].split(':')[0]) and current_hour < int(signal['time'].split('-')[1].split(':')[0])
            
            if 'Strength' in signal['trend'] or 'Rally' in signal['trend'] or 'Bullish' in signal['trend']:
                css_class = 'live-signal' if is_active else 'trend-bullish'
            elif 'Weakness' in signal['trend'] or 'Pressure' in signal['trend']:
                css_class = 'warning-signal' if is_active else 'trend-bearish'
            else:
                css_class = 'trend-volatile'
            
            active_text = " 🔥 LIVE NOW" if is_active else ""
            if signal['strength'] == 'Excellent':
                active_text += " ⭐ PEAK"
            
            with market_cols[col_idx]:
                st.markdown(f"""
                <div class="{css_class}">
                    <strong>{signal['time']} - {signal['planet']}{active_text}</strong><br>
                    <strong>📊 DOW:</strong> {signal['dow']} | <strong>💻 NASDAQ:</strong> {signal['nasdaq']} | <strong>📈 S&P500:</strong> {signal['sp500']}<br>
                    <strong>Trend:</strong> {signal['trend']} | <strong>Strength:</strong> {signal['strength']}
                </div>
                """, unsafe_allow_html=True)
        
        # Evening Hours (4 PM - 11:55 PM)
        st.markdown("#### 🌙 After Hours & Evening (4:00 PM - 11:55 PM)")
        evening_cols = st.columns(2)
        
        for idx, signal in enumerate(evening_hours):
            col_idx = idx % 2
            is_active = current_hour >= int(signal['time'].split('-')[0].split(':')[0]) and current_hour < int(signal['time'].split('-')[1].split(':')[0])
            
            if 'Rally' in signal['trend'] or 'Strength' in signal['trend'] or 'Recovery' in signal['trend']:
                css_class = 'live-signal' if is_active else 'trend-bullish'
            elif 'Weakness' in signal['trend']:
                css_class = 'warning-signal' if is_active else 'trend-bearish'
            else:
                css_class = 'trend-volatile'
            
            active_text = " 🔥 LIVE NOW" if is_active else ""
            if signal['strength'] == 'Maximum':
                active_text += " ⭐ PEAK"
            
            with evening_cols[col_idx]:
                st.markdown(f"""
                <div class="{css_class}">
                    <strong>{signal['time']} - {signal['planet']}{active_text}</strong><br>
                    <strong>📊 DOW:</strong> {signal['dow']} | <strong>💻 NASDAQ:</strong> {signal['nasdaq']} | <strong>📈 S&P500:</strong> {signal['sp500']}<br>
                    <strong>Trend:</strong> {signal['trend']} | <strong>Strength:</strong> {signal['strength']}
                </div>
                """, unsafe_allow_html=True)
    
    elif market_type == "equity":
        st.markdown("### 📈 NIFTY 50 • 🏦 BANKNIFTY - Indian Market Planetary Transit")
        
        st.markdown("#### 🇮🇳 Indian Equity Market Hours (9:15 AM - 3:30 PM)")
        equity_cols = st.columns(2)
        
        for idx, signal in enumerate(signals):
            col_idx = idx % 2
            is_active = current_hour >= int(signal['time'].split('-')[0].split(':')[0]) and current_hour < int(signal['time'].split('-')[1].split(':')[0])
            
            if 'Bullish' in signal['trend'] or 'Strength' in signal['trend']:
                css_class = 'live-signal' if is_active else 'trend-bullish'
            elif 'Weakness' in signal['trend'] or 'Pressure' in signal['trend']:
                css_class = 'warning-signal' if is_active else 'trend-bearish'
            else:
                css_class = 'trend-volatile'
            
            active_text = " 🔥 LIVE NOW" if is_active else ""
            if signal['strength'] == 'Maximum':
                active_text += " ⭐ PEAK BANKING HOUR"
            elif signal['time'] == '09:15-10:15':
                active_text += " 🔔 OPENING"
            elif signal['time'] == '15:15-15:30':
                active_text += " 🔔 CLOSING"
            
            with equity_cols[col_idx]:
                st.markdown(f"""
                <div class="{css_class}">
                    <strong>{signal['time']} - {signal['planet']}{active_text}</strong><br>
                    <strong>📈 NIFTY:</strong> {signal['nifty']} | <strong>🏦 BANKNIFTY:</strong> {signal['banknifty']}<br>
                    <strong>Trend:</strong> {signal['trend']} | <strong>Strength:</strong> {signal['strength']}
                </div>
                """, unsafe_allow_html=True)

def generate_symbol_data(symbol_name):
    """Generate realistic data for any custom symbol"""
    # Create realistic price based on symbol type
    if 'BANK' in symbol_name.upper() or symbol_name.upper() in ['HDFC', 'ICICI', 'SBI', 'KOTAK', 'AXIS']:
        base_price = random.uniform(800, 1800)
    elif symbol_name.upper() in ['RELIANCE', 'TCS', 'INFOSYS']:
        base_price = random.uniform(2500, 4000)
    elif 'PHARMA' in symbol_name.upper() or symbol_name.upper() in ['SUN PHARMA', 'DR REDDY', 'CIPLA']:
        base_price = random.uniform(600, 1500)
    elif 'AUTO' in symbol_name.upper() or symbol_name.upper() in ['TATA MOTORS', 'MARUTI']:
        base_price = random.uniform(300, 800)
    else:
        base_price = random.uniform(150, 2000)
    
    change_percent = random.uniform(-5, 5)
    high_price = base_price * (1 + abs(change_percent)/100 + random.uniform(0.01, 0.03))
    low_price = base_price * (1 - abs(change_percent)/100 - random.uniform(0.01, 0.03))
    
    return {
        'price': base_price,
        'change': change_percent,
        'high': high_price,
        'low': low_price,
        'volume': random.randint(50000, 5000000),
        'market_cap': random.randint(10000, 500000)  # in crores
    }

def create_symbol_intraday_signals(symbol_name):
    """Generate symbol-specific intraday signals based on symbol characteristics"""
    
    # Determine sector characteristics
    if 'BANK' in symbol_name.upper():
        sector_type = 'banking'
    elif 'IT' in symbol_name.upper() or symbol_name.upper() in ['TCS', 'INFOSYS', 'WIPRO']:
        sector_type = 'tech'
    elif 'PHARMA' in symbol_name.upper():
        sector_type = 'pharma'
    elif 'AUTO' in symbol_name.upper():
        sector_type = 'auto'
    elif 'METAL' in symbol_name.upper():
        sector_type = 'metal'
    else:
        sector_type = 'general'
    
    # Base signals adjusted for sector
    if sector_type == 'banking':
        signals = [
            {'time': '09:15-10:15', 'planet': 'Venus ♀', 'signal': 'BUY', 'target': '+1.2%', 'sl': '-0.4%', 'trend': 'Bullish'},
            {'time': '10:15-11:15', 'planet': 'Sun ☀️', 'signal': 'STRONG BUY', 'target': '+1.8%', 'sl': '-0.5%', 'trend': 'Strong Bullish'},
            {'time': '11:15-12:15', 'planet': 'Mercury ☿', 'signal': 'HOLD', 'target': '+0.5%', 'sl': '-0.3%', 'trend': 'Neutral'},
            {'time': '12:15-13:15', 'planet': 'Saturn ♄', 'signal': 'SELL', 'target': '-0.8%', 'sl': '+0.3%', 'trend': 'Bearish'},
            {'time': '13:15-14:15', 'planet': 'Jupiter ♃', 'signal': 'PEAK BUY', 'target': '+2.5%', 'sl': '-0.6%', 'trend': 'Peak Bullish'},
            {'time': '14:15-15:15', 'planet': 'Mars ♂️', 'signal': 'VOLATILE', 'target': '±1.8%', 'sl': '±0.6%', 'trend': 'High Volatility'},
            {'time': '15:15-15:30', 'planet': 'Sun ☀️', 'signal': 'BUY', 'target': '+1.0%', 'sl': '-0.3%', 'trend': 'Closing Strength'}
        ]
    elif sector_type == 'tech':
        signals = [
            {'time': '09:15-10:15', 'planet': 'Venus ♀', 'signal': 'HOLD', 'target': '+0.8%', 'sl': '-0.4%', 'trend': 'Cautious'},
            {'time': '10:15-11:15', 'planet': 'Sun ☀️', 'signal': 'BUY', 'target': '+1.2%', 'sl': '-0.4%', 'trend': 'Bullish'},
            {'time': '11:15-12:15', 'planet': 'Mercury ☿', 'signal': 'SELL', 'target': '-1.2%', 'sl': '+0.4%', 'trend': 'Tech Pressure'},
            {'time': '12:15-13:15', 'planet': 'Saturn ♄', 'signal': 'STRONG SELL', 'target': '-1.8%', 'sl': '+0.6%', 'trend': 'Strong Bearish'},
            {'time': '13:15-14:15', 'planet': 'Jupiter ♃', 'signal': 'BUY', 'target': '+1.5%', 'sl': '-0.5%', 'trend': 'Recovery'},
            {'time': '14:15-15:15', 'planet': 'Mars ♂️', 'signal': 'VOLATILE', 'target': '±2.2%', 'sl': '±0.7%', 'trend': 'Extreme Volatility'},
            {'time': '15:15-15:30', 'planet': 'Sun ☀️', 'signal': 'HOLD', 'target': '+0.6%', 'sl': '-0.3%', 'trend': 'Neutral Close'}
        ]
    elif sector_type == 'pharma':
        signals = [
            {'time': '09:15-10:15', 'planet': 'Venus ♀', 'signal': 'BUY', 'target': '+1.0%', 'sl': '-0.3%', 'trend': 'Bullish'},
            {'time': '10:15-11:15', 'planet': 'Sun ☀️', 'signal': 'STRONG BUY', 'target': '+2.0%', 'sl': '-0.6%', 'trend': 'Strong Bullish'},
            {'time': '11:15-12:15', 'planet': 'Mercury ☿', 'signal': 'BUY', 'target': '+1.3%', 'sl': '-0.4%', 'trend': 'Bullish'},
            {'time': '12:15-13:15', 'planet': 'Saturn ♄', 'signal': 'CAUTION', 'target': '±0.8%', 'sl': '±0.3%', 'trend': 'Mixed'},
            {'time': '13:15-14:15', 'planet': 'Jupiter ♃', 'signal': 'BUY', 'target': '+1.5%', 'sl': '-0.5%', 'trend': 'Good'},
            {'time': '14:15-15:15', 'planet': 'Mars ♂️', 'signal': 'SELL', 'target': '-1.2%', 'sl': '+0.4%', 'trend': 'Bearish'},
            {'time': '15:15-15:30', 'planet': 'Sun ☀️', 'signal': 'HOLD', 'target': '+0.5%', 'sl': '-0.2%', 'trend': 'Stable'}
        ]
    else:
        # General signals for other sectors
        signals = [
            {'time': '09:15-10:15', 'planet': 'Venus ♀', 'signal': 'BUY', 'target': '+1.0%', 'sl': '-0.3%', 'trend': 'Bullish'},
            {'time': '10:15-11:15', 'planet': 'Sun ☀️', 'signal': 'BUY', 'target': '+1.2%', 'sl': '-0.4%', 'trend': 'Bullish'},
            {'time': '11:15-12:15', 'planet': 'Mercury ☿', 'signal': 'HOLD', 'target': '+0.6%', 'sl': '-0.3%', 'trend': 'Neutral'},
            {'time': '12:15-13:15', 'planet': 'Saturn ♄', 'signal': 'SELL', 'target': '-0.9%', 'sl': '+0.3%', 'trend': 'Bearish'},
            {'time': '13:15-14:15', 'planet': 'Jupiter ♃', 'signal': 'BUY', 'target': '+1.5%', 'sl': '-0.5%', 'trend': 'Recovery'},
            {'time': '14:15-15:15', 'planet': 'Mars ♂️', 'signal': 'VOLATILE', 'target': '±1.5%', 'sl': '±0.5%', 'trend': 'High Volatility'},
            {'time': '15:15-15:30', 'planet': 'Sun ☀️', 'signal': 'BUY', 'target': '+0.8%', 'sl': '-0.3%', 'trend': 'Closing Strength'}
        ]
    
    return signals

def display_symbol_signals(symbol_name, signals, current_hour):
    """Display symbol-specific planetary signals"""
    st.markdown(f"### 📊 {symbol_name} - Intraday Planetary Transit Signals")
    
    # Market Hours Display
    st.markdown("#### 🇮🇳 Indian Market Hours (9:15 AM - 3:30 PM)")
    
    signal_cols = st.columns(2)
    
    for idx, signal in enumerate(signals):
        col_idx = idx % 2
        is_active = current_hour >= int(signal['time'].split('-')[0].split(':')[0]) and current_hour < int(signal['time'].split('-')[1].split(':')[0])
        
        if signal['trend'] in ['Bullish', 'Strong Bullish', 'Peak Bullish', 'Recovery']:
            css_class = 'live-signal' if is_active else 'trend-bullish'
        elif signal['trend'] in ['Bearish', 'Strong Bearish', 'Tech Pressure']:
            css_class = 'warning-signal' if is_active else 'trend-bearish'
        else:
            css_class = 'trend-volatile'
        
        active_text = " 🔥 LIVE NOW" if is_active else ""
        if 'PEAK' in signal['signal']:
            active_text += " ⭐ PEAK HOUR"
        elif signal['time'] == '09:15-10:15':
            active_text += " 🔔 OPENING"
        elif signal['time'] == '15:15-15:30':
            active_text += " 🔔 CLOSING"
        
        with signal_cols[col_idx]:
            st.markdown(f"""
            <div class="{css_class}">
                <strong>{signal['time']} - {signal['planet']}{active_text}</strong><br>
                <strong>📊 {symbol_name}:</strong> <span style="background: {'#28a745' if 'BUY' in signal['signal'] else '#dc3545' if 'SELL' in signal['signal'] else '#ffc107'}; color: white; padding: 2px 6px; border-radius: 4px; font-weight: bold;">{signal['signal']}</span><br>
                <strong>Target:</strong> {signal['target']} | <strong>SL:</strong> {signal['sl']} | <strong>Trend:</strong> {signal['trend']}
            </div>
            """, unsafe_allow_html=True)

def generate_symbol_weekly_data(symbol_name):
    """Generate weekly performance data for custom symbol"""
    weekly_data = []
    today = datetime.now(ist_tz)
    week_start = today - timedelta(days=today.weekday())
    
    planets = ['Sun ☀️', 'Moon 🌙', 'Mars ♂️', 'Mercury ☿', 'Jupiter ♃', 'Venus ♀', 'Saturn ♄']
    
    # Generate sector-appropriate trends
    if 'BANK' in symbol_name.upper():
        trends = ['Bullish', 'Strong Bullish', 'Bearish', 'Neutral', 'Peak Bullish', 'Bullish', 'Bearish']
    elif 'IT' in symbol_name.upper():
        trends = ['Bearish', 'Volatile', 'Strong Bearish', 'Neutral', 'Recovery', 'Bullish', 'Bearish']
    elif 'PHARMA' in symbol_name.upper():
        trends = ['Strong Bullish', 'Bullish', 'Neutral', 'Bullish', 'Strong Bullish', 'Volatile', 'Neutral']
    else:
        trends = ['Bullish', 'Volatile', 'Bearish', 'Neutral', 'Bullish', 'Bullish', 'Bearish']
    
    for i in range(7):
        current_date = week_start + timedelta(days=i)
        target_change = random.uniform(-3, 4) if trends[i] == 'Volatile' else random.uniform(-2, 3)
        
        weekly_data.append({
            'date': current_date.strftime('%Y-%m-%d'),
            'day': current_date.strftime('%A'),
            'short_day': current_date.strftime('%a'),
            'day_num': current_date.strftime('%d'),
            'month': current_date.strftime('%m'),
            'planet': planets[i],
            'trend': trends[i],
            'target': f"{'+' if target_change > 0 else ''}{target_change:.1f}%",
            'is_today': current_date.date() == today.date(),
            'rating': 'Strong Buy' if trends[i] in ['Strong Bullish', 'Peak Bullish'] else 'Buy' if trends[i] == 'Bullish' else 'Sell' if trends[i] in ['Bearish', 'Strong Bearish'] else 'Hold'
        })
    
    return weekly_data

def generate_monthly_calendar(market_name):
    """Generate monthly planetary calendar for sectors"""
    ist_tz = pytz.timezone('Asia/Kolkata')
    today = datetime.now(ist_tz)
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

def generate_symbol_monthly_data(symbol_name):
    """Generate monthly performance data for custom symbol"""
    today = datetime.now(ist_tz)
    month_start = today.replace(day=1)
    
    if month_start.month == 12:
        next_month = month_start.replace(year=month_start.year + 1, month=1)
    else:
        next_month = month_start.replace(month=month_start.month + 1)
    month_end = next_month - timedelta(days=1)
    
    monthly_data = []
    planets = ['Sun ☀️', 'Moon 🌙', 'Mars ♂️', 'Mercury ☿', 'Jupiter ♃', 'Venus ♀', 'Saturn ♄', 'Rahu ☊', 'Ketu ☋']
    
    # Generate sector-appropriate monthly trends
    if 'BANK' in symbol_name.upper():
        base_trends = ['Strong Bullish', 'Bullish', 'Bearish', 'Neutral', 'Peak Bullish', 'Bullish', 'Volatile', 'Bearish', 'Recovery']
    elif 'IT' in symbol_name.upper():
        base_trends = ['Bearish', 'Volatile', 'Strong Bearish', 'Weak', 'Recovery', 'Neutral', 'Bearish', 'Volatile', 'Weak']
    elif 'PHARMA' in symbol_name.upper():
        base_trends = ['Strong Bullish', 'Bullish', 'Neutral', 'Bullish', 'Strong Bullish', 'Volatile', 'Bullish', 'Neutral', 'Strong Bullish']
    else:
        base_trends = ['Bullish', 'Volatile', 'Bearish', 'Neutral', 'Bullish', 'Bullish', 'Bearish', 'Volatile', 'Neutral']
    
    current_date = month_start
    day_count = 0
    
    while current_date <= month_end:
        trend_idx = day_count % len(base_trends)
        planet_idx = day_count % len(planets)
        
        target_change = random.uniform(-2.5, 3.5)
        
        monthly_data.append({
            'date': current_date.strftime('%Y-%m-%d'),
            'day': current_date.strftime('%a'),
            'day_num': current_date.strftime('%d'),
            'month': current_date.strftime('%m'),
            'planet': planets[planet_idx],
            'trend': base_trends[trend_idx],
            'target': f"{'+' if target_change > 0 else ''}{target_change:.1f}%",
            'is_today': current_date.date() == today.date(),
            'rating': 'Strong Buy' if base_trends[trend_idx] in ['Strong Bullish', 'Peak Bullish'] else 'Buy' if base_trends[trend_idx] == 'Bullish' else 'Sell' if base_trends[trend_idx] in ['Bearish', 'Strong Bearish'] else 'Hold'
        })
        
        current_date += timedelta(days=1)
        day_count += 1
    
    return monthly_data

def generate_weekly_calendar(market_name):
    """Generate weekly planetary calendar for sectors"""
    ist_tz = pytz.timezone('Asia/Kolkata')
    today = datetime.now(ist_tz)
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
        st.markdown(f'<div class="timeframe-header"><h4>⚡ {market_name} - Today\'s Intraday Planetary Signals</h4></div>', unsafe_allow_html=True)
        
        # Show specific market details based on type
        if market_type == "equity":
            # Display NIFTY and BANKNIFTY details
            equity_col1, equity_col2 = st.columns(2)
            
            with equity_col1:
                nifty_data = st.session_state.market_data['NIFTY']
                color_class = "positive" if nifty_data['change'] >= 0 else "negative"
                arrow = "▲" if nifty_data['change'] >= 0 else "▼"
                
                st.markdown(f"""
                <div class="sector-price-card">
                    <h3 style="margin: 0 0 10px 0; color: #333;">📈 NIFTY 50</h3>
                    <h1 style="margin: 0; color: #007bff;">{nifty_data['price']:,.2f}</h1>
                    <h3 class="{color_class}" style="margin: 5px 0;">{arrow} {abs(nifty_data['change']):.2f}%</h3>
                    <p style="margin: 0;"><strong>High:</strong> {nifty_data['high']:,.2f} | <strong>Low:</strong> {nifty_data['low']:,.2f}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with equity_col2:
                banknifty_data = st.session_state.market_data['BANKNIFTY']
                color_class = "positive" if banknifty_data['change'] >= 0 else "negative"
                arrow = "▲" if banknifty_data['change'] >= 0 else "▼"
                
                st.markdown(f"""
                <div class="sector-price-card">
                    <h3 style="margin: 0 0 10px 0; color: #333;">🏦 BANKNIFTY</h3>
                    <h1 style="margin: 0; color: #007bff;">{banknifty_data['price']:,.2f}</h1>
                    <h3 class="{color_class}" style="margin: 5px 0;">{arrow} {abs(banknifty_data['change']):.2f}%</h3>
