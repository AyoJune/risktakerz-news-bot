# ⚙️ Configuration Guide

How to customize the RiskTakerZ News Bot to your trading style.

---

## 🏃 Quick Customizations (No Coding Required)

### 1. Change Alert Channel
1. Go to Railway dashboard
2. Click **Variables**
3. Update `ALERTS_CHANNEL_ID` with your preferred channel ID
4. Redeploy: Click the deployment → Redeploy button

### 2. Change Bot Prefix
1. Edit [.env](.env)
2. Update `BOT_PREFIX = !` to your preferred prefix (e.g., `$`, `>`, `&`)
3. Push to GitHub - Railway will redeploy automatically

---

## 🔧 Advanced Customizations (Code Edits)

### Change Breaking News Keywords

**File:** `src/scraper.py`, Function: `get_breaking_news()`

```python
keywords = ['Fed', 'Powell', 'Earnings', 'Inflation', 'NFP', 'Halt', 'China', 'Tech']
```

**Add more:**
```python
keywords = ['Fed', 'Powell', 'Earnings', 'Inflation', 'NFP', 'Halt', 'China', 'Tech', 'Crypto', 'FOMC', 'GDP']
```

**Remove less relevant:**
```python
keywords = ['Fed', 'Powell', 'Earnings', 'NFP']  # Only absolute essentials
```

**Then:** Push to GitHub → Railway redeploys automatically ✅

---

### Adjust Economic Calendar Filters

**File:** `src/scraper.py`, Function: `get_economic_calendar()`

```python
# Current: Only USD events
if 'USD' in country or any(keyword in event_name.upper() for keyword in 
    ['NFP', 'FOMC', 'CPI', 'INFLATION', 'EMPLOYMENT', 'GDP', 'FED']):
```

**Add EUR events:**
```python
if 'USD' in country or 'EUR' in country or any(keyword in event_name.upper() for keyword in 
    ['NFP', 'FOMC', 'CPI', 'INFLATION', 'EMPLOYMENT', 'GDP', 'FED']):
```

**More restrictive (Fed only):**
```python
if any(keyword in event_name.upper() for keyword in ['FOMC', 'FED SPEAKER', 'POWELL']):
```

---

### Change Background Task Timing

**File:** `src/bot.py`

#### Change Morning Prep Time (currently 6:00 AM PST)

```python
@tasks.loop(hours=24)
async def morning_prep():
    now = datetime.now(TIMEZONE)
    target_time = time(6, 0)  # ← Change this: (hour, minute)
```

**Examples:**
- `time(5, 0)` = 5:00 AM PST
- `time(7, 30)` = 7:30 AM PST
- `time(9, 45)` = 9:45 AM PST

#### Change Daily Bias Time (currently 6:15 AM PST)

```python
@tasks.loop(hours=24)
async def daily_bias_poll():
    now = datetime.now(TIMEZONE)
    target_time = time(6, 15)  # ← Change this
```

#### Change Breaking News Check Frequency (currently every 10 minutes)

```python
@tasks.loop(minutes=10)  # ← Change to: 5, 15, 30, 60, etc.
async def breaking_news_monitor():
```

#### Change Breaking News Market Hours (currently 3 AM - 1 PM PST)

```python
# Check if we're in market hours (PST)
market_start = time(3, 0)   # ← Change from 3:00 AM
market_end = time(13, 0)    # ← Change to 1:00 PM
```

**Examples:**
- `time(8, 0)` and `time(17, 0)` = Regular trading hours only
- `time(6, 0)` and `time(20, 0)` = Extended hours

---

## 🎨 Customize Embed Styling

**File:** `src/utils.py`

### Change Colors

Current: Bright red `(255, 0, 0)`

```python
# Change to dark red
color=discord.Color.from_rgb(139, 0, 0)

# Or use Discord presets
color=discord.Color.red()      # Bright red
color=discord.Color.dark_red() # Dark red
color=discord.Color.gold()     # Gold
color=discord.Color.blue()     # Blue
```

### Add Bot Avatar

1. Create your bot avatar image (512x512 PNG recommended)
2. Go to [Discord Developer Portal](https://discord.com/developers/applications)
3. Select your bot
4. Click **General Information**
5. Upload your image under **APP ICON**

### Change Bot Status Text

**File:** `src/bot.py`, Function: `on_ready()`

```python
await bot.change_presence(
    activity=discord.Activity(
        type=discord.ActivityType.watching,
        name="NQ Futures 📈 | Analyzing Liquidity"  # ← Change this
    )
)
```

**Examples:**
```python
name="Earnings Season 📊"
name="Fed Decisions 🏦"
name="Tech Volatility 💻"
name="Your Portfolio 💰"
name="Market Gaps 📈"
```

---

## 📊 Adjust Number of Events Returned

### Economic Calendar Events

**File:** `src/scraper.py`

```python
return events[:5]  # Return top 5 - change 5 to your preference
```

**Examples:**
- `[:3]` = Top 3 events only (most concise)
- `[:10]` = Top 10 events (comprehensive)

### Breaking News Articles

**File:** `src/scraper.py`

```python
for item in items[:5]:  # Check first 5 - change 5 to your preference
```

---

## 🌍 Change Timezone

**File:** `src/bot.py` and `src/scraper.py`

```python
TIMEZONE = pytz.timezone("US/Pacific")  # ← Change this
```

**Examples:**
```python
TIMEZONE = pytz.timezone("US/Eastern")      # EST
TIMEZONE = pytz.timezone("US/Central")      # CST
TIMEZONE = pytz.timezone("America/Chicago") # Chicago time
TIMEZONE = pytz.timezone("Europe/London")   # UK time
TIMEZONE = pytz.timezone("Asia/Tokyo")      # Tokyo time
```

**Valid timezones:** https://en.wikipedia.org/wiki/List_of_tz_database_time_zones

---

## 🧪 Test Your Changes

After editing, test locally:

```bash
# Install updated dependencies (if needed)
pip install -r requirements.txt

# Run locally
python main.py

# Test commands in Discord
!ping              # Should work
!test_event        # See updated formatting
!test_breaking     # See updated formatting
!alerts            # Trigger manually
```

---

## 🚀 Deploy Your Changes

Once tested locally:

```bash
git add .
git commit -m "Custom configuration: [describe changes]"
git push origin main
```

Railway automatically redeploys when you push! ✅

---

## 📋 Common Recipes

### Recipe 1: "Earnings Season Scoreboard"
```python
keywords = ['Earnings', 'Beat', 'Miss', 'Guidance', 'Surprise']
target_time = time(9, 0)  # Run after market open
market_start = time(9, 30)  # Track during trading hours
market_end = time(16, 0)
```

### Recipe 2: "Crypto Volatility Alerts"
```python
keywords = ['Crypto', 'Bitcoin', 'Ethereum', 'SEC', 'Fed', 'Regulation']
market_start = time(0, 0)  # 24/7 monitoring (crypto never sleeps)
market_end = time(23, 59)
```

### Recipe 3: "Minimal (Fed Eyes Only)"
```python
keywords = ['FOMC', 'Powell', 'FED SPEAKER']
return events[:2]  # Only 2 most important
```

### Recipe 4: "Hyper-Active (Every 5 Minutes)"
```python
@tasks.loop(minutes=5)  # Check every 5 instead of 10
```

---

## ❓ FAQ

**Q: Can I have multiple alert channels?**
A: Currently no, but you could edit `bot.py` to loop through a list of channel IDs.

**Q: What if I want alerts on my phone?**
A: Use Discord's mobile app or enable push notifications.

**Q: Can I connect to paid APIs for more data?**
A: Yes! Update `scraper.py` to call APIs like SearchAPI Google Finance, AlphaVantage, or IEX Cloud.

**Q: Will these changes break anything?**
A: No—test locally first, then push. If something breaks, you can roll back via GitHub.

---

**Need help?** Check [DEPLOYMENT.md](DEPLOYMENT.md) for troubleshooting. 🚀
