# Vedic Birth Chart & Live Market Intelligence - Setup Guide

## Requirements

### requirements.txt
```
Flask==2.3.3
pytz==2023.3
```

### Optional Requirements (for advanced features)
``` File "/mount/src/birthchart/birthchart.py", line 6
  ```
  ^
SyntaxError: invalid syntax 
# For database storage
SQLAlchemy==2.0.19
psycopg2-binary==2.9.7

# For real-time market data (if integrating with APIs)
requests==2.31.0
yfinance==0.2.28
pandas==2.0.3

# For astrological calculations
swisseph==2.10.3
astropy==5.3.2

# For websockets (real-time updates)
flask-socketio==5.3.4
python-socketio==5.9.0

# For scheduled tasks
APScheduler==3.10.4

# For caching
Flask-Caching==2.0.2
redis==4.6.0
```

## Installation & Setup

### 1. Basic Setup
```bash
# Clone or download the code
mkdir vedic-market-app
cd vedic-market-app

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install requirements
pip install Flask pytz
```

### 2. Running the Application

#### Option A: Standalone Version (Recommended)
```bash
# Save the standalone code as app.py
python app.py
```

#### Option B: Full Version with Templates
```bash
# Create directory structure
mkdir templates static

# Save the main code as app.py
# Create templates/index.html with the HTML template

python app.py
```

### 3. Access the Application
Open your browser and navigate to:
```
http://localhost:5000
```

## Features Included

### Market Data (Current July 2025 Prices)
- **NIFTY 50**: 24,780.50
- **Bank Nifty**: 52,435.75
- **Sensex**: 81,342.15
- **Gold (COMEX)**: $3,326.50/oz
- **Silver (COMEX)**: $38.25/oz
- **All NIFTY Sectors**: IT, Pharma, Auto, FMCG, Metal, Realty, Energy, PSU Bank, etc.
- **Global Indices**: Dow Jones, S&P 500, NASDAQ, FTSE, DAX, Nikkei, etc.
- **Forex**: USD/INR, EUR/INR, GBP/INR, etc.
- **Crypto**: Bitcoin, Ethereum, BNB, XRP, Solana

### Real-time Updates
- Market prices update every 5 seconds
- Ticker updates every 3 seconds
- Realistic market movements based on asset volatility

### Astrological Features
- Today's planetary transits
- Market impact predictions
- Time-based recommendations

## API Endpoints

### Get All Market Data
```
GET /api/market_data
```
Returns JSON with all current market prices

### Get Ticker Data
```
GET /api/ticker
```
Returns current ticker string

## Extending the Application

### Adding New Markets
```python
# Add to market_data dictionary
market_data['newMarket'] = MarketData(
    price=100.00,        # Current price
    change=1.50,         # Change amount
    change_percent=1.52, # Change percentage
    high=101.00,         # Day's high
    low=98.50           # Day's low
)
```

### Integrating Real Market Data
```python
import yfinance as yf

def get_real_market_data():
    # Fetch NIFTY data
    nifty = yf.Ticker("^NSEI")
    data = nifty.history(period="1d")
    
    # Update market_data with real values
    market_data['nifty'].price = data['Close'].iloc[-1]
    # ... update other fields
```

### Adding Database Storage
```python
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market_data.db'
db = SQLAlchemy(app)

class MarketPrice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(50))
    price = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
```

### Adding WebSocket Support
```python
from flask_socketio import SocketIO, emit

socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('connect')
def handle_connect():
    emit('market_update', get_market_data())

def broadcast_market_update():
    socketio.emit('market_update', get_market_data())
```

## Production Deployment

### Using Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

### Using Docker
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

### Environment Variables
```python
import os

# Use environment variables for configuration
PORT = int(os.environ.get('PORT', 5000))
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key')

app.config['SECRET_KEY'] = SECRET_KEY
```

## Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Change port in app.py
   app.run(port=5001)
   ```

2. **Import Errors**
   ```bash
   # Ensure virtual environment is activated
   # Reinstall requirements
   pip install -r requirements.txt
   ```

3. **Market Data Not Updating**
   - Check if background thread is running
   - Verify browser JavaScript console for errors
   - Ensure CORS is properly configured

## License
This is a demo application for educational purposes. 
For production use, ensure compliance with financial data licensing requirements.
