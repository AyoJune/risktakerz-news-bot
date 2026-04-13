"""
Main Discord bot client and event handling
RiskTakerZ News Bot - High Impact Market Alerts
"""

import discord
from discord.ext import commands, tasks
import os
from dotenv import load_dotenv
from datetime import datetime, time
import pytz
from src.scraper import get_economic_calendar, get_breaking_news
from src.utils import create_economic_event_embed, create_daily_bias_embed, create_breaking_news_embed

# Load environment variables
load_dotenv()


def _env_to_bool(name: str, default: str = "false") -> bool:
    """Parse common truthy env var values."""
    return os.getenv(name, default).strip().lower() in {"1", "true", "yes", "on"}


def _clean_env_value(name: str) -> str | None:
    """Return a normalized env var value with surrounding quotes removed."""
    value = os.getenv(name)
    if value is None:
        return None

    cleaned = value.strip()
    if len(cleaned) >= 2 and cleaned[0] == cleaned[-1] and cleaned[0] in {'"', "'"}:
        cleaned = cleaned[1:-1].strip()

    return cleaned or None

# Create bot instance
intents = discord.Intents.default()
ENABLE_MESSAGE_CONTENT_INTENT = _env_to_bool("ENABLE_MESSAGE_CONTENT_INTENT", "false")
BOT_PREFIX = os.getenv("BOT_PREFIX", "!")
intents.message_content = ENABLE_MESSAGE_CONTENT_INTENT
bot = commands.Bot(command_prefix=BOT_PREFIX, intents=intents)

# Configuration
try:
    ALERTS_CHANNEL_ID = int(os.getenv("ALERTS_CHANNEL_ID", "0"))
except ValueError:
    print("⚠️  WARNING: ALERTS_CHANNEL_ID must be a number. Using 0 (disabled).")
    ALERTS_CHANNEL_ID = 0

TIMEZONE = pytz.timezone("US/Pacific")


@bot.event
async def on_ready():
    """Called when the bot successfully connects to Discord"""
    print(f"✅ {bot.user} has connected to Discord!")
    print(f"📍 Ready to send market alerts.")
    if not ENABLE_MESSAGE_CONTENT_INTENT:
        print("ℹ️ Message content intent is disabled. Prefix commands are disabled.")
        print("ℹ️ Set ENABLE_MESSAGE_CONTENT_INTENT=true and enable it in Discord Portal to use !commands.")
    
    # Set bot status
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="NQ Futures 📈 | Analyzing Liquidity"
        )
    )
    
    # Start background tasks
    if not morning_prep.is_running():
        morning_prep.start()
    if not daily_bias_poll.is_running():
        daily_bias_poll.start()
    if not breaking_news_monitor.is_running():
        breaking_news_monitor.start()
    
    print("🔄 Background tasks started")
    print("------")


@bot.event
async def on_message(message):
    """Handle incoming messages"""
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return
    
    # Process commands
    await bot.process_commands(message)


@tasks.loop(hours=24)
async def morning_prep():
    """
    Daily task: Sends pre-market alert at 6:00 AM PST (9:00 AM EST)
    with high-impact economic events for the day
    """
    # Check if it's the right time (6:00 AM PST)
    now = datetime.now(TIMEZONE)
    target_time = time(6, 0)  # 6:00 AM
    
    # Only run if within the target hour
    if now.hour != target_time.hour or now.minute > 5:
        return
    
    # Get the alerts channel
    if ALERTS_CHANNEL_ID == 0:
        print("⚠️ ALERTS_CHANNEL_ID not configured in .env")
        return
    
    channel = bot.get_channel(ALERTS_CHANNEL_ID)
    if not channel:
        print(f"⚠️ Could not find alerts channel with ID: {ALERTS_CHANNEL_ID}")
        return
    
    try:
        # Fetch high-impact events
        events = get_economic_calendar()
        
        if not events:
            print("📊 No high-impact events found for today")
            return
        
        # Create main alert embed
        embed = discord.Embed(
            title="🎯 PRE-MARKET CATALYSTS",
            description="High-impact data dropping today. Know your levels.",
            color=discord.Color.red()
        )
        
        for event in events:
            embed.add_field(
                name=f"⏰ {event['time']}",
                value=f"**{event['event']}** ({event['country']})\n{event['impact']}",
                inline=False
            )
        
        embed.set_footer(text="RiskTakerZ News Bot | NQ Futures Focused")
        
        # Send alert
        await channel.send(
            content="**@everyone** Markets open in 30 mins. Red folder alerts incoming 🔴",
            embed=embed
        )
        print("✅ Morning prep alert sent")
        
    except Exception as e:
        print(f"❌ Error in morning_prep: {e}")


@morning_prep.before_loop
async def before_morning_prep():
    """Ensure bot is ready before running the task"""
    await bot.wait_until_ready()


@tasks.loop(hours=24)
async def daily_bias_poll():
    """
    Daily task: Posts a "Daily Bias" poll 15 minutes after market open
    to gauge bullish/bearish sentiment
    """
    now = datetime.now(TIMEZONE)
    target_time = time(6, 15)  # 6:15 AM PST (30 mins after morning prep)
    
    if now.hour != target_time.hour or now.minute > 20:
        return
    
    if ALERTS_CHANNEL_ID == 0:
        return
    
    channel = bot.get_channel(ALERTS_CHANNEL_ID)
    if not channel:
        return
    
    try:
        embed = create_daily_bias_embed()
        
        poll_message = await channel.send(
            content="**📊 Daily Bias Poll - Show your conviction!**",
            embed=embed
        )
        
        # Add reaction options
        await poll_message.add_reaction("📈")  # Bullish
        await poll_message.add_reaction("📉")  # Bearish
        await poll_message.add_reaction("↔️")   # Neutral
        
        print("✅ Daily bias poll posted")
        
    except Exception as e:
        print(f"❌ Error in daily_bias_poll: {e}")


@daily_bias_poll.before_loop
async def before_daily_bias_poll():
    """Ensure bot is ready before running the task"""
    await bot.wait_until_ready()


@tasks.loop(minutes=10)
async def breaking_news_monitor():
    """
    Background task: Checks for breaking news every 10 minutes
    during market hours (6:00 AM - 4:00 PM EST / 3:00 AM - 1:00 PM PST)
    """
    if ALERTS_CHANNEL_ID == 0:
        return
    
    channel = bot.get_channel(ALERTS_CHANNEL_ID)
    if not channel:
        return
    
    # Check if we're in market hours (PST)
    now = datetime.now(TIMEZONE)
    market_start = time(3, 0)  # 3:00 AM PST
    market_end = time(13, 0)   # 1:00 PM PST (after hours)
    
    if not (market_start <= now.time() <= market_end):
        return  # Skip outside market hours
    
    try:
        news = get_breaking_news()
        
        if not news:
            return  # No breaking news
        
        for article in news:
            # Create and send breaking news embed
            embed = create_breaking_news_embed(
                title=article["title"],
                url=article["link"],
                source=article["source"]
            )
            
            await channel.send(
                content="🚨 **BREAKING NEWS ALERT**",
                embed=embed
            )
            print(f"✅ Breaking news posted: {article['title'][:50]}...")
        
    except Exception as e:
        print(f"❌ Error in breaking_news_monitor: {e}")


@breaking_news_monitor.before_loop
async def before_breaking_news_monitor():
    """Ensure bot is ready before running the task"""
    await bot.wait_until_ready()


@bot.command(name="ping")
async def ping(ctx):
    """Simple ping command to test if bot is responsive"""
    await ctx.send(f"🏓 Pong! {round(bot.latency * 1000)}ms")


@bot.command(name="alerts")
async def alerts_command(ctx):
    """Manually trigger the pre-market alerts"""
    await morning_prep()
    await ctx.send("✅ Manual alert triggered!")


@bot.command(name="bias")
async def bias_command(ctx):
    """Manually trigger the daily bias poll"""
    await daily_bias_poll()
    await ctx.send("✅ Bias poll triggered!")


@bot.command(name="test_event")
async def test_event(ctx):
    """Test command to display a sample high-impact event"""
    from src.utils import create_economic_event_embed
    embed = create_economic_event_embed(
        event_name="Non-Farm Payroll (NFP)",
        time="8:30 AM EST",
        impact="High",
        forecast="Expected: 250K | Previous: 220K"
    )
    await ctx.send(embed=embed)


@bot.command(name="test_breaking")
async def test_breaking(ctx):
    """Test command to display a sample breaking news alert"""
    embed = create_breaking_news_embed(
        title="Fed Chair Powell Signals Potential Rate Cut in June",
        url="https://example.com/news",
        source="Reuters"
    )
    await ctx.send(content="🚨 **BREAKING NEWS ALERT**", embed=embed)


def run():
    """Start the bot with the Discord token from environment variables"""
    token = _clean_env_value("DISCORD_TOKEN")
    if not token or token == "your_token_here":
        raise ValueError("DISCORD_TOKEN not found in environment variables")

    try:
        bot.run(token)
    except discord.errors.LoginFailure as exc:
        raise ValueError(
            "Discord login failed. Check that DISCORD_TOKEN is the current bot token from the Discord Developer Portal and does not include stale or copied credentials."
        ) from exc
