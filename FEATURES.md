# 🎯 Features Overview

Complete guide to RiskTakerZ News Bot capabilities.

---

## 📌 Automatic Background Tasks

### 1. Pre-Market Catalysts Alert (6:00 AM PST Daily)

**What:** Scans Investing.com for high-impact (3-star) economic events

**How Often:** Once per day at market open

**Data Used:**
- Event name (NFP, CPI, FOMC, etc.)
- Time (8:30 AM EST, 2:00 PM UTC, etc.)
- Country (USD, EUR, JPY, etc.)
- Impact level (High/Medium/Low)

**Filtered For:** 
- USD events only (default)
- Major volatility catalysts: NFP, FOMC, Fed speakers, CPI, GDP, Inflation data

**Alert Format:**
```
🎯 PRE-MARKET CATALYSTS
High-impact data dropping today. Know your levels.

⏰ 8:30 AM | Non-Farm Payroll (USD) | 🔴 HIGH
⏰ 1:00 PM | Fed Speaker | 🔴 HIGH
```

**Mentions:** `@everyone` (so no one misses it)

**Customizable:** ✅ Keywords, times, event count (see [CONFIG.md](CONFIG.md))

---

### 2. Daily Bias Poll (6:15 AM PST Daily)

**What:** Gauges group sentiment before market open

**How Often:** Once per day (15 minutes after market prep alert)

**Poll Options:**
- 📈 **Bullish** - Expecting up day
- 📉 **Bearish** - Expecting down day
- ↔️ **Neutral** - Choppy/Unclear

**How to Vote:** React with emoji to the poll message

**Benefits:**
- See group conviction before bell
- Shared accountability
- Community engagement

**Customizable:** ✅ Time, poll wording (see [CONFIG.md](CONFIG.md))

---

### 3. Real-Time Breaking News Monitor (Every 10 Minutes)

**What:** Scans Google News RSS for market-moving headlines

**How Often:** Every 10 minutes (24/5 during market hours)

**Market Hours:** 3:00 AM - 1:00 PM PST (includes pre-market & post-market)

**Data Source:** Google News RSS (fast, free, less blocking)

**Keywords Monitored:**
- 🏦 Fed, Powell (monetary policy)
- 💰 Earnings, Earnings beats/misses (company news)
- 📊 Inflation, CPI, NFP (economic data)
- ⛔ Halt (trading halts)
- 🌍 China (geopolitical risk)
- 💻 Tech (sector-specific)

**Alert Format:**
```
🚨 BREAKING NEWS ALERT

Fed Chair Powell Signals Potential Rate Cut in June
Source: Reuters
[Link to full article]
```

**Customizable:** ✅ Keywords, frequency, market hours (see [CONFIG.md](CONFIG.md))

---

## 💬 Manual Commands

Use these commands anytime in Discord. Prefix default is `!` (customizable).

### !ping
**Purpose:** Test bot responsiveness

**Response:** Shows bot latency in milliseconds
```
🏓 Pong! 45ms
```

---

### !alerts
**Purpose:** Manually trigger pre-market alert (don't wait for 6 AM)

**Response:** Posts the day's high-impact economic events immediately

**Use Case:** Testing, or if you missed the 6 AM alert

---

### !bias
**Purpose:** Manually trigger daily bias poll

**Response:** Posts sentiment poll with emoji options

**Use Case:** Weekend testing, or mid-morning check-in

---

### !test_event
**Purpose:** Display sample economic event formatting

**Response:** Shows what an economic alert looks like
```
🔴 Non-Farm Payroll (NFP)
⏰ Time: 8:30 AM EST
📊 Impact: High
📈 Forecast: Expected: 250K | Previous: 220K
```

---

### !test_breaking
**Purpose:** Display sample breaking news formatting

**Response:** Shows what a breaking news alert looks like
```
🚨 BREAKING NEWS ALERT

Fed Chair Powell Signals Potential Rate Cut in June
Source: Reuters
```

---

## 🎨 Customization Options

### Data Filtering

| Option | Customizable | Details |
|--------|---|---|
| Breaking news keywords | ✅ | Add/remove keywords that trigger alerts |
| Economic event keywords | ✅ | Filter for specific events (NFP, Fed speakers, etc.) |
| Countries monitored | ✅ | Default: USD only, can add EUR, JPY, etc. |
| Number of events | ✅ | Default: top 5, can change to 3, 10, etc. |

### Timing

| Option | Customizable | Details |
|--------|---|---|
| Morning alert time | ✅ | Default: 6:00 AM PST, change to any time |
| Bias poll time | ✅ | Default: 6:15 AM PST, change to any time |
| News check frequency | ✅ | Default: every 10 min, change to 5, 15, 30 min |
| Market hours start | ✅ | Default: 3:00 AM PST, adjust for your markets |
| Market hours end | ✅ | Default: 1:00 PM PST, adjust for your markets |

### Display

| Option | Customizable | Details |
|--------|---|---|
| Embed colors | ✅ | Change red theme to other colors |
| Emoji usage | ✅ | Add custom Discord emojis |
| Bot status text | ✅ | What bot shows as "Playing/Watching" |
| Channel ID | ✅ | Send alerts to different channels |
| Bot prefix | ✅ | Change `!` to `$`, `>`, `&`, etc. |

---

## 🔌 Integration Points

### Data Sources

1. **Investing.com Economic Calendar**
   - Scrapes real HTML table
   - Filters for 3-star events
   - Free, no API key needed

2. **Google News RSS**
   - Uses RSS feed (fast, less blocking)
   - Keyword filtering for relevance
   - Free, no API key needed

3. **Optional: NewsAPI**
   - Paid tier available
   - More focused news filtering
   - Add to scraper.py (currently placeholder)

### Discord Integration

1. **Discord.py library** (Python wrapper for Discord API)
2. **Message embeds** (rich formatting, links, images)
3. **Reactions** (for bias poll voting)
4. **Slash commands** (extensible for future)

---

## 📊 Example Alert Flow

### 6:00 AM PST (2:00 PM UTC)
Bot posts:
```
🎯 PRE-MARKET CATALYSTS
⏰ 8:30 AM | NFP (USD) | 🔴 HIGH
```
@everyone sees it instantly

### 6:15 AM PST (2:15 PM UTC)
Bot posts:
```
📊 Daily Bias Poll
📈 = Bullish | 📉 = Bearish | ↔️ = Neutral  
```
Traders react with conviction

### 6:20 AM PST (2:20 PM UTC)
Google News drops breaking story about Fed comments:
```
🚨 BREAKING NEWS ALERT
Fed Official Hints at Pause in Rate Hikes
Source: Bloomberg
```
Bot posts instantly (within 10 minutes of news)

### Throughout Trading Hours
Every 10 minutes, bot checks for news matching keywords and posts any breaking headlines

---

## 🚀 Performance

### Resource Usage
- **CPU:** Minimal (idle tasks until scheduled triggers)
- **Memory:** ~50-100 MB (Discord.py overhead)
- **Network:** ~1-2 requests per 10 minutes during market hours
- **Cost on Railway:** Free tier sufficient

### Reliability
- **Uptime:** 99%+ (Railway infrastructure)
- **Redundancy:** Automatic restarts if crashed
- **Fallback:** Manual commands always available

---

## 🔐 Permissions Required

### Discord Bot Needs:
- ✅ Send Messages
- ✅ Embed Links
- ✅ Add Reactions (for polls)
- ✅ Read Message History
- ❌ Manage Messages (not needed)
- ❌ Manage Channels (not needed)
- ❌ Administrator (not needed)

---

## 📈 Future Roadmap

### Planned Features
- [ ] Real-time stock price integration
- [ ] Portfolio tracking (buy/sell alerts)
- [ ] Sentiment analysis on headlines
- [ ] Historical event success rate
- [ ] SMS/Push notifications
- [ ] ML-powered catalyst prediction
- [ ] Multi-symbol tracking (not just NQ)

### Community Requests Welcome!

---

## 🆘 Troubleshooting Features

### If Alerts Don't Post:

1. **Check command permissions**
   ```
   !ping  # Should respond
   ```

2. **Manually trigger alerts**
   ```
   !alerts        # Try pre-market alert
   !bias          # Try bias poll
   !test_breaking # Test news format
   ```

3. **View logs**
   - Railway dashboard → Logs tab
   - Look for errors or HTTP failures

4. **Verify configuration**
   - Railway Variables tab has DISCORD_TOKEN?
   - ALERTS_CHANNEL_ID correct?
   - Bot has permissions in channel?

---

**Questions?** See [DEPLOYMENT.md](DEPLOYMENT.md) or [CONFIG.md](CONFIG.md) 🎯
