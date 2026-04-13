"""
Utility functions for formatting and styling Discord embeds
RiskTakerZ Branding: "SA + PSYCHO // SOUND" aesthetic
"""

import discord


def create_news_embed(title: str, description: str, url: str = None, image_url: str = None) -> discord.Embed:
    """
    Create a stylized Discord embed for news articles with RiskTakerZ branding
    
    Args:
        title: The title of the article
        description: The article summary or content
        url: Optional URL to the article
        image_url: Optional image URL for the embed
        
    Returns:
        A formatted Discord Embed object
    """
    embed = discord.Embed(
        title=f"📰 {title}",
        description=description,
        color=discord.Color.from_rgb(255, 0, 0),  # Red for high impact
        url=url
    )
    
    if image_url:
        embed.set_image(url=image_url)
    
    embed.set_footer(text="RiskTakerZ News Bot | High Impact Only 🔴")
    
    return embed


def create_economic_event_embed(event_name: str, time: str, impact: str, forecast: str = None) -> discord.Embed:
    """
    Create a stylized Discord embed for economic calendar events
    RED folder events only
    
    Args:
        event_name: Name of the economic event
        time: When the event occurs
        impact: The expected impact level (High, Medium, Low)
        forecast: Optional forecast value
        
    Returns:
        A formatted Discord Embed object
    """
    # Impact emoji mapping
    impact_config = {
        "High": {"color": discord.Color.from_rgb(255, 0, 0), "emoji": "🔴"},
        "Medium": {"color": discord.Color.from_rgb(255, 165, 0), "emoji": "🟠"},
        "Low": {"color": discord.Color.from_rgb(0, 128, 0), "emoji": "🟢"}
    }
    
    config = impact_config.get(impact, {"color": discord.Color.blue(), "emoji": "🔵"})
    
    embed = discord.Embed(
        title=f"{config['emoji']} {event_name}",
        color=config["color"],
        description=f"⏰ **Time:** {time}\n📊 **Impact:** {impact}"
    )
    
    if forecast:
        embed.add_field(name="📈 Forecast", value=forecast, inline=False)
    
    embed.set_footer(text="RiskTakerZ | NQ Volatility Focus")
    
    return embed


def create_daily_bias_embed() -> discord.Embed:
    """
    Create a daily sentiment poll embed for pre-market bias
    
    Returns:
        A formatted Discord Embed object for the daily bias poll
    """
    embed = discord.Embed(
        title="🚀 What's your bias before the open?",
        description=(
            "Cast your vote on today's market direction.\n\n"
            "📈 = Bullish\n"
            "📉 = Bearish\n"
            "↔️ = Neutral/Choppy"
        ),
        color=discord.Color.from_rgb(255, 0, 0)
    )
    
    embed.add_field(
        name="💭 Context",
        value="React below with your conviction. Results visible after close.",
        inline=False
    )
    
    embed.set_footer(text="RiskTakerZ Daily Bias | PSYCHO // SOUND 🎚️")
    embed.set_thumbnail(url="https://images.unsplash.com/photo-1516573541612-4a0ec3b7eeab?w=60&h=60")
    
    return embed


def create_breaking_news_embed(title: str, url: str, source: str) -> discord.Embed:
    """
    Create a breaking news alert embed
    
    Args:
        title: The news headline
        url: Link to the full article
        source: News source (e.g., Reuters, Bloomberg, Google News)
        
    Returns:
        A formatted Discord Embed object for breaking news
    """
    embed = discord.Embed(
        title=title,
        color=discord.Color.from_rgb(255, 0, 0),  # Bright red for breaking
        url=url,
        description=f"**Source:** {source}"
    )
    
    embed.set_footer(text="RiskTakerZ | Real-Time Market Intelligence")
    
    return embed


def truncate_text(text: str, max_length: int = 2000) -> str:
    """
    Truncate text to Discord's message length limit
    
    Args:
        text: The text to truncate
        max_length: Maximum allowed length (default Discord limit is 2000)
        
    Returns:
        Truncated text with ellipsis if necessary
    """
    if len(text) > max_length:
        return text[:max_length - 3] + "..."
    return text


def format_market_status(market: str, status: str, price: float = None) -> str:
    """
    Format market status for display
    
    Args:
        market: Market name (e.g., "NQ", "ES", "GC")
        status: Status (e.g., "OPEN", "CLOSED", "HALTED")
        price: Optional current price
        
    Returns:
        Formatted status string with emoji
    """
    status_emoji = {
        "OPEN": "🟢",
        "CLOSED": "🔴",
        "HALTED": "⚠️"
    }
    
    emoji = status_emoji.get(status, "❓")
    price_str = f"@ ${price:.2f}" if price else ""
    
    return f"{emoji} **{market}** {status} {price_str}"
