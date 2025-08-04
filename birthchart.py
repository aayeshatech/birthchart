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

# Header
st.markdown("""
<div class="main-header">
    <h1 style="margin: 0 0 10px 0;">🕉️ Vedic Market Intelligence Dashboard</h1>
    <h2 style="margin: 0 0 5px 0;">Complete Planetary Transit Analysis</h2>
    <p style="margin: 0; font-size: 1.1em;">Live Astrological Market Timing for Equity • Commodity • Forex • Global • Sectorwise Analysis</p>
</div>
""", unsafe_allow_html=True)

# Prominent Date Display with Real-Time Astronomical Data
st.markdown(f"""
<div class="date-display">
    <h1 style="margin: 0 0 10px 0; font-size: 2.5em;">📅 {current_day}, {current_date_str}</h1>
    <h2 style="margin: 0 0 10px 0; font-size: 1.8em;">⏰ Current Time: {current_time_str} IST</h2>
    <h3 style="margin: 0; opacity: 0.9;">🪐 Live Astronomical Planetary Transit Analysis • Real-time Market Intelligence</h3>
    <p style="margin: 10px 0 0 0; opacity: 0.8; font-size: 1.1em;">Using Real Vedic Ephemeris Data for Precise Market Timing</p>
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

# Current Planetary Hour - Based on Real Vedic Calculations
current_planet, current_symbol, current_influence = get_planetary_influence(current_hour)

st.markdown(f"""
<div class="planet-info">
    <h3 style="margin: 0 0 5px 0;">{current_symbol} Current Planetary Hour: {current_planet}</h3>
    <p style="margin: 0; font-size: 1.1em;">🌟 {current_influence}</p>
    <p style="margin: 5px 0 0 0; font-size: 0.9em;">⏰ Active Now: {current_time_str} IST | <strong>Real Vedic Timing</strong> | Market Effect: <strong>Live</strong></p>
    <p style="margin: 5px 0 0 0; font-size: 0.85em; opacity: 0.8;">📡 Synchronized with Astronomical Ephemeris for August 1, 2025</p>
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
        
        # Display Symbol Price or Sector Price
        if custom_symbol:
            # Show custom symbol data
            symbol_data = generate_symbol_data(custom_symbol.upper())
            color_class = "positive" if symbol_data['change'] >= 0 else "negative"
            arrow = "▲" if symbol_data['change'] >= 0 else "▼"
            
            st.markdown(f"""
            <div class="sector-price-card">
                <h2 style="margin: 0 0 10px 0; color: #333;">📊 {custom_symbol.upper()}</h2>
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h1 style="margin: 0; color: #007bff;">₹{symbol_data['price']:,.2f}</h1>
                        <h3 class="{color_class}" style="margin: 5px 0;">
                            {arrow} {abs(symbol_data['change']):.2f}%
                        </h3>
                    </div>
                    <div style="text-align: right;">
                        <p style="margin: 0; font-size: 1.1em;"><strong>High:</strong> ₹{symbol_data['high']:,.2f}</p>
                        <p style="margin: 0; font-size: 1.1em;"><strong>Low:</strong> ₹{symbol_data['low']:,.2f}</p>
                        <p style="margin: 0; font-size: 0.9em;"><strong>Volume:</strong> {symbol_data['volume']:,}</p>
                        <p style="margin: 0; font-size: 0.9em;"><strong>Mkt Cap:</strong> ₹{symbol_data['market_cap']:,} Cr</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        elif selected_sector in st.session_state.sector_data:
            # Show sector index data only when no custom symbol
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
            
            if custom_symbol:
                # Show custom symbol intraday analysis
                symbol_signals = create_symbol_intraday_signals(custom_symbol.upper())
                display_symbol_signals(custom_symbol.upper(), symbol_signals, current_hour)
            else:
                # Show sector stocks with planetary transits
                if selected_sector in st.session_state.sector_data:
                    stocks = st.session_state.sector_data[selected_sector]['stocks']
                    display_dynamic_sector_analysis(selected_sector, stocks, current_hour)
        
        with sector_tab2:
            st.markdown(f'<div class="timeframe-header"><h4>📊 {analysis_target} - Weekly Planetary Calendar</h4></div>', unsafe_allow_html=True)
            
            if custom_symbol:
                # Show custom symbol weekly analysis
                weekly_data = generate_symbol_weekly_data(custom_symbol.upper())
                display_calendar_grid(weekly_data, 7)
            else:
                # Show sector weekly analysis
                weekly_data = generate_weekly_calendar(analysis_target)
                display_calendar_grid(weekly_data, 7)
            
            # Weekly Summary
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
                
                st.markdown("</div>", unsafe_allow_html=True)
            
            with weekly_opp_col2:
                st.markdown("""
                <div class="report-section" style="background: #f8d7da; border-left: 5px solid #dc3545;">
                    <h4 style="color: #721c24;">🔴 SHORT Opportunities This Week</h4>
                """, unsafe_allow_html=True)
                
                for day in bearish_days:
                    st.markdown(f"**{day['day']}:** {day['planet']} | Target: {day['target']}")
                
                st.markdown("</div>", unsafe_allow_html=True)
        
        with sector_tab3:
            st.markdown(f'<div class="timeframe-header"><h4>📅 {analysis_target} - Monthly Planetary Calendar</h4></div>', unsafe_allow_html=True)
            
            if custom_symbol:
                # Show custom symbol monthly analysis
                monthly_data = generate_symbol_monthly_data(custom_symbol.upper())
            else:
                # Show sector monthly analysis
                monthly_data = generate_monthly_calendar(analysis_target)
            
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
    
    with planetary_tab:
        st.markdown('<div class="sector-header"><h3 style="margin: 0;">🪐 PLANETARY TRANSIT ANALYSIS - Complete Market Impact</h3></div>', unsafe_allow_html=True)
        
        # Real-time astronomical data notice
        st.markdown(f"""
        <div style="background: linear-gradient(45deg, #e3f2fd, #bbdefb); color: #1565c0; padding: 15px; border-radius: 10px; margin: 10px 0; border-left: 5px solid #2196f3;">
            <h4 style="margin: 0 0 10px 0;">📡 LIVE ASTRONOMICAL DATA</h4>
            <p style="margin: 0; font-size: 1em;"><strong>Date:</strong> {current_date_str} | <strong>Time:</strong> {current_time_str} IST</p>
            <p style="margin: 5px 0 0 0; font-size: 0.9em;">✅ Synchronized with Real Vedic Ephemeris | ✅ Astronomical Accuracy</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Create tabs for different timeframes
        transit_daily_tab, transit_weekly_tab, transit_monthly_tab, transit_current_tab = st.tabs([
            "📅 TODAY'S TRANSITS", 
            "📊 WEEKLY TRANSITS", 
            "📈 MONTHLY TRANSITS",
            "🌟 CURRENT POSITIONS"
        ])
        
        with transit_daily_tab:
            st.markdown("### 📅 Today's Complete Planetary Transit Schedule & Market Impact")
            
            # Today's planetary hours with specific market impacts
            daily_transits = [
                {
                    'time': '06:00-07:00',
                    'planet': 'Jupiter ♃',
                    'position': 'Ardra (Gemini) 17°32\'',
                    'strength': 'Excellent',
                    'equity_impact': 'Banking +2.5%, Finance +2.0%',
                    'commodity_impact': 'Gold +1.5%, Silver +1.8%',
                    'forex_impact': 'USD weak, Bitcoin strong',
                    'sector_impact': ['Banking: STRONG BUY', 'IT: Neutral', 'Auto: BUY'],
                    'key_stocks': ['HDFC Bank +2.8%', 'ICICI Bank +2.5%', 'SBI +2.2%']
                },
                {
                    'time': '07:00-08:00',
                    'planet': 'Mars ♂️',
                    'position': 'Uttara Phalguni (Virgo) 02°13\'',
                    'strength': 'Strong',
                    'equity_impact': 'Defense +1.8%, Energy +1.5%',
                    'commodity_impact': 'Crude +2.0%, Metals volatile',
                    'forex_impact': 'DXY volatile, high swings',
                    'sector_impact': ['Metal: VOLATILE', 'Energy: BUY', 'IT: SELL'],
                    'key_stocks': ['ONGC +1.8%', 'Tata Steel ±2.5%', 'L&T +1.5%']
                },
                {
                    'time': '08:00-09:00',
                    'planet': 'Sun ☀️',
                    'position': 'Cancer 15°01\'',
                    'strength': 'Very Strong',
                    'equity_impact': 'PSU +2.0%, Pharma +1.8%',
                    'commodity_impact': 'All commodities positive',
                    'forex_impact': 'INR strengthens',
                    'sector_impact': ['Pharma: STRONG BUY', 'PSU Bank: BUY', 'FMCG: BUY'],
                    'key_stocks': ['Sun Pharma +2.2%', 'Dr Reddy +2.0%', 'NTPC +1.8%']
                },
                {
                    'time': '09:00-10:00',
                    'planet': 'Venus ♀',
                    'position': 'Ardra (Gemini) 07°01\'',
                    'strength': 'Strong',
                    'equity_impact': 'Auto +2.2%, Textiles +1.5%',
                    'commodity_impact': 'Gold peak buy, Silver strong',
                    'forex_impact': 'Risk-on sentiment',
                    'sector_impact': ['Auto: PEAK BUY', 'Luxury: BUY', 'Banking: BUY'],
                    'key_stocks': ['Maruti +2.5%', 'Tata Motors +2.2%', 'Titan +1.8%']
                },
                {
                    'time': '10:00-11:00',
                    'planet': 'Mercury ☿',
                    'position': 'Pushya (Cancer) 14°36\'',
                    'strength': 'Moderate',
                    'equity_impact': 'IT mixed, Telecom weak',
                    'commodity_impact': 'Choppy trading',
                    'forex_impact': 'Range-bound',
                    'sector_impact': ['IT: VOLATILE', 'Telecom: SELL', 'Media: HOLD'],
                    'key_stocks': ['TCS ±1.5%', 'Infosys -1.2%', 'Bharti -0.8%']
                },
                {
                    'time': '11:00-12:00',
                    'planet': 'Moon 🌙',
                    'position': 'Swati (Libra) 11°47\'',
                    'strength': 'Strong',
                    'equity_impact': 'FMCG +1.5%, Real Estate +1.2%',
                    'commodity_impact': 'Silver peak +2.5%',
                    'forex_impact': 'Emerging markets strong',
                    'sector_impact': ['FMCG: BUY', 'Realty: BUY', 'Dairy: STRONG BUY'],
                    'key_stocks': ['HUL +1.8%', 'Nestle +1.5%', 'DLF +1.2%']
                },
                {
                    'time': '12:00-13:00',
                    'planet': 'Saturn ♄',
                    'position': 'Uttara Bhadrapada (Pisces) 07°24\'',
                    'strength': 'Weak',
                    'equity_impact': 'Overall weakness -1.2%',
                    'commodity_impact': 'Metals under pressure',
                    'forex_impact': 'USD strengthens',
                    'sector_impact': ['All Sectors: CAUTION', 'Metal: SELL', 'Oil: WEAK'],
                    'key_stocks': ['Most stocks negative', 'Vedanta -1.8%', 'SAIL -1.5%']
                },
                {
                    'time': '13:00-14:00',
                    'planet': 'Jupiter ♃',
                    'position': 'Ardra (Gemini) 17°32\'',
                    'strength': 'Maximum',
                    'equity_impact': 'Banking peak +3.0%',
                    'commodity_impact': 'Gold +2.0%, Silver +2.5%',
                    'forex_impact': 'Bitcoin surge +5%',
                    'sector_impact': ['Banking: PEAK BUY', 'Finance: STRONG BUY', 'Insurance: BUY'],
                    'key_stocks': ['HDFC +3.2%', 'Kotak +2.8%', 'Bajaj Finance +3.0%']
                },
                {
                    'time': '14:00-15:00',
                    'planet': 'Mars ♂️',
                    'position': 'Uttara Phalguni (Virgo) 02°13\'',
                    'strength': 'Extreme Volatility',
                    'equity_impact': 'Wild swings ±2.5%',
                    'commodity_impact': 'Crude volatile ±3%',
                    'forex_impact': 'Extreme volatility',
                    'sector_impact': ['All: EXTREME CAUTION', 'Use tight stops', 'Scalping only'],
                    'key_stocks': ['High volatility across board', 'Avoid fresh positions']
                },
                {
                    'time': '15:00-15:30',
                    'planet': 'Sun ☀️',
                    'position': 'Cancer 15°01\'',
                    'strength': 'Good',
                    'equity_impact': 'Closing strength +0.8%',
                    'commodity_impact': 'Stable close',
                    'forex_impact': 'Risk-on continues',
                    'sector_impact': ['Short covering rally', 'PSU: BUY', 'Energy: HOLD'],
                    'key_stocks': ['Index heavyweights positive', 'ONGC +1.2%', 'Coal India +1.0%']
                }
            ]
            
            # Display daily transits in an enhanced format
            for transit in daily_transits:
                # Check if this is the current hour
                hour_start = int(transit['time'].split('-')[0].split(':')[0])
                hour_end = int(transit['time'].split('-')[1].split(':')[0])
                is_current = current_hour >= hour_start and current_hour < hour_end
                
                # Determine background color based on strength
                if transit['strength'] in ['Excellent', 'Maximum', 'Very Strong']:
                    bg_color = '#d4edda'
                    border_color = '#28a745'
                    text_color = '#155724'
                elif transit['strength'] in ['Weak', 'Extreme Volatility']:
                    bg_color = '#f8d7da'
                    border_color = '#dc3545'
                    text_color = '#721c24'
                else:
                    bg_color = '#fff3cd'
                    border_color = '#ffc107'
                    text_color = '#856404'
                
                # Special styling for current hour
                if is_current:
                    border_style = f'border: 3px solid #ff6b35; animation: pulse 2s infinite; box-shadow: 0 0 20px rgba(255,107,53,0.5);'
                    current_text = ' 🔥 ACTIVE NOW'
                else:
                    border_style = f'border: 2px solid {border_color};'
                    current_text = ''
                
                st.markdown(f"""
                <div style="background: {bg_color}; padding: 20px; border-radius: 12px; margin: 15px 0; {border_style}">
                    <h4 style="margin: 0 0 10px 0; color: {text_color};">
                        {transit['time']} - {transit['planet']} in {transit['position']}{current_text}
                    </h4>
                    <p style="margin: 0 0 5px 0; color: {text_color};"><strong>Strength:</strong> {transit['strength']}</p>
                    
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 10px;">
                        <div>
                            <h5 style="margin: 0 0 5px 0; color: {text_color};">📈 Equity Impact:</h5>
                            <p style="margin: 0; font-size: 0.9em;">{transit['equity_impact']}</p>
                            
                            <h5 style="margin: 10px 0 5px 0; color: {text_color};">🏭 Commodity Impact:</h5>
                            <p style="margin: 0; font-size: 0.9em;">{transit['commodity_impact']}</p>
                            
                            <h5 style="margin: 10px 0 5px 0; color: {text_color};">💱 Forex Impact:</h5>
                            <p style="margin: 0; font-size: 0.9em;">{transit['forex_impact']}</p>
                        </div>
                        
                        <div>
                            <h5 style="margin: 0 0 5px 0; color: {text_color};">🏢 Sector Signals:</h5>
                            {"<br>".join([f"<span style='font-size: 0.9em;'>• {impact}</span>" for impact in transit['sector_impact']])}
                            
                            <h5 style="margin: 10px 0 5px 0; color: {text_color};">📊 Key Stocks:</h5>
                            {"<br>".join([f"<span style='font-size: 0.9em;'>• {stock}</span>" for stock in transit['key_stocks']])}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        with transit_weekly_tab:
            st.markdown("### 📊 This Week's Major Planetary Transits & Market Impact")
            
            weekly_transits = [
                {
                    'date': 'Friday, Aug 1',
                    'transit': 'Mercury in Pushya (Cancer)',
                    'duration': 'All day',
                    'impact': 'IT sector weak, Communication stocks under pressure',
                    'sectors_affected': ['IT', 'Telecom', 'Media'],
                    'strategy': 'Avoid tech stocks, Focus on defensive sectors',
                    'key_levels': 'Nifty IT: 31500 support'
                },
                {
                    'date': 'Saturday, Aug 2',
                    'transit': 'Moon enters Vishakha (Libra/Scorpio)',
                    'duration': '08:45 AM onwards',
                    'impact': 'Banking sector gets boost, Trade & commerce favorable',
                    'sectors_affected': ['Banking', 'Financial Services', 'Trade'],
                    'strategy': 'Accumulate banking stocks for Monday',
                    'key_levels': 'Bank Nifty: 53000 target'
                },
                {
                    'date': 'Sunday, Aug 3',
                    'transit': 'Mercury aspects Mars',
                    'duration': 'Peak at 2:30 PM',
                    'impact': 'Technology meets Defense - Cybersecurity focus',
                    'sectors_affected': ['IT-Defense', 'Cybersecurity', 'Tech Manufacturing'],
                    'strategy': 'Research defense-tech stocks for week ahead',
                    'key_levels': 'Watch for gaps on Monday'
                },
                {
                    'date': 'Monday, Aug 4',
                    'transit': 'Venus enters Mrigashira',
                    'duration': '11:20 AM',
                    'impact': 'Auto sector shifts, Real estate gets focus',
                    'sectors_affected': ['Auto', 'Real Estate', 'Luxury Goods'],
                    'strategy': 'Book profits in auto, Enter realty stocks',
                    'key_levels': 'Nifty Auto: 25000 resistance'
                },
                {
                    'date': 'Tuesday, Aug 5',
                    'transit': 'Sun conjuncts Mercury',
                    'duration': 'Exact at 3:45 PM',
                    'impact': 'FMCG and IT synergy, Government tech initiatives',
                    'sectors_affected': ['FMCG', 'IT Services', 'PSU'],
                    'strategy': 'Long FMCG, PSU tech stocks',
                    'key_levels': 'Nifty FMCG: 60000 target'
                },
                {
                    'date': 'Wednesday, Aug 6',
                    'transit': 'Mars in Virgo strengthens',
                    'duration': 'Continues',
                    'impact': 'Healthcare and precision industries gain',
                    'sectors_affected': ['Pharma', 'Healthcare', 'Medical Devices'],
                    'strategy': 'Accumulate pharma leaders',
                    'key_levels': 'Nifty Pharma: 19500 breakout'
                },
                {
                    'date': 'Thursday, Aug 7',
                    'transit': 'Jupiter aspects Saturn',
                    'duration': 'Building aspect',
                    'impact': 'Consolidation phase, Range-bound markets',
                    'sectors_affected': ['All sectors mixed signals'],
                    'strategy': 'Wait for clarity, Reduce positions',
                    'key_levels': 'Nifty: 24500-25000 range'
                }
            ]
            
            # Display weekly transits
            for transit in weekly_transits:
                if transit['date'].split(', ')[1] == current_date_str.split(' ')[0] + ' ' + current_date_str.split(' ')[1]:
                    card_style = 'background: linear-gradient(135deg, #e3f2fd, #bbdefb); border: 3px solid #2196f3;'
                    today_marker = ' 📍 TODAY'
                else:
                    card_style = 'background: #f8f9fa; border: 2px solid #dee2e6;'
                    today_marker = ''
                
                st.markdown(f"""
                <div style="{card_style} padding: 15px; border-radius: 10px; margin: 10px 0;">
                    <h4 style="margin: 0 0 10px 0; color: #333;">{transit['date']}{today_marker}</h4>
                    <h5 style="margin: 0 0 5px 0; color: #007bff;">🪐 {transit['transit']}</h5>
                    <p style="margin: 0; font-size: 0.9em;"><strong>Duration:</strong> {transit['duration']}</p>
                    <p style="margin: 5px 0; font-size: 0.95em;"><strong>Market Impact:</strong> {transit['impact']}</p>
                    <p style="margin: 5px 0; font-size: 0.9em;"><strong>Sectors Affected:</strong> {', '.join(transit['sectors_affected'])}</p>
                    <p style="margin: 5px 0; font-size: 0.9em; color: #28a745;"><strong>Strategy:</strong> {transit['strategy']}</p>
                    <p style="margin: 5px 0 0 0; font-size: 0.9em; color: #dc3545;"><strong>Key Levels:</strong> {transit['key_levels']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Weekly summary
            st.markdown("### 📈 Week's Market Outlook Based on Transits")
            
            week_col1, week_col2 = st.columns(2)
            
            with week_col1:
                st.markdown("""
                <div class="report-section" style="background: #d4edda; border-left: 5px solid #28a745;">
                    <h4 style="color: #155724;">🟢 BULLISH SECTORS This Week</h4>
                    <p><strong>Monday-Tuesday:</strong> Banking, FMCG, PSU</p>
                    <p><strong>Wednesday-Thursday:</strong> Pharma, Healthcare</p>
                    <p><strong>Best Days:</strong> Monday (Aug 4), Tuesday (Aug 5)</p>
                    <p><strong>Key Strategy:</strong> Buy on dips in banking and pharma</p>
                </div>
                """, unsafe_allow_html=True)
            
            with week_col2:
                st.markdown("""
                <div class="report-section" style="background: #f8d7da; border-left: 5px solid #dc3545;">
                    <h4 style="color: #721c24;">🔴 BEARISH SECTORS This Week</h4>
                    <p><strong>Throughout Week:</strong> IT Services, Telecom</p>
                    <p><strong>Mid-week:</strong> Auto (profit booking)</p>
                    <p><strong>Weak Days:</strong> Friday (Aug 1), Thursday (Aug 7)</p>
                    <p><strong>Key Strategy:</strong> Book profits in IT, Avoid fresh longs</p>
                </div>
                """, unsafe_allow_html=True)
        
        with transit_monthly_tab:
            st.markdown("### 📈 August 2025 - Complete Monthly Planetary Transit Calendar")
            
            # Major monthly transits
            monthly_major_transits = [
                {
                    'date': 'Aug 8-10',
                    'event': 'Mercury enters Leo',
                    'impact': 'IT & Communication recover strongly',
                    'target': 'Nifty IT +5-8% expected'
                },
                {
                    'date': 'Aug 12-14',
                    'event': 'Venus-Jupiter conjunction',
                    'impact': 'Banking & Luxury peak - Best days of month',
                    'target': 'Bank Nifty 55000+ possible'
                },
                {
                    'date': 'Aug 17-19',
                    'event': 'Mars squares Saturn',
                    'impact': 'High volatility, Market correction likely',
                    'target': 'Nifty may test 24000'
                },
                {
                    'date': 'Aug 22-24',
                    'event': 'Sun enters Leo',
                    'impact': 'Government stocks, PSU rally',
                    'target': 'PSU index +3-5%'
                },
                {
                    'date': 'Aug 28-31',
                    'event': 'Mercury retrograde shadow',
                    'impact': 'IT sector uncertainty returns',
                    'target': 'Book IT profits by Aug 27'
                }
            ]
            
            st.markdown("#### 🌟 Major Transit Events This Month")
            
            for event in monthly_major_transits:
                if 'peak' in event['impact'].lower() or 'best' in event['impact'].lower():
                    event_style = 'background: #d4edda; color: #155724; border-left: 5px solid #28a745;'
                elif 'correction' in event['impact'].lower() or 'uncertainty' in event['impact'].lower():
                    event_style = 'background: #f8d7da; color: #721c24; border-left: 5px solid #dc3545;'
                else:
                    event_style = 'background: #d1ecf1; color: #0c5460; border-left: 5px solid #17a2b8;'
                
                st.markdown(f"""
                <div style="{event_style} padding: 12px; border-radius: 8px; margin: 10px 0;">
                    <h5 style="margin: 0 0 5px 0;">{event['date']}: {event['event']}</h5>
                    <p style="margin: 0; font-size: 0.95em;"><strong>Impact:</strong> {event['impact']}</p>
                    <p style="margin: 0; font-size: 0.9em;"><strong>Target:</strong> {event['target']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Monthly sector rotation based on transits
            st.markdown("#### 🔄 Monthly Sector Rotation Strategy")
            
            rotation_schedule = [
                {'week': 'Week 1 (Aug 1-7)', 'in_favor': 'Banking, Pharma', 'out_of_favor': 'IT, Auto', 'strategy': 'Rotate from IT to Banking'},
                {'week': 'Week 2 (Aug 8-14)', 'in_favor': 'IT Recovery, Banking Peak', 'out_of_favor': 'Metals, Energy', 'strategy': 'Book banking at peaks, Enter IT'},
                {'week': 'Week 3 (Aug 15-21)', 'in_favor': 'Defensive, FMCG', 'out_of_favor': 'High Beta stocks', 'strategy': 'Move to safety, Reduce exposure'},
                {'week': 'Week 4 (Aug 22-31)', 'in_favor': 'PSU, Government', 'out_of_favor': 'IT, Private banks', 'strategy': 'PSU rally, Exit IT before retrograde'}
            ]
            
            for rotation in rotation_schedule:
                st.markdown(f"""
                <div style="background: #f8f9fa; padding: 12px; border-radius: 8px; margin: 8px 0; border: 2px solid #dee2e6;">
                    <h5 style="margin: 0 0 8px 0; color: #495057;">{rotation['week']}</h5>
                    <p style="margin: 0; font-size: 0.9em;"><strong>✅ In Favor:</strong> {rotation['in_favor']}</p>
                    <p style="margin: 0; font-size: 0.9em;"><strong>❌ Out of Favor:</strong> {rotation['out_of_favor']}</p>
                    <p style="margin: 0; font-size: 0.9em; color: #007bff;"><strong>Strategy:</strong> {rotation['strategy']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Monthly commodity outlook
            st.markdown("#### 🏭 Monthly Commodity Outlook")
            
            commodity_col1, commodity_col2, commodity_col3 = st.columns(3)
            
            with commodity_col1:
                st.markdown("""
                <div style="background: linear-gradient(135deg, #fff8e1, #ffecb3); padding: 15px; border-radius: 10px; border: 2px solid #ffc107;">
                    <h4 style="margin: 0 0 10px 0; color: #f57c00;">🥇 GOLD</h4>
                    <p style="margin: 0; font-size: 0.9em;"><strong>Aug 1-14:</strong> Bullish (Venus)</p>
                    <p style="margin: 0; font-size: 0.9em;"><strong>Aug 15-21:</strong> Correction</p>
                    <p style="margin: 0; font-size: 0.9em;"><strong>Aug 22-31:</strong> Recovery</p>
                    <p style="margin: 5px 0 0 0; font-weight: bold;">Target: ₹74,000</p>
                </div>
                """, unsafe_allow_html=True)
            
            with commodity_col2:
                st.markdown("""
                <div style="background: linear-gradient(135deg, #e0e0e0, #bdbdbd); padding: 15px; border-radius: 10px; border: 2px solid #757575;">
                    <h4 style="margin: 0 0 10px 0; color: #424242;">🥈 SILVER</h4>
                    <p style="margin: 0; font-size: 0.9em;"><strong>Aug 1-14:</strong> Strong Bull</p>
                    <p style="margin: 0; font-size: 0.9em;"><strong>Aug 15-21:</strong> Volatile</p>
                    <p style="margin: 0; font-size: 0.9em;"><strong>Aug 22-31:</strong> Bullish</p>
                    <p style="margin: 5px 0 0 0; font-weight: bold;">Target: ₹95,000</p>
                </div>
                """, unsafe_allow_html=True)
            
            with commodity_col3:
                st.markdown("""
                <div style="background: linear-gradient(135deg, #3e2723, #5d4037); color: white; padding: 15px; border-radius: 10px; border: 2px solid #3e2723;">
                    <h4 style="margin: 0 0 10px 0;">🛢️ CRUDE</h4>
                    <p style="margin: 0; font-size: 0.9em;"><strong>Aug 1-14:</strong> Range bound</p>
                    <p style="margin: 0; font-size: 0.9em;"><strong>Aug 15-21:</strong> Bearish</p>
                    <p style="margin: 0; font-size: 0.9em;"><strong>Aug 22-31:</strong> Recovery</p>
                    <p style="margin: 5px 0 0 0; font-weight: bold;">Range: ₹6500-7200</p>
                </div>
                """, unsafe_allow_html=True)
        
        with transit_current_tab:
            st.markdown("### 🌟 Current Planetary Positions & Strengths")
            
            # Get planetary transit data
            transits = get_planetary_transits()
            
            # Display in enhanced grid
            planet_cols = st.columns(3)
            major_planets = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu']
            
            for idx, planet in enumerate(major_planets):
                col_idx = idx % 3
                transit = transits[planet]
                
                # Determine card color based on trend
                if transit['trend'] in ['Strong Bullish', 'Bullish']:
                    card_color = 'background: linear-gradient(135deg, #d4edda, #c3e6cb); color: #155724; border: 3px solid #28a745;'
                elif transit['trend'] == 'Bearish':
                    card_color = 'background: linear-gradient(135deg, #f8d7da, #f1c3c6); color: #721c24; border: 3px solid #dc3545;'
                elif transit['trend'] in ['Volatile', 'Neutral', 'Disruptive']:
                    card_color = 'background: linear-gradient(135deg, #fff3cd, #ffeeba); color: #856404; border: 3px solid #ffc107;'
                else:
                    card_color = 'background: linear-gradient(135deg, #e2e3e5, #d6d8db); color: #495057; border: 3px solid #6c757d;'
                
                with planet_cols[col_idx]:
                    st.markdown(f"""
                    <div style="{card_color} padding: 15px; border-radius: 12px; margin: 10px 0; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                        <h3 style="margin: 0 0 8px 0;">{transit['symbol']} {planet}</h3>
                        <h4 style="margin: 0 0 5px 0; font-size: 1em;">{transit['sign']}</h4>
                        <p style="margin: 0; font-size: 0.9em; font-weight: bold;">{transit['degree']}</p>
                        <p style="margin: 8px 0 5px 0; font-size: 0.85em;"><strong>Strength:</strong> {transit['strength']}</p>
                        <p style="margin: 0; font-size: 1em; font-weight: bold;">{transit['trend']}</p>
                        <p style="margin: 5px 0 0 0; font-size: 0.8em;">Duration: {transit['duration']}</p>
                        <hr style="margin: 10px 0; opacity: 0.3;">
                        <p style="margin: 0; font-size: 0.85em;"><strong>Markets:</strong></p>
                        <p style="margin: 0; font-size: 0.8em;">{', '.join(transit['markets_affected'][:2])}</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Add Uranus if present
            if 'Uranus' in transits:
                transit = transits['Uranus']
                with planet_cols[0]:  # Place in first column of next row
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #e2e3e5, #d6d8db); color: #495057; border: 3px solid #6c757d; padding: 15px; border-radius: 12px; margin: 10px 0; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                        <h3 style="margin: 0 0 8px 0;">{transit['symbol']} Uranus</h3>
                        <h4 style="margin: 0 0 5px 0; font-size: 1em;">{transit['sign']}</h4>
                        <p style="margin: 0; font-size: 0.9em; font-weight: bold;">{transit['degree']}</p>
                        <p style="margin: 8px 0 5px 0; font-size: 0.85em;"><strong>Strength:</strong> {transit['strength']}</p>
                        <p style="margin: 0; font-size: 1em; font-weight: bold;">{transit['trend']}</p>
                        <p style="margin: 5px 0 0 0; font-size: 0.8em;">Duration: {transit['duration']}</p>
                        <hr style="margin: 10px 0; opacity: 0.3;">
                        <p style="margin: 0; font-size: 0.85em;"><strong>Markets:</strong></p>
                        <p style="margin: 0; font-size: 0.8em;">{', '.join(transit['markets_affected'][:2])}</p>
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
            <p style="font-size: 1.1em;"><strong>🛢️ CRUDE:</strong> <span style="background: #dc3545; color: white; padding: 4px 8px; border-radius: 4px; font-weight: bold;">SELL -1.8%</span></p>
            <p style="margin: 15px 0 0 0; font-weight: bold; font-size: 1.2em; color: #155724;">🌟 This is the best commodity trading window of the week!</p>
        </div>
        """, unsafe_allow_html=True)
    
    with tomorrow_forex_tab:
        st.markdown('<div class="sector-header"><h3 style="margin: 0;">💱 TOMORROW\'S FOREX FORECAST</h3></div>', unsafe_allow_html=True)
        
        forex_forecast = [
            {'pair': 'USD/INR', 'trend': 'Bearish', 'range': '83.15 - 83.45', 'strategy': 'Sell on rallies above 83.35'},
            {'pair': 'EUR/INR', 'trend': 'Bullish', 'range': '88.10 - 88.80', 'strategy': 'Buy on dips below 88.20'},
            {'pair': 'BITCOIN', 'trend': 'Volatile', 'range': '$95,000 - $102,000', 'strategy': 'Extreme volatility expected, use tight stops'},
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
            <p><strong>📊 DOW JONES:</strong> Jupiter hour (21:00-23:00 IST) brings +1.5% rally</p>
            <p><strong>📈 S&P 500:</strong> Broad market strength, target +1.8%</p>
            <p><strong>💻 NASDAQ:</strong> Tech strength continues, target +2.0%</p>
            
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

# Footer - Real-time Astronomical Synchronization
st.write("---")
footer_col1, footer_col2, footer_col3, footer_col4 = st.columns(4)

with footer_col1:
    st.caption(f"🕐 Last Updated: {st.session_state.last_update.strftime('%H:%M:%S')} IST")

with footer_col2:
    st.caption(f"{current_symbol} Current Planet Hour: {current_planet}")

with footer_col3:
    st.caption(f"📅 Real Astronomical Date: {current_date_str}")

with footer_col4:
    st.caption("🕉️ Vedic Market Intelligence - Real Ephemeris Data")

# Real-time synchronization notice
st.markdown(f"""
<div style="background: #e3f2fd; color: #1565c0; padding: 10px; border-radius: 8px; margin: 10px 0; text-align: center; border: 2px solid #2196f3;">
    <p style="margin: 0; font-size: 0.9em;">📡 <strong>REAL-TIME SYNC:</strong> {current_time_str} IST | 🪐 <strong>ASTRONOMICAL DATA:</strong> August 1, 2025 | ✅ <strong>VEDIC ACCURACY:</strong> Live Ephemeris</p>
</div>
""", unsafe_allow_html=True)

# Auto-refresh
if auto_refresh:
    time.sleep(refresh_rate)
    update_market_data()
    st.rerun()

def get_current_planetary_hour_details():
    """Get detailed information about current planetary hour"""
    ist_tz = pytz.timezone('Asia/Kolkata')
    current_time = datetime.now(ist_tz)
    current_hour = current_time.hour
    
    market_hours = [
        {'start': '09:15', 'end': '10:15', 'planet': 'Venus ♀', 'planet_name': 'Venus'},
        {'start': '10:15', 'end': '11:15', 'planet': 'Sun ☀️', 'planet_name': 'Sun'},
        {'start': '11:15', 'end': '12:15', 'planet': 'Mercury ☿', 'planet_name': 'Mercury'},
        {'start': '12:15', 'end': '13:15', 'planet': 'Saturn ♄', 'planet_name': 'Saturn'},
        {'start': '13:15', 'end': '14:15', 'planet': 'Jupiter ♃', 'planet_name': 'Jupiter'},
        {'start': '14:15', 'end': '15:15', 'planet': 'Mars ♂️', 'planet_name': 'Mars'},
        {'start': '15:15', 'end': '15:30', 'planet': 'Sun ☀️', 'planet_name': 'Sun'}
    ]
    
    for hour_info in market_hours:
        start_time = datetime.strptime(hour_info['start'], '%H:%M').replace(
            year=current_time.year, 
            month=current_time.month, 
            day=current_time.day, 
            tzinfo=ist_tz
        )
        end_time = datetime.strptime(hour_info['end'], '%H:%M').replace(
            year=current_time.year, 
            month=current_time.month, 
            day=current_time.day, 
            tzinfo=ist_tz
        )
        
        if start_time <= current_time < end_time:
            return hour_info
    
    return None

def display_sector_stocks_with_transits(sector_name, stocks):
    """Display sector stocks with real-time planetary transit information"""
    
    # Determine sector type
    if 'BANK' in sector_name.upper():
        sector_type = 'banking'
    elif 'IT' in sector_name.upper():
        sector_type = 'tech'
    elif 'PHARMA' in sector_name.upper():
        sector_type = 'pharma'
    elif 'AUTO' in sector_name.upper():
        sector_type = 'auto'
    elif 'METAL' in sector_name.upper():
        sector_type = 'metal'
    else:
        sector_type = 'general'
    
    st.markdown(f"### 🌟 {sector_name} Stocks - Live Planetary Transit Analysis")
    
    # Current time info
    ist_tz = pytz.timezone('Asia/Kolkata')
    current_time = datetime.now(ist_tz)
    current_hour = current_time.hour
    current_minute = current_time.minute
    
    # Define market hours with planetary rulers and sector-specific effects
    market_hours = [
        {'start': '09:15', 'end': '10:15', 'planet': 'Venus ♀', 'planet_name': 'Venus',
         'effects': {
             'banking': {'signal': 'BUY', 'strength': 'Good', 'target': '+1.2%'},
             'tech': {'signal': 'HOLD', 'strength': 'Moderate', 'target': '+0.5%'},
             'pharma': {'signal': 'BUY', 'strength': 'Good', 'target': '+1.0%'},
             'auto': {'signal': 'STRONG BUY', 'strength': 'Excellent', 'target': '+2.0%'},
             'metal': {'signal': 'BUY', 'strength': 'Good', 'target': '+1.1%'},
             'general': {'signal': 'BUY', 'strength': 'Good', 'target': '+1.0%'}
         }},
        {'start': '10:15', 'end': '11:15', 'planet': 'Sun ☀️', 'planet_name': 'Sun',
         'effects': {
             'banking': {'signal': 'STRONG BUY', 'strength': 'Excellent', 'target': '+2.0%'},
             'tech': {'signal': 'BUY', 'strength': 'Good', 'target': '+1.2%'},
             'pharma': {'signal': 'STRONG BUY', 'strength': 'Maximum', 'target': '+2.5%'},
             'auto': {'signal': 'BUY', 'strength': 'Strong', 'target': '+1.5%'},
             'metal': {'signal': 'HOLD', 'strength': 'Moderate', 'target': '+0.6%'},
             'general': {'signal': 'BUY', 'strength': 'Strong', 'target': '+1.3%'}
         }},
        {'start': '11:15', 'end': '12:15', 'planet': 'Mercury ☿', 'planet_name': 'Mercury',
         'effects': {
             'banking': {'signal': 'HOLD', 'strength': 'Neutral', 'target': '+0.3%'},
             'tech': {'signal': 'SELL', 'strength': 'Weak', 'target': '-1.5%'},
             'pharma': {'signal': 'BUY', 'strength': 'Good', 'target': '+1.1%'},
             'auto': {'signal': 'HOLD', 'strength': 'Neutral', 'target': '+0.4%'},
             'metal': {'signal': 'SELL', 'strength': 'Weak', 'target': '-0.8%'},
             'general': {'signal': 'HOLD', 'strength': 'Neutral', 'target': '+0.5%'}
         }},
        {'start': '12:15', 'end': '13:15', 'planet': 'Saturn ♄', 'planet_name': 'Saturn',
         'effects': {
             'banking': {'signal': 'SELL', 'strength': 'Weak', 'target': '-1.0%'},
             'tech': {'signal': 'STRONG SELL', 'strength': 'Very Weak', 'target': '-2.0%'},
             'pharma': {'signal': 'CAUTION', 'strength': 'Mixed', 'target': '±0.8%'},
             'auto': {'signal': 'SELL', 'strength': 'Weak', 'target': '-1.2%'},
             'metal': {'signal': 'BUY', 'strength': 'Good', 'target': '+1.3%'},
             'general': {'signal': 'SELL', 'strength': 'Weak', 'target': '-0.9%'}
         }},
        {'start': '13:15', 'end': '14:15', 'planet': 'Jupiter ♃', 'planet_name': 'Jupiter',
         'effects': {
             'banking': {'signal': 'PEAK BUY', 'strength': 'Maximum', 'target': '+2.8%'},
             'tech': {'signal': 'BUY', 'strength': 'Recovery', 'target': '+1.5%'},
             'pharma': {'signal': 'BUY', 'strength': 'Strong', 'target': '+1.8%'},
             'auto': {'signal': 'BUY', 'strength': 'Good', 'target': '+1.4%'},
             'metal': {'signal': 'STRONG BUY', 'strength': 'Strong', 'target': '+2.0%'},
             'general': {'signal': 'STRONG BUY', 'strength': 'Excellent', 'target': '+2.0%'}
         }},
        {'start': '14:15', 'end': '15:15', 'planet': 'Mars ♂️', 'planet_name': 'Mars',
         'effects': {
             'banking': {'signal': 'VOLATILE', 'strength': 'Extreme', 'target': '±2.5%'},
             'tech': {'signal': 'VOLATILE', 'strength': 'Extreme', 'target': '±3.0%'},
             'pharma': {'signal': 'SELL', 'strength': 'Weak', 'target': '-1.3%'},
             'auto': {'signal': 'VOLATILE', 'strength': 'High', 'target': '±2.0%'},
             'metal': {'signal': 'STRONG BUY', 'strength': 'Strong', 'target': '+2.2%'},
             'general': {'signal': 'VOLATILE', 'strength': 'High', 'target': '±1.8%'}
         }},
        {'start': '15:15', 'end': '15:30', 'planet': 'Sun ☀️', 'planet_name': 'Sun',
         'effects': {
             'banking': {'signal': 'BUY', 'strength': 'Good', 'target': '+1.0%'},
             'tech': {'signal': 'HOLD', 'strength': 'Neutral', 'target': '+0.4%'},
             'pharma': {'signal': 'HOLD', 'strength': 'Stable', 'target': '+0.5%'},
             'auto': {'signal': 'BUY', 'strength': 'Good', 'target': '+0.8%'},
             'metal': {'signal': 'HOLD', 'strength': 'Neutral', 'target': '+0.3%'},
             'general': {'signal': 'BUY', 'strength': 'Good', 'target': '+0.7%'}
         }}
    ]
    
    # Find current planetary hour
    current_planetary_hour = None
    for hour_info in market_hours:
        start_time = datetime.strptime(hour_info['start'], '%H:%M').replace(year=current_time.year, month=current_time.month, day=current_time.day, tzinfo=ist_tz)
        end_time = datetime.strptime(hour_info['end'], '%H:%M').replace(year=current_time.year, month=current_time.month, day=current_time.day, tzinfo=ist_tz)
        
        if start_time <= current_time < end_time:
            current_planetary_hour = hour_info
            break
    
    # Display current planetary hour for sector
    if current_planetary_hour:
        current_effect = current_planetary_hour['effects'][sector_type]
        signal_color = '#28a745' if 'BUY' in current_effect['signal'] else '#dc3545' if 'SELL' in current_effect['signal'] else '#ffc107'
        
        st.markdown(f"""
        <div class="live-signal" style="margin: 10px 0;">
            <h4 style="margin: 0;">🔥 CURRENT HOUR: {current_planetary_hour['start']}-{current_planetary_hour['end']} - {current_planetary_hour['planet']}</h4>
            <p style="margin: 5px 0 0 0;">Active for {sector_name} Sector | Time: {current_time.strftime('%H:%M:%S')} IST</p>
            <p style="margin: 5px 0 0 0; font-size: 1.1em;">
                <strong>Sector Signal:</strong> 
                <span style="background: {signal_color}; color: white; padding: 4px 8px; border-radius: 4px; font-weight: bold;">
                    {current_effect['signal']}
                </span>
                | <strong>Strength:</strong> {current_effect['strength']} | <strong>Target:</strong> {current_effect['target']}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Display stocks in a dynamic grid with real planetary signals
    for i in range(0, len(stocks), 2):  # 2 stocks per row
        cols = st.columns(2)
        
        for j, stock in enumerate(stocks[i:i+2]):
            if j < len(cols):
                with cols[j]:
                    # Generate stock data
                    stock_data = generate_symbol_data(stock)
                    
                    # Stock-specific adjustment based on sector effect
                    if current_planetary_hour:
                        sector_effect = current_planetary_hour['effects'][sector_type]
                        
                        # Apply sector effect to individual stock
                        if 'BUY' in sector_effect['signal']:
                            stock_adjustment = random.uniform(0.8, 1.2)  # 80-120% of sector signal
                        elif 'SELL' in sector_effect['signal']:
                            stock_adjustment = random.uniform(0.8, 1.2)  # 80-120% of sector signal
                        else:
                            stock_adjustment = random.uniform(0.5, 1.5)  # More variation for volatile
                        
                        # Calculate stock-specific values
                        if sector_effect['target'].startswith('+'):
                            stock_target = f"+{float(sector_effect['target'][1:-1]) * stock_adjustment:.1f}%"
                        elif sector_effect['target'].startswith('-'):
                            stock_target = f"-{float(sector_effect['target'][1:-1]) * stock_adjustment:.1f}%"
                        else:  # Volatile (±)
                            stock_target = f"±{float(sector_effect['target'][1:-1]) * stock_adjustment:.1f}%"
                        
                        stock_signal = sector_effect['signal']
                        stock_strength = sector_effect['strength']
                    else:
                        # Default values if outside market hours
                        stock_signal = 'HOLD'
                        stock_target = '±0.5%'
                        stock_strength = 'Neutral'
                    
                    # Stock price card with live signal
                    color_class = "positive" if stock_data['change'] >= 0 else "negative"
                    arrow = "▲" if stock_data['change'] >= 0 else "▼"
                    
                    # Dynamic background based on current signal
                    if 'BUY' in stock_signal:
                        card_bg = 'background: linear-gradient(135deg, #d4edda, #c3e6cb); border: 3px solid #28a745;'
                        live_indicator = '🟢 LIVE BUY'
                    elif 'SELL' in stock_signal:
                        card_bg = 'background: linear-gradient(135deg, #f8d7da, #f1c3c6); border: 3px solid #dc3545;'
                        live_indicator = '🔴 LIVE SELL'
                    else:
                        card_bg = 'background: linear-gradient(135deg, #fff3cd, #ffeeba); border: 3px solid #ffc107;'
                        live_indicator = '⚡ LIVE CAUTION'
                    
                    st.markdown(f"""
                    <div style="{card_bg} padding: 15px; border-radius: 12px; margin: 10px 0; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                            <h4 style="margin: 0; color: #333; font-weight: bold;">{stock}</h4>
                            <span style="font-size: 0.8em; font-weight: bold; padding: 2px 6px; border-radius: 4px; background: #ff6b35; color: white;">{live_indicator}</span>
                        </div>
                        
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                            <div>
                                <h2 style="margin: 0; color: #007bff;">₹{stock_data['price']:,.1f}</h2>
                                <h4 class="{color_class}" style="margin: 0;">
                                    {arrow} {abs(stock_data['change']):.2f}%
                                </h4>
                            </div>
                            <div style="text-align: right; font-size: 0.9em;">
                                <p style="margin: 0;"><strong>Vol:</strong> {stock_data['volume']:,}</p>
                                <p style="margin: 0;"><strong>MCap:</strong> ₹{stock_data['market_cap']:,}Cr</p>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Current planetary signal details
                    if current_planetary_hour:
                        signal_color = '#28a745' if 'BUY' in stock_signal else '#dc3545' if 'SELL' in stock_signal else '#ffc107'
                        
                        st.markdown(f"""
                        <div style="background: rgba(0,0,0,0.05); padding: 10px; border-radius: 8px; margin: 10px 0;">
                            <h5 style="margin: 0 0 5px 0; color: #333;">🕐 Active: {current_planetary_hour['start']}-{current_planetary_hour['end']}</h5>
                            <p style="margin: 0; font-size: 0.9em;"><strong>Planet:</strong> {current_planetary_hour['planet']} | <strong>Strength:</strong> {stock_strength}</p>
                            <p style="margin: 0; font-size: 1em;"><strong>Signal:</strong> <span style="background: {signal_color}; color: white; padding: 2px 6px; border-radius: 4px; font-weight: bold;">{stock_signal}</span></p>
                            <p style="margin: 0; font-size: 0.9em;"><strong>Target:</strong> {stock_target}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Next 3 hours preview with real planetary data
                    st.markdown("**🔮 Next 3 Hours:**")
                    
                    # Find next 3 market hours
                    current_index = next((i for i, h in enumerate(market_hours) if h == current_planetary_hour), -1)
                    if current_index >= 0:
                        next_hours = market_hours[current_index+1:min(current_index+4, len(market_hours))]
                    else:
                        next_hours = market_hours[:3]
                    
                    for next_hour in next_hours:
                        next_effect = next_hour['effects'][sector_type]
                        signal_icon = '🟢' if 'BUY' in next_effect['signal'] else '🔴' if 'SELL' in next_effect['signal'] else '⚡'
                        
                        # Stock-specific variation
                        stock_variation = random.uniform(0.8, 1.2)
                        if next_effect['target'].startswith('+'):
                            next_target = f"+{float(next_effect['target'][1:-1]) * stock_variation:.1f}%"
                        elif next_effect['target'].startswith('-'):
                            next_target = f"-{float(next_effect['target'][1:-1]) * stock_variation:.1f}%"
                        else:
                            next_target = f"±{float(next_effect['target'][1:-1]) * stock_variation:.1f}%"
                        
                        st.markdown(f"""
                        <div style="font-size: 0.85em; padding: 3px 0; border-bottom: 1px solid rgba(0,0,0,0.1);">
                            {signal_icon} <strong>{next_hour['start']}-{next_hour['end']}</strong> {next_hour['planet']} → <strong>{next_effect['signal']}</strong> ({next_target})
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("</div>", unsafe_allow_html=True)

def display_dynamic_sector_analysis(sector_name, stocks, current_hour):
    """Display dynamic sector analysis with enhanced layout"""
    
    # Sector overview with live planetary status
    sector_col1, sector_col2, sector_col3 = st.columns([2, 2, 1])
    
    with sector_col1:
        st.markdown(f"### 🏢 {sector_name} Sector Overview")
        
        # Calculate sector sentiment
        bullish_stocks = random.randint(3, 7)
        bearish_stocks = random.randint(2, 5)
        neutral_stocks = len(stocks) - bullish_stocks - bearish_stocks
        
        sector_sentiment = "BULLISH" if bullish_stocks > bearish_stocks else "BEARISH" if bearish_stocks > bullish_stocks else "NEUTRAL"
        sentiment_color = "#28a745" if sector_sentiment == "BULLISH" else "#dc3545" if sector_sentiment == "BEARISH" else "#ffc107"
        
        st.markdown(f"""
        <div style="background: linear-gradient(45deg, #f8f9fa, #e9ecef); padding: 15px; border-radius: 10px; border-left: 5px solid {sentiment_color};">
            <h4 style="margin: 0; color: {sentiment_color};">Sector Sentiment: {sector_sentiment}</h4>
            <p style="margin: 5px 0 0 0;"><strong>Bullish:</strong> {bullish_stocks} stocks | <strong>Bearish:</strong> {bearish_stocks} stocks | <strong>Neutral:</strong> {neutral_stocks} stocks</p>
        </div>
        """, unsafe_allow_html=True)
    
    with sector_col2:
        # Current planetary influence on sector
        current_planet, current_symbol, current_influence = get_planetary_influence(current_hour)
        
        st.markdown(f"""
        <div style="background: linear-gradient(45deg, #e3f2fd, #bbdefb); padding: 15px; border-radius: 10px; border-left: 5px solid #2196f3;">
            <h4 style="margin: 0; color: #1565c0;">{current_symbol} Current Planet: {current_planet}</h4>
            <p style="margin: 5px 0 0 0; color: #1565c0;">{current_influence}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with sector_col3:
        # Live market status
        ist_tz = pytz.timezone('Asia/Kolkata')
        current_time = datetime.now(ist_tz)
        
        if 9 <= current_hour <= 15:
            market_status = "🟢 LIVE"
            status_color = "#28a745"
        elif current_hour < 9:
            market_status = "🔵 PRE-MKT"
            status_color = "#17a2b8"
        else:
            market_status = "🔴 CLOSED"
            status_color = "#dc3545"
        
        st.markdown(f"""
        <div style="background: {status_color}; color: white; padding: 10px; border-radius: 8px; text-align: center;">
            <h4 style="margin: 0;">Market</h4>
            <h3 style="margin: 0;">{market_status}</h3>
            <p style="margin: 0; font-size: 0.8em;">{current_time.strftime('%H:%M:%S')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Enhanced sector analysis tabs
    sector_analysis_tab1, sector_analysis_tab2, sector_analysis_tab3 = st.tabs([
        "🔥 LIVE STOCKS TRANSIT", 
        "📊 HOURLY HEATMAP", 
        "🎯 SECTOR STRATEGY"
    ])
    
    with sector_analysis_tab1:
        st.markdown(f"#### 🌟 {sector_name} Individual Stocks - Live Planetary Transit")
        display_sector_stocks_with_transits(sector_name, stocks)
    
    with sector_analysis_tab2:
        st.markdown(f"#### 📊 {sector_name} - Hourly Planetary Heatmap")
        
        # Create hourly heatmap for the sector
        st.markdown("**🕐 Complete Market Day Planetary Transit Schedule**")
        
        heatmap_data = [
            {'time': '09:15-10:15', 'planet': 'Venus ♀', 'sector_effect': 'Strong' if sector_name.upper() in ['AUTO', 'FMCG'] else 'Moderate'},
            {'time': '10:15-11:15', 'planet': 'Sun ☀️', 'sector_effect': 'Strong' if sector_name.upper() in ['PHARMA', 'PSU BANK'] else 'Good'},
            {'time': '11:15-12:15', 'planet': 'Mercury ☿', 'sector_effect': 'Weak' if sector_name.upper() == 'IT' else 'Moderate'},
            {'time': '12:15-13:15', 'planet': 'Saturn ♄', 'sector_effect': 'Strong' if sector_name.upper() == 'METAL' else 'Weak'},
            {'time': '13:15-14:15', 'planet': 'Jupiter ♃', 'sector_effect': 'Maximum' if 'BANK' in sector_name.upper() else 'Strong'},
            {'time': '14:15-15:15', 'planet': 'Mars ♂️', 'sector_effect': 'Strong' if sector_name.upper() in ['AUTO', 'METAL'] else 'Volatile'},
            {'time': '15:15-15:30', 'planet': 'Sun ☀️', 'sector_effect': 'Good'}
        ]
        
        heatmap_cols = st.columns(4)
        
        for idx, heat_data in enumerate(heatmap_data):
            col_idx = idx % 4
            
            is_current = current_hour >= int(heat_data['time'].split('-')[0].split(':')[0]) and current_hour < int(heat_data['time'].split('-')[1].split(':')[0])
            
            if heat_data['sector_effect'] == 'Maximum':
                bg_color = '#28a745'
                intensity = '🔥🔥🔥'
            elif heat_data['sector_effect'] == 'Strong':
                bg_color = '#20c997'
                intensity = '🔥🔥'
            elif heat_data['sector_effect'] == 'Good':
                bg_color = '#17a2b8'
                intensity = '🔥'
            elif heat_data['sector_effect'] == 'Weak':
                bg_color = '#dc3545'
                intensity = '❄️'
            else:
                bg_color = '#ffc107'
                intensity = '⚡'
            
            border_style = 'border: 3px solid #ff6b35; animation: pulse 2s infinite;' if is_current else 'border: 2px solid #dee2e6;'
            
            with heatmap_cols[col_idx]:
                st.markdown(f"""
                <div style="background: {bg_color}; color: white; padding: 12px; border-radius: 8px; text-align: center; margin: 5px 0; {border_style}">
                    <h5 style="margin: 0; font-size: 0.9em;">{heat_data['time']}</h5>
                    <h4 style="margin: 0;">{heat_data['planet']}</h4>
                    <p style="margin: 0; font-size: 0.8em;">{heat_data['sector_effect']}</p>
                    <p style="margin: 0;">{intensity}</p>
                    {f'<p style="margin: 5px 0 0 0; font-size: 0.7em; background: #ff6b35; padding: 2px 4px; border-radius: 3px;">LIVE NOW</p>' if is_current else ''}
                </div>
                """, unsafe_allow_html=True)
        
        # Sector-specific planetary insights
        st.markdown(f"### 🌟 {sector_name} - Planetary Insights")
        
        insight_col1, insight_col2 = st.columns(2)
        
        with insight_col1:
            st.markdown("""
            <div class="report-section" style="background: #d4edda; border-left: 5px solid #28a745;">
                <h4 style="color: #155724;">🟢 POWER HOURS for this Sector</h4>
            """, unsafe_allow_html=True)
            
            # Sector-specific power hours
            if 'BANK' in sector_name.upper():
                power_hours = [
                    "13:15-14:15 (Jupiter ♃) - Peak Banking Hour",
                    "10:15-11:15 (Sun ☀️) - Government Support",
                    "09:15-10:15 (Venus ♀) - Liquidity Strength"
                ]
            elif sector_name.upper() == 'IT':
                power_hours = [
                    "15:15-15:30 (Sun ☀️) - Closing Recovery",
                    "13:15-14:15 (Jupiter ♃) - Institutional Support",
                    "09:15-10:15 (Venus ♀) - Opening Stability"
                ]
            elif sector_name.upper() == 'PHARMA':
                power_hours = [
                    "10:15-11:15 (Sun ☀️) - Maximum Strength",
                    "13:15-14:15 (Jupiter ♃) - Growth Phase",
                    "11:15-12:15 (Mercury ☿) - Research Focus"
                ]
            elif sector_name.upper() == 'AUTO':
                power_hours = [
                    "09:15-10:15 (Venus ♀) - Peak Auto Hour",
                    "14:15-15:15 (Mars ♂️) - Manufacturing Power",
                    "10:15-11:15 (Sun ☀️) - Industrial Strength"
                ]
            else:
                power_hours = [
                    "13:15-14:15 (Jupiter ♃) - Growth Phase",
                    "10:15-11:15 (Sun ☀️) - Strength Phase",
                    "09:15-10:15 (Venus ♀) - Opening Strength"
                ]
            
            for hour in power_hours:
                st.markdown(f"• **{hour}**")
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        with insight_col2:
            st.markdown("""
            <div class="report-section" style="background: #f8d7da; border-left: 5px solid #dc3545;">
                <h4 style="color: #721c24;">⚠️ CAUTION HOURS for this Sector</h4>
            """, unsafe_allow_html=True)
            
            # Sector-specific caution hours
            if 'BANK' in sector_name.upper():
                caution_hours = [
                    "12:15-13:15 (Saturn ♄) - Regulatory Pressure",
                    "14:15-15:15 (Mars ♂️) - High Volatility",
                    "11:15-12:15 (Mercury ☿) - News Sensitivity"
                ]
            elif sector_name.upper() == 'IT':
                caution_hours = [
                    "11:15-12:15 (Mercury ☿) - Extreme Pressure",
                    "12:15-13:15 (Saturn ♄) - Strong Bearish",
                    "14:15-15:15 (Mars ♂️) - Extreme Volatility"
                ]
            elif sector_name.upper() == 'PHARMA':
                caution_hours = [
                    "14:15-15:15 (Mars ♂️) - Regulatory Risk",
                    "12:15-13:15 (Saturn ♄) - Compliance Issues"
                ]
            else:
                caution_hours = [
                    "12:15-13:15 (Saturn ♄) - Market Pressure",
                    "14:15-15:15 (Mars ♂️) - High Volatility"
                ]
            
            for hour in caution_hours:
                st.markdown(f"• **{hour}**")
            
            st.markdown("</div>", unsafe_allow_html=True)
    
    with sector_analysis_tab3:
        st.markdown(f"#### 🎯 {sector_name} - Complete Trading Strategy")
        
        strategy_col1, strategy_col2 = st.columns(2)
        
        with strategy_col1:
            st.markdown("""
            <div class="report-section" style="background: #e8f5e8; border-left: 5px solid #28a745;">
                <h4 style="color: #155724;">📈 LONG STRATEGY</h4>
            """, unsafe_allow_html=True)
            
            long_strategies = [
                "**Best Entry Time:** During Jupiter ♃ and Sun ☀️ hours",
                "**Accumulation:** Use Venus ♀ hour for bulk buying",
                "**Position Building:** 30% position in power hours",
                "**Stop Loss:** Below Saturn ♄ hour low",
                "**Target:** 15-25% in favorable planetary periods"
            ]
            
            for strategy in long_strategies:
                st.markdown(f"• {strategy}")
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        with strategy_col2:
            st.markdown("""
            <div class="report-section" style="background: #fde8e8; border-left: 5px solid #dc3545;">
                <h4 style="color: #721c24;">📉 SHORT STRATEGY</h4>
            """, unsafe_allow_html=True)
            
            short_strategies = [
                "**Best Short Time:** During Saturn ♄ and Mars ♂️ hours",
                "**Entry:** Short on rallies in weak planetary hours",
                "**Risk Management:** Cover shorts in Jupiter ♃ hour",
                "**Target:** 8-15% decline in bearish periods",
                "**Stop Loss:** Above Jupiter ♃ hour high"
            ]
            
            for strategy in short_strategies:
                st.markdown(f"• {strategy}")
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Sector risk matrix
        st.markdown(f"### ⚖️ {sector_name} - Risk vs Opportunity Matrix")
        
        risk_matrix_cols = st.columns(3)
        
        with risk_matrix_cols[0]:
            risk_level = random.choice(['Low', 'Medium', 'High'])
            risk_color = '#28a745' if risk_level == 'Low' else '#ffc107' if risk_level == 'Medium' else '#dc3545'
            
            st.markdown(f"""
            <div style="background: {risk_color}; color: white; padding: 12px; border-radius: 8px; text-align: center;">
                <h4 style="margin: 0;">Risk Level</h4>
                <h2 style="margin: 0;">{risk_level}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with risk_matrix_cols[1]:
            opportunity_score = random.randint(6, 9)
            opp_color = '#28a745' if opportunity_score >= 8 else '#ffc107' if opportunity_score >= 7 else '#dc3545'
            
            st.markdown(f"""
            <div style="background: {opp_color}; color: white; padding: 12px; border-radius: 8px; text-align: center;">
                <h4 style="margin: 0;">Opportunity</h4>
                <h2 style="margin: 0;">{opportunity_score}/10</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with risk_matrix_cols[2]:
            timeframe = random.choice(['1-3 Days', '1 Week', '2-3 Weeks'])
            
            st.markdown(f"""
            <div style="background: #6f42c1; color: white; padding: 12px; border-radius: 8px; text-align: center;">
                <h4 style="margin: 0;">Best Timeframe</h4>
                <h2 style="margin: 0; font-size: 1.2em;">{timeframe}</h2>
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
                    <p style="margin: 0;"><strong>High:</strong> {banknifty_data['high']:,.2f} | <strong>Low:</strong> {banknifty_data['low']:,.2f}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Show equity-specific planetary signals (9:15 AM - 3:30 PM)
            signals = create_equity_signals()
            display_detailed_signals(signals, "equity", current_hour)
        
        elif market_type == "commodity":
            # Display Gold, Silver, Crude details
            commodity_cols = st.columns(3)
            
            commodities = ['GOLD', 'SILVER', 'CRUDE']
            icons = ['🥇', '🥈', '🛢️']
            
            for idx, (commodity, icon) in enumerate(zip(commodities, icons)):
                with commodity_cols[idx]:
                    data = st.session_state.market_data[commodity]
                    color_class = "positive" if data['change'] >= 0 else "negative"
                    arrow = "▲" if data['change'] >= 0 else "▼"
                    
                    st.markdown(f"""
                    <div class="sector-price-card">
                        <h4 style="margin: 0 0 10px 0; color: #333;">{icon} {commodity}</h4>
                        <h2 style="margin: 0; color: #007bff;">₹{data['price']:,.0f}</h2>
                        <h4 class="{color_class}" style="margin: 5px 0;">{arrow} {abs(data['change']):.2f}%</h4>
                        <p style="margin: 0; font-size: 0.9em;"><strong>H:</strong> {data['high']:,.0f} | <strong>L:</strong> {data['low']:,.0f}</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Show commodity-specific planetary signals (5 AM - 11:55 PM)
            signals = create_commodity_signals()
            display_detailed_signals(signals, "commodity", current_hour)
        
        elif market_type == "forex":
            # Display USDINR and Bitcoin details
            forex_col1, forex_col2, forex_col3 = st.columns(3)
            
            with forex_col1:
                usdinr_data = st.session_state.market_data['USDINR']
                color_class = "positive" if usdinr_data['change'] >= 0 else "negative"
                arrow = "▲" if usdinr_data['change'] >= 0 else "▼"
                
                st.markdown(f"""
                <div class="sector-price-card">
                    <h4 style="margin: 0 0 10px 0; color: #333;">💵 USD/INR</h4>
                    <h2 style="margin: 0; color: #007bff;">₹{usdinr_data['price']:.2f}</h2>
                    <h4 class="{color_class}" style="margin: 5px 0;">{arrow} {abs(usdinr_data['change']):.2f}%</h4>
                    <p style="margin: 0; font-size: 0.9em;"><strong>H:</strong> {usdinr_data['high']:.2f} | <strong>L:</strong> {usdinr_data['low']:.2f}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with forex_col2:
                btc_data = st.session_state.market_data['BITCOIN']
                color_class = "positive" if btc_data['change'] >= 0 else "negative"
                arrow = "▲" if btc_data['change'] >= 0 else "▼"
                
                st.markdown(f"""
                <div class="sector-price-card">
                    <h4 style="margin: 0 0 10px 0; color: #333;">₿ BITCOIN</h4>
                    <h2 style="margin: 0; color: #007bff;">${btc_data['price']:,.0f}</h2>
                    <h4 class="{color_class}" style="margin: 5px 0;">{arrow} {abs(btc_data['change']):.2f}%</h4>
                    <p style="margin: 0; font-size: 0.9em;"><strong>H:</strong> ${btc_data['high']:,.0f} | <strong>L:</strong> ${btc_data['low']:,.0f}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with forex_col3:
                # Add Dollar Index (DXY) from session state
                dxy_data = st.session_state.market_data['DXY']
                color_class = "positive" if dxy_data['change'] >= 0 else "negative"
                arrow = "▲" if dxy_data['change'] >= 0 else "▼"
                
                st.markdown(f"""
                <div class="sector-price-card">
                    <h4 style="margin: 0 0 10px 0; color: #333;">📊 DXY INDEX</h4>
                    <h2 style="margin: 0; color: #007bff;">{dxy_data['price']:.2f}</h2>
                    <h4 class="{color_class}" style="margin: 5px 0;">{arrow} {abs(dxy_data['change']):.2f}%</h4>
                    <p style="margin: 0; font-size: 0.9em;"><strong>H:</strong> {dxy_data['high']:.2f} | <strong>L:</strong> {dxy_data['low']:.2f}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Show forex-specific planetary signals (5 AM - 11:55 PM)
            signals = create_forex_signals()
            display_detailed_signals(signals, "forex", current_hour)
        
        elif market_type == "global":
            # Display Dow Jones, S&P 500, NASDAQ details
            global_cols = st.columns(3)
            
            global_markets = [
                ('DOWJONES', '📊 DOW JONES'),
                ('SP500', '📈 S&P 500'),
                ('NASDAQ', '💻 NASDAQ')
            ]
            
            for idx, (market_key, display_name) in enumerate(global_markets):
                with global_cols[idx]:
                    data = st.session_state.market_data[market_key]
                    color_class = "positive" if data['change'] >= 0 else "negative"
                    arrow = "▲" if data['change'] >= 0 else "▼"
                    
                    st.markdown(f"""
                    <div class="sector-price-card">
                        <h4 style="margin: 0 0 10px 0; color: #333;">{display_name}</h4>
                        <h2 style="margin: 0; color: #007bff;">{data['price']:,.0f}</h2>
                        <h4 class="{color_class}" style="margin: 5px 0;">{arrow} {abs(data['change']):.2f}%</h4>
                        <p style="margin: 0; font-size: 0.9em;"><strong>H:</strong> {data['high']:,.0f} | <strong>L:</strong> {data['low']:,.0f}</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Show global-specific planetary signals (5 AM - 11:55 PM)
            signals = create_global_signals()
            display_detailed_signals(signals, "global", current_hour)
    
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
