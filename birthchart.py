from flask import Flask, render_template_string, jsonify, request
from datetime import datetime
import json
import random
import pytz

app = Flask(__name__)

# HTML Template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vedic Birth Chart & Live Market Intelligence</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Arial', sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 20px; }
        .container { max-width: 1800px; margin: 0 auto; background: white; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.3); overflow: hidden; }
        .header { background: linear-gradient(45deg, #ff6b35, #f7931e); color: white; padding: 20px; text-align: center; }
        .header h1 { font-size: 2.5em; margin-bottom: 10px; }
        .live-ticker { background: #000; color: #00ff00; padding: 10px; font-family: 'Courier New', monospace; font-size: 14px; overflow: hidden; white-space: nowrap; }
        .input-section { background: #f8f9fa; padding: 20px; border-bottom: 2px solid #e9ecef; }
        .input-row { display: flex; gap: 20px; flex-wrap: wrap; align-items: center; justify-content: center; }
        .input-group { display: flex; flex-direction: column; gap: 5px; }
        .input-group label { font-weight: bold; color: #333; }
        .input-group input, .input-group select { padding: 10px; border: 2px solid #ddd; border-radius: 5px; font-size: 14px; }
        .generate-btn, .market-analysis-btn, .live-market-btn, .today-astro-btn { background: linear-gradient(45deg, #28a745, #20c997); color: white; border: none; padding: 12px 30px; border-radius: 25px; font-size: 16px; font-weight: bold; cursor: pointer; margin: 5px; transition: transform 0.2s; }
        .generate-btn:hover, .market-analysis-btn:hover, .live-market-btn:hover, .today-astro-btn:hover { transform: scale(1.05); }
        .market-analysis-btn { background: linear-gradient(45deg, #007bff, #0056b3); }
        .live-market-btn { background: linear-gradient(45deg, #dc3545, #c82333); }
        .today-astro-btn { background: linear-gradient(45deg, #6f42c1, #d63384); }
        .main-content { display: grid; grid-template-columns: 1fr 1fr; gap: 30px; padding: 30px; }
        .chart-section, .planetary-details { background: #fff; }
        .chart-title { background: linear-gradient(45deg, #ff6b35, #f7931e); color: white; padding: 15px; text-align: center; font-size: 1.3em; font-weight: bold; margin-bottom: 20px; border-radius: 10px; }
        .birth-chart { width: 100%; max-width: 450px; margin: 0 auto; border: 4px solid #8B4513; background: linear-gradient(45deg, #F5DEB3, #DDD0C0); }
        .chart-grid { display: grid; grid-template-columns: repeat(4, 1fr); grid-template-rows: repeat(4, 1fr); width: 100%; height: 450px; }
        .house { border: 2px solid #8B4513; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 8px; font-size: 11px; text-align: center; position: relative; }
        .house-number { font-size: 12px; font-weight: bold; color: #8B4513; position: absolute; top: 5px; left: 5px; }
        .house-sign { font-size: 10px; font-weight: bold; color: #4169E1; margin-bottom: 5px; }
        .planets { font-weight: bold; color: #d32f2f; line-height: 1.3; }
        .planet { display: block; margin: 2px 0; font-size: 11px; }
        .current-info { background: #e3f2fd; padding: 15px; border-radius: 10px; margin-bottom: 20px; }
        .info-row { display: flex; justify-content: space-between; margin-bottom: 8px; }
        .info-label { font-weight: bold; color: #1976d2; }
        .planetary-table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        .planetary-table th { background: linear-gradient(45deg, #ff6b35, #f7931e); color: white; padding: 12px 8px; text-align: center; font-size: 12px; }
        .planetary-table td { padding: 10px 8px; border: 1px solid #ddd; text-align: center; font-size: 11px; }
        .planetary-table tr:nth-child(even) { background-color: #f8f9fa; }
        .lower-panel { background: #f8f9fa; padding: 30px; display: grid; grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); gap: 20px; }
        .panel-section { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .panel-section h3 { color: #ff6b35; margin-bottom: 15px; }
        .panel-item { padding: 8px 0; border-bottom: 1px solid #eee; font-size: 14px; }
        .panel-item:last-child { border-bottom: none; }
        .transit-details { margin-top: 20px; padding: 15px; background: #f8f9fa; border-radius: 10px; }
        .transit-details h4 { color: #ff6b35; margin-bottom: 10px; }
        .transit-item { padding: 5px 0; font-size: 12px; }
        .price-positive { color: #28a745; }
        .price-negative { color: #dc3545; }
        .market-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px; }
        .market-card { background: #f8f9fa; padding: 15px; border-radius: 10px; text-align: center; }
        .market-card h4 { color: #333; margin-bottom: 10px; }
        .market-price { font-size: 24px; font-weight: bold; margin: 10px 0; }
        .market-change { font-size: 16px; font-weight: bold; }
        .sector-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 20px; margin-top: 20px; }
        .sector-card { background: white; border-radius: 15px; padding: 20px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); border-left: 5px solid; }
        .sector-card.bullish { border-left-color: #28a745; }
        .sector-card.bearish { border-left-color: #dc3545; }
        .sector-card.neutral { border-left-color: #ffc107; }
        .sector-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }
        .market-analysis-panel, .live-market-panel, .astro-panel { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); z-index: 1000; display: none; }
        .market-content, .live-content, .astro-content { background: white; margin: 50px auto; padding: 30px; width: 95%; max-width: 1600px; border-radius: 15px; max-height: 90vh; overflow-y: auto; }
        .close-btn { float: right; font-size: 30px; font-weight: bold; cursor: pointer; color: #ff6b35; }
        .close-btn:hover { color: #d32f2f; }
        .analysis-tabs, .live-tabs, .astro-tabs { display: flex; gap: 10px; margin-bottom: 20px; flex-wrap: wrap; }
        .tab-btn { padding: 10px 20px; border: none; background: #f8f9fa; border-radius: 25px; cursor: pointer; font-weight: bold; transition: all 0.3s; }
        .tab-btn.active { background: linear-gradient(45deg, #007bff, #0056b3); color: white; }
        @media (max-width: 768px) { 
            .main-content { grid-template-columns: 1fr; } 
            .input-row { flex-direction: column; } 
            .sector-grid { grid-template-columns: 1fr; }
            .lower-panel { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🕉️ Vedic Birth Chart & Live Market Intelligence 🕉️</h1>
            <p>Real-time Kundali Analysis with Live Market Data & Astrological Predictions</p>
        </div>
        
        <div class="live-ticker" id="liveTicker"></div>
        
        <div class="input-section">
            <div class="input-row">
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
                <button class="generate-btn" onclick="updateChart()">Generate Chart</button>
                <button class="market-analysis-btn" onclick="openMarketAnalysis()">📈 Market Analysis</button>
                <button class="live-market-btn" onclick="openLiveMarket()">🔴 Live Market</button>
                <button class="today-astro-btn" onclick="openTodayAstro()">Today Astro</button>
            </div>
        </div>
        
        <div class="main-content">
            <div class="chart-section">
                <div class="chart-title">Lagna Kundali - North Indian Style</div>
                
                <div class="current-info">
                    <div class="info-row">
                        <span class="info-label">Date & Time:</span>
                        <span id="currentDateTime"></span>
                    </div>
                    <div class="info-row">
                        <span class="info-label">Location:</span>
                        <span id="currentLocation">Mumbai, India</span>
                    </div>
                    <div class="info-row">
                        <span class="info-label">Rasi:</span>
                        <span id="currentRasi">Cancer (Karka)</span>
                    </div>
                    <div class="info-row">
                        <span class="info-label">Ascendant:</span>
                        <span id="currentAsc">Leo (Simha)</span>
                    </div>
                </div>
                
                <div class="birth-chart">
                    <div class="chart-grid" id="chartGrid">
                        <!-- Chart will be generated dynamically -->
                    </div>
                </div>
                
                <div class="transit-details">
                    <h4>Planetary Transits & Market Impact</h4>
                    <div id="transitList"></div>
                </div>
            </div>
            
            <div class="planetary-details">
                <div class="chart-title">Planetary Positions & Transit Details</div>
                
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
            </div>
        </div>
        
        <div class="lower-panel">
            <div class="panel-section">
                <h3>Today's Important Planetary Transits</h3>
                <div id="todayTransits"></div>
            </div>
            <div class="panel-section">
                <h3>Bullish/Bearish Sector Indices & Global Markets</h3>
                <div id="marketSummary"></div>
            </div>
            <div class="panel-section">
                <h3>Upcoming Planetary Transits</h3>
                <div id="upcomingTransits"></div>
            </div>
        </div>
    </div>
    
    <!-- Market Analysis Panel -->
    <div class="market-analysis-panel" id="marketPanel">
        <div class="market-content">
            <span class="close-btn" onclick="closeMarketAnalysis()">&times;</span>
            <h2>📈 Advanced Astro-Market Analysis Dashboard</h2>
            <div class="analysis-tabs">
                <button class="tab-btn active" onclick="showTab(event, 'sectors')">NIFTY Sectors</button>
                <button class="tab-btn" onclick="showTab(event, 'indices')">Indices</button>
                <button class="tab-btn" onclick="showTab(event, 'commodities')">Commodities</button>
                <button class="tab-btn" onclick="showTab(event, 'forex')">Forex & Crypto</button>
                <button class="tab-btn" onclick="showTab(event, 'global')">Global Indices</button>
            </div>
            <div id="analysisContent"></div>
        </div>
    </div>
    
    <!-- Live Market Panel -->
    <div class="live-market-panel" id="liveMarketPanel">
        <div class="live-content">
            <span class="close-btn" onclick="closeLiveMarket()">&times;</span>
            <h2>🔴 Live Market Data & Analysis</h2>
            <div class="live-tabs">
                <button class="tab-btn active" onclick="showLiveTab(event, 'highlights')">Market Highlights</button>
                <button class="tab-btn" onclick="showLiveTab(event, 'indices')">Indian Indices</button>
                <button class="tab-btn" onclick="showLiveTab(event, 'global')">Global Markets</button>
                <button class="tab-btn" onclick="showLiveTab(event, 'commodities')">Commodities</button>
                <button class="tab-btn" onclick="showLiveTab(event, 'crypto')">Cryptocurrency</button>
            </div>
            <div id="liveContent"></div>
        </div>
    </div>
    
    <!-- Today Astro Panel -->
    <div class="astro-panel" id="astroPanel">
        <div class="astro-content">
            <span class="close-btn" onclick="closeTodayAstro()">&times;</span>
            <h2>🌌 Today Astro - Intraday Transit & Market Insights</h2>
            <div class="astro-tabs">
                <button class="tab-btn active" onclick="showAstroTab(event, 'nifty')">NIFTY</button>
                <button class="tab-btn" onclick="showAstroTab(event, 'banknifty')">BANK NIFTY</button>
                <button class="tab-btn" onclick="showAstroTab(event, 'gold')">Gold</button>
                <button class="tab-btn" onclick="showAstroTab(event, 'crude')">Crude Oil</button>
                <button class="tab-btn" onclick="showAstroTab(event, 'btc')">Bitcoin</button>
                <button class="tab-btn" onclick="showAstroTab(event, 'dowjones')">Dow Jones</button>
            </div>
            <div id="astroContent"></div>
        </div>
    </div>

    <script>
        let marketData = {};
        let planetaryData = {};
        
        // Fetch initial data and start updates
        fetchMarketData();
        fetchPlanetaryData();
        
        // Update functions
        function fetchMarketData() {
            fetch('/api/market_data')
                .then(response => response.json())
                .then(data => {
                    marketData = data;
                    updateMarketSummary();
                    updateTicker();
                });
        }
        
        function fetchPlanetaryData() {
            fetch('/api/planetary_data')
                .then(response => response.json())
                .then(data => {
                    planetaryData = data;
                    generateChart();
                    updatePlanetaryTable();
                    updateTransits();
                });
        }
        
        function updateDateTime() {
            const now = new Date();
            const options = { 
                weekday: 'long', 
                year: 'numeric', 
                month: 'long', 
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit',
                timeZoneName: 'short'
            };
            document.getElementById('currentDateTime').textContent = now.toLocaleString('en-US', options);
        }
        
        function generateChart() {
            const chartGrid = document.getElementById('chartGrid');
            chartGrid.innerHTML = '';
            
            // North Indian chart layout
            const layout = [
                {house: 12, planets: ['saturn', 'neptune']},
                {house: 1, planets: ['rahu']},
                {house: 2, planets: ['uranus']},
                {house: 3, planets: ['venus', 'jupiter']},
                {house: 11, planets: []},
                {center: true, content: 'center1'},
                {center: true, content: 'center2'},
                {house: 4, planets: ['sun', 'mercury']},
                {house: 10, planets: ['pluto']},
                {house: 9, planets: []},
                {house: 8, planets: []},
                {house: 5, planets: []},
                {house: 9, planets: []},
                {house: 8, planets: []},
                {house: 7, planets: ['ketu']},
                {house: 6, planets: ['moon', 'mars']}
            ];
            
            const houseSignMap = {
                1: 'Ar', 2: 'Ta', 3: 'Ge', 4: 'Ca', 5: 'Le', 6: 'Vi',
                7: 'Li', 8: 'Sc', 9: 'Sg', 10: 'Cp', 11: 'Aq', 12: 'Pi'
            };
            
            layout.forEach((cell, index) => {
                const div = document.createElement('div');
                div.className = 'house';
                
                if (cell.center) {
                    if (cell.content === 'center1') {
                        const birthDate = document.getElementById('birthDate').value;
                        const birthTime = document.getElementById('birthTime').value;
                        const date = new Date(birthDate + 'T' + birthTime);
                        div.innerHTML = `
                            <div style="font-weight: bold; color: #8B4513; text-align: center;">
                                <span>${date.toLocaleDateString()}</span><br>
                                <span>${birthTime}</span><br><br>
                                <span style="color: #d32f2f;">Rasi</span><br>
                                <small id="chartRasi">Cancer (Karka)</small>
                            </div>
                        `;
                    } else {
                        div.innerHTML = `
                            <div style="font-weight: bold; color: #8B4513; font-size: 11px; text-align: center;">
                                Planetary Transit<br>Analysis Dashboard<br>
                                <span style="color: #ff6b35;">Live Market Intelligence</span>
                            </div>
                        `;
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
        
        function updatePlanetaryTable() {
            const tbody = document.getElementById('planetaryTableBody');
            tbody.innerHTML = '';
            
            Object.entries(planetaryData).forEach(([planet, data]) => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${data.symbol} ${planet.charAt(0).toUpperCase() + planet.slice(1)}</td>
                    <td>${data.sign}</td>
                    <td>${data.degree}</td>
                    <td>${data.nakshatra}</td>
                    <td>House ${data.house}</td>
                `;
                tbody.appendChild(row);
            });
        }
        
        function updateTransits() {
            fetch('/api/transits')
                .then(response => response.json())
                .then(data => {
                    const transitList = document.getElementById('transitList');
                    const todayTransits = document.getElementById('todayTransits');
                    const upcomingTransits = document.getElementById('upcomingTransits');
                    
                    transitList.innerHTML = data.today.map(t => 
                        `<div class="transit-item"><strong>${t.time}:</strong> ${t.event} - ${t.impact}</div>`
                    ).join('');
                    
                    todayTransits.innerHTML = data.today.map(t => 
                        `<div class="panel-item">${t.time} - ${t.event} - ${t.impact}</div>`
                    ).join('');
                    
                    upcomingTransits.innerHTML = data.upcoming.map(t => 
                        `<div class="panel-item">${t.date}: ${t.event} - ${t.impact}</div>`
                    ).join('');
                });
        }
        
        function updateMarketSummary() {
            const summary = document.getElementById('marketSummary');
            const html = `
                <div class="panel-item">
                    NIFTY 50: ${marketData.nifty.price.toFixed(2)} 
                    <span class="${marketData.nifty.changePercent >= 0 ? 'price-positive' : 'price-negative'}">
                        (${marketData.nifty.changePercent >= 0 ? '+' : ''}${marketData.nifty.changePercent.toFixed(2)}%)
                    </span>
                </div>
                <div class="panel-item">
                    BANK NIFTY: ${marketData.bankNifty.price.toFixed(2)} 
                    <span class="${marketData.bankNifty.changePercent >= 0 ? 'price-positive' : 'price-negative'}">
                        (${marketData.bankNifty.changePercent >= 0 ? '+' : ''}${marketData.bankNifty.changePercent.toFixed(2)}%)
                    </span>
                </div>
                <div class="panel-item">
                    Global Markets: DOW ${marketData.dowJones.price.toFixed(2)} 
                    <span class="${marketData.dowJones.changePercent >= 0 ? 'price-positive' : 'price-negative'}">
                        (${marketData.dowJones.changePercent >= 0 ? '+' : ''}${marketData.dowJones.changePercent.toFixed(2)}%)
                    </span>
                </div>
                <div class="panel-item">
                    Gold (COMEX): $${marketData.gold.price.toFixed(2)}/oz 
                    <span class="${marketData.gold.changePercent >= 0 ? 'price-positive' : 'price-negative'}">
                        (${marketData.gold.changePercent >= 0 ? '+' : ''}${marketData.gold.changePercent.toFixed(2)}%)
                    </span>
                </div>
            `;
            summary.innerHTML = html;
        }
        
        function updateTicker() {
            fetch('/api/ticker')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('liveTicker').innerHTML = data.ticker;
                });
        }
        
        function updateChart() {
            fetchPlanetaryData();
            updateDateTime();
            const location = document.getElementById('birthPlace').value;
            document.getElementById('currentLocation').textContent = location;
        }
        
        // Panel functions
        function openMarketAnalysis() { 
            document.getElementById('marketPanel').style.display = 'block'; 
            showTab(null, 'sectors'); 
        }
        
        function closeMarketAnalysis() { 
            document.getElementById('marketPanel').style.display = 'none'; 
        }
        
        function openLiveMarket() { 
            document.getElementById('liveMarketPanel').style.display = 'block'; 
            showLiveTab(null, 'highlights'); 
        }
        
        function closeLiveMarket() { 
            document.getElementById('liveMarketPanel').style.display = 'none'; 
        }
        
        function openTodayAstro() { 
            document.getElementById('astroPanel').style.display = 'block'; 
            showAstroTab(null, 'nifty'); 
        }
        
        function closeTodayAstro() { 
            document.getElementById('astroPanel').style.display = 'none'; 
        }
        
        function showTab(event, tabName) {
            fetch(`/api/analysis_content?tab=${tabName}`)
                .then(response => response.text())
                .then(html => {
                    document.getElementById('analysisContent').innerHTML = html;
                    document.querySelectorAll('.analysis-tabs .tab-btn').forEach(btn => btn.classList.remove('active'));
                    if (event && event.target) event.target.classList.add('active');
                });
        }
        
        function showLiveTab(event, tabName) {
            fetch(`/api/live_content?tab=${tabName}`)
                .then(response => response.text())
                .then(html => {
                    document.getElementById('liveContent').innerHTML = html;
                    document.querySelectorAll('.live-tabs .tab-btn').forEach(btn => btn.classList.remove('active'));
                    if (event && event.target) event.target.classList.add('active');
                });
        }
        
        function showAstroTab(event, tabName) {
            fetch(`/api/astro_content?tab=${tabName}`)
                .then(response => response.text())
                .then(html => {
                    document.getElementById('astroContent').innerHTML = html;
                    document.querySelectorAll('.astro-tabs .tab-btn').forEach(btn => btn.classList.remove('active'));
                    if (event && event.target) event.target.classList.add('active');
                });
        }
        
        // Initialize
        updateDateTime();
        setInterval(updateDateTime, 1000);
        setInterval(fetchMarketData, 5000);
        setInterval(updateTicker, 3000);
        
        // Close modals on outside click
        window.addEventListener('click', function(event) {
            if (event.target === document.getElementById('marketPanel')) closeMarketAnalysis();
            if (event.target === document.getElementById('liveMarketPanel')) closeLiveMarket();
            if (event.target === document.getElementById('astroPanel')) closeTodayAstro();
        });
    </script>
</body>
</html>
'''

# Market Data
class MarketData:
    def __init__(self, price, change, change_percent, high, low):
        self.price = price
        self.change = change
        self.changePercent = change_percent
        self.high = high
        self.low = low

# Initialize market data with current July 2025 prices
market_data = {
    # Indian Indices
    'nifty': MarketData(24780.50, -125.30, -0.50, 24920.15, 24750.20),
    'bankNifty': MarketData(52435.75, 315.25, 0.60, 52580.40, 52120.50),
    'sensex': MarketData(81342.15, -285.40, -0.35, 81650.30, 81250.80),
    'niftyIT': MarketData(32156.40, -425.30, -1.31, 32600.20, 32100.15),
    'niftyPharma': MarketData(18925.60, 156.80, 0.84, 19050.30, 18750.40),
    'niftyAuto': MarketData(22485.30, -185.60, -0.82, 22680.50, 22400.20),
    'niftyFMCG': MarketData(55342.80, 125.40, 0.23, 55450.60, 55200.30),
    'niftyMetal': MarketData(8956.45, -145.30, -1.60, 9120.50, 8920.40),
    'niftyRealty': MarketData(785.25, 12.40, 1.60, 792.30, 772.50),
    'niftyEnergy': MarketData(35426.90, -256.40, -0.72, 35680.20, 35350.40),
    'niftyInfra': MarketData(8234.60, 45.20, 0.55, 8280.40, 8180.30),
    'niftyPSUBank': MarketData(6842.35, 85.60, 1.27, 6890.40, 6750.20),
    'niftyPSE': MarketData(10256.40, -65.30, -0.63, 10350.60, 10220.40),
    'cnx100': MarketData(24156.30, -98.50, -0.41, 24280.40, 24120.60),
    'cnx500': MarketData(21845.75, -75.30, -0.34, 21950.80, 21800.40),
    
    # Global Indices
    'dowJones': MarketData(43825.40, 186.25, 0.43, 43920.60, 43650.30),
    'sp500': MarketData(5932.15, 22.40, 0.38, 5945.80, 5910.20),
    'nasdaq': MarketData(19456.80, 85.30, 0.44, 19520.40, 19380.60),
    'ftse': MarketData(8445.60, -32.40, -0.38, 8485.30, 8430.20),
    'dax': MarketData(19328.45, 125.60, 0.65, 19380.60, 19250.40),
    'nikkei': MarketData(41580.20, 325.40, 0.79, 41650.80, 41250.60),
    'hangseng': MarketData(19845.60, -156.30, -0.78, 20050.40, 19820.30),
    'shanghai': MarketData(3045.80, -28.60, -0.93, 3080.40, 3040.20),
    
    # Commodities
    'gold': MarketData(3326.50, 18.30, 0.55, 3335.20, 3308.40),
    'goldMCX': MarketData(72850, 385, 0.53, 73100, 72500),
    'silver': MarketData(38.25, -0.32, -0.83, 38.65, 38.10),
    'silverMCX': MarketData(91250, -650, -0.71, 91800, 90800),
    'crudeOil': MarketData(82.45, -1.25, -1.49, 83.80, 82.20),
    'crudeOilMCX': MarketData(6842, -95, -1.37, 6950, 6820),
    
    # Forex
    'usdinr': MarketData(83.45, -0.12, -0.14, 83.58, 83.42),
    'eurinr': MarketData(90.85, 0.25, 0.28, 90.95, 90.60),
    'eurusd': MarketData(1.0885, 0.0045, 0.42, 1.0895, 1.0840),
    
    # Crypto
    'bitcoin': MarketData(97850.50, 2450.30, 2.57, 98500.00, 95200.00),
    'ethereum': MarketData(3685.40, 125.60, 3.53, 3720.00, 3560.00),
}

# Planetary Data
planetary_data = {
    'sun': {'sign': 'Cancer', 'degree': '7°15\'', 'nakshatra': 'Pushya', 'house': 4, 'symbol': '☀️'},
    'moon': {'sign': 'Virgo', 'degree': '12°30\'', 'nakshatra': 'Hasta', 'house': 6, 'symbol': '🌙'},
    'mars': {'sign': 'Virgo', 'degree': '25°45\'', 'nakshatra': 'Chitra', 'house': 6, 'symbol': '♂️'},
    'mercury': {'sign': 'Cancer', 'degree': '15°20\'', 'nakshatra': 'Ashlesha', 'house': 4, 'symbol': '☿️'},
    'jupiter': {'sign': 'Gemini', 'degree': '22°10\'', 'nakshatra': 'Punarvasu', 'house': 3, 'symbol': '♃'},
    'venus': {'sign': 'Gemini', 'degree': '8°35\'', 'nakshatra': 'Ardra', 'house': 3, 'symbol': '♀'},
    'saturn': {'sign': 'Pisces', 'degree': '18°25\'', 'nakshatra': 'Revati', 'house': 12, 'symbol': '♄'},
    'rahu': {'sign': 'Aries', 'degree': '5°40\'', 'nakshatra': 'Ashwini', 'house': 1, 'symbol': '☊'},
    'ketu': {'sign': 'Libra', 'degree': '5°40\'', 'nakshatra': 'Swati', 'house': 7, 'symbol': '☋'},
    'uranus': {'sign': 'Taurus', 'degree': '26°15\'', 'nakshatra': 'Mrigashira', 'house': 2, 'symbol': '♅'},
    'neptune': {'sign': 'Pisces', 'degree': '29°50\'', 'nakshatra': 'Revati', 'house': 12, 'symbol': '♆'},
    'pluto': {'sign': 'Capricorn', 'degree': '1°30\'', 'nakshatra': 'Uttarashada', 'house': 10, 'symbol': '♇'}
}

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/market_data')
def get_market_data():
    # Simulate market movements
    for key, data in market_data.items():
        volatility = 0.1
        if 'bitcoin' in key or 'ethereum' in key:
            volatility = 0.3
        elif 'gold' in key or 'silver' in key:
            volatility = 0.05
        
        change_percent = (random.random() - 0.5) * volatility
        data.change = data.price * change_percent / 100
        data.changePercent += change_percent
        data.price += data.change
        
        if data.price > data.high:
            data.high = data.price
        if data.price < data.low:
            data.low = data.price
    
    return jsonify({k: v.__dict__ for k, v in market_data.items()})

@app.route('/api/planetary_data')
def get_planetary_data():
    return jsonify(planetary_data)

@app.route('/api/transits')
def get_transits():
    today = datetime.now(pytz.timezone('Asia/Kolkata'))
    
    transits = {
        'today': [
            {'time': '09:15 AM', 'event': 'Moon enters Hasta Nakshatra', 'impact': 'Bearish for IT sector'},
            {'time': '11:30 AM', 'event': 'Mars aspects Jupiter', 'impact': 'Bullish for Banking'},
            {'time': '02:45 PM', 'event': 'Mercury in Ashlesha', 'impact': 'Volatile for Communications'},
            {'time': '04:00 PM', 'event': 'Venus trine Saturn', 'impact': 'Stable for Luxury goods'}
        ],
        'upcoming': [
            {'date': 'July 2025', 'event': 'Mercury Retrograde (Jul 15 - Aug 8)', 'impact': 'Bearish for communication sector'},
            {'date': 'August 2025', 'event': 'Mars enters Libra (Aug 12)', 'impact': 'Neutral for trade sectors'},
            {'date': 'August 2025', 'event': 'Jupiter enters Cancer (Aug 25)', 'impact': 'Bullish for real estate'}
        ]
    }
    
    return jsonify(transits)

@app.route('/api/ticker')
def get_ticker():
    ticker_items = []
    for key, data in market_data.items():
        if key in ['nifty', 'bankNifty', 'sensex', 'gold', 'bitcoin', 'crudeOil', 'usdinr']:
            symbol = key.upper().replace('NIFTY', 'NIFTY 50').replace('BANKNIFTY', 'BANK NIFTY')
            arrow = '▲' if data.changePercent >= 0 else '▼'
            ticker_items.append(f"{symbol} {data.price:.2f} {arrow} {abs(data.changePercent):.2f}%")
    
    ticker_text = ' | '.join(ticker_items) + ' | ' + ' | '.join(ticker_items)
    return jsonify({'ticker': ticker_text})

@app.route('/api/analysis_content')
def get_analysis_content():
    tab = request.args.get('tab', 'sectors')
    
    if tab == 'sectors':
        html = '<div class="sector-grid">'
        
        sectors = [
            ('Banking & Finance', 'niftyBank', 'HDFCBANK, ICICIBANK, SBIN, KOTAKBANK'),
            ('Information Technology', 'niftyIT', 'TCS, INFY, WIPRO, HCLTECH'),
            ('Pharmaceuticals', 'niftyPharma', 'SUNPHARMA, CIPLA, DRREDDY, DIVISLAB'),
            ('Auto', 'niftyAuto', 'MARUTI, M&M, TATAMOTORS, BAJAJ-AUTO'),
            ('FMCG', 'niftyFMCG', 'HUL, ITC, NESTLEIND, BRITANNIA'),
            ('Metal', 'niftyMetal', 'TATASTEEL, HINDALCO, JSW, VEDL'),
            ('Realty', 'niftyRealty', 'DLF, GODREJPROP, BRIGADE, PRESTIGE'),
            ('Oil & Gas', 'niftyEnergy', 'RELIANCE, ONGC, IOC, BPCL'),
            ('PSU Bank', 'niftyPSUBank', 'SBIN, BANKBARODA, PNB, CANBK')
        ]
        
        for name, key, stocks in sectors:
            if key == 'niftyBank':
                data = market_data['bankNifty']
            else:
                data = market_data.get(key, market_data['nifty'])
            
            sentiment = 'bullish' if data.changePercent > 0 else 'bearish' if data.changePercent < -0.5 else 'neutral'
            html += f'''
            <div class="sector-card {sentiment}">
                <div class="sector-header">
                    <h3>{name}</h3>
                    <span style="color: {'#28a745' if data.changePercent > 0 else '#dc3545'}; font-size: 24px;">
                        {'↑' if data.changePercent > 0 else '↓'} {abs(data.changePercent):.2f}%
                    </span>
                </div>
                <p>{name} Index: {data.price:.2f}</p>
                <p><strong>Key Stocks:</strong> {stocks}</p>
            </div>
            '''
        
        html += '</div>'
        return html
    
    elif tab == 'indices':
        html = '<div class="market-grid">'
        indices = ['nifty', 'bankNifty', 'sensex', 'cnx100', 'cnx500']
        
        for key in indices:
            data = market_data[key]
            name = key.replace('nifty', 'NIFTY 50').replace('bankNifty', 'BANK NIFTY').upper()
            html += f'''
            <div class="market-card">
                <h4>{name}</h4>
                <div class="market-price">{data.price:.2f}</div>
                <div class="market-change {'price-positive' if data.changePercent >= 0 else 'price-negative'}">
                    {'+' if data.changePercent >= 0 else ''}{data.change:.2f} ({data.changePercent:.2f}%)
                </div>
                <p>High: {data.high:.2f} | Low: {data.low:.2f}</p>
            </div>
            '''
        
        html += '</div>'
        return html
    
    elif tab == 'commodities':
        html = '<div class="market-grid">'
        commodities = [
            ('Gold (COMEX)', 'gold', 'oz', f"MCX: ₹{market_data['goldMCX'].price:.0f}/10g"),
            ('Silver (COMEX)', 'silver', 'oz', f"MCX: ₹{market_data['silverMCX'].price:.0f}/kg"),
            ('Crude Oil (WTI)', 'crudeOil', 'bbl', f"MCX: ₹{market_data['crudeOilMCX'].price:.0f}/bbl")
        ]
        
        for name, key, unit, mcx_text in commodities:
            data = market_data[key]
            html += f'''
            <div class="market-card">
                <h4>{name}</h4>
                <div class="market-price">${data.price:.2f}/{unit}</div>
                <div class="market-change {'price-positive' if data.changePercent >= 0 else 'price-negative'}">
                    {'+' if data.changePercent >= 0 else ''}{data.changePercent:.2f}%
                </div>
                <p>{mcx_text}</p>
            </div>
            '''
        
        html += '</div>'
        return html
    
    elif tab == 'forex':
        html = '<div class="market-grid">'
        forex_pairs = [
            ('USD/INR', 'usdinr', 4),
            ('EUR/INR', 'eurinr', 4),
            ('EUR/USD', 'eurusd', 4),
            ('Bitcoin', 'bitcoin', 2),
            ('Ethereum', 'ethereum', 2)
        ]
        
        for name, key, decimals in forex_pairs:
            data = market_data[key]
            prefix = '$' if key in ['bitcoin', 'ethereum'] else ''
            html += f'''
            <div class="market-card">
                <h4>{name}</h4>
                <div class="market-price">{prefix}{data.price:.{decimals}f}</div>
                <div class="market-change {'price-positive' if data.changePercent >= 0 else 'price-negative'}">
                    {'+' if data.changePercent >= 0 else ''}{data.changePercent:.2f}%
                </div>
            </div>
            '''
        
        html += '</div>'
        return html
    
    elif tab == 'global':
        html = '<div class="market-grid">'
        global_indices = [
            ('Dow Jones', 'dowJones', '🇺🇸'),
            ('S&P 500', 'sp500', '🇺🇸'),
            ('NASDAQ', 'nasdaq', '🇺🇸'),
            ('FTSE 100', 'ftse', '🇬🇧'),
            ('DAX', 'dax', '🇩🇪'),
            ('Nikkei 225', 'nikkei', '🇯🇵'),
            ('Hang Seng', 'hangseng', '🇭🇰'),
            ('Shanghai', 'shanghai', '🇨🇳')
        ]
        
        for name, key, flag in global_indices:
            data = market_data[key]
            html += f'''
            <div class="market-card">
                <h4>{flag} {name}</h4>
                <div class="market-price">{data.price:.2f}</div>
                <div class="market-change {'price-positive' if data.changePercent >= 0 else 'price-negative'}">
                    {'+' if data.changePercent >= 0 else ''}{data.changePercent:.2f}%
                </div>
            </div>
            '''
        
        html += '</div>'
        return html
    
    return ''

@app.route('/api/live_content')
def get_live_content():
    tab = request.args.get('tab', 'highlights')
    
    if tab == 'highlights':
        html = '<h3>Market Highlights - Live Updates</h3>'
        html += '<div class="market-grid">'
        
        for key in ['nifty', 'bankNifty', 'sensex', 'gold']:
            data = market_data[key]
            name = key.replace('nifty', 'NIFTY 50').replace('bankNifty', 'BANK NIFTY').upper()
            if key == 'gold':
                name = 'Gold (COMEX)'
            
            html += f'''
            <div class="market-card">
                <h4>🔴 LIVE - {name}</h4>
                <div class="market-price">{data.price:.2f}</div>
                <div class="market-change {'price-positive' if data.changePercent >= 0 else 'price-negative'}">
                    {'▲' if data.changePercent >= 0 else '▼'} {abs(data.change):.2f} ({data.changePercent:.2f}%)
                </div>
                <p>High: {data.high:.2f} | Low: {data.low:.2f}</p>
            </div>
            '''
        
        html += '</div>'
        html += '<h4>Market Sentiment</h4>'
        html += '''
        <div style="background: #f8f9fa; padding: 15px; border-radius: 10px;">
            <div class="panel-item">🟢 Advances: 1,285 stocks | 🔴 Declines: 765 stocks</div>
            <div class="panel-item">FII Activity: Net Buy ₹2,345 Cr | DII: Net Sell ₹1,125 Cr</div>
            <div class="panel-item">Market Breadth: Positive (1.68:1)</div>
            <div class="panel-item">VIX: 14.25 (-3.45%) - Low volatility</div>
        </div>
        '''
        return html
    
    elif tab == 'indices':
        html = '<h3>Indian Indices - Real-time Data</h3>'
        html += '<div class="market-grid">'
        
        indian_indices = ['nifty', 'bankNifty', 'sensex', 'niftyIT', 'niftyPharma', 
                         'niftyAuto', 'niftyFMCG', 'niftyMetal', 'niftyRealty', 
                         'niftyEnergy', 'niftyPSUBank', 'cnx100', 'cnx500']
        
        for key in indian_indices:
            data = market_data[key]
            name = key.replace('nifty', 'NIFTY ').replace('bankNifty', 'BANK NIFTY').replace('cnx', 'CNX ').upper()
            
            html += f'''
            <div class="market-card">
                <h4>{name}</h4>
                <div class="market-price">{data.price:.2f}</div>
                <div class="market-change {'price-positive' if data.changePercent >= 0 else 'price-negative'}">
                    {'+' if data.changePercent >= 0 else ''}{data.change:.2f} ({data.changePercent:.2f}%)
                </div>
            </div>
            '''
        
        html += '</div>'
        return html
    
    return ''

@app.route('/api/astro_content')
def get_astro_content():
    tab = request.args.get('tab', 'nifty')
    
    astro_data = {
        'nifty': {
            'prediction': 'Bearish to Neutral',
            'range': '24,700 - 24,850',
            'keyTimes': [
                '09:15-09:45 AM: Bearish opening (Moon in 6th house)',
                '10:30-11:30 AM: Recovery expected (Jupiter aspect)',
                '02:00-03:00 PM: Volatile (Mercury influence)',
                '03:15-03:30 PM: Day\'s decision time'
            ],
            'advice': 'Avoid fresh long positions. Wait for 24,700 support test.'
        },
        'banknifty': {
            'prediction': 'Bullish',
            'range': '52,300 - 52,600',
            'keyTimes': [
                '09:15-10:00 AM: Positive opening expected',
                '11:00-12:00 PM: Strong momentum (Jupiter favorable)',
                '01:30-02:30 PM: Profit booking zone',
                '03:00-03:30 PM: EOD positioning'
            ],
            'advice': 'Buy on dips near 52,350. Target 52,550.'
        },
        'gold': {
            'prediction': 'Bullish',
            'range': '$3,320 - $3,340',
            'keyTimes': [
                '09:00 AM: Asian session positive',
                '01:30 PM: European session momentum',
                '07:00 PM: US session volatility',
                '11:30 PM: Fed speakers impact'
            ],
            'advice': 'Accumulate on dips below $3,325. Venus favorable for precious metals.'
        }
    }
    
    data = astro_data.get(tab, astro_data['nifty'])
    current_date = datetime.now().strftime('%B %d, %Y')
    
    html = f'<h3>{tab.upper()} - Astrological Analysis for {current_date}</h3>'
    html += f'''
    <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0;">
        <h4>Daily Prediction: <span style="color: {'#28a745' if 'Bullish' in data["prediction"] else '#dc3545'}">{data["prediction"]}</span></h4>
        <p><strong>Expected Range:</strong> {data["range"]}</p>
        <p><strong>Astrological Advice:</strong> {data["advice"]}</p>
    </div>
    <h4>Key Time Zones & Planetary Influences:</h4>
    <div style="background: white; padding: 15px; border-radius: 10px;">
    '''
    
    for time in data['keyTimes']:
        html += f'<div class="panel-item">{time}</div>'
    
    html += '''
    </div>
    <div style="margin-top: 20px; padding: 15px; background: #e3f2fd; border-radius: 10px;">
        <h4>Current Planetary Positions Impact:</h4>
        <p>☽ Moon in Virgo (6th house): Technical analysis favored</p>
        <p>♃ Jupiter in Gemini (3rd house): Communication sector volatility</p>
        <p>☿ Mercury in Cancer (4th house): Domestic market focus</p>
        <p>♂ Mars in Virgo (6th house): Healthcare sector active</p>
    </div>
    '''
    
    return html

if __name__ == '__main__':
    app.run(debug=True, port=5000)
