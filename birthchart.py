from flask import Flask, render_template_string, jsonify, request
from datetime import datetime, timedelta
import json
import random
import threading
import time

app = Flask(__name__)

# Global market data storage
market_data = {}
last_update = datetime.now()
update_lock = threading.Lock()

# Initialize market data
def initialize_market_data():
    global market_data
    market_data = {
        # Indian Indices
        'nifty': {'price': 24780.50, 'change': -125.30, 'changePercent': -0.50, 'high': 24920.15, 'low': 24750.20},
        'bankNifty': {'price': 52435.75, 'change': 315.25, 'changePercent': 0.60, 'high': 52580.40, 'low': 52120.50},
        'sensex': {'price': 81342.15, 'change': -285.40, 'changePercent': -0.35, 'high': 81650.30, 'low': 81250.80},
        'niftyIT': {'price': 32156.40, 'change': -425.30, 'changePercent': -1.31, 'high': 32600.20, 'low': 32100.15},
        'niftyPharma': {'price': 18925.60, 'change': 156.80, 'changePercent': 0.84, 'high': 19050.30, 'low': 18750.40},
        'niftyAuto': {'price': 22485.30, 'change': -185.60, 'changePercent': -0.82, 'high': 22680.50, 'low': 22400.20},
        'niftyFMCG': {'price': 55342.80, 'change': 125.40, 'changePercent': 0.23, 'high': 55450.60, 'low': 55200.30},
        'niftyMetal': {'price': 8956.45, 'change': -145.30, 'changePercent': -1.60, 'high': 9120.50, 'low': 8920.40},
        'niftyRealty': {'price': 785.25, 'change': 12.40, 'changePercent': 1.60, 'high': 792.30, 'low': 772.50},
        'niftyEnergy': {'price': 35426.90, 'change': -256.40, 'changePercent': -0.72, 'high': 35680.20, 'low': 35350.40},
        'niftyPSUBank': {'price': 6842.35, 'change': 85.60, 'changePercent': 1.27, 'high': 6890.40, 'low': 6750.20},
        'cnx100': {'price': 24156.30, 'change': -98.50, 'changePercent': -0.41, 'high': 24280.40, 'low': 24120.60},
        'cnx500': {'price': 21845.75, 'change': -75.30, 'changePercent': -0.34, 'high': 21950.80, 'low': 21800.40},
        
        # Global Indices
        'dowJones': {'price': 43825.40, 'change': 186.25, 'changePercent': 0.43, 'high': 43920.60, 'low': 43650.30},
        'sp500': {'price': 5932.15, 'change': 22.40, 'changePercent': 0.38, 'high': 5945.80, 'low': 5910.20},
        'nasdaq': {'price': 19456.80, 'change': 85.30, 'changePercent': 0.44, 'high': 19520.40, 'low': 19380.60},
        'ftse': {'price': 8445.60, 'change': -32.40, 'changePercent': -0.38, 'high': 8485.30, 'low': 8430.20},
        'dax': {'price': 19328.45, 'change': 125.60, 'changePercent': 0.65, 'high': 19380.60, 'low': 19250.40},
        'nikkei': {'price': 41580.20, 'change': 325.40, 'changePercent': 0.79, 'high': 41650.80, 'low': 41250.60},
        'hangseng': {'price': 19845.60, 'change': -156.30, 'changePercent': -0.78, 'high': 20050.40, 'low': 19820.30},
        'shanghai': {'price': 3045.80, 'change': -28.60, 'changePercent': -0.93, 'high': 3080.40, 'low': 3040.20},
        
        # Commodities
        'gold': {'price': 3326.50, 'change': 18.30, 'changePercent': 0.55, 'high': 3335.20, 'low': 3308.40},
        'goldMCX': {'price': 72850, 'change': 385, 'changePercent': 0.53, 'high': 73100, 'low': 72500},
        'silver': {'price': 38.25, 'change': -0.32, 'changePercent': -0.83, 'high': 38.65, 'low': 38.10},
        'silverMCX': {'price': 91250, 'change': -650, 'changePercent': -0.71, 'high': 91800, 'low': 90800},
        'crudeOil': {'price': 82.45, 'change': -1.25, 'changePercent': -1.49, 'high': 83.80, 'low': 82.20},
        'crudeOilMCX': {'price': 6842, 'change': -95, 'changePercent': -1.37, 'high': 6950, 'low': 6820},
        
        # Forex
        'usdinr': {'price': 83.45, 'change': -0.12, 'changePercent': -0.14, 'high': 83.58, 'low': 83.42},
        'eurinr': {'price': 90.85, 'change': 0.25, 'changePercent': 0.28, 'high': 90.95, 'low': 90.60},
        'eurusd': {'price': 1.0885, 'change': 0.0045, 'changePercent': 0.42, 'high': 1.0895, 'low': 1.0840},
        
        # Crypto
        'bitcoin': {'price': 97850.50, 'change': 2450.30, 'changePercent': 2.57, 'high': 98500.00, 'low': 95200.00},
        'ethereum': {'price': 3685.40, 'change': 125.60, 'changePercent': 3.53, 'high': 3720.00, 'low': 3560.00},
    }

# Dynamic market data updater
def update_market_data():
    global market_data, last_update
    with update_lock:
        try:
            for key, data in market_data.items():
                # Different volatility for different asset classes
                if 'bitcoin' in key.lower() or 'ethereum' in key.lower():
                    volatility = 0.5  # Higher for crypto
                elif 'gold' in key.lower() or 'silver' in key.lower():
                    volatility = 0.1  # Lower for precious metals
                elif 'usd' in key.lower() or 'eur' in key.lower():
                    volatility = 0.05  # Very low for forex
                else:
                    volatility = 0.2  # Normal for indices
                
                # Generate realistic price movement
                change_percent = (random.gauss(0, 1) * volatility)
                new_change = data['price'] * change_percent / 100
                
                # Update price and prevent negative prices
                new_price = max(data['price'] + new_change, data['price'] * 0.01)
                data['price'] = new_price
                data['change'] = new_change
                data['changePercent'] = change_percent
                
                # Update high/low
                if data['price'] > data['high']:
                    data['high'] = data['price']
                if data['price'] < data['low']:
                    data['low'] = data['price']
            
            last_update = datetime.now()
        except Exception as e:
            print(f"Error updating market data: {e}")

# Background updater thread
def background_updater():
    while True:
        update_market_data()
        time.sleep(3)  # Update every 3 seconds

# Start background thread
def start_background_updater():
    updater_thread = threading.Thread(target=background_updater, daemon=True)
    updater_thread.start()

# Planetary data with dynamic calculation
def get_planetary_data():
    # Simplified dynamic planetary positions based on current date
    now = datetime.now()
    day_of_year = now.timetuple().tm_yday
    
    # Base positions with daily movement simulation
    base_positions = {
        'sun': {'sign': 'Cancer', 'base_degree': 7.25, 'daily_move': 1.0, 'nakshatra': 'Pushya', 'house': 4, 'symbol': '☀️'},
        'moon': {'sign': 'Virgo', 'base_degree': 12.50, 'daily_move': 13.2, 'nakshatra': 'Hasta', 'house': 6, 'symbol': '🌙'},
        'mars': {'sign': 'Virgo', 'base_degree': 25.75, 'daily_move': 0.5, 'nakshatra': 'Chitra', 'house': 6, 'symbol': '♂️'},
        'mercury': {'sign': 'Cancer', 'base_degree': 15.33, 'daily_move': 1.3, 'nakshatra': 'Ashlesha', 'house': 4, 'symbol': '☿️'},
        'jupiter': {'sign': 'Gemini', 'base_degree': 22.17, 'daily_move': 0.08, 'nakshatra': 'Punarvasu', 'house': 3, 'symbol': '♃'},
        'venus': {'sign': 'Gemini', 'base_degree': 8.58, 'daily_move': 1.2, 'nakshatra': 'Ardra', 'house': 3, 'symbol': '♀'},
        'saturn': {'sign': 'Pisces', 'base_degree': 18.42, 'daily_move': 0.03, 'nakshatra': 'Revati', 'house': 12, 'symbol': '♄'},
        'rahu': {'sign': 'Aries', 'base_degree': 5.67, 'daily_move': -0.05, 'nakshatra': 'Ashwini', 'house': 1, 'symbol': '☊'},
        'ketu': {'sign': 'Libra', 'base_degree': 5.67, 'daily_move': -0.05, 'nakshatra': 'Swati', 'house': 7, 'symbol': '☋'},
    }
    
    planetary_data = {}
    for planet, data in base_positions.items():
        # Calculate current degree based on days passed
        current_degree = (data['base_degree'] + (day_of_year * data['daily_move'])) % 30
        degree_str = f"{int(current_degree)}°{int((current_degree % 1) * 60)}'"
        
        planetary_data[planet] = {
            'sign': data['sign'],
            'degree': degree_str,
            'nakshatra': data['nakshatra'],
            'house': data['house'],
            'symbol': data['symbol']
        }
    
    return planetary_data

# HTML Template (simplified and error-free)
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vedic Market Intelligence</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: Arial, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            min-height: 100vh; 
            padding: 10px; 
        }
        .container { 
            max-width: 1400px; 
            margin: 0 auto; 
            background: white; 
            border-radius: 15px; 
            box-shadow: 0 10px 30px rgba(0,0,0,0.3); 
            overflow: hidden; 
        }
        .header { 
            background: linear-gradient(45deg, #ff6b35, #f7931e); 
            color: white; 
            padding: 20px; 
            text-align: center; 
        }
        .ticker { 
            background: #000; 
            color: #00ff00; 
            padding: 10px; 
            font-family: 'Courier New', monospace; 
            font-size: 14px; 
            overflow: hidden; 
            white-space: nowrap; 
        }
        .controls { 
            background: #f8f9fa; 
            padding: 15px; 
            display: flex; 
            gap: 15px; 
            flex-wrap: wrap; 
            align-items: center; 
            justify-content: center; 
        }
        .input-group { 
            display: flex; 
            flex-direction: column; 
            gap: 5px; 
        }
        .input-group label { 
            font-weight: bold; 
            color: #333; 
        }
        .input-group input, .input-group select { 
            padding: 8px; 
            border: 2px solid #ddd; 
            border-radius: 5px; 
            font-size: 14px; 
        }
        .btn { 
            background: linear-gradient(45deg, #28a745, #20c997); 
            color: white; 
            border: none; 
            padding: 10px 20px; 
            border-radius: 25px; 
            font-size: 14px; 
            font-weight: bold; 
            cursor: pointer; 
            transition: transform 0.2s; 
            margin: 5px;
        }
        .btn:hover { transform: scale(1.05); }
        .btn-primary { background: linear-gradient(45deg, #007bff, #0056b3); }
        .btn-danger { background: linear-gradient(45deg, #dc3545, #c82333); }
        .btn-purple { background: linear-gradient(45deg, #6f42c1, #d63384); }
        .main-content { 
            display: grid; 
            grid-template-columns: 1fr 1fr; 
            gap: 20px; 
            padding: 20px; 
        }
        .chart-section { 
            background: #fff; 
        }
        .chart-title { 
            background: linear-gradient(45deg, #ff6b35, #f7931e); 
            color: white; 
            padding: 15px; 
            text-align: center; 
            font-size: 1.2em; 
            font-weight: bold; 
            margin-bottom: 15px; 
            border-radius: 10px; 
        }
        .birth-chart { 
            width: 100%; 
            max-width: 400px; 
            margin: 0 auto; 
            border: 3px solid #8B4513; 
            background: linear-gradient(45deg, #F5DEB3, #DDD0C0); 
        }
        .chart-grid { 
            display: grid; 
            grid-template-columns: repeat(4, 1fr); 
            grid-template-rows: repeat(4, 1fr); 
            width: 100%; 
            height: 400px; 
        }
        .house { 
            border: 2px solid #8B4513; 
            display: flex; 
            flex-direction: column; 
            align-items: center; 
            justify-content: center; 
            padding: 5px; 
            font-size: 10px; 
            text-align: center; 
            position: relative; 
        }
        .house-number { 
            font-size: 11px; 
            font-weight: bold; 
            color: #8B4513; 
            position: absolute; 
            top: 3px; 
            left: 3px; 
        }
        .house-sign { 
            font-size: 9px; 
            font-weight: bold; 
            color: #4169E1; 
            margin-bottom: 3px; 
        }
        .planets { 
            font-weight: bold; 
            color: #d32f2f; 
            line-height: 1.2; 
        }
        .planet { 
            display: block; 
            margin: 1px 0; 
            font-size: 10px; 
        }
        .current-info { 
            background: #e3f2fd; 
            padding: 15px; 
            border-radius: 10px; 
            margin-bottom: 15px; 
        }
        .info-row { 
            display: flex; 
            justify-content: space-between; 
            margin-bottom: 8px; 
        }
        .info-label { 
            font-weight: bold; 
            color: #1976d2; 
        }
        .planetary-table { 
            width: 100%; 
            border-collapse: collapse; 
            margin-top: 15px; 
        }
        .planetary-table th { 
            background: linear-gradient(45deg, #ff6b35, #f7931e); 
            color: white; 
            padding: 10px 5px; 
            text-align: center; 
            font-size: 11px; 
        }
        .planetary-table td { 
            padding: 8px 5px; 
            border: 1px solid #ddd; 
            text-align: center; 
            font-size: 10px; 
        }
        .planetary-table tr:nth-child(even) { 
            background-color: #f8f9fa; 
        }
        .market-grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); 
            gap: 15px; 
            margin: 20px 0; 
        }
        .market-card { 
            background: #f8f9fa; 
            padding: 15px; 
            border-radius: 10px; 
            text-align: center; 
            border: 1px solid #dee2e6;
        }
        .market-card h4 { 
            color: #333; 
            margin-bottom: 10px; 
            font-size: 14px;
        }
        .market-price { 
            font-size: 20px; 
            font-weight: bold; 
            margin: 8px 0; 
        }
        .market-change { 
            font-size: 14px; 
            font-weight: bold; 
        }
        .price-positive { color: #28a745; }
        .price-negative { color: #dc3545; }
        .modal { 
            position: fixed; 
            top: 0; 
            left: 0; 
            width: 100%; 
            height: 100%; 
            background: rgba(0,0,0,0.8); 
            z-index: 1000; 
            display: none; 
        }
        .modal-content { 
            background: white; 
            margin: 5% auto; 
            padding: 20px; 
            width: 95%; 
            max-width: 1200px; 
            border-radius: 15px; 
            max-height: 80vh; 
            overflow-y: auto; 
        }
        .close-btn { 
            float: right; 
            font-size: 25px; 
            font-weight: bold; 
            cursor: pointer; 
            color: #ff6b35; 
        }
        .close-btn:hover { color: #d32f2f; }
        .tabs { 
            display: flex; 
            gap: 10px; 
            margin-bottom: 20px; 
            flex-wrap: wrap; 
        }
        .tab-btn { 
            padding: 8px 15px; 
            border: none; 
            background: #f8f9fa; 
            border-radius: 20px; 
            cursor: pointer; 
            font-weight: bold; 
            font-size: 12px;
            transition: all 0.3s; 
        }
        .tab-btn.active { 
            background: linear-gradient(45deg, #007bff, #0056b3); 
            color: white; 
        }
        .sector-card { 
            background: white; 
            border-radius: 10px; 
            padding: 15px; 
            margin-bottom: 10px; 
            box-shadow: 0 2px 10px rgba(0,0,0,0.1); 
            border-left: 4px solid; 
        }
        .sector-card.bullish { border-left-color: #28a745; }
        .sector-card.bearish { border-left-color: #dc3545; }
        .sector-card.neutral { border-left-color: #ffc107; }
        .error-message { 
            color: #dc3545; 
            background: #f8d7da; 
            padding: 10px; 
            border-radius: 5px; 
            margin: 10px 0; 
        }
        @media (max-width: 768px) { 
            .main-content { grid-template-columns: 1fr; } 
            .controls { flex-direction: column; }
            .modal-content { margin: 10% auto; width: 98%; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🕉️ Vedic Market Intelligence 🕉️</h1>
            <p>Real-time Market Analysis with Astrological Insights</p>
        </div>
        
        <div class="ticker" id="liveTicker">Loading market data...</div>
        
        <div class="controls">
            <div class="input-group">
                <label for="birthDate">Birth Date:</label>
                <input type="date" id="birthDate" value="1990-01-01">
            </div>
            <div class="input-group">
                <label for="birthTime">Birth Time:</label>
                <input type="time" id="birthTime" value="12:00">
            </div>
            <div class="input-group">
                <label for="birthPlace">Birth Place:</label>
                <input type="text" id="birthPlace" value="Mumbai, India">
            </div>
            <div class="input-group">
                <label for="timezone">Timezone:</label>
                <select id="timezone">
                    <option value="+05:30" selected>IST (+05:30)</option>
                    <option value="+00:00">UTC (+00:00)</option>
                    <option value="-05:00">EST (-05:00)</option>
                    <option value="+08:00">CST (+08:00)</option>
                </select>
            </div>
            <button class="btn" onclick="updateChart()">🔄 Generate Chart</button>
            <button class="btn btn-primary" onclick="openModal('marketModal')">📈 Market Analysis</button>
            <button class="btn btn-danger" onclick="openModal('liveModal')">🔴 Live Market</button>
            <button class="btn btn-purple" onclick="openModal('astroModal')">🌌 Astro Analysis</button>
        </div>
        
        <div class="main-content">
            <div class="chart-section">
                <div class="chart-title">Birth Chart - North Indian Style</div>
                
                <div class="current-info">
                    <div class="info-row">
                        <span class="info-label">Date & Time:</span>
                        <span id="currentDateTime">Loading...</span>
                    </div>
                    <div class="info-row">
                        <span class="info-label">Location:</span>
                        <span id="currentLocation">Mumbai, India</span>
                    </div>
                    <div class="info-row">
                        <span class="info-label">Last Update:</span>
                        <span id="lastUpdate">Just now</span>
                    </div>
                </div>
                
                <div class="birth-chart">
                    <div class="chart-grid" id="chartGrid">
                        <!-- Chart will be generated dynamically -->
                    </div>
                </div>
            </div>
            
            <div class="chart-section">
                <div class="chart-title">Planetary Positions</div>
                
                <table class="planetary-table">
                    <thead>
                        <tr>
                            <th>Planet</th>
                            <th>Sign</th>
                            <th>Degree</th>
                            <th>Nakshatra</th>
                            <th>House</th>
                        </tr>
                    </thead>
                    <tbody id="planetaryTableBody">
                        <!-- Table will be populated dynamically -->
                    </tbody>
                </table>
                
                <div style="margin-top: 20px; padding: 15px; background: #f8f9fa; border-radius: 10px;">
                    <h4 style="color: #ff6b35; margin-bottom: 10px;">Today's Market Influences</h4>
                    <div id="marketInfluences">Loading...</div>
                </div>
            </div>
        </div>
        
        <div class="market-grid" id="quickMarketView"></div>
    </div>
    
    <!-- Market Analysis Modal -->
    <div class="modal" id="marketModal">
        <div class="modal-content">
            <span class="close-btn" onclick="closeModal('marketModal')">&times;</span>
            <h2>📈 Market Analysis Dashboard</h2>
            <div class="tabs">
                <button class="tab-btn active" onclick="showContent('market', 'sectors')">Sectors</button>
                <button class="tab-btn" onclick="showContent('market', 'indices')">Indices</button>
                <button class="tab-btn" onclick="showContent('market', 'global')">Global</button>
                <button class="tab-btn" onclick="showContent('market', 'commodities')">Commodities</button>
            </div>
            <div id="marketContent">Loading...</div>
        </div>
    </div>
    
    <!-- Live Market Modal -->
    <div class="modal" id="liveModal">
        <div class="modal-content">
            <span class="close-btn" onclick="closeModal('liveModal')">&times;</span>
            <h2>🔴 Live Market Data</h2>
            <div class="tabs">
                <button class="tab-btn active" onclick="showContent('live', 'highlights')">Highlights</button>
                <button class="tab-btn" onclick="showContent('live', 'indian')">Indian Markets</button>
                <button class="tab-btn" onclick="showContent('live', 'global')">Global Markets</button>
                <button class="tab-btn" onclick="showContent('live', 'crypto')">Crypto</button>
            </div>
            <div id="liveContent">Loading...</div>
        </div>
    </div>
    
    <!-- Astro Analysis Modal -->
    <div class="modal" id="astroModal">
        <div class="modal-content">
            <span class="close-btn" onclick="closeModal('astroModal')">&times;</span>
            <h2>🌌 Astrological Market Analysis</h2>
            <div class="tabs">
                <button class="tab-btn active" onclick="showContent('astro', 'nifty')">NIFTY</button>
                <button class="tab-btn" onclick="showContent('astro', 'banknifty')">BANK NIFTY</button>
                <button class="tab-btn" onclick="showContent('astro', 'gold')">Gold</button>
                <button class="tab-btn" onclick="showContent('astro', 'bitcoin')">Bitcoin</button>
            </div>
            <div id="astroContent">Loading...</div>
        </div>
    </div>

    <script>
        let isLoading = false;
        
        // Utility functions
        function showError(message) {
            console.error(message);
        }
        
        function formatNumber(num, decimals = 2) {
            return parseFloat(num).toFixed(decimals);
        }
        
        function formatChange(change, changePercent) {
            const sign = changePercent >= 0 ? '+' : '';
            return `${sign}${formatNumber(change)} (${sign}${formatNumber(changePercent)}%)`;
        }
        
        // API functions with error handling
        async function fetchWithRetry(url, retries = 3) {
            for (let i = 0; i < retries; i++) {
                try {
                    const response = await fetch(url);
                    if (!response.ok) throw new Error(`HTTP ${response.status}`);
                    return await response.json();
                } catch (error) {
                    if (i === retries - 1) throw error;
                    await new Promise(resolve => setTimeout(resolve, 1000 * (i + 1)));
                }
            }
        }
        
        async function fetchMarketData() {
            try {
                const data = await fetchWithRetry('/api/market_data');
                updateQuickMarketView(data);
                updateTicker(data);
            } catch (error) {
                showError('Failed to fetch market data: ' + error.message);
            }
        }
        
        async function fetchPlanetaryData() {
            try {
                const data = await fetchWithRetry('/api/planetary_data');
                updatePlanetaryTable(data);
                generateChart(data);
                updateMarketInfluences();
            } catch (error) {
                showError('Failed to fetch planetary data: ' + error.message);
            }
        }
        
        // Update functions
        function updateQuickMarketView(marketData) {
            const container = document.getElementById('quickMarketView');
            const majorIndices = ['nifty', 'bankNifty', 'sensex', 'gold', 'bitcoin', 'usdinr'];
            
            let html = '';
            majorIndices.forEach(key => {
                if (marketData[key]) {
                    const data = marketData[key];
                    const name = key.replace('nifty', 'NIFTY 50').replace('bankNifty', 'BANK NIFTY').toUpperCase();
                    html += `
                        <div class="market-card">
                            <h4>${name}</h4>
                            <div class="market-price">${formatNumber(data.price)}</div>
                            <div class="market-change ${data.changePercent >= 0 ? 'price-positive' : 'price-negative'}">
                                ${'▲▼'[+(data.changePercent < 0)]} ${formatChange(data.change, data.changePercent)}
                            </div>
                        </div>
                    `;
                }
            });
            container.innerHTML = html;
        }
        
        function updateTicker(marketData) {
            const ticker = document.getElementById('liveTicker');
            const tickerItems = [];
            
            ['nifty', 'bankNifty', 'sensex', 'gold', 'bitcoin'].forEach(key => {
                if (marketData[key]) {
                    const data = marketData[key];
                    const name = key.replace('nifty', 'NIFTY').replace('bankNifty', 'BANKNIFTY').toUpperCase();
                    const arrow = data.changePercent >= 0 ? '▲' : '▼';
                    tickerItems.push(`${name}: ${formatNumber(data.price)} ${arrow} ${formatNumber(Math.abs(data.changePercent))}%`);
                }
            });
            
            const tickerText = tickerItems.join(' | ') + ' | ' + tickerItems.join(' | ');
            ticker.innerHTML = tickerText;
        }
        
        function updatePlanetaryTable(planetaryData) {
            const tbody = document.getElementById('planetaryTableBody');
            tbody.innerHTML = '';
            
            Object.entries(planetaryData).forEach(([planet, data]) => {
                const row = tbody.insertRow();
                row.innerHTML = `
                    <td>${data.symbol} ${planet.charAt(0).toUpperCase() + planet.slice(1)}</td>
                    <td>${data.sign}</td>
                    <td>${data.degree}</td>
                    <td>${data.nakshatra}</td>
                    <td>House ${data.house}</td>
                `;
            });
        }
        
        function generateChart(planetaryData) {
            const chartGrid = document.getElementById('chartGrid');
            chartGrid.innerHTML = '';
            
            // Simplified chart layout
            const layout = [
                {house: 12, planets: ['saturn']}, {house: 1, planets: ['rahu']}, {house: 2, planets: []}, {house: 3, planets: ['venus', 'jupiter']},
                {house: 11, planets: []}, {center: true, content: 'center'}, {center: true, content: 'time'}, {house: 4, planets: ['sun', 'mercury']},
                {house: 10, planets: []}, {center: true, content: 'rasi'}, {center: true, content: 'nav'}, {house: 5, planets: []},
                {house: 9, planets: []}, {house: 8, planets: []}, {house: 7, planets: ['ketu']}, {house: 6, planets: ['moon', 'mars']}
            ];
            
            const houseSignMap = {1: 'Ar', 2: 'Ta', 3: 'Ge', 4: 'Ca', 5: 'Le', 6: 'Vi', 7: 'Li', 8: 'Sc', 9: 'Sg', 10: 'Cp', 11: 'Aq', 12: 'Pi'};
            
            layout.forEach(cell => {
                const div = document.createElement('div');
                div.className = 'house';
                
                if (cell.center) {
                    if (cell.content === 'center') {
                        div.innerHTML = '<div style="font-weight: bold; color: #8B4513; font-size: 10px;">Vedic<br>Chart</div>';
                    } else if (cell.content === 'time') {
                        const date = new Date(document.getElementById('birthDate').value + 'T' + document.getElementById('birthTime').value);
                        div.innerHTML = `<div style="font-size: 9px; color: #8B4513;">${date.toLocaleDateString()}<br>${document.getElementById('birthTime').value}</div>`;
                    } else {
                        div.innerHTML = '<div style="font-size: 9px; color: #d32f2f;">Rasi<br>Kundali</div>';
                    }
                } else {
                    const houseNum = cell.house;
                    const sign = houseSignMap[houseNum];
                    const planetsHtml = cell.planets.map(p => {
                        const planet = planetaryData[p];
                        return planet ? `<span class="planet">${planet.symbol}</span>` : '';
                    }).join('');
                    
                    div.innerHTML = `
                        <div class="house-number">${houseNum}</div>
                        <div class="house-sign">${sign}</div>
                        <div class="planets">${planetsHtml}</div>
                    `;
                }
                
                chartGrid.appendChild(div);
            });
        }
        
        function updateMarketInfluences() {
            const influences = document.getElementById('marketInfluences');
            const today = new Date();
            const influences_list = [
                "🌙 Moon in Virgo: Technical analysis favored for IT stocks",
                "♂️ Mars aspect: Banking sector showing strength",
                "☿️ Mercury transit: Communication stocks volatile",
                "♃ Jupiter favorable: Long-term investments positive"
            ];
            
            influences.innerHTML = influences_list.map(inf => `<div style="margin: 5px 0;">${inf}</div>`).join('');
        }
        
        function updateDateTime() {
            const now = new Date();
            const options = {
                weekday: 'short',
                year: 'numeric',
                month: 'short',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit'
            };
            document.getElementById('currentDateTime').textContent = now.toLocaleString('en-US', options);
            document.getElementById('lastUpdate').textContent = now.toLocaleTimeString();
        }
        
        function updateChart() {
            const location = document.getElementById('birthPlace').value;
            document.getElementById('currentLocation').textContent = location;
            fetchPlanetaryData();
            updateDateTime();
        }
        
        // Modal functions
        function openModal(modalId) {
            document.getElementById(modalId).style.display = 'block';
            if (modalId === 'marketModal') showContent('market', 'sectors');
            if (modalId === 'liveModal') showContent('live', 'highlights');
            if (modalId === 'astroModal') showContent('astro', 'nifty');
        }
        
        function closeModal(modalId) {
            document.getElementById(modalId).style.display = 'none';
        }
        
        async function showContent(type, tab) {
            if (isLoading) return;
            isLoading = true;
            
            try {
                const response = await fetch(`/api/${type}_content?tab=${tab}`);
                const html = await response.text();
                document.getElementById(`${type}Content`).innerHTML = html;
                
                // Update active tab
                document.querySelectorAll(`.modal#${type}Modal .tab-btn`).forEach(btn => btn.classList.remove('active'));
                event?.target?.classList.add('active');
            } catch (error) {
                showError(`Failed to load ${type} content: ` + error.message);
            } finally {
                isLoading = false;
            }
        }
        
        // Initialize app
        function initializeApp() {
            updateDateTime();
            fetchMarketData();
            fetchPlanetaryData();
            
            // Set up intervals
            setInterval(updateDateTime, 1000);
            setInterval(fetchMarketData, 5000);
            setInterval(fetchPlanetaryData, 30000);
        }
        
        // Event listeners
        window.addEventListener('click', function(event) {
            if (event.target.classList.contains('modal')) {
                event.target.style.display = 'none';
            }
        });
        
        // Start the app
        document.addEventListener('DOMContentLoaded', initializeApp);
    </script>
</body>
</html>
'''

# Routes
@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/market_data')
def api_market_data():
    try:
        with update_lock:
            return jsonify(market_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/planetary_data')
def api_planetary_data():
    try:
        return jsonify(get_planetary_data())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/market_content')
def api_market_content():
    try:
        tab = request.args.get('tab', 'sectors')
        
        if tab == 'sectors':
            html = '<div class="market-grid">'
            sectors = [
                ('Banking & Finance', 'bankNifty', 'HDFCBANK, ICICIBANK, SBIN'),
                ('Information Technology', 'niftyIT', 'TCS, INFY, WIPRO'),
                ('Pharmaceuticals', 'niftyPharma', 'SUNPHARMA, CIPLA, DRREDDY'),
                ('Auto', 'niftyAuto', 'MARUTI, M&M, TATAMOTORS'),
                ('FMCG', 'niftyFMCG', 'HUL, ITC, NESTLEIND'),
                ('Metal', 'niftyMetal', 'TATASTEEL, HINDALCO, JSW')
            ]
            
            for name, key, stocks in sectors:
                data = market_data.get(key, market_data['nifty'])
                sentiment = 'bullish' if data['changePercent'] > 0 else 'bearish' if data['changePercent'] < -0.5 else 'neutral'
                html += f'''
                <div class="sector-card {sentiment}">
                    <h3>{name}</h3>
                    <p>Index: {data['price']:.2f}</p>
                    <p class="{'price-positive' if data['changePercent'] > 0 else 'price-negative'}">
                        {'↑' if data['changePercent'] > 0 else '↓'} {abs(data['changePercent']):.2f}%
                    </p>
                    <p><strong>Key Stocks:</strong> {stocks}</p>
                </div>
                '''
            html += '</div>'
            return html
            
        elif tab == 'indices':
            html = '<div class="market-grid">'
            for key in ['nifty', 'bankNifty', 'sensex', 'cnx100', 'cnx500']:
                data = market_data[key]
                name = key.replace('nifty', 'NIFTY ').replace('bankNifty', 'BANK NIFTY').upper()
                html += f'''
                <div class="market-card">
                    <h4>{name}</h4>
                    <div class="market-price">{data['price']:.2f}</div>
                    <div class="market-change {'price-positive' if data['changePercent'] >= 0 else 'price-negative'}">
                        {'+' if data['changePercent'] >= 0 else ''}{data['change']:.2f} ({data['changePercent']:+.2f}%)
                    </div>
                </div>
                '''
            html += '</div>'
            return html
            
        elif tab == 'global':
            html = '<div class="market-grid">'
            global_markets = [('Dow Jones', 'dowJones', '🇺🇸'), ('S&P 500', 'sp500', '🇺🇸'), ('NASDAQ', 'nasdaq', '🇺🇸'), ('FTSE 100', 'ftse', '🇬🇧')]
            for name, key, flag in global_markets:
                data = market_data[key]
                html += f'''
                <div class="market-card">
                    <h4>{flag} {name}</h4>
                    <div class="market-price">{data['price']:.2f}</div>
                    <div class="market-change {'price-positive' if data['changePercent'] >= 0 else 'price-negative'}">
                        {'+' if data['changePercent'] >= 0 else ''}{data['change']:.2f} ({data['changePercent']:+.2f}%)
                    </div>
                </div>
                '''
            html += '</div>'
            return html
            
        elif tab == 'commodities':
            html = '<div class="market-grid">'
            commodities = [('Gold', 'gold', '$'), ('Silver', 'silver', '$'), ('Crude Oil', 'crudeOil', '$')]
            for name, key, symbol in commodities:
                data = market_data[key]
                html += f'''
                <div class="market-card">
                    <h4>{name}</h4>
                    <div class="market-price">{symbol}{data['price']:.2f}</div>
                    <div class="market-change {'price-positive' if data['changePercent'] >= 0 else 'price-negative'}">
                        {'+' if data['changePercent'] >= 0 else ''}{data['change']:.2f} ({data['changePercent']:+.2f}%)
                    </div>
                </div>
                '''
            html += '</div>'
            return html
            
        return '<p>Content not found</p>'
        
    except Exception as e:
        return f'<div class="error-message">Error loading content: {str(e)}</div>'

@app.route('/api/live_content')
def api_live_content():
    try:
        tab = request.args.get('tab', 'highlights')
        
        if tab == 'highlights':
            html = '<h3>🔴 Live Market Highlights</h3><div class="market-grid">'
            for key in ['nifty', 'bankNifty', 'sensex', 'gold']:
                data = market_data[key]
                name = key.replace('nifty', 'NIFTY 50').replace('bankNifty', 'BANK NIFTY').upper()
                html += f'''
                <div class="market-card">
                    <h4>LIVE - {name}</h4>
                    <div class="market-price">{data['price']:.2f}</div>
                    <div class="market-change {'price-positive' if data['changePercent'] >= 0 else 'price-negative'}">
                        {'▲' if data['changePercent'] >= 0 else '▼'} {'+' if data['changePercent'] >= 0 else ''}{data['change']:.2f} ({data['changePercent']:+.2f}%)
                    </div>
                </div>
                '''
            html += '</div>'
            return html
            
        elif tab == 'indian':
            html = '<h3>Indian Markets</h3><div class="market-grid">'
            indian_keys = ['nifty', 'bankNifty', 'sensex', 'niftyIT', 'niftyPharma', 'niftyAuto']
            for key in indian_keys:
                data = market_data[key]
                name = key.replace('nifty', 'NIFTY ').replace('bankNifty', 'BANK NIFTY').upper()
                html += f'''
                <div class="market-card">
                    <h4>{name}</h4>
                    <div class="market-price">{data['price']:.2f}</div>
                    <div class="market-change {'price-positive' if data['changePercent'] >= 0 else 'price-negative'}">
                        {'+' if data['changePercent'] >= 0 else ''}{data['change']:.2f} ({data['changePercent']:+.2f}%)
                    </div>
                </div>
                '''
            html += '</div>'
            return html
            
        return '<p>Content loading...</p>'
        
    except Exception as e:
        return f'<div class="error-message">Error: {str(e)}</div>'

@app.route('/api/astro_content')
def api_astro_content():
    try:
        tab = request.args.get('tab', 'nifty')
        
        predictions = {
            'nifty': {'trend': 'Bearish to Neutral', 'range': '24,700 - 24,850', 'advice': 'Wait for support test at 24,700'},
            'banknifty': {'trend': 'Bullish', 'range': '52,300 - 52,600', 'advice': 'Buy on dips near 52,350'},
            'gold': {'trend': 'Bullish', 'range': '$3,320 - $3,340', 'advice': 'Accumulate below $3,325'},
            'bitcoin': {'trend': 'Volatile', 'range': '$96,000 - $99,000', 'advice': 'Use tight stops'}
        }
        
        pred = predictions.get(tab, predictions['nifty'])
        
        html = f'''
        <h3>🌌 {tab.upper()} - Astrological Analysis</h3>
        <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0;">
            <h4>Prediction: <span style="color: {'#28a745' if 'Bullish' in pred['trend'] else '#dc3545'}">{pred['trend']}</span></h4>
            <p><strong>Expected Range:</strong> {pred['range']}</p>
            <p><strong>Advice:</strong> {pred['advice']}</p>
        </div>
        <h4>Key Time Zones:</h4>
        <div style="background: white; padding: 15px; border-radius: 10px;">
            <p>🕘 09:15-10:00 AM: Opening volatility (Moon influence)</p>
            <p>🕚 10:30-11:30 AM: Trend formation (Jupiter aspect)</p>
            <p>🕐 02:00-03:00 PM: Reversal zone (Mercury)</p>
            <p>🕞 03:15-03:30 PM: Closing positions (Venus)</p>
        </div>
        '''
        
        return html
        
    except Exception as e:
        return f'<div class="error-message">Error: {str(e)}</div>'

# Initialize and start
if __name__ == '__main__':
    initialize_market_data()
    start_background_updater()
    app.run(debug=True, host='0.0.0.0', port=5000)
