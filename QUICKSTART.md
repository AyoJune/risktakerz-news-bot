# ⚡ QUICKSTART (5 Minutes)

Get the RiskTakerZ News Bot running on Railway in 5 minutes.

---

## Step 1: Get Discord Bot Token (2 min)

1. Go to https://discord.com/developers/applications
2. Click **New Application** → Name it "RiskTakerZ"
3. Go to **Bot** → Click **Add Bot**
4. Copy the **TOKEN** (click Copy button)
5. Save it somewhere safe

---

## Step 2: Get Channel ID (1 min)

1. In Discord, enable **Developer Mode** (Settings → Advanced → Developer Mode)
2. Right-click your alerts channel → **Copy Channel ID**
3. Save it

---

## Step 3: Push to GitHub (1 min)

```bash
# In your project folder (PowerShell/Terminal):
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/risktakerz-news-bot.git
git push -u origin main
```

---

## Step 4: Deploy to Railway (1 min)

1. Go to https://railway.app
2. Click **New Project** → **Deploy from GitHub**
3. Select your `risktakerz-news-bot` repo
4. Railway auto-detects and builds ✅
5. Click **Variables** tab
6. Add these two variables:
   - `DISCORD_TOKEN` = your token from Step 1
   - `ALERTS_CHANNEL_ID` = your channel ID from Step 2
7. **Done!** 🚀 Bot is now running

---

## Step 5: Test It

In Discord, type:
- `!ping` → Should see latency response ✅
- `!alerts` → Should see economic events
- `!test_breaking` → Should see sample news alert

---

## 🎯 What It Does

| Time | Alert |
|------|-------|
| 6:00 AM PST | High-impact economic events |
| 6:15 AM PST | Daily bias poll |
| Every 10 min | Breaking news (Fed, earnings, etc.) |

---

## 📚 Full Docs

- [README.md](README.md) - Project overview
- [DEPLOYMENT.md](DEPLOYMENT.md) - Detailed setup & troubleshooting
- [CONFIG.md](CONFIG.md) - Customize keywords, times, channels

---

## ⚠️ Important

- **Never share** your `DISCORD_TOKEN`
- **Don't commit** `.env` file (already blocked in `.gitignore`)
- **Test locally** before deploying (use `python main.py`)

---

## 🆘 If It Doesn't Work

1. Check Railway **Logs** tab for errors
2. Verify `DISCORD_TOKEN` and `ALERTS_CHANNEL_ID` in Railway Variables
3. Make sure bot has permissions in the Discord channel
4. See [DEPLOYMENT.md](DEPLOYMENT.md) troubleshooting section

---

**That's it!** Your bot is live. 🔴📈
