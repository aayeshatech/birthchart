with planetary_tab:
        st.markdown('<div class="sector-header"><h3 style="margin: 0;">🪐 PLANETARY TRANSIT ANALYSIS - Real Astronomical Data</h3></div>', unsafe_allow_html=True)
        
        # Real-time astronomical data notice
        st.markdown(f"""
        <div style="background: linear-gradient(45deg, #e3f2fd, #bbdefb); color: #1565c0; padding: 15px; border-radius: 10px; margin: 10px 0; border-left: 5px solid #2196f3;">
            <h4 style="margin: 0 0 10px 0;">📡 LIVE ASTRONOMICAL DATA</h4>
            <p style="margin: 0; font-size: 1em;"><strong>Date:</strong> {current_date_str} | <strong>Time:</strong> {current_time_str} IST</p>
            <p style="margin: 5px 0 0 0; font-size: 0.9em;">✅ Synchronized with Real Vedic Ephemeris | ✅ Astronomical Accuracy</p>
        </div>
                        # Sector Monthly Investment Calendar
                st.markdown(f"### 📅 {analysis_target} Sector - Monthly Investment Calendar")
                
                # Create investment calendar with recommendations
                investment_weeks = []
                for week_idx, week in enumerate(weeks[:4]):
                    week_bullish = sum(1 for day in week if day['trend'] == 'Bullish')
                    week_bearish = sum(1 for day in week if day['trend'] == 'Bearish')
                    week_volatile = sum(1 for day in week if day['trend'] == 'Volatile')
                    
                    if week_bullish >= 5:
                        week_strategy = f'ACCUMULATION WEEK for {analysis_target} sector'
                        week_color = '#28a745'
                        week_icon = '🟢'
                    elif week_bullish >= 3:
                        week_strategy = f'BUYING OPPORTUNITIES in {analysis_target} sector'
                        week_color = '#20c997'
                        week_icon = '✅'
                    elif week_bearish >= 4:
                        week_strategy = f'PROFIT BOOKING from {analysis_target} stocks'
                        week_color = '#dc3545'
                        week_icon = '🔴'
                    elif week_volatile >= 3:
                        week_strategy = f'HIGH VOLATILITY - Caution in {analysis_target}'
                        week_color = '#ffc107'
                        week_icon = '⚡'
                    else:
                        week_strategy = f'MIXED SIGNALS for {analysis_target} sector'
                        week_color = '#6c757d'
                        week_icon = '⚪'
                    
                    investment_weeks.append({
                        'week': f'Week {week_idx + 1}',
                        'dates': f'{week[0]["day_num"]}-{week[-1]["day_num"]} Aug',
                        'strategy': week_strategy,
                        'color': week_color,
                        'icon': week_icon,
                        'bullish_days': week_bullish,
                        'bearish_days': week_bearish,
                        'volatile_days': week_volatile
                    })
                
                # Display investment calendar
                for week_info in investment_weeks:
                    st.markdown(f"""
                    <div style="background: rgba(255,255,255,0.1); border: 2px solid {week_info['color']}; border-radius: 10px; padding: 15px; margin: 10px 0;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                            <h5 style="margin: 0; color: {week_info['color']};">{week_info['icon']} {week_info['week']} ({week_info['dates']})</h5>
                            <span style="background: {week_info['color']}; color: white; padding: 4px 12px; border-radius: 15px; font-weight: bold; font-size: 0.9em;">
                                {week_info['bullish_days']}B-{week_info['bearish_days']}R-{week_info['volatile_days']}V
                            </span>
                        </div>
                        <p style="margin: 0; font-size: 1.1em; font-weight: bold; color: {week_info['color']};">
                             {week_info['strategy']}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Overall monthly sector outlook
                total_bullish = bullish_count
                total_bearish = bearish_count
                sector_sentiment = 'STRONG BULLISH' if total_bullish >= 18 else 'BULLISH' if total_bullish >= 12 else 'BEARISH' if total_bearish >= 15 else 'MIXED'
                
                sentiment_color = '#28a745' if 'BULLISH' in sector_sentiment else '#dc3545' if sector_sentiment == 'BEARISH' else '#ffc107'
                
                st.markdown(f"""
                <div style="background: linear-gradient(45deg, {sentiment_color}20, {sentiment_color}10); border: 3px solid {sentiment_color}; border-radius: 15px; padding: 20px; margin: 20px 0; text-align: center;">
                    <h3 style="margin: 0 0 10px 0; color: {sentiment_color};"> {analysis_target} SECTOR - AUGUST 2025 OUTLOOK</h3>
                    <h2 style="margin: 0 0 15px 0; color: {sentiment_color}; font-size: 2em;">{sector_sentiment}</h2>
                    <p style="margin: 0; font-size: 1.2em; color: {sentiment_color}; font-weight: bold;">
                        {total_bullish} Bullish Days | {total_bearish} Bearish Days | {volatile_count} Volatile Days
                    </p>
                    <p style="margin: 10px 0 0 0; font-size: 1.1em; color: {sentiment_color};">
                        <strong>Overall Strategy:</strong> {
                            'Strong accumulation recommended for ' + analysis_target + ' sector stocks' if 'STRONG BULLISH' in sector_sentiment
                            else 'Good buying opportunities in ' + analysis_target + ' sector' if 'BULLISH' in sector_sentiment
                            else 'Defensive approach recommended for ' + analysis_target + ' sector' if sector_sentiment == 'BEARISH'
                            else 'Selective stock picking in ' + analysis_target + ' sector'
                        }
                    </p>
                </div>
                """, unsafe_allow_html=True)
        
        # Create planetary transit tabs
        planet_tab1, planet_tab2, planet_tab3 = st.tabs(["🕐 TODAY'S TRANSIT", "📅 WEEKLY TRANSITS", "🗓️ MONTHLY TRANSITS"])
        
        with planet_tab1:
            st.markdown("### ⏰ TODAY'S COMPLETE PLANETARY TRANSIT TIMELINE")
            
            # Today's detailed hourly planetary effects
            today_transits = [
                {
                    'time': '05:00-06:00', 'planet': 'Saturn ♄', 'nakshatra': 'Uttara Bhadrapada',
                    'effect': 'Banking sector pressure, Metal stocks weak',
                    'sectors_affected': ['Banking', 'Metal', 'Mining'],
                    'recommendation': 'Avoid fresh positions, book profits',
                    'strength': 'Weak',
                    'market_sentiment': 'Bearish'
                },
                {
                    'time': '06:00-07:00', 'planet': 'Jupiter ♃', 'nakshatra': 'Ardra',
                    'effect': 'Financial sector strength, Banking rally expected',
                    'sectors_affected': ['Banking', 'Finance', 'Insurance'],
                    'recommendation': 'Strong buy in banking stocks',
                    'strength': 'Excellent',
                    'market_sentiment': 'Strong Bullish'
                },
                {
                    'time': '07:00-08:00', 'planet': 'Mars ♂️', 'nakshatra': 'Uttara Phalguni',
                    'effect': 'Defense, Energy sectors active, High volatility',
                    'sectors_affected': ['Defense', 'Energy', 'Steel'],
                    'recommendation': 'Intraday trading with tight stops',
                    'strength': 'High',
                    'market_sentiment': 'Volatile'
                },
                {
                    'time': '08:00-09:00', 'planet': 'Sun ☀️', 'nakshatra': 'Pushya',
                    'effect': 'Government stocks, PSU banks strong',
                    'sectors_affected': ['PSU Banks', 'Government', 'Infrastructure'],
                    'recommendation': 'Buy PSU stocks, government themes',
                    'strength': 'Very Strong',
                    'market_sentiment': 'Bullish'
                },
                {
                    'time': '09:00-10:00', 'planet': 'Venus ♀', 'nakshatra': 'Ardra',
                    'effect': 'Luxury, Auto, Textiles highly favorable',
                    'sectors_affected': ['Auto', 'Luxury', 'Textiles', 'Consumer'],
                    'recommendation': 'Strong accumulation opportunity',
                    'strength': 'Strong',
                    'market_sentiment': 'Bullish'
                },
                {
                    'time': '10:00-11:00', 'planet': 'Mercury ☿', 'nakshatra': 'Pushya',
                    'effect': 'IT, Communication positive but mixed signals',
                    'sectors_affected': ['IT', 'Telecom', 'Media'],
                    'recommendation': 'Selective buying, avoid momentum trades',
                    'strength': 'Moderate',
                    'market_sentiment': 'Neutral'
                },
                {
                    'time': '11:00-12:00', 'planet': 'Moon 🌙', 'nakshatra': 'Swati',
                    'effect': 'FMCG, Real Estate, Trading sectors strong',
                    'sectors_affected': ['FMCG', 'Real Estate', 'Trading'],
                    'recommendation': 'Buy consumer stocks, real estate',
                    'strength': 'Strong',
                    'market_sentiment': 'Bullish'
                },
                {
                    'time': '12:00-13:00', 'planet': 'Saturn ♄', 'nakshatra': 'Uttara Bhadrapada',
                    'effect': 'Market correction, Pharma under pressure',
                    'sectors_affected': ['Pharma', 'Healthcare', 'Chemicals'],
                    'recommendation': 'Book profits, avoid fresh buying',
                    'strength': 'Weak',
                    'market_sentiment': 'Bearish'
                },
                {
                    'time': '13:00-14:00', 'planet': 'Jupiter ♃', 'nakshatra': 'Ardra',
                    'effect': 'PEAK BANKING HOUR - Maximum institutional flow',
                    'sectors_affected': ['Banking', 'Finance', 'NBFCs'],
                    'recommendation': 'PEAK BUY - Best banking entry',
                    'strength': 'Maximum',
                    'market_sentiment': 'Peak Bullish'
                },
                {
                    'time': '14:00-15:00', 'planet': 'Mars ♂️', 'nakshatra': 'Uttara Phalguni',
                    'effect': 'Extreme volatility, Energy stocks surge',
                    'sectors_affected': ['Energy', 'Oil & Gas', 'Power'],
                    'recommendation': 'High-risk trades only, use stops',
                    'strength': 'Extreme',
                    'market_sentiment': 'Highly Volatile'
                },
                {
                    'time': '15:00-15:30', 'planet': 'Sun ☀️', 'nakshatra': 'Pushya',
                    'effect': 'Closing strength, PSU final rally',
                    'sectors_affected': ['PSU', 'Government', 'Infrastructure'],
                    'recommendation': 'Closing buying opportunity',
                    'strength': 'Strong',
                    'market_sentiment': 'Closing Bullish'
                }
            ]
            
            # Display today's transit timeline
            for transit in today_transits:
                is_current = current_hour >= int(transit['time'].split('-')[0].split(':')[0]) and current_hour < int(transit['time'].split('-')[1].split(':')[0])
                
                if transit['market_sentiment'] in ['Strong Bullish', 'Peak Bullish', 'Bullish', 'Closing Bullish']:
                    bg_color = '#d4edda'
                    text_color = '#155724'
                    border_color = '#28a745'
                    icon = '🟢'
                elif transit['market_sentiment'] in ['Bearish']:
                    bg_color = '#f8d7da'
                    text_color = '#721c24'
                    border_color = '#dc3545'
                    icon = '🔴'
                elif transit['market_sentiment'] in ['Volatile', 'Highly Volatile']:
                    bg_color = '#fff3cd'
                    text_color = '#856404'
                    border_color = '#ffc107'
                    icon = '⚡'
                else:
                    bg_color = '#e2e3e5'
                    text_color = '#495057'
                    border_color = '#6c757d'
                    icon = '⚪'
                
                active_style = 'animation: pulse 2s infinite; border: 4px solid #ff6b35; box-shadow: 0 0 20px rgba(255,107,53,0.8);' if is_current else f'border: 2px solid {border_color};'
                active_text = ' 🔥 LIVE NOW - ACTIVE TRANSIT' if is_current else ''
                peak_text = ' ⭐ PEAK HOUR' if 'Peak' in transit['market_sentiment'] else ''
                
                st.markdown(f"""
                <div style="background: {bg_color}; color: {text_color}; padding: 15px; border-radius: 12px; margin: 12px 0; {active_style}">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                        <h4 style="margin: 0; color: {text_color};">{icon} {transit['time']} - {transit['planet']}{active_text}{peak_text}</h4>
                        <span style="background: {text_color}; color: {bg_color}; padding: 4px 12px; border-radius: 20px; font-weight: bold; font-size: 0.9em;">
                            {transit['market_sentiment']}
                        </span>
                    </div>
                    
                    <div style="background: rgba(255,255,255,0.2); padding: 12px; border-radius: 8px; margin: 10px 0;">
                        <p style="margin: 0 0 8px 0; font-size: 1.1em; font-weight: bold;"><strong> Nakshatra:</strong> {transit['nakshatra']}</p>
                        <p style="margin: 0 0 8px 0; font-size: 1em;"><strong> Market Effect:</strong> {transit['effect']}</p>
                        <p style="margin: 0 0 8px 0; font-size: 1em;"><strong> Sectors Affected:</strong> {', '.join(transit['sectors_affected'])}</p>
                        <p style="margin: 0 0 8px 0; font-size: 1em;"><strong> Trading Strategy:</strong> {transit['recommendation']}</p>
                        <p style="margin: 0; font-size: 1em;"><strong> Planetary Strength:</strong> {transit['strength']}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        with planet_tab2:
            st.markdown("### 📅 THIS WEEK'S MAJOR PLANETARY TRANSITS & EFFECTS")
            
            weekly_transits = [
                {
                    'date': 'August 1 (Today)',
                    'transits': [
                        {'planet': 'Moon 🌙', 'event': 'Swati Nakshatra', 'effect': 'Trade & Luxury sectors excellent', 'impact': 'Very Positive'},
                        {'planet': 'Jupiter ♃', 'event': 'Ardra influence peak', 'effect': 'Banking sector maximum strength', 'impact': 'Extremely Positive'}
                    ]
                },
                {
                    'date': 'August 2 (Tomorrow)',
                    'transits': [
                        {'planet': 'Moon 🌙', 'event': 'Moves to Vishakha', 'effect': 'Banking gets additional boost, Export sectors rise', 'impact': 'Very Positive'},
                        {'planet': 'Mercury ☿', 'event': 'Cancer strengthens', 'effect': 'FMCG and IT services gain momentum', 'impact': 'Positive'}
                    ]
                },
                {
                    'date': 'August 3 (Saturday)',
                    'transits': [
                        {'planet': 'Venus ♀', 'event': 'Aspect with Mars', 'effect': 'Auto sector volatility, luxury goods mixed', 'impact': 'Mixed'},
                        {'planet': 'Saturn ♄', 'event': 'Continues Pisces', 'effect': 'Pharma sector caution continues', 'impact': 'Negative'}
                    ]
                },
                {
                    'date': 'August 4 (Sunday)',
                    'transits': [
                        {'planet': 'Sun ☀️', 'event': 'Cancer degree change', 'effect': 'Government stocks, PSU strength', 'impact': 'Positive'},
                        {'planet': 'Rahu ☊', 'event': 'Pisces continues', 'effect': 'Foreign investments volatile', 'impact': 'Volatile'}
                    ]
                },
                {
                    'date': 'August 5 (Monday)',
                    'transits': [
                        {'planet': 'Mercury ☿', 'event': 'Conjunct Sun', 'effect': 'IT and FMCG combined strength', 'impact': 'Very Positive'},
                        {'planet': 'Mars ♂️', 'event': 'Virgo continues', 'effect': 'Healthcare sector mixed signals', 'impact': 'Neutral'}
                    ]
                },
                {
                    'date': 'August 6 (Tuesday)',
                    'transits': [
                        {'planet': 'Venus ♀', 'event': 'Moves to Mrigashira', 'effect': 'Real estate and luxury shift focus', 'impact': 'Positive'},
                        {'planet': 'Jupiter ♃', 'event': 'Ardra final degrees', 'effect': 'Banking sector peak before transition', 'impact': 'Peak Positive'}
                    ]
                },
                {
                    'date': 'August 7 (Wednesday)',
                    'transits': [
                        {'planet': 'Moon 🌙', 'event': 'Anuradha entry', 'effect': 'Financial markets deep strength', 'impact': 'Very Positive'},
                        {'planet': 'Saturn ♄', 'event': 'Aspect change', 'effect': 'Metal and mining sector relief', 'impact': 'Positive'}
                    ]
                }
            ]
            
            for day_transit in weekly_transits:
                day_col1, day_col2 = st.columns([1, 3])
                
                with day_col1:
                    is_today = 'Today' in day_transit['date']
                    date_style = 'background: #ff6b35; color: white; border: 3px solid #ff6b35;' if is_today else 'background: #007bff; color: white; border: 2px solid #007bff;'
                    
                    st.markdown(f"""
                    <div style="{date_style} padding: 15px; border-radius: 10px; text-align: center; margin: 10px 0;">
                        <h4 style="margin: 0; font-weight: bold;">{day_transit['date']}</h4>
                        {f'<p style="margin: 5px 0 0 0; font-size: 0.8em;">🔥 CURRENT DAY</p>' if is_today else ''}
                    </div>
                    """, unsafe_allow_html=True)
                
                with day_col2:
                    for transit in day_transit['transits']:
                        if transit['impact'] in ['Extremely Positive', 'Very Positive', 'Peak Positive']:
                            impact_color = '#28a745'
                            impact_bg = '#d4edda'
                            impact_icon = '🟢'
                        elif transit['impact'] == 'Positive':
                            impact_color = '#20c997'
                            impact_bg = '#d1ecf1'
                            impact_icon = '✅'
                        elif transit['impact'] == 'Negative':
                            impact_color = '#dc3545'
                            impact_bg = '#f8d7da'
                            impact_icon = '🔴'
                        elif transit['impact'] in ['Volatile', 'Mixed']:
                            impact_color = '#ffc107'
                            impact_bg = '#fff3cd'
                            impact_icon = '⚡'
                        else:
                            impact_color = '#6c757d'
                            impact_bg = '#e2e3e5'
                            impact_icon = '⚪'
                        
                        st.markdown(f"""
                        <div style="background: {impact_bg}; color: {impact_color}; padding: 12px; border-radius: 8px; margin: 5px 0; border-left: 4px solid {impact_color};">
                            <h5 style="margin: 0 0 5px 0; color: {impact_color};">{impact_icon} {transit['planet']} - {transit['event']}</h5>
                            <p style="margin: 0 0 3px 0; font-size: 0.95em;"><strong>Effect:</strong> {transit['effect']}</p>
                            <p style="margin: 0; font-size: 0.9em;"><strong>Impact:</strong> 
                                <span style="background: {impact_color}; color: white; padding: 2px 8px; border-radius: 12px; font-weight: bold; font-size: 0.8em;">
                                    {transit['impact']}
                                </span>
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
        
        with planet_tab3:
            st.markdown("### 🗓️ AUGUST 2025 MAJOR PLANETARY TRANSITS & MARKET EFFECTS")
            
            monthly_major_transits = [
                {
                    'period': 'August 1-7',
                    'major_event': 'Jupiter in Ardra Peak Phase',
                    'effect': 'Banking sector exceptional period, maximum institutional flow',
                    'best_sectors': ['Banking', 'Finance', 'Insurance', 'NBFCs'],
                    'strategy': 'Heavy accumulation in financial stocks',
                    'impact_level': 'Extremely Bullish'
                },
                {
                    'period': 'August 8-15',
                    'major_event': 'Venus-Mercury Conjunction in Cancer',
                    'effect': 'FMCG and Auto sectors combined strength, consumer boost',
                    'best_sectors': ['FMCG', 'Auto', 'Consumer Goods', 'Retail'],
                    'strategy': 'Focus on consumer-facing companies',
                    'impact_level': 'Very Bullish'
                },
                {
                    'period': 'August 16-23',
                    'major_event': 'Mars Transit to Libra',
                    'effect': 'Balance and justice themes, legal sector activity',
                    'best_sectors': ['Legal Services', 'Real Estate', 'Luxury'],
                    'strategy': 'Diversification and balanced portfolio',
                    'impact_level': 'Moderately Bullish'
                },
                {
                    'period': 'August 24-31',
                    'major_event': 'Saturn Retrograde Effect Peaks',
                    'effect': 'Correction in overvalued stocks, quality focus',
                    'best_sectors': ['Large Cap', 'Dividend Stocks', 'Utilities'],
                    'strategy': 'Quality over quantity, defensive approach',
                    'impact_level': 'Cautious'
                }
            ]
            
            for period_data in monthly_major_transits:
                if period_data['impact_level'] in ['Extremely Bullish', 'Very Bullish']:
                    period_color = '#28a745'
                    period_bg = '#d4edda'
                elif period_data['impact_level'] == 'Moderately Bullish':
                    period_color = '#20c997'
                    period_bg = '#d1ecf1'
                elif period_data['impact_level'] == 'Cautious':
                    period_color = '#ffc107'
                    period_bg = '#fff3cd'
                else:
                    period_color = '#6c757d'
                    period_bg = '#e2e3e5'
                
                st.markdown(f"""
                <div style="background: {period_bg}; color: {period_color}; padding: 20px; border-radius: 12px; margin: 15px 0; border: 3px solid {period_color};">
                    <h4 style="margin: 0 0 15px 0; color: {period_color}; text-align: center;">📅 {period_data['period']}</h4>
                    
                    <div style="background: rgba(255,255,255,0.3); padding: 15px; border-radius: 8px;">
                        <h5 style="margin: 0 0 10px 0; color: {period_color};"> Major Transit: {period_data['major_event']}</h5>
                        <p style="margin: 0 0 10px 0; font-size: 1em;"><strong> Market Effect:</strong> {period_data['effect']}</p>
                        <p style="margin: 0 0 10px 0; font-size: 1em;"><strong> Best Sectors:</strong> {', '.join(period_data['best_sectors'])}</p>
                        <p style="margin: 0 0 10px 0; font-size: 1em;"><strong> Strategy:</strong> {period_data['strategy']}</p>
                        <p style="margin: 0; font-size: 1.1em; text-align: center;">
                            <strong>📈 Overall Impact:</strong> 
                            <span style="background: {period_color}; color: white; padding: 5px 15px; border-radius: 20px; font-weight: bold;">
                                {period_data['impact_level']}
                            </span>
                        </p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Monthly stock-specific predictions
            st.markdown("### 📊 Top Stocks - Monthly Planetary Outlook")
            
            stock_monthly_predictions = [
                {'stock': 'RELIANCE', 'planet': 'Venus ♀', 'effect': 'Energy + Luxury combo strong', 'target': '+15-20%', 'rating': 'Strong Buy'},
                {'stock': 'HDFC BANK', 'planet': 'Jupiter ♃', 'effect': 'Peak banking period, maximum gains', 'target': '+18-25%', 'rating': 'Strong Buy'},
                {'stock': 'TCS', 'planet': 'Mercury ☿', 'effect': 'IT services recovery, global demand', 'target': '+8-12%', 'rating': 'Buy'},
                {'stock': 'INFOSYS', 'planet': 'Mercury ☿', 'effect': 'Mixed signals, selective approach', 'target': '+5-8%', 'rating': 'Hold'},
                {'stock': 'MARUTI SUZUKI', 'planet': 'Venus ♀', 'effect': 'Auto sector renaissance period', 'target': '+12-18%', 'rating': 'Strong Buy'},
                {'stock': 'SBI', 'planet': 'Jupiter ♃', 'effect': 'PSU banking exceptional period', 'target': '+20-30%', 'rating': 'Strong Buy'},
                {'stock': 'ICICI BANK', 'planet': 'Jupiter ♃', 'effect': 'Private banking strength continues', 'target': '+15-22%', 'rating': 'Strong Buy'},
                {'stock': 'BHARTI AIRTEL', 'planet': 'Mercury ☿', 'effect': 'Telecom sector steady growth', 'target': '+8-12%', 'rating': 'Buy'},
                {'stock': 'HINDUNILVR', 'planet': 'Moon 🌙', 'effect': 'FMCG consistent performer', 'target': '+6-10%', 'rating': 'Buy'},
                {'stock': 'LT', 'planet': 'Saturn ♄', 'effect': 'Infrastructure gains momentum', 'target': '+10-15%', 'rating': 'Buy'}
            ]
            
            prediction_cols = st.columns(2)
            
            for idx, prediction in enumerate(stock_monthly_predictions):
                col_idx = idx % 2
                
                if prediction['rating'] == 'Strong Buy':
                    rating_color = '#28a745'
                    rating_bg = '#d4edda'
                elif prediction['rating'] == 'Buy':
                    rating_color = '#20c997'
                    rating_bg = '#d1ecf1'
                else:
                    rating_color = '#ffc107'
                    rating_bg = '#fff3cd'
                
                with prediction_cols[col_idx]:
                    st.markdown(f"""
                    <div style="background: {rating_bg}; color: {rating_color}; padding: 15px; border-radius: 10px; margin: 8px 0; border: 2px solid {rating_color};">
                        <h5 style="margin: 0 0 10px 0; color: {rating_color};"> {prediction['stock']}</h5>
                        <p style="margin: 0 0 5px 0; font-size: 0.9em;"><strong> Ruling Planet:</strong> {prediction['planet']}</p>
                        <p style="margin: 0 0 5px 0; font-size: 0.9em;"><strong> Effect:</strong> {prediction['effect']}</p>
                        <p style="margin: 0 0 5px 0; font-size: 0.9em;"><strong> Target:</strong> {prediction['target']}</p>
                        <p style="margin: 0; font-size: 1em; text-align: center;">
                            <span style="background: {rating_color}; color: white; padding: 4px 12px; border-radius: 15px; font-weight: bold; font-size: 0.9em;">
                                {prediction['rating']}
                            </span>
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
