# 🔴 RiskTakerZ News Bot

A **high-impact market alert Discord bot** for traders focused on Nasdaq (NQ) volatility. Delivers only RED folder events—Fed announcements, NFP data, earnings surprises—nothing else.

**Philosophy:** "What moves the market moves the signal." 

---

## 📌 Features

### 🎯 Pre-Market Catalyst Alerts (6:00 AM PST)
- Daily scan of high-impact economic events (3-star events only)
- Optional SearchAPI-backed pre-market snapshot for QQQ, SPY, VIX, and TLT
- Filters for USD and Nasdaq volatility catalysts
- Formatted with time, event name, and impact level
- Daily bias poll: Gauge group sentiment before market open (Bullish/Bearish/Neutral)

### 🚨 Real-Time Breaking News Monitor (Every 10 Minutes)
- Scans Google News RSS for breaking headlines
- Keywords: Fed, Powell, Earnings, Inflation, NFP, China, Tech
- Posts alert instantly when market-moving news drops
- Active during market hours (3 AM - 1 PM PST)

### 🎚️ RiskTakerZ Branding
- Red-themed embeds (High Impact Only aesthetic)
- Custom emojis: 🔴 🎯 📈 📉 🚨
- Bot status: "Watching NQ Futures 📈 | Analyzing Liquidity"
- PSYCHO // SOUND theme throughout

---

## 🏗️ Project Structure

```
risktakerz-news-bot/
├── src/
│   ├── bot.py           # Discord client, event handlers, background tasks
│   ├── scraper.py       # Economic calendar & breaking news scraper
│   ├── utils.py         # Embed formatting & styling helpers
│   └── __init__.py
├── main.py              # Entry point (Railway runs this)
├── requirements.txt     # Python dependencies
├── .env                 # Local environment variables (don't push!)
├── Procfile             # Railway deployment command
├── DEPLOYMENT.md        # Complete Railway setup guide
└── .gitignore          # Prevents pushing secrets
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Discord server (with message history permission)
- Discord bot token ([Get here](https://discord.com/developers/applications))

### Local Setup
```bash
# Clone repo
git clone https://github.com/YOUR_USERNAME/risktakerz-news-bot.git
cd risktakerz-news-bot

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Add your DISCORD_TOKEN and ALERTS_CHANNEL_ID

# Run locally
python main.py
```

### Test Commands
```
!ping              # Check if bot is responsive
!snapshot          # Show SearchAPI-backed market snapshot
!test_event        # Display sample economic event
!test_breaking     # Display sample breaking news alert
!alerts            # Manually trigger pre-market alert
!bias              # Manually trigger daily bias poll
```

### Deploy to Railway
See [DEPLOYMENT.md](DEPLOYMENT.md) for step-by-step Railway setup instructions.

---

## ⏰ Background Tasks

| Task | When | What |
|------|------|------|
| **Morning Prep** | 6:00 AM PST | Economic calendar with high-impact events |
| **Daily Bias Poll** | 6:15 AM PST | React poll: 📈 Bullish / 📉 Bearish / ↔️ Neutral |
| **Breaking News Monitor** | Every 10 min (during market hours) | Real-time alerts for market-moving news |

---

## 📊 Data Sources

- **Economic Calendar:** Investing.com (3-star events only)
- **Breaking News:** SearchAPI Google News when configured, otherwise Google News RSS fallback
- **Market Data:** SearchAPI Google Finance (optional, for QQQ/SPY/VIX/TLT snapshot)

### Optional Market Data API

Add `SEARCHAPI_API_KEY` in your `.env` or Railway Variables to enable API-backed market context.

```dotenv
SEARCHAPI_API_KEY=your_searchapi_api_key_here
MARKET_SYMBOLS=QQQ:NYSEARCA,SPY:NYSEARCA,VIX:INDEXCBOE,TLT:NASDAQ
```

With that set, the bot will:
- add a pre-market snapshot before the economic calendar alert
- expose `!snapshot` for a manual tape check
- summarize the tape as risk-on, risk-off, or mixed

---

## 🔧 Customization

### Change Alert Keywords
Edit `src/scraper.py`:
```python
keywords = ['Fed', 'Powell', 'Earnings', 'Inflation', 'NFP', 'Halt', 'China', 'Tech']
```

### Adjust News Check Frequency
Edit `src/bot.py`:
```python
@tasks.loop(minutes=10)  # Change 10 to your preferred interval
async def breaking_news_monitor():
```

### Change Alert Times
Edit `src/bot.py`:
```python
target_time = time(6, 0)  # Change 6, 0 to desired hour, minute (PST)
```

---

## ⚙️ Requirements

```
discord.py>=2.3.0          # Discord API wrapper
requests>=2.31.0           # HTTP requests for scraping
python-dotenv>=1.0.0       # Load environment variables
beautifulsoup4>=4.12.0     # HTML/XML parsing
pytz>=2024.1               # Timezone handling
lxml>=4.9.0                # XML parser for RSS feeds
```

---

## 🔐 Security

- **Never commit `.env` file** - Already in `.gitignore`
- **Use Railway Variables** for production (encrypted)
- **Regenerate Discord token** if accidentally shared
- **Bot permissions** limited to: Send Messages, Embed Links, Add Reactions

---

## 📈 Roadmap

- [x] API-backed pre-market stock/ETF snapshot
- [ ] Historical event database
- [ ] Sentiment analysis on breaking news
- [ ] Portfolio tracking per trader
- [ ] Machine learning catalyst prediction
- [ ] SMS/Push notifications

---

## 🚨 Troubleshooting

**Bot offline?**
- Check Discord token in Railway Variables
- Verify channel ID is correct
- See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed troubleshooting

**No alerts posting?**
- Verify bot has message permissions in channel
- Check bot is running (Railway Logs tab)
- Try manual commands (`!alerts`, `!bias`)

**Too many/few alerts?**
- Adjust keywords in `scraper.py`
- Change breaking news check frequency
- Customize time filters

---

## 📝 License

Built for traders, by traders. Use freely for personal trading groups.

---

## 🎯 Philosophy

**"High Impact Only"** = No spam, only catalysts that move markets.

Smart traders only need to know when:
- The Fed talks
- Jobs data drops
- Tech earnings surprise
- Major volatility spikes

Everything else is noise. 🔴

---

## 📞 Support

Found a bug? Have a feature idea?

1. Check [DEPLOYMENT.md](DEPLOYMENT.md) troubleshooting section
2. Review bot logs in Railway dashboard
3. Test with `!test_event` and `!test_breaking` commands

---

**Made for traders. Deployed with Railway. Running 24/5.** 🚀
