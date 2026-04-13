# 🚀 RiskTakerZ News Bot - Deployment Guide

Complete setup instructions for deploying to Railway.

---

## 📋 Pre-Deployment Checklist

### 1. **Local Testing** ✅
```bash
# Install dependencies
pip install -r requirements.txt

# Update your .env file with:
DISCORD_TOKEN=your_token_here
ALERTS_CHANNEL_ID=your_channel_id_here

# Run locally
python main.py
```

Test the bot works with:
- `!ping` - Should get latency response
- `!test_event` - Should show sample economic event
- `!test_breaking` - Should show sample breaking news alert

---

## 🔗 Discord Setup

### Get Your Discord Token
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" → Name it "RiskTakerZ News Bot"
3. Go to **Bot** section → Click "Add Bot"
4. Under **TOKEN**, click "Copy"
5. Paste into your `.env` file as `DISCORD_TOKEN`

### Get Your Alerts Channel ID
1. Enable Developer Mode in Discord (User Settings → Advanced → Developer Mode)
2. Right-click your alerts channel → "Copy Channel ID"
3. Paste into your `.env` file as `ALERTS_CHANNEL_ID`

### Set Bot Permissions
1. In Developer Portal, go to **OAuth2** → **URL Generator**
2. Select scopes: `bot`
3. Select permissions:
   - Send Messages
   - Embed Links
   - Add Reactions
   - Read Message History
4. Copy the generated URL and invite your bot to your server

---

## 🚂 Railway Deployment

### Step 1: Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit: RiskTakerZ News Bot"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/risktakerz-news-bot.git
git push -u origin main
```

### Step 2: Connect to Railway
1. Go to [Railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub"
3. Select your `risktakerz-news-bot` repository
4. Railway will auto-detect `requirements.txt` and `Procfile`

### Step 3: Add Environment Variables
1. In Railway dashboard, go to **Variables**
2. Add these variables manually (Railway doesn't read `.env` files):

```
DISCORD_TOKEN = your_discord_token_here
ALERTS_CHANNEL_ID = your_alerts_channel_id_here
NEWS_API_KEY = (optional)
```

⚠️ **DO NOT commit your `.env` file to GitHub** - It's already in `.gitignore`

### Step 4: Deploy
1. Railway auto-deploys on git push
2. Check the **Deployments** tab for status
3. View logs in the **Logs** tab

---

## ⏰ CRITICAL: Timezone Handling

Railway servers run on **UTC time**, not your local time. You must convert:

### PST to UTC Conversion
- **6:00 AM PST** (Market Open Prep) = **2:00 PM UTC**
- **6:15 AM PST** (Daily Bias Poll) = **2:15 PM UTC**

### Current Implementation
The bot uses `pytz` to handle timezone conversion automatically:
- All tasks use `TIMEZONE = pytz.timezone("US/Pacific")`
- The bot checks `datetime.now(TIMEZONE)` internally
- Railway's UTC environment is handled transparently

✅ **You don't need to change anything** - the code handles UTC→PST conversion automatically.

---

## 🔧 Background Tasks Schedule

| Task | Frequency | PST Time | What It Does |
|------|-----------|----------|---|
| `morning_prep` | Daily | 6:00 AM | Posts high-impact economic events |
| `daily_bias_poll` | Daily | 6:15 AM | Posts sentiment poll with reactions |
| `breaking_news_monitor` | Every 10 min | 3 AM - 1 PM | Scans Google News for breaking headlines |

**Market Hours Coverage:** 3:00 AM PST - 1:00 PM PST (24 hours including pre-market & post-market)

---

## 🧪 Commands for Testing

Once deployed, use these commands in Discord to verify functionality:

```
!ping                  # Test bot responsiveness
!test_event           # Display sample economic event
!test_breaking        # Display sample breaking news alert
!alerts               # Manually trigger pre-market alert
!bias                 # Manually trigger daily bias poll
```

---

## 🐛 Troubleshooting

### Bot Not Online
- Check **Logs** tab in Railway dashboard
- Verify `DISCORD_TOKEN` is correct and hasn't been regenerated
- Restart deployment: Click redeploy button

### Tasks Not Running
- Check if `ALERTS_CHANNEL_ID` is correct
- Verify bot has permission to send messages in that channel
- Check logs for errors

### Economic Calendar Returns No Events
- Investing.com site structure may have changed
- Check scraper logs for HTTP errors
- Try using `!alerts` command to manually trigger

### Breaking News Alerts Spam
- Adjust `keywords` list in `src/scraper.py` to be more restrictive
- Increase loop time from 10 minutes to 15-30 minutes

---

## 📊 Monitoring

### View Logs
Railway dashboard → **Logs** tab shows all print statements from your bot

### Check Status
- Go to Railway dashboard
- "Status" shows if bot is running
- Restart by clicking the deployment

### Scale Up (Optional)
- Railway allows you to increase compute resources
- Default free tier is sufficient for this bot

---

## 🔐 Security Notes

✅ **Never commit `.env` file** - Already in `.gitignore`

✅ **Regenerate token if leaked** - Discord Developer Portal → Bot → Reset Token

✅ **Use Railway Variables** - They're encrypted and never logged

---

## 📈 Next Steps

### Monitor Performance
- Run the bot for a week
- Check logs for errors
- Adjust keyword filters based on feedback

### Add Features
- Connect to paid news APIs for more sources
- Add sentiment analysis
- Create historical event database
- Add portfolio tracking

### Community
- Invite friends to your Discord
- Get feedback on alert timing & formatting
- Iterate on features

---

## 🆘 Need Help?

- **Discord Bot Issues**: Check [Discord.py Docs](https://discordpy.readthedocs.io/)
- **Railway Issues**: Check [Railway Docs](https://docs.railway.app/)
- **Code Issues**: Check logs and Python error messages

Good luck! 🚀
