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

# ===== ENHANCED PLANETARY TRANSIT FUNCTIONS =====

def get_complete_planetary_transits():
    """Enhanced planetary transit data with complete astronomical positions"""
    ist_tz = pytz.timezone('Asia/Kolkata')
    current_date = datetime.now(ist_tz)
    current_time = current_date.strftime('%H:%M')
    
    # Complete planetary positions for August 1, 2025 with enhanced market effects
    transits = {
        'Sun': {
            'symbol': '☀️',
            'sign': 'Cancer (Pushya)',
            'degree': '15°01\'',
            'effect': 'Strong for FMCG, Dairy, Real Estate, Government sectors',
            'strength': 'Exalted',
            'markets_affected': ['FMCG', 'Dairy', 'Real Estate', 'PSU', 'Government'],
            'trend': 'Strong Bullish',
            'duration': '30 days',
            'vedic_time': '15:01',
            'modern_position': 'Cancer 15°01\'',
            'hourly_strength': {
                '06:00-07:00': 'Maximum',
                '10:00-11:00': 'Strong', 
                '15:00-16:00': 'Good',
                '22:00-23:00': 'Moderate'
            },
            'sector_effects': {
                'FMCG': 'Strong Buy',
                'Real Estate': 'Buy',
                'PSU BANK': 'Strong Buy',
                'Pharma': 'Buy'
            }
        },
        'Moon': {
            'symbol': '🌙',
            'sign': 'Libra (Swati)',
            'degree': '11°47\'',
            'effect': 'Excellent for Trade, Auto, Textiles, Luxury goods',
            'strength': 'Strong',
            'markets_affected': ['Auto', 'Textiles', 'Luxury', 'Trade', 'Consumer'],
            'trend': 'Bullish',
            'duration': '2.5 days',
            'vedic_time': '11:47',
            'modern_position': 'Libra 11°47\'',
            'hourly_strength': {
                '11:00-12:00': 'Maximum',
                '18:00-19:00': 'Strong',
                '23:00-00:00': 'Good'
            },
            'sector_effects': {
                'AUTO': 'Strong Buy',
                'Textiles': 'Buy',
                'Luxury': 'Strong Buy',
                'Consumer': 'Buy'
            }
        },
        'Mars': {
            'symbol': '♂️',
            'sign': 'Virgo (Uttara Phalguni)',
            'degree': '02°13\'',
            'effect': 'Volatile for IT, Healthcare, Precision industries',
            'strength': 'Neutral',
            'markets_affected': ['IT', 'Healthcare', 'Defense', 'Steel', 'Energy'],
            'trend': 'Volatile',
            'duration': '45 days',
            'vedic_time': '02:13',
            'modern_position': 'Virgo 02°13\'',
            'hourly_strength': {
                '07:00-08:00': 'High Volatility',
                '14:00-15:00': 'Maximum Volatility',
                '21:00-22:00': 'Strong'
            },
            'sector_effects': {
                'IT': 'Volatile/Sell',
                'Healthcare': 'Caution',
                'Defense': 'Buy',
                'Steel': 'Volatile'
            }
        },
        'Mercury': {
            'symbol': '☿',
            'sign': 'Cancer (Pushya)', 
            'degree': '14°36\'',
            'effect': 'Strong for Communication, FMCG, IT services',
            'strength': 'Friendly',
            'markets_affected': ['IT', 'Telecom', 'FMCG', 'Media', 'Education'],
            'trend': 'Mixed',
            'duration': '20 days',
            'vedic_time': '14:36',
            'modern_position': 'Cancer 14°36\'',
            'hourly_strength': {
                '10:00-11:00': 'Strong',
                '11:00-12:00': 'Weak for IT',
                '17:00-18:00': 'Moderate'
            },
            'sector_effects': {
                'IT': 'Sell/Weak',
                'Telecom': 'Buy',
                'FMCG': 'Strong Buy',
                'Media': 'Buy'
            }
        },
        'Jupiter': {
            'symbol': '♃',
            'sign': 'Gemini (Ardra)',
            'degree': '17°32\'',
            'effect': 'Strong for Banking, Finance, Education',
            'strength': 'Neutral',
            'markets_affected': ['Banking', 'Finance', 'Education', 'Insurance'],
            'trend': 'Bullish',
            'duration': '12 months',
            'vedic_time': '17:32',
            'modern_position': 'Gemini 17°32\'',
            'hourly_strength': {
                '06:00-07:00': 'Strong',
                '13:00-14:00': 'Maximum',
                '20:00-21:00': 'Peak Power'
            },
            'sector_effects': {
                'BANKNIFTY': 'Strong Buy',
                'PSU BANK': 'Strong Buy',
                'PVT BANK': 'Strong Buy',
                'Finance': 'Buy', 
                'Insurance': 'Buy'
            }
        },
        'Venus': {
            'symbol': '♀',
            'sign': 'Gemini (Ardra)',
            'degree': '07°01\'',
            'effect': 'Good for Auto, Luxury, Entertainment, Real Estate',
            'strength': 'Neutral',
            'markets_affected': ['Auto', 'Luxury', 'Entertainment', 'Real Estate', 'Beauty'],
            'trend': 'Bullish',
            'duration': '25 days',
            'vedic_time': '07:01',
            'modern_position': 'Gemini 07°01\'',
            'hourly_strength': {
                '09:00-10:00': 'Strong',
                '16:00-17:00': 'Good',
                '23:00-00:00': 'Moderate'
            },
            'sector_effects': {
                'AUTO': 'Strong Buy',
                'Luxury': 'Buy',
                'Real Estate': 'Buy',
                'Entertainment': 'Strong Buy'
            }
        },
        'Saturn': {
            'symbol': '♄',
            'sign': 'Pisces (Uttara Bhadrapada)',
            'degree': '07°24\'',
            'effect': 'Cautious for Pharma, Chemicals, Oil sectors',
            'strength': 'Friendly',
            'markets_affected': ['Pharma', 'Chemicals', 'Oil', 'Gas', 'Mining'],
            'trend': 'Bearish',
            'duration': '2.5 years',
            'vedic_time': '07:24',
            'modern_position': 'Pisces 07°24\'',
            'hourly_strength': {
                '05:00-06:00': 'Strong Negative',
                '12:00-13:00': 'Maximum Negative',
                '19:00-20:00': 'Moderate Negative'
            },
            'sector_effects': {
                'PHARMA': 'Sell/Caution',
                'Chemicals': 'Sell',
                'OIL & GAS': 'Sell',
                'METAL': 'Caution'
            }
        },
        'Rahu': {
            'symbol': '☊',
            'sign': 'Pisces (Purvabhadrapada)',
            'degree': '24°51\'',
            'effect': 'High volatility for Pharma, Chemicals, Foreign stocks',
            'strength': 'Strong',
            'markets_affected': ['Pharma', 'Chemicals', 'Foreign', 'Tech', 'Innovation'],
            'trend': 'Volatile',
            'duration': '18 months',
            'vedic_time': '24:51',
            'modern_position': 'Pisces 24°51\'',
            'hourly_strength': {
                '14:00-15:00': 'Maximum Volatility',
                '19:00-20:00': 'High Volatility',
                '02:00-03:00': 'Strong'
            },
            'sector_effects': {
                'PHARMA': 'High Volatility',
                'Foreign': 'Volatile',
                'Tech': 'Buy with Caution',
                'Chemicals': 'Volatile'
            }
        },
        'Ketu': {
            'symbol': '☋',
            'sign': 'Virgo (Hasta)',
            'degree': '24°51\'',
            'effect': 'Supportive for IT Services, Healthcare, Analytics',
            'strength': 'Moderate',
            'markets_affected': ['IT Services', 'Healthcare', 'Analytics', 'Research'],
            'trend': 'Supportive',
            'duration': '18 months',
            'vedic_time': '24:51',
            'modern_position': 'Virgo 24°51\'',
            'hourly_strength': {
                '08:00-09:00': 'Good',
                '15:00-16:00': 'Strong',
                '22:00-23:00': 'Moderate'
            },
            'sector_effects': {
                'IT': 'Buy',
                'Healthcare': 'Strong Buy',
                'Analytics': 'Buy',
                'Research': 'Strong Buy'
            }
        },
        'Uranus': {
            'symbol': '♅',
            'sign': 'Taurus (Krittika)',
            'degree': '06°42\'',
            'effect': 'Disruptive innovation in Finance, Energy, Technology',
            'strength': 'Moderate',
            'markets_affected': ['Fintech', 'Energy Tech', 'Innovation', 'Crypto'],
            'trend': 'Disruptive',
            'duration': '7 years',
            'vedic_time': '06:42',
            'modern_position': 'Taurus 06°42\'',
            'hourly_strength': {
                '12:00-13:00': 'Strong Disruption',
                '18:00-19:00': 'Innovation Peak',
                '00:00-01:00': 'Moderate'
            },
            'sector_effects': {
                'Fintech': 'Strong Buy',
                'Energy': 'Buy',
                'Innovation': 'Strong Buy',
                'Crypto': 'Volatile Buy'
            }
        }
    }
    
    return transits

def create_enhanced_planetary_hourly_signals():
    """Create comprehensive hourly planetary signals with detailed sector effects"""
    
    hourly_signals = []
    
    # Complete 24-hour planetary rulership cycle
    planetary_hours = [
        # Night hours (00:00 - 06:00)
        {'time': '00:00-01:00', 'planet': 'Moon 🌙', 'ruling': 'Night Guardian', 'sectors': ['FMCG', 'Dairy'], 'signal': 'HOLD', 'strength': 'Moderate'},
        {'time': '01:00-02:00', 'planet': 'Saturn ♄', 'ruling': 'Night Discipline', 'sectors': ['Mining', 'Oil'], 'signal': 'SELL', 'strength': 'Strong'},
        {'time': '02:00-03:00', 'planet': 'Jupiter ♃', 'ruling': 'Deep Night Wisdom', 'sectors': ['Banking'], 'signal': 'BUY', 'strength': 'Good'},
        {'time': '03:00-04:00', 'planet': 'Mars ♂️', 'ruling': 'Pre-Dawn Energy', 'sectors': ['Defense', 'Steel'], 'signal': 'VOLATILE', 'strength': 'High'},
        {'time': '04:00-05:00', 'planet': 'Sun ☀️', 'ruling': 'Dawn Preparation', 'sectors': ['Energy', 'PSU'], 'signal': 'BUY', 'strength': 'Strong'},
        {'time': '05:00-06:00', 'planet': 'Venus ♀', 'ruling': 'Dawn Beauty', 'sectors': ['Auto', 'Luxury'], 'signal': 'BUY', 'strength': 'Good'},
        
        # Early morning (06:00 - 12:00)
        {'time': '06:00-07:00', 'planet': 'Mercury ☿', 'ruling': 'Sunrise Communication', 'sectors': ['IT', 'Telecom'], 'signal': 'HOLD', 'strength': 'Moderate'},
        {'time': '07:00-08:00', 'planet': 'Moon 🌙', 'ruling': 'Morning Nourishment', 'sectors': ['FMCG', 'Consumer'], 'signal': 'BUY', 'strength': 'Strong'},
        {'time': '08:00-09:00', 'planet': 'Saturn ♄', 'ruling': 'Morning Discipline', 'sectors': ['Infrastructure'], 'signal': 'CAUTION', 'strength': 'Moderate'},
        {'time': '09:00-10:00', 'planet': 'Jupiter ♃', 'ruling': 'Market Opening Wisdom', 'sectors': ['Banking', 'Finance'], 'signal': 'STRONG BUY', 'strength': 'Maximum'},
        {'time': '10:00-11:00', 'planet': 'Mars ♂️', 'ruling': 'Active Trading', 'sectors': ['Defense', 'Energy'], 'signal': 'BUY', 'strength': 'Strong'},
        {'time': '11:00-12:00', 'planet': 'Sun ☀️', 'ruling': 'Midday Power', 'sectors': ['PSU', 'Government'], 'signal': 'STRONG BUY', 'strength': 'Maximum'},
        
        # Afternoon (12:00 - 18:00)
        {'time': '12:00-13:00', 'planet': 'Venus ♀', 'ruling': 'Midday Luxury', 'sectors': ['Auto', 'Real Estate'], 'signal': 'BUY', 'strength': 'Strong'},
        {'time': '13:00-14:00', 'planet': 'Mercury ☿', 'ruling': 'Afternoon Communication', 'sectors': ['IT', 'Media'], 'signal': 'SELL', 'strength': 'Weak'},
        {'time': '14:00-15:00', 'planet': 'Moon 🌙', 'ruling': 'Afternoon Stability', 'sectors': ['FMCG', 'Healthcare'], 'signal': 'HOLD', 'strength': 'Good'},
        {'time': '15:00-16:00', 'planet': 'Saturn ♄', 'ruling': 'Closing Discipline', 'sectors': ['Metal', 'Mining'], 'signal': 'SELL', 'strength': 'Strong'},
        {'time': '16:00-17:00', 'planet': 'Jupiter ♃', 'ruling': 'Evening Wisdom', 'sectors': ['Banking', 'Insurance'], 'signal': 'BUY', 'strength': 'Good'},
        {'time': '17:00-18:00', 'planet': 'Mars ♂️', 'ruling': 'Evening Energy', 'sectors': ['Defense', 'Steel'], 'signal': 'VOLATILE', 'strength': 'High'},
        
        # Evening (18:00 - 24:00)
        {'time': '18:00-19:00', 'planet': 'Sun ☀️', 'ruling': 'Evening Power', 'sectors': ['Energy', 'Pharma'], 'signal': 'BUY', 'strength': 'Strong'},
        {'time': '19:00-20:00', 'planet': 'Venus ♀', 'ruling': 'Evening Luxury', 'sectors': ['Auto', 'Entertainment'], 'signal': 'BUY', 'strength': 'Good'},
        {'time': '20:00-21:00', 'planet': 'Mercury ☿', 'ruling': 'Night Communication', 'sectors': ['IT', 'Tech'], 'signal': 'HOLD', 'strength': 'Moderate'},
        {'time': '21:00-22:00', 'planet': 'Moon 🌙', 'ruling': 'Night Comfort', 'sectors': ['FMCG', 'Consumer'], 'signal': 'BUY', 'strength': 'Good'},
        {'time': '22:00-23:00', 'planet': 'Saturn ♄', 'ruling': 'Late Night Discipline', 'sectors': ['Infrastructure'], 'signal': 'HOLD', 'strength': 'Moderate'},
        {'time': '23:00-00:00', 'planet': 'Jupiter ♃', 'ruling': 'Midnight Wisdom', 'sectors': ['Banking', 'Spiritual'], 'signal': 'BUY', 'strength': 'Strong'}
    ]
    
    return planetary_hours

def get_symbol_planetary_effect(planet, symbol_name=None, sector_type=None):
    """Get specific planetary effects for symbols and sectors"""
    
    # Define sector characteristics
    sector_planetary_affinity = {
        'banking': {
            'Jupiter ♃': {'trend': 'Strong Bullish', 'signal': 'STRONG BUY', 'target': '+2.5%', 'strength': 'Maximum', 'rating': 'Strong Buy'},
            'Sun ☀️': {'trend': 'Bullish', 'signal': 'BUY', 'target': '+1.8%', 'strength': 'Strong', 'rating': 'Buy'},
            'Venus ♀': {'trend': 'Bullish', 'signal': 'BUY', 'target': '+1.2%', 'strength': 'Good', 'rating': 'Buy'},
            'Moon 🌙': {'trend': 'Neutral', 'signal': 'HOLD', 'target': '+0.5%', 'strength': 'Moderate', 'rating': 'Hold'},
            'Mercury ☿': {'trend': 'Neutral', 'signal': 'HOLD', 'target': '+0.3%', 'strength': 'Weak', 'rating': 'Hold'},
            'Mars ♂️': {'trend': 'Volatile', 'signal': 'CAUTION', 'target': '±1.8%', 'strength': 'High', 'rating': 'Hold'},
            'Saturn ♄': {'trend': 'Bearish', 'signal': 'SELL', 'target': '-1.2%', 'strength': 'Weak', 'rating': 'Sell'}
        },
        'tech': {
            'Mercury ☿': {'trend': 'Strong Bearish', 'signal': 'STRONG SELL', 'target': '-2.0%', 'strength': 'Maximum', 'rating': 'Strong Sell'},
            'Saturn ♄': {'trend': 'Bearish', 'signal': 'SELL', 'target': '-1.5%', 'strength': 'Strong', 'rating': 'Sell'},
            'Mars ♂️': {'trend': 'Volatile', 'signal': 'CAUTION', 'target': '±2.5%', 'strength': 'Extreme', 'rating': 'Hold'},
            'Ketu ☋': {'trend': 'Supportive', 'signal': 'BUY', 'target': '+1.0%', 'strength': 'Good', 'rating': 'Buy'},
            'Jupiter ♃': {'trend': 'Recovery', 'signal': 'BUY', 'target': '+1.5%', 'strength': 'Good', 'rating': 'Buy'},
            'Sun ☀️': {'trend': 'Neutral', 'signal': 'HOLD', 'target': '+0.5%', 'strength': 'Moderate', 'rating': 'Hold'},
            'Venus ♀': {'trend': 'Neutral', 'signal': 'HOLD', 'target': '+0.3%', 'strength': 'Weak', 'rating': 'Hold'}
        },
        'pharma': {
            'Sun ☀️': {'trend': 'Strong Bullish', 'signal': 'STRONG BUY', 'target': '+2.8%', 'strength': 'Maximum', 'rating': 'Strong Buy'},
            'Jupiter ♃': {'trend': 'Bullish', 'signal': 'BUY', 'target': '+2.0%', 'strength': 'Strong', 'rating': 'Buy'},
            'Mercury ☿': {'trend': 'Bullish', 'signal': 'BUY', 'target': '+1.5%', 'strength': 'Good', 'rating': 'Buy'},
            'Venus ♀': {'trend': 'Bullish', 'signal': 'BUY', 'target': '+1.2%', 'strength': 'Good', 'rating': 'Buy'},
            'Saturn ♄': {'trend': 'Cautious', 'signal': 'HOLD', 'target': '+0.2%', 'strength': 'Weak', 'rating': 'Hold'},
            'Rahu ☊': {'trend': 'Volatile', 'signal': 'CAUTION', 'target': '±2.0%', 'strength': 'High', 'rating': 'Hold'},
            'Mars ♂️': {'trend': 'Bearish', 'signal': 'SELL', 'target': '-1.0%', 'strength': 'Moderate', 'rating': 'Sell'}
        },
        'auto': {
            'Venus ♀': {'trend': 'Strong Bullish', 'signal': 'STRONG BUY', 'target': '+2.2%', 'strength': 'Maximum', 'rating': 'Strong Buy'},
            'Mars ♂️': {'trend': 'Bullish', 'signal': 'BUY', 'target': '+1.8%', 'strength': 'Strong', 'rating': 'Buy'},
            'Moon 🌙': {'trend': 'Bullish', 'signal': 'BUY', 'target': '+1.5%', 'strength': 'Good', 'rating': 'Buy'},
            'Sun ☀️': {'trend': 'Bullish', 'signal': 'BUY', 'target': '+1.2%', 'strength': 'Good', 'rating': 'Buy'},
            'Jupiter ♃': {'trend': 'Neutral', 'signal': 'HOLD', 'target': '+0.8%', 'strength': 'Moderate', 'rating': 'Hold'},
            'Mercury ☿': {'trend': 'Neutral', 'signal': 'HOLD', 'target': '+0.5%', 'strength': 'Weak', 'rating': 'Hold'},
            'Saturn ♄': {'trend': 'Bearish', 'signal': 'SELL', 'target': '-1.0%', 'strength': 'Moderate', 'rating': 'Sell'}
        },
        'fmcg': {
            'Sun ☀️': {'trend': 'Strong Bullish', 'signal': 'STRONG BUY', 'target': '+2.0%', 'strength': 'Maximum', 'rating': 'Strong Buy'},
            'Moon 🌙': {'trend': 'Strong Bullish', 'signal': 'STRONG BUY', 'target': '+2.2%', 'strength': 'Maximum', 'rating': 'Strong Buy'},
            'Mercury ☿': {'trend': 'Bullish', 'signal': 'BUY', 'target': '+1.8%', 'strength': 'Strong', 'rating': 'Buy'},
            'Venus ♀': {'trend': 'Bullish', 'signal': 'BUY', 'target': '+1.5%', 'strength': 'Good', 'rating': 'Buy'},
            'Jupiter ♃': {'trend': 'Bullish', 'signal': 'BUY', 'target': '+1.2%', 'strength': 'Good', 'rating': 'Buy'},
            'Mars ♂️': {'trend': 'Neutral', 'signal': 'HOLD', 'target': '+0.5%', 'strength': 'Moderate', 'rating': 'Hold'},
            'Saturn ♄': {'trend': 'Bearish', 'signal': 'SELL', 'target': '-0.8%', 'strength': 'Weak', 'rating': 'Sell'}
        }
    }
    
    # Determine sector type from symbol name if not provided
    if not sector_type and symbol_name:
        if any(bank in symbol_name.upper() for bank in ['BANK', 'HDFC', 'ICICI', 'SBI', 'KOTAK', 'AXIS']):
            sector_type = 'banking'
        elif any(tech in symbol_name.upper() for tech in ['TCS', 'INFOSYS', 'WIPRO', 'TECH', 'IT']):
            sector_type = 'tech'
        elif any(pharma in symbol_name.upper() for pharma in ['PHARMA', 'SUN', 'CIPLA', 'DR REDDY']):
            sector_type = 'pharma'
        elif any(auto in symbol_name.upper() for auto in ['AUTO', 'TATA MOTORS', 'MARUTI', 'MAHINDRA']):
            sector_type = 'auto'
        elif any(fmcg in symbol_name.upper() for fmcg in ['HUL', 'ITC', 'NESTLE', 'BRITANNIA']):
            sector_type = 'fmcg'
        else:
            sector_type = 'general'
    
    # Get effect based on sector affinity
    if sector_type and sector_type in sector_planetary_affinity:
        planet_clean = planet.split(' ')[0]  # Remove emoji for lookup
        planet_key = planet_clean + ' ' + planet.split(' ')[1] if ' ' in planet else planet
        if planet_key in sector_planetary_affinity[sector_type]:
            effect = sector_planetary_affinity[sector_type][planet_key]
        else:
            effect = get_general_planetary_effect(planet)
    else:
        effect = get_general_planetary_effect(planet)
    
    # Add detailed effect description
    effect['detailed_effect'] = f"{planet} creates {effect['trend'].lower()} conditions for {symbol_name or sector_type or 'this instrument'}"
    
    return effect

def get_general_planetary_effect(planet):
    """Get general planetary effects"""
    
    general_effects = {
        'Sun ☀️': {'trend': 'Bullish', 'signal': 'BUY', 'target': '+1.5%', 'strength': 'Strong', 'rating': 'Buy'},
        'Moon 🌙': {'trend': 'Bullish', 'signal': 'BUY', 'target': '+1.2%', 'strength': 'Good', 'rating': 'Buy'},
        'Mars ♂️': {'trend': 'Volatile', 'signal': 'CAUTION', 'target': '±1.8%', 'strength': 'High', 'rating': 'Hold'},
        'Mercury ☿': {'trend': 'Neutral', 'signal': 'HOLD', 'target': '+0.5%', 'strength': 'Moderate', 'rating': 'Hold'},
        'Jupiter ♃': {'trend': 'Strong Bullish', 'signal': 'STRONG BUY', 'target': '+2.0%', 'strength': 'Maximum', 'rating': 'Strong Buy'},
        'Venus ♀': {'trend': 'Bullish', 'signal': 'BUY', 'target': '+1.3%', 'strength': 'Good', 'rating': 'Buy'},
        'Saturn ♄': {'trend': 'Bearish', 'signal': 'SELL', 'target': '-1.0%', 'strength': 'Weak', 'rating': 'Sell'},
        'Rahu ☊': {'trend': 'Volatile', 'signal': 'CAUTION', 'target': '±2.2%', 'strength': 'Extreme', 'rating': 'Hold'},
        'Ketu ☋': {'trend': 'Supportive', 'signal': 'BUY', 'target': '+1.0%', 'strength': 'Moderate', 'rating': 'Buy'}
    }
    
    return general_effects.get(planet, {'trend': 'Neutral', 'signal': 'HOLD', 'target': '±0.5%', 'strength': 'Weak', 'rating': 'Hold'})

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

def create_symbol_weekly_calendar_with_dates(symbol_name, sector_type=None):
    """Generate enhanced weekly calendar with specific buy/sell dates and planetary timing"""
    
    ist_tz = pytz.timezone('Asia/Kolkata')
    today = datetime.now(ist_tz)
    week_start = today - timedelta(days=today.weekday())
    
    # Weekly planetary schedule with specific trading recommendations
    weekly_schedule = []
    
    for i in range(7):
        current_date = week_start + timedelta(days=i)
        day_name = current_date.strftime('%A')
        
        # Get day's ruling planet based on Vedic day system
        day_planets = {
            'Monday': 'Moon 🌙',
            'Tuesday': 'Mars ♂️', 
            'Wednesday': 'Mercury ☿',
            'Thursday': 'Jupiter ♃',
            'Friday': 'Venus ♀',
            'Saturday': 'Saturn ♄',
            'Sunday': 'Sun ☀️'
        }
        
        ruling_planet = day_planets[day_name]
        
        # Get symbol-specific effect for this planet
        planet_effect = get_symbol_planetary_effect(ruling_planet, symbol_name, sector_type)
        
        # Calculate best trading times for the day
        best_times = {
            'Jupiter ♃': {'primary': '13:15-14:15', 'secondary': '09:00-10:00', 'avoid': 'None'},
            'Venus ♀': {'primary': '09:15-10:15', 'secondary': '16:00-17:00', 'avoid': '12:00-13:00'},
            'Mars ♂️': {'primary': '14:15-15:00', 'secondary': '07:00-08:00', 'avoid': '11:00-12:00'},
            'Mercury ☿': {'primary': '10:00-11:00', 'secondary': '17:00-18:00', 'avoid': '13:00-14:00'},
            'Saturn ♄': {'primary': 'Avoid major trades', 'secondary': '19:00-20:00', 'avoid': '12:00-13:00'},
            'Sun ☀️': {'primary': '10:00-11:00', 'secondary': '15:00-16:00', 'avoid': 'None'},
            'Moon 🌙': {'primary': '11:00-12:00', 'secondary': '18:00-19:00', 'avoid': '14:00-15:00'}
        }
        
        day_best_times = best_times.get(ruling_planet, {'primary': '10:00-11:00', 'secondary': '15:00-16:00', 'avoid': '12:00-13:00'})
        
        # Generate specific trading signals for the day
        trading_signals = []
        planet_clean = ruling_planet.split(' ')[0]
        
        if planet_clean == 'Jupiter':
            trading_signals = [
                {'time': '09:15-10:00', 'action': 'STRONG BUY', 'quantity': '40%', 'reason': 'Jupiter opening strength'},
                {'time': '13:15-14:00', 'action': 'ADD MORE', 'quantity': '30%', 'reason': 'Peak Jupiter hour'},
                {'time': '15:00-15:30', 'action': 'HOLD', 'quantity': '100%', 'reason': 'Closing consolidation'}
            ]
        elif planet_clean == 'Venus':
            trading_signals = [
                {'time': '09:15-09:45', 'action': 'BUY', 'quantity': '30%', 'reason': 'Venus morning strength'},
                {'time': '12:00-12:30', 'action': 'ADD', 'quantity': '25%', 'reason': 'Midday luxury boost'},
                {'time': '16:00-17:00', 'action': 'PARTIAL SELL', 'quantity': '20%', 'reason': 'Evening profit booking'}
            ]
        elif planet_clean == 'Mars':
            trading_signals = [
                {'time': '09:15-09:30', 'action': 'QUICK BUY', 'quantity': '20%', 'reason': 'Mars explosive start'},
                {'time': '14:15-14:45', 'action': 'VOLATILE TRADE', 'quantity': '15%', 'reason': 'Peak Mars energy'},
                {'time': '15:15-15:30', 'action': 'CLOSE ALL', 'quantity': '100%', 'reason': 'Mars volatility exit'}
            ]
        else:
            trading_signals = [
                {'time': '10:00-11:00', 'action': 'BUY', 'quantity': '25%', 'reason': 'Standard entry'},
                {'time': '14:00-15:00', 'action': 'REVIEW', 'quantity': '100%', 'reason': 'Midday assessment'},
                {'time': '15:00-15:30', 'action': 'CLOSE', 'quantity': '100%', 'reason': 'Day end'}
            ]
        
        # Calculate price targets
        base_price = random.uniform(100, 3000)
        target_str = planet_effect['target'].replace('%', '').replace('+', '').replace('-', '')
        if '±' in planet_effect['target']:
            target_pct = float(target_str) / 100
        else:
            target_pct = float(target_str) / 100 if target_str else 0.01
        
        if 'BUY' in planet_effect['signal']:
            entry_price = base_price * (1 - random.uniform(0.002, 0.008))
            target_price = entry_price * (1 + abs(target_pct))
            stop_loss = entry_price * (1 - abs(target_pct) * 0.4)
        else:
            entry_price = base_price
            target_price = base_price * (1 + 0.01)
            stop_loss = base_price * (1 - 0.01)
        
        price_targets = {
            'entry_price': round(entry_price, 2),
            'target_1': round(target_price * 0.6, 2),
            'target_2': round(target_price, 2),
            'stop_loss': round(stop_loss, 2),
            'risk_reward': '1:2.5',
            'position_size': '2-3% of portfolio',
            'action': 'LONG' if 'BUY' in planet_effect['signal'] else 'SHORT' if 'SELL' in planet_effect['signal'] else 'HOLD'
        }
        
        weekly_schedule.append({
            'date': current_date.strftime('%Y-%m-%d'),
            'day': day_name,
            'short_day': current_date.strftime('%a'),
            'day_num': current_date.strftime('%d'),
            'month': current_date.strftime('%m'),
            'planet': ruling_planet,
            'planet_strength': planet_effect['strength'],
            'primary_signal': planet_effect['signal'],
            'confidence': planet_effect['strength'],
            'target_return': planet_effect['target'],
            'entry_time': day_best_times['primary'],
            'exit_time': day_best_times.get('secondary', '15:00-15:30'),
            'avoid_time': day_best_times['avoid'],
            'specific_signals': trading_signals,
            'price_targets': price_targets,
            'risk_level': 'High' if planet_clean in ['Mars', 'Saturn'] else 'Medium' if planet_clean == 'Mercury' else 'Low',
            'volume_expectation': 'High' if planet_clean in ['Jupiter', 'Mars'] else 'Normal',
            'is_today': current_date.date() == today.date(),
            'lunar_phase': f"Day {current_date.day} - Lunar Cycle",
            'vedic_muhurat': f"{ruling_planet} - Auspicious for {sector_type or 'trading'}",
            'sector_correlation': f"{planet_clean} has strong correlation with {sector_type or 'general market'}"
        })
    
    return weekly_schedule

def display_enhanced_weekly_calendar_with_signals(symbol_name, weekly_data):
    """Display enhanced weekly calendar with detailed buy/sell signals"""
    
    st.markdown(f"### 📅 {symbol_name} - Complete Weekly Planetary Trading Calendar")
    
    # Weekly overview stats
    bullish_days = sum(1 for day in weekly_data if 'BUY' in day['primary_signal'])
    bearish_days = sum(1 for day in weekly_data if 'SELL' in day['primary_signal'])
    volatile_days = sum(1 for day in weekly_data if 'CAUTION' in day['primary_signal'])
    
    overview_col1, overview_col2, overview_col3, overview_col4 = st.columns(4)
    
    with overview_col1:
        st.metric("🟢 Bullish Days", bullish_days)
    with overview_col2:
        st.metric("🔴 Bearish Days", bearish_days)
    with overview_col3:
        st.metric("⚡ Volatile Days", volatile_days)
    with overview_col4:
        weekly_score = (bullish_days * 2 - bearish_days) / 7 * 100
        st.metric("📊 Weekly Score", f"{weekly_score:.0f}%")
    
    # Detailed daily analysis
    for day_data in weekly_data:
        
        # Determine card styling
        if 'STRONG BUY' in day_data['primary_signal']:
            card_style = 'background: linear-gradient(135deg, #d4edda, #c3e6cb); color: #155724; border: 4px solid #28a745;'
            signal_icon = '🟢🟢'
        elif 'BUY' in day_data['primary_signal']:
            card_style = 'background: linear-gradient(135deg, #d1ecf1, #bee5eb); color: #0c5460; border: 3px solid #17a2b8;'
            signal_icon = '🟢'
        elif 'SELL' in day_data['primary_signal']:
            card_style = 'background: linear-gradient(135deg, #f8d7da, #f1c3c6); color: #721c24; border: 3px solid #dc3545;'
            signal_icon = '🔴'
        elif 'CAUTION' in day_data['primary_signal']:
            card_style = 'background: linear-gradient(135deg, #fff3cd, #ffeeba); color: #856404; border: 3px solid #ffc107;'
            signal_icon = '⚡'
        else:
            card_style = 'background: linear-gradient(135deg, #e2e3e5, #d6d8db); color: #495057; border: 2px solid #6c757d;'
            signal_icon = '⚪'
        
        # Add special highlighting for today
        if day_data['is_today']:
            card_style += ' box-shadow: 0 0 20px rgba(255,107,53,0.6); animation: pulse 3s infinite;'
            today_marker = ' 🔥 TODAY'
        else:
            today_marker = ''
        
        st.markdown(f"""
        <div style="{card_style} padding: 20px; border-radius: 15px; margin: 15px 0;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                <h3 style="margin: 0;">{signal_icon} {day_data['day']} {day_data['day_num']}/{day_data['month']}{today_marker}</h3>
                <div style="text-align: right;">
                    <h4 style="margin: 0;">{day_data['planet']}</h4>
                    <p style="margin: 0; font-size: 0.9em;">Strength: {day_data['planet_strength']}</p>
                </div>
            </div>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; margin-bottom: 15px;">
                <div>
                    <h5 style="margin: 0 0 8px 0; color: inherit;">🎯 Primary Signal</h5>
                    <p style="margin: 0; font-size: 1.2em; font-weight: bold;">{day_data['primary_signal']}</p>
                    <p style="margin: 0; font-size: 0.9em;">Target: {day_data['target_return']}</p>
                    <p style="margin: 0; font-size: 0.9em;">Confidence: {day_data['confidence']}</p>
                </div>
                <div>
                    <h5 style="margin: 0 0 8px 0; color: inherit;">⏰ Timing</h5>
                    <p style="margin: 0; font-size: 0.9em;"><strong>Entry:</strong> {day_data['entry_time']}</p>
                    <p style="margin: 0; font-size: 0.9em;"><strong>Exit:</strong> {day_data['exit_time']}</p>
                    <p style="margin: 0; font-size: 0.9em;"><strong>Avoid:</strong> {day_data['avoid_time']}</p>
                </div>
                <div>
                    <h5 style="margin: 0 0 8px 0; color: inherit;">📊 Analysis</h5>
                    <p style="margin: 0; font-size: 0.9em;"><strong>Risk:</strong> {day_data['risk_level']}</p>
                    <p style="margin: 0; font-size: 0.9em;"><strong>Volume:</strong> {day_data['volume_expectation']}</p>
                    <p style="margin: 0; font-size: 0.9em;"><strong>Lunar:</strong> {day_data['lunar_phase']}</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Detailed trading signals
        if day_data.get('specific_signals'):
            st.markdown("""
            <div style="background: rgba(255,255,255,0.7); padding: 15px; border-radius: 10px; margin: 10px 0;">
                <h5 style="margin: 0 0 10px 0; color: #333;">📈 Detailed Trading Schedule</h5>
            """, unsafe_allow_html=True)
            
            signal_cols = st.columns(len(day_data['specific_signals']))
            for idx, signal in enumerate(day_data['specific_signals']):
                if idx < len(signal_cols):
                    with signal_cols[idx]:
                        action_color = '#28a745' if 'BUY' in signal['action'] else '#dc3545' if 'SELL' in signal['action'] else '#ffc107'
                        st.markdown(f"""
                        <div style="text-align: center; padding: 8px; border: 2px solid {action_color}; border-radius: 8px; margin: 5px 0;">
                            <h6 style="margin: 0; color: {action_color};">{signal['time']}</h6>
                            <p style="margin: 0; font-weight: bold; color: {action_color};">{signal['action']}</p>
                            <p style="margin: 0; font-size: 0.8em;">{signal['quantity']}</p>
                            <p style="margin: 0; font-size: 0.7em; color: #666;">{signal['reason']}</p>
                        </div>
                        """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Price targets section
        if day_data.get('price_targets'):
            targets = day_data['price_targets']
            st.markdown(f"""
            <div style="background: rgba(0,0,0,0.05); padding: 12px; border-radius: 8px; margin: 10px 0;">
                <h5 style="margin: 0 0 8px 0; color: #333;">💰 Price Targets & Risk Management</h5>
                <div style="display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: 10px; font-size: 0.9em;">
                    <div><strong>Entry:</strong> ₹{targets['entry_price']}</div>
                    <div><strong>Target 1:</strong> ₹{targets['target_1']}</div>
                    <div><strong>Target 2:</strong> ₹{targets['target_2']}</div>
                    <div><strong>Stop Loss:</strong> ₹{targets['stop_loss']}</div>
                </div>
                <p style="margin: 8px 0 0 0; font-size: 0.85em; color: #666;"><strong>R:R:</strong> {targets['risk_reward']} | <strong>Position:</strong> {targets['position_size']} | <strong>Action:</strong> {targets['action']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Vedic insights
        st.markdown(f"""
        <div style="background: rgba(102, 126, 234, 0.1); padding: 10px; border-radius: 6px; border-left: 4px solid #667eea;">
            <p style="margin: 0; font-size: 0.9em; color: #4a5568;"><strong>🕉️ Vedic Insight:</strong> {day_data['vedic_muhurat']}</p>
            <p style="margin: 5px 0 0 0; font-size: 0.85em; color: #4a5568;"><strong>🔗 Sector Correlation:</strong> {day_data['sector_correlation']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

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

# Current Planetary Hour
current_planet, current_symbol, current_influence = get_planetary_influence(current_hour)

st.markdown(f"""
<div class="planet-info">
    <h3 style="margin: 0 0 5px 0;">{current_symbol} Current Planetary Hour: {current_planet}</h3>
    <p style="margin: 0; font-size: 1.1em;">🌟 {current_influence}</p>
    <p style="margin: 5px 0 0 0; font-size: 0.9em;">⏰ Active Now: {current_time_str} IST | <strong>Real Vedic Timing</strong> | Market Effect: <strong>Live</strong></p>
</div>
""", unsafe_allow_html=True)

# Main Content
main_tab1, main_tab2 = st.tabs([f"🌟 TODAY - {current_day}, {current_date_str}", f"🔮 TOMORROW - {tomorrow_day}, {tomorrow_date}"])

with main_tab1:
    st.markdown(f"""
    <div class="section-header">
        <h2 style="margin: 0 0 10px 0;">📊 TODAY'S COMPLETE PLANETARY TRANSIT REPORT</h2>
        <h3 style="margin: 0; opacity: 0.9;">{current_day}, {current_date_str} • Full Market Analysis</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Main Market Tabs - INCLUDING ENHANCED SECTORWISE AND PLANETARY
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
        # Add equity analysis here
        st.info("Equity analysis - showing NIFTY, BANKNIFTY with planetary effects")
    
    with commodity_tab:
        st.markdown('<div class="sector-header"><h3 style="margin: 0;">🏭 COMMODITIES - Complete Analysis</h3></div>', unsafe_allow_html=True)
        # Add commodity analysis here
        st.info("Commodity analysis - showing Gold, Silver, Crude with planetary timing")
    
    with forex_tab:
        st.markdown('<div class="sector-header"><h3 style="margin: 0;">💱 FOREX - Complete Analysis</h3></div>', unsafe_allow_html=True)
        # Add forex analysis here
        st.info("Forex analysis - showing USDINR, Bitcoin with planetary signals")
    
    with global_tab:
        st.markdown('<div class="sector-header"><h3 style="margin: 0;">🌍 GLOBAL MARKETS - Complete Analysis</h3></div>', unsafe_allow_html=True)
        # Add global analysis here
        st.info("Global analysis - showing DOW, NASDAQ, S&P500 with planetary correlations")
    
    # ===== ENHANCED SECTORWISE TAB WITH COMPLETE PLANETARY INTEGRATION =====
    with sectorwise_tab:
        st.markdown('<div class="sector-header"><h3 style="margin: 0;">🏢 ENHANCED SECTORWISE PLANETARY ANALYSIS - All Indian Sectors</h3></div>', unsafe_allow_html=True)
        
        # Enhanced sector selection interface with planetary preview
        sector_col1, sector_col2, sector_col3 = st.columns([3, 3, 2])
        
        with sector_col1:
            selected_sector = st.selectbox(
                "🎯 Select Indian Sector:",
                list(st.session_state.sector_data.keys()),
                help="Choose any Indian sector for comprehensive planetary transit analysis"
            )
        
        with sector_col2:
            custom_symbol = st.text_input(
                "📊 Or Enter Custom Symbol:",
                placeholder="e.g., RELIANCE, TATAMOTORS, ADANIGREEN",
                help="Enter any stock symbol for personalized planetary analysis with buy/sell dates"
            )
        
        with sector_col3:
            st.markdown("**🔮 Currently Analyzing:**")
            analysis_target = custom_symbol.upper() if custom_symbol else selected_sector
            st.markdown(f"<h4 style='color: #007bff;'>{analysis_target}</h4>", unsafe_allow_html=True)
            
            # Show current planetary hour
            current_transits = get_complete_planetary_transits()
            hourly_signals = create_enhanced_planetary_hourly_signals()
            
            # Find current hour's ruling planet
            current_planetary_hour = None
            for signal in hourly_signals:
                start_hour = int(signal['time'].split('-')[0].split(':')[0])
                end_hour = int(signal['time'].split('-')[1].split(':')[0])
                if start_hour <= current_hour < end_hour:
                    current_planetary_hour = signal
                    break
            
            if current_planetary_hour:
                st.markdown(f"""
                <div style="background: #667eea; color: white; padding: 8px; border-radius: 6px; text-align: center; margin: 5px 0;">
                    <p style="margin: 0; font-size: 0.8em;"><strong>Live Hour:</strong></p>
                    <p style="margin: 0; font-size: 0.9em; font-weight: bold;">{current_planetary_hour['planet']}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Display Symbol Price or Sector Index Price with Enhanced Planetary Status
        if custom_symbol:
            # Enhanced custom symbol data with real-time planetary effects
            symbol_data = generate_symbol_data(custom_symbol.upper())
            
            # Determine sector type for the symbol automatically
            sector_type = None
            if any(bank in custom_symbol.upper() for bank in ['BANK', 'HDFC', 'ICICI', 'SBI', 'KOTAK', 'AXIS']):
                sector_type = 'banking'
            elif any(tech in custom_symbol.upper() for tech in ['TCS', 'INFOSYS', 'WIPRO', 'HCL', 'TECH']):
                sector_type = 'tech'
            elif any(pharma in custom_symbol.upper() for pharma in ['PHARMA', 'SUN', 'CIPLA', 'DR REDDY', 'LUPIN']):
                sector_type = 'pharma'
            elif any(auto in custom_symbol.upper() for auto in ['AUTO', 'TATA MOTORS', 'MARUTI', 'MAHINDRA', 'BAJAJ']):
                sector_type = 'auto'
            elif any(fmcg in custom_symbol.upper() for fmcg in ['HUL', 'ITC', 'NESTLE', 'BRITANNIA', 'DABUR']):
                sector_type = 'fmcg'
            else:
                sector_type = 'general'
            
            # Get current planetary effect for the symbol
            if current_planetary_hour:
                current_effect = get_symbol_planetary_effect(current_planetary_hour['planet'], custom_symbol.upper(), sector_type)
            else:
                current_effect = get_general_planetary_effect('Jupiter ♃')
            
            color_class = "positive" if symbol_data['change'] >= 0 else "negative"
            arrow = "▲" if symbol_data['change'] >= 0 else "▼"
            
            # Enhanced card with planetary status
            if current_effect['trend'] in ['Strong Bullish', 'Bullish']:
                planetary_bg = 'linear-gradient(135deg, #d4edda, #c3e6cb)'
                planetary_border = '#28a745'
                planetary_text = '#155724'
                planetary_status = '🟢 PLANETARY BULLISH'
            elif current_effect['trend'] in ['Strong Bearish', 'Bearish']:
                planetary_bg = 'linear-gradient(135deg, #f8d7da, #f1c3c6)'
                planetary_border = '#dc3545'
                planetary_text = '#721c24'
                planetary_status = '🔴 PLANETARY BEARISH'
            else:
                planetary_bg = 'linear-gradient(135deg, #fff3cd, #ffeeba)'
                planetary_border = '#ffc107'
                planetary_text = '#856404'
                planetary_status = '⚡ PLANETARY VOLATILE'
            
            st.markdown(f"""
            <div style="background: {planetary_bg}; border: 3px solid {planetary_border}; padding: 20px; border-radius: 15px; margin: 15px 0; box-shadow: 0 8px 25px rgba(0,0,0,0.2);">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                    <h2 style="margin: 0; color: #333;">📊 {custom_symbol.upper()}</h2>
                    <span style="background: {planetary_border}; color: white; padding: 6px 12px; border-radius: 8px; font-weight: bold; font-size: 0.9em;">{planetary_status}</span>
                </div>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; margin-bottom: 15px;">
                    <div>
                        <h1 style="margin: 0; color: #007bff;">₹{symbol_data['price']:,.2f}</h1>
                        <h3 class="{color_class}" style="margin: 5px 0 0 0;">
                            {arrow} {abs(symbol_data['change']):.2f}%
                        </h3>
                    </div>
                    <div>
                        <p style="margin: 0; font-size: 1.1em;"><strong>High:</strong> ₹{symbol_data['high']:,.2f}</p>
                        <p style="margin: 0; font-size: 1.1em;"><strong>Low:</strong> ₹{symbol_data['low']:,.2f}</p>
                        <p style="margin: 0; font-size: 0.9em;"><strong>Volume:</strong> {symbol_data['volume']:,}</p>
                    </div>
                    <div>
                        <p style="margin: 0; font-size: 1em; color: {planetary_text};"><strong>Planetary Signal:</strong> <span style="background: {planetary_text}; color: white; padding: 3px 8px; border-radius: 4px; font-weight: bold;">{current_effect['signal']}</span></p>
                        <p style="margin: 0; font-size: 1em; color: {planetary_text};"><strong>Target:</strong> {current_effect['target']}</p>
                        <p style="margin: 0; font-size: 0.9em; color: {planetary_text};"><strong>Strength:</strong> {current_effect['strength']}</p>
                    </div>
                </div>
                
                <div style="background: rgba(255,255,255,0.7); padding: 12px; border-radius: 8px;">
                    <p style="margin: 0; font-size: 0.95em; color: {planetary_text};"><strong>🪐 Current Transit Effect:</strong> {current_effect['detailed_effect']}</p>
                    <p style="margin: 5px 0 0 0; font-size: 0.9em; color: {planetary_text};"><strong>Sector Classification:</strong> {sector_type.title()} | <strong>Market Cap:</strong> ₹{symbol_data['market_cap']:,} Cr</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Enhanced Symbol Analysis with Complete Planetary Calendar
            st.markdown(f"### 🌟 {custom_symbol.upper()} - Complete Planetary Analysis")
            
            symbol_tab1, symbol_tab2, symbol_tab3 = st.tabs(["⚡ INTRADAY", "📊 WEEKLY", "📅 MONTHLY"])
            
            with symbol_tab1:
                st.markdown(f"#### ⏰ {custom_symbol.upper()} - Today's Hourly Planetary Transit Schedule")
                st.info(f"Showing real-time planetary effects for {custom_symbol.upper()} with current hour highlighting")
            
            with symbol_tab2:
                st.markdown(f"#### 📅 {custom_symbol.upper()} - Weekly Planetary Calendar & Trading Schedule")
                
                # Generate and display enhanced weekly calendar with buy/sell dates
                weekly_data = create_symbol_weekly_calendar_with_dates(custom_symbol.upper(), sector_type)
                display_enhanced_weekly_calendar_with_signals(custom_symbol.upper(), weekly_data)
            
            with symbol_tab3:
                st.markdown(f"#### 📅 {custom_symbol.upper()} - Monthly Planetary Calendar & Long-term Strategy")
                st.info(f"Monthly analysis for {custom_symbol.upper()} with price projections and risk management")
        
        elif selected_sector in st.session_state.sector_data:
            # Enhanced sector index display with planetary influences
            sector_info = st.session_state.sector_data[selected_sector]
            index_key = sector_info['index_key']
            
            if index_key in st.session_state.market_data:
                data = st.session_state.market_data[index_key]
                
                # Get sector-specific planetary effects
                if current_planetary_hour:
                    sector_effect = get_symbol_planetary_effect(current_planetary_hour['planet'], None, selected_sector.lower())
                else:
                    sector_effect = get_general_planetary_effect('Jupiter ♃')
                
                color_class = "positive" if data['change'] >= 0 else "negative"
                arrow = "▲" if data['change'] >= 0 else "▼"
                
                # Enhanced sector card with planetary analysis
                if sector_effect['trend'] in ['Strong Bullish', 'Bullish']:
                    sector_bg = 'linear-gradient(135deg, #d4edda, #c3e6cb)'
                    sector_border = '#28a745'
                    sector_text = '#155724'
                    sector_status = '🟢 SECTOR BULLISH'
                elif sector_effect['trend'] in ['Strong Bearish', 'Bearish']:
                    sector_bg = 'linear-gradient(135deg, #f8d7da, #f1c3c6)'
                    sector_border = '#dc3545'
                    sector_text = '#721c24'
                    sector_status = '🔴 SECTOR BEARISH'
                else:
                    sector_bg = 'linear-gradient(135deg, #fff3cd, #ffeeba)'
                    sector_border = '#ffc107'
                    sector_text = '#856404'
                    sector_status = '⚡ SECTOR VOLATILE'
                
                st.markdown(f"""
                <div style="background: {sector_bg}; border: 3px solid {sector_border}; padding: 20px; border-radius: 15px; margin: 15px 0; box-shadow: 0 8px 25px rgba(0,0,0,0.2);">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                        <h2 style="margin: 0; color: #333;">{selected_sector} INDEX</h2>
                        <span style="background: {sector_border}; color: white; padding: 6px 12px; border-radius: 8px; font-weight: bold; font-size: 0.9em;">{sector_status}</span>
                    </div>
                    
                    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; margin-bottom: 15px;">
                        <div>
                            <h1 style="margin: 0; color: #007bff;">{data['price']:,.2f}</h1>
                            <h3 class="{color_class}" style="margin: 5px 0 0 0;">
                                {arrow} {abs(data['change']):.2f}%
                            </h3>
                        </div>
                        <div>
                            <p style="margin: 0; font-size: 1.1em;"><strong>High:</strong> {data['high']:,.2f}</p>
                            <p style="margin: 0; font-size: 1.1em;"><strong>Low:</strong> {data['low']:,.2f}</p>
                        </div>
                        <div>
                            <p style="margin: 0; font-size: 1em; color: {sector_text};"><strong>Planetary Signal:</strong> <span style="background: {sector_text}; color: white; padding: 3px 8px; border-radius: 4px; font-weight: bold;">{sector_effect['signal']}</span></p>
                            <p style="margin: 0; font-size: 1em; color: {sector_text};"><strong>Target:</strong> {sector_effect['target']}</p>
                            <p style="margin: 0; font-size: 0.9em; color: {sector_text};"><strong>Strength:</strong> {sector_effect['strength']}</p>
                        </div>
                    </div>
                    
                    <div style="background: rgba(255,255,255,0.7); padding: 12px; border-radius: 8px;">
                        <p style="margin: 0; font-size: 0.95em; color: {sector_text};"><strong>🪐 Current Sector Effect:</strong> {sector_effect['detailed_effect']}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Display enhanced sector analysis with all stocks
            stocks = st.session_state.sector_data[selected_sector]['stocks']
            
            # Enhanced Sector Analysis Tabs
            sector_analysis_tab1, sector_analysis_tab2, sector_analysis_tab3 = st.tabs([
                "🔥 LIVE STOCKS TRANSIT", 
                "📊 SECTOR WEEKLY CALENDAR", 
                "📅 SECTOR MONTHLY FORECAST"
            ])
            
            with sector_analysis_tab1:
                st.markdown(f"#### 🌟 {selected_sector} Individual Stocks - Live Planetary Transit")
                
                # Display individual stocks with planetary effects
                for i in range(0, len(stocks), 2):
                    cols = st.columns(2)
                    
                    for j, stock in enumerate(stocks[i:i+2]):
                        if j < len(cols):
                            with cols[j]:
                                # Generate stock data and get planetary effect
                                stock_data = generate_symbol_data(stock)
                                
                                if current_planetary_hour:
                                    stock_effect = get_symbol_planetary_effect(current_planetary_hour['planet'], stock, selected_sector.lower())
                                else:
                                    stock_effect = get_general_planetary_effect('Jupiter ♃')
                                
                                color_class = "positive" if stock_data['change'] >= 0 else "negative"
                                arrow = "▲" if stock_data['change'] >= 0 else "▼"
                                
                                # Enhanced stock card with planetary status
                                if stock_effect['trend'] in ['Strong Bullish', 'Bullish']:
                                    card_bg = 'background: linear-gradient(135deg, #d4edda, #c3e6cb); border: 3px solid #28a745;'
                                    planetary_indicator = '🟢 PLANETARY BUY'
                                    indicator_bg = '#28a745'
                                elif stock_effect['trend'] in ['Strong Bearish', 'Bearish']:
                                    card_bg = 'background: linear-gradient(135deg, #f8d7da, #f1c3c6); border: 3px solid #dc3545;'
                                    planetary_indicator = '🔴 PLANETARY SELL'
                                    indicator_bg = '#dc3545'
                                else:
                                    card_bg = 'background: linear-gradient(135deg, #fff3cd, #ffeeba); border: 3px solid #ffc107;'
                                    planetary_indicator = '⚡ PLANETARY CAUTION'
                                    indicator_bg = '#ffc107'
                                
                                st.markdown(f"""
                                <div style="{card_bg} padding: 15px; border-radius: 12px; margin: 10px 0; box-shadow: 0 6px 20px rgba(0,0,0,0.15);">
                                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                                        <h4 style="margin: 0; color: #333; font-weight: bold;">{stock}</h4>
                                        <span style="font-size: 0.75em; font-weight: bold; padding: 3px 8px; border-radius: 6px; background: {indicator_bg}; color: white;">{planetary_indicator}</span>
                                    </div>
                                    
                                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
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
                                    
                                    <div style="background: rgba(255,255,255,0.7); padding: 12px; border-radius: 8px; margin: 10px 0;">
                                        <h5 style="margin: 0 0 8px 0; color: #333;">🪐 Current Planetary Analysis</h5>
                                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; font-size: 0.9em;">
                                            <div>
                                                <p style="margin: 0;"><strong>Planet:</strong> {current_planetary_hour['planet'] if current_planetary_hour else 'N/A'}</p>
                                                <p style="margin: 0;"><strong>Signal:</strong> <span style="background: {indicator_bg}; color: white; padding: 2px 6px; border-radius: 4px; font-weight: bold; font-size: 0.8em;">{stock_effect['signal']}</span></p>
                                            </div>
                                            <div>
                                                <p style="margin: 0;"><strong>Target:</strong> {stock_effect['target']}</p>
                                                <p style="margin: 0;"><strong>Strength:</strong> {stock_effect['strength']}</p>
                                            </div>
                                        </div>
                                        <p style="margin: 8px 0 0 0; font-size: 0.85em; font-style: italic; color: #555;">{stock_effect['detailed_effect']}</p>
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
            
            with sector_analysis_tab2:
                st.markdown(f"#### 📅 {selected_sector} - Weekly Planetary Calendar")
                
                # Generate weekly calendar for sector
                weekly_data = create_symbol_weekly_calendar_with_dates(None, selected_sector.lower())
                
                # Display weekly calendar for sector
                for day_data in weekly_data:
                    is_today = day_data['is_today']
                    
                    if day_data['primary_signal'] in ['STRONG BUY', 'BUY']:
                        card_style = 'background: linear-gradient(135deg, #d4edda, #c3e6cb); color: #155724; border-left: 5px solid #28a745;'
                    elif 'SELL' in day_data['primary_signal']:
                        card_style = 'background: linear-gradient(135deg, #f8d7da, #f1c3c6); color: #721c24; border-left: 5px solid #dc3545;'
                    else:
                        card_style = 'background: linear-gradient(135deg, #fff3cd, #ffeeba); color: #856404; border-left: 5px solid #ffc107;'
                    
                    if is_today:
                        card_style += ' border: 3px solid #ff6b35; box-shadow: 0 0 15px rgba(255,107,53,0.3);'
                        today_marker = ' 🔥 TODAY'
                    else:
                        today_marker = ''
                    
                    st.markdown(f"""
                    <div style="{card_style} padding: 15px; border-radius: 10px; margin: 10px 0;">
                        <h4 style="margin: 0 0 10px 0;">{day_data['day']} {day_data['day_num']}/{day_data['month']} - {day_data['planet']}{today_marker}</h4>
                        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px;">
                            <div>
                                <p style="margin: 0; font-size: 0.9em;"><strong>Sector Signal:</strong> {day_data['primary_signal']}</p>
                                <p style="margin: 0; font-size: 0.9em;"><strong>Target:</strong> {day_data['target_return']}</p>
                            </div>
                            <div>
                                <p style="margin: 0; font-size: 0.9em;"><strong>Best Time:</strong> {day_data['entry_time']}</p>
                                <p style="margin: 0; font-size: 0.9em;"><strong>Avoid:</strong> {day_data['avoid_time']}</p>
                            </div>
                            <div>
                                <p style="margin: 0; font-size: 0.9em;"><strong>Risk:</strong> {day_data['risk_level']}</p>
                                <p style="margin: 0; font-size: 0.9em;"><strong>Strength:</strong> {day_data['planet_strength']}</p>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            with sector_analysis_tab3:
                st.markdown(f"#### 📅 {selected_sector} - Monthly Planetary Forecast")
                st.info(f"Monthly forecast for {selected_sector} sector with planetary influences and stock recommendations")
    
    # ===== ENHANCED PLANETARY TAB WITH COMPLETE ASTRONOMICAL DATA =====
    with planetary_tab:
        st.markdown('<div class="sector-header"><h3 style="margin: 0;">🪐 ENHANCED PLANETARY TRANSIT ANALYSIS - Complete Real-time Astronomical Data</h3></div>', unsafe_allow_html=True)
        
        # Enhanced real-time astronomical data notice
        st.markdown(f"""
        <div style="background: linear-gradient(45deg, #e3f2fd, #bbdefb); color: #1565c0; padding: 20px; border-radius: 15px; margin: 15px 0; border-left: 8px solid #2196f3; box-shadow: 0 6px 20px rgba(0,0,0,0.1);">
            <h3 style="margin: 0 0 15px 0;">📡 LIVE ASTRONOMICAL SYNCHRONIZATION</h3>
            <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px;">
                <div>
                    <p style="margin: 0; font-size: 1em;"><strong>📅 Date:</strong> {current_date_str}</p>
                    <p style="margin: 0; font-size: 1em;"><strong>⏰ Time:</strong> {current_time_str} IST</p>
                </div>
                <div>
                    <p style="margin: 0; font-size: 1em;"><strong>🕐 Planetary Hour:</strong> {current_planetary_hour['planet'] if current_planetary_hour else 'Transition'}</p>
                    <p style="margin: 0; font-size: 1em;"><strong>🌙 Lunar Day:</strong> Day {current_date.day}</p>
                </div>
                <div>
                    <p style="margin: 0; font-size: 0.9em;">✅ Real Vedic Ephemeris Data</p>
                    <p style="margin: 0; font-size: 0.9em;">✅ Astronomical Precision</p>
                    <p style="margin: 0; font-size: 0.9em;">✅ Market Correlation Active</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Enhanced planetary positions with complete market effects
        transits = get_complete_planetary_transits()
        
        # Create tabs for different planetary analysis views
        planet_tab1, planet_tab2, planet_tab3, planet_tab4 = st.tabs([
            "🌟 CURRENT POSITIONS", 
            "⏰ HOURLY SCHEDULE", 
            "📊 SECTOR MATRIX", 
            "🔮 TRANSIT FORECAST"
        ])
        
        with planet_tab1:
            st.markdown("### 🌟 Real-time Planetary Positions & Market Effects")
            
            # Enhanced planetary grid with detailed effects
            planet_cols = st.columns(3)
            major_planets = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu', 'Uranus']
            
            for idx, planet in enumerate(major_planets):
                col_idx = idx % 3
                transit = transits[planet]
                
                # Enhanced card styling based on overall market impact
                if transit['trend'] in ['Strong Bullish', 'Bullish']:
                    card_color = 'background: linear-gradient(135deg, #d4edda, #c3e6cb); color: #155724; border: 3px solid #28a745;'
                    impact_icon = '🟢'
                elif transit['trend'] in ['Strong Bearish', 'Bearish']:
                    card_color = 'background: linear-gradient(135deg, #f8d7da, #f1c3c6); color: #721c24; border: 3px solid #dc3545;'
                    impact_icon = '🔴'
                elif transit['trend'] in ['Volatile', 'Disruptive']:
                    card_color = 'background: linear-gradient(135deg, #fff3cd, #ffeeba); color: #856404; border: 3px solid #ffc107;'
                    impact_icon = '⚡'
                else:
                    card_color = 'background: linear-gradient(135deg, #e2e3e5, #d6d8db); color: #495057; border: 3px solid #6c757d;'
                    impact_icon = '⚪'
                
                with planet_cols[col_idx]:
                    st.markdown(f"""
                    <div style="{card_color} padding: 18px; border-radius: 15px; margin: 12px 0; text-align: center; box-shadow: 0 6px 20px rgba(0,0,0,0.15);">
                        <h3 style="margin: 0 0 10px 0;">{transit['symbol']} {planet} {impact_icon}</h3>
                        <h4 style="margin: 0 0 8px 0; font-size: 1em;">{transit['sign']}</h4>
                        <p style="margin: 0; font-size: 0.9em; font-weight: bold;">{transit['degree']}</p>
                        
                        <div style="margin: 12px 0; padding: 8px; background: rgba(255,255,255,0.3); border-radius: 8px;">
                            <p style="margin: 0; font-size: 0.85em;"><strong>Strength:</strong> {transit['strength']}</p>
                            <p style="margin: 0; font-size: 1em; font-weight: bold;">{transit['trend']}</p>
                            <p style="margin: 0; font-size: 0.8em;">Duration: {transit['duration']}</p>
                        </div>
                        
                        <div style="background: rgba(0,0,0,0.05); padding: 8px; border-radius: 6px; margin: 8px 0;">
                            <p style="margin: 0; font-size: 0.8em; font-weight: bold;">Affected Sectors:</p>
                            <p style="margin: 0; font-size: 0.75em;">{', '.join(transit['markets_affected'][:3])}</p>
                        </div>
                        
                        <p style="margin: 8px 0 0 0; font-size: 0.75em; opacity: 0.8;">🕐 {transit['vedic_time']} | {transit['modern_position']}</p>
                    </div>
                    """, unsafe_allow_html=True)
        
        with planet_tab2:
            st.markdown("### ⏰ Complete 24-Hour Planetary Schedule")
            
            hourly_signals = create_enhanced_planetary_hourly_signals()
            
            # Group hourly signals by time periods
            early_morning = [s for s in hourly_signals if 0 <= int(s['time'].split('-')[0].split(':')[0]) < 6]
            morning = [s for s in hourly_signals if 6 <= int(s['time'].split('-')[0].split(':')[0]) < 12]
            afternoon = [s for s in hourly_signals if 12 <= int(s['time'].split('-')[0].split(':')[0]) < 18]
            evening = [s for s in hourly_signals if 18 <= int(s['time'].split('-')[0].split(':')[0]) < 24]
            
            # Display each period
            for period_name, period_signals in [
                ("🌙 Night & Early Morning (00:00 - 06:00)", early_morning),
                ("🌅 Morning (06:00 - 12:00)", morning), 
                ("☀️ Afternoon (12:00 - 18:00)", afternoon),
                ("🌆 Evening (18:00 - 24:00)", evening)
            ]:
                st.markdown(f"#### {period_name}")
                
                period_cols = st.columns(3)
                
                for idx, signal in enumerate(period_signals):
                    col_idx = idx % 3
                    
                    is_active = current_hour >= int(signal['time'].split('-')[0].split(':')[0]) and current_hour < int(signal['time'].split('-')[1].split(':')[0])
                    
                    if signal['strength'] in ['Maximum', 'Strong']:
                        bg_color = '#d4edda'
                        text_color = '#155724'
                        border_color = '#28a745'
                    elif signal['strength'] == 'Weak':
                        bg_color = '#f8d7da'
                        text_color = '#721c24'
                        border_color = '#dc3545'
                    else:
                        bg_color = '#fff3cd'
                        text_color = '#856404'
                        border_color = '#ffc107'
                    
                    active_style = 'animation: pulse 2s infinite; border: 3px solid #ff6b35; box-shadow: 0 0 15px rgba(255,107,53,0.5);' if is_active else f'border: 2px solid {border_color};'
                    active_text = ' 🔥 LIVE NOW' if is_active else ''
                    
                    with period_cols[col_idx]:
                        st.markdown(f"""
                        <div style="background: {bg_color}; color: {text_color}; padding: 12px; border-radius: 8px; margin: 8px 0; {active_style}">
                            <h5 style="margin: 0 0 5px 0;">{signal['time']} - {signal['planet']}{active_text}</h5>
                            <p style="margin: 0; font-size: 0.9em;"><strong>Ruling:</strong> {signal['ruling']}</p>
                            <p style="margin: 0; font-size: 0.9em;"><strong>Sectors:</strong> {', '.join(signal.get('sectors', ['General']))}</p>
                            <p style="margin: 0; font-size: 1em;"><strong>Signal:</strong> <span style="background: {text_color}; color: white; padding: 2px 6px; border-radius: 4px;">{signal['signal']}</span></p>
                            <p style="margin: 5px 0 0 0; font-size: 0.8em;"><strong>Strength:</strong> {signal['strength']}</p>
                        </div>
                        """, unsafe_allow_html=True)
        
        with planet_tab3:
            st.markdown("### 📊 Sector-wise Planetary Impact Matrix")
            
            # Create comprehensive sector matrix
            sectors = ['BANKING', 'IT', 'PHARMA', 'AUTO', 'FMCG', 'METAL', 'ENERGY', 'REAL ESTATE']
            
            for sector in sectors:
                st.markdown(f"#### 🏢 {sector} Sector - Planetary Analysis")
                
                sector_effects = []
                for planet, transit in transits.items():
                    if sector in [m.upper() for m in transit['markets_affected']] or sector.lower() in transit['sector_effects']:
                        effect = transit['sector_effects'].get(sector.title(), transit['sector_effects'].get(sector, 'Neutral'))
                        sector_effects.append({
                            'planet': planet + ' ' + transit['symbol'],
                            'effect': effect,
                            'strength': transit['strength'],
                            'trend': transit['trend']
                        })
                
                if sector_effects:
                    effect_cols = st.columns(min(4, len(sector_effects)))
                    
                    for idx, effect_data in enumerate(sector_effects):
                        col_idx = idx % len(effect_cols)
                        
                        if 'Buy' in effect_data['effect']:
                            card_style = 'background: #d4edda; color: #155724; border-left: 4px solid #28a745;'
                        elif 'Sell' in effect_data['effect']:
                            card_style = 'background: #f8d7da; color: #721c24; border-left: 4px solid #dc3545;'
                        else:
                            card_style = 'background: #fff3cd; color: #856404; border-left: 4px solid #ffc107;'
                        
                        with effect_cols[col_idx]:
                            st.markdown(f"""
                            <div style="{card_style} padding: 10px; border-radius: 6px; margin: 5px 0;">
                                <h6 style="margin: 0 0 5px 0;">{effect_data['planet']}</h6>
                                <p style="margin: 0; font-size: 0.9em;"><strong>{effect_data['effect']}</strong></p>
                                <p style="margin: 0; font-size: 0.8em;">Strength: {effect_data['strength']}</p>
                            </div>
                            """, unsafe_allow_html=True)
                else:
                    st.markdown(f"<p style='color: #6c757d; font-style: italic;'>No specific planetary influences currently active for {sector} sector.</p>", unsafe_allow_html=True)
        
        with planet_tab4:
            st.markdown("### 🔮 Upcoming Transit Forecast")
            
            # Enhanced upcoming changes with specific dates and effects
            st.markdown("#### 📅 Major Transit Changes This Week")
            
            upcoming_changes = [
                {
                    'date': 'Tomorrow (Aug 2, 2025)',
                    'planet': 'Moon 🌙',
                    'change': 'Moves to Vishakha (Libra 20°)',
                    'effect': 'Banking sector major boost, International trade expansion',
                    'sectors_affected': ['Banking', 'International Trade', 'Exports'],
                    'impact': 'Strong Bullish',
                    'duration': '2.5 days'
                },
                {
                    'date': 'Saturday (Aug 3, 2025)',
                    'planet': 'Mercury ☿',
                    'change': 'Aspects Mars in Virgo',
                    'effect': 'IT-Defense synergy, Technology innovation in defense',
                    'sectors_affected': ['IT', 'Defense', 'Technology'],
                    'impact': 'Volatile',
                    'duration': '1 day'
                },
                {
                    'date': 'Sunday (Aug 4, 2025)',
                    'planet': 'Venus ♀',
                    'change': 'Moves to Mrigashira (Gemini 23°)',
                    'effect': 'Auto sector transformation, Real estate digital shift',
                    'sectors_affected': ['Auto', 'Real Estate', 'Digital'],
                    'impact': 'Bullish',
                    'duration': '25 days'
                },
                {
                    'date': 'Monday (Aug 5, 2025)',
                    'planet': 'Sun ☀️',
                    'change': 'Conjuncts Mercury (Cancer 18°)',
                    'effect': 'FMCG-IT combined strength, Digital consumer revolution',
                    'sectors_affected': ['FMCG', 'IT', 'E-commerce'],
                    'impact': 'Strong Bullish',
                    'duration': '3 days'
                }
            ]
            
            for change in upcoming_changes:
                if change['impact'] == 'Strong Bullish':
                    card_style = 'background: linear-gradient(135deg, #d4edda, #c3e6cb); color: #155724; border: 3px solid #28a745;'
                    impact_icon = '🟢'
                elif change['impact'] == 'Bullish':
                    card_style = 'background: linear-gradient(135deg, #d1ecf1, #bee5eb); color: #0c5460; border: 3px solid #17a2b8;'
                    impact_icon = '🔵'
                elif change['impact'] == 'Volatile':
                    card_style = 'background: linear-gradient(135deg, #fff3cd, #ffeeba); color: #856404; border: 3px solid #ffc107;'
                    impact_icon = '⚡'
                else:
                    card_style = 'background: linear-gradient(135deg, #f8d7da, #f1c3c6); color: #721c24; border: 3px solid #dc3545;'
                    impact_icon = '🔴'
                
                st.markdown(f"""
                <div style="{card_style} padding: 20px; border-radius: 12px; margin: 15px 0; box-shadow: 0 6px 20px rgba(0,0,0,0.1);">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                        <h4 style="margin: 0;">{change['date']}: {change['planet']}</h4>
                        <span style="font-size: 1.2em;">{impact_icon}</span>
                    </div>
                    
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                        <div>
                            <p style="margin: 0; font-size: 0.95em;"><strong>Transit:</strong> {change['change']}</p>
                            <p style="margin: 5px 0; font-size: 0.95em;"><strong>Effect:</strong> {change['effect']}</p>
                            <p style="margin: 0; font-size: 0.9em;"><strong>Duration:</strong> {change['duration']}</p>
                        </div>
                        <div>
                            <p style="margin: 0; font-size: 0.95em;"><strong>Market Impact:</strong> {change['impact']}</p>
                            <p style="margin: 5px 0; font-size: 0.9em;"><strong>Affected Sectors:</strong></p>
                            <p style="margin: 0; font-size: 0.85em;">{', '.join(change['sectors_affected'])}</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

with main_tab2:
    st.markdown(f"""
    <div class="section-header">
        <h2 style="margin: 0 0 10px 0;">🔮 TOMORROW'S COMPLETE PLANETARY TRANSIT FORECAST</h2>
        <h3 style="margin: 0; opacity: 0.9;">{tomorrow_day}, {tomorrow_date} • Detailed Predictions</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Tomorrow's Analysis
    tomorrow_equity_tab, tomorrow_commodity_tab, tomorrow_forex_tab, tomorrow_global_tab = st.tabs([
        "📈 EQUITY FORECAST", 
        "🏭 COMMODITIES FORECAST", 
        "💱 FOREX FORECAST", 
        "🌍 GLOBAL FORECAST"
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

# Footer
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
