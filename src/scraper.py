"""
Logic for scraping news, economic calendars, and other data sources

Strategy: "High Impact Only" - Focus on RED events that move markets
USD and Nasdaq volatility events only
"""

import requests
from bs4 import BeautifulSoup
import os
from typing import List, Dict
from datetime import datetime
import pytz

TIMEZONE = pytz.timezone("US/Pacific")


def get_economic_calendar() -> List[Dict]:
    """
    Scrapes high-impact events from Investing.com for the current day.
    Focus: USD / Nasdaq impact (3-star events only).
    
    Returns:
        List of high-impact economic events
    """
    url = "https://www.investing.com/economic-calendar/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        events = []
        # Find the economic calendar table
        table = soup.find('table', {'id': 'economicCalendarData'})
        
        if not table:
            print("Could not find calendar table - structure may have changed")
            return []
        
        rows = table.find_all('tr', class_='js-event-item')
        
        for row in rows:
            try:
                # Check for 3-star (red/high) impact
                impact_td = row.find('td', class_='sentiment')
                if not impact_td:
                    continue
                
                # Look for high impact indicators (3 bulls or red stars)
                impact_icons = impact_td.find_all('i', class_=lambda x: x and 'BullishIcon' in x)
                
                # Only process if 3 stars (high impact)
                if len(impact_icons) != 3:
                    continue
                
                time_td = row.find('td', class_='time')
                event_td = row.find('td', class_='event')
                country_td = row.find('td', class_='country')
                
                if not all([time_td, event_td]):
                    continue
                
                time_text = time_td.text.strip()
                event_name = event_td.text.strip()
                country = country_td.text.strip() if country_td else "N/A"
                
                # Filter for USD and major volatility events
                if 'USD' in country or any(keyword in event_name.upper() for keyword in 
                    ['NFP', 'FOMC', 'CPI', 'INFLATION', 'EMPLOYMENT', 'GDP', 'FED']):
                    events.append({
                        "time": time_text,
                        "event": event_name,
                        "country": country,
                        "impact": "🔴 HIGH"
                    })
            except Exception as e:
                print(f"Error parsing row: {e}")
                continue
        
        return events[:5]  # Return top 5 high-impact events
        
    except requests.exceptions.RequestException as e:
        print(f"Scraper Error fetching calendar: {e}")
        return []
    except Exception as e:
        print(f"Scraper Error: {e}")
        return []


def fetch_news_from_api(api_key: str) -> List[Dict]:
    """
    Fetch high-impact news articles from NewsAPI
    
    Args:
        api_key: API key for NewsAPI
        
    Returns:
        List of relevant news articles
    """
    try:
        url = "https://newsapi.org/v2/everything"
        params = {
            "q": "USD OR NASDAQ OR volatility OR market OR Fed OR inflation",
            "sortBy": "publishedAt",
            "apiKey": api_key,
            "pageSize": 5,
            "language": "en"
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json().get("articles", [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news: {e}")
        return []


def get_breaking_news() -> List[Dict]:
    """
    Scrapes breaking news from Google News RSS feed.
    Filters for Nasdaq/Tech volatility keywords.
    Much faster than HTML scraping - uses RSS feed.
    
    Returns:
        List of breaking news headlines matching keywords
    """
    url = "https://news.google.com/rss/search?q=Nasdaq+futures+breaking+news&tbs=qdr:h12"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    # Keywords that trigger a post (market movers)
    keywords = ['Fed', 'Powell', 'Earnings', 'Inflation', 'NFP', 'Halt', 'China', 'Tech']
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse XML/RSS feed
        soup = BeautifulSoup(response.content, 'xml')
        items = soup.find_all('item')
        
        breaking = []
        
        for item in items[:5]:  # Check first 5 items
            try:
                title_tag = item.find('title')
                link_tag = item.find('link')
                
                if not title_tag or not link_tag:
                    continue
                
                title = title_tag.get_text().strip()
                link = link_tag.get_text().strip()
                
                # Check if title contains any high-impact keywords
                if any(keyword.lower() in title.lower() for keyword in keywords):
                    breaking.append({
                        "title": title,
                        "link": link,
                        "source": "Google News",
                        "timestamp": datetime.now(TIMEZONE)
                    })
            except Exception as e:
                print(f"Error parsing news item: {e}")
                continue
        
        return breaking
        
    except Exception as e:
        print(f"Breaking News Error: {e}")
        return []


def parse_html(url: str) -> str:
    """
    Parse HTML from a given URL
    
    Args:
        url: The URL to scrape
        
    Returns:
        Parsed text content
    """
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup.get_text()
    except requests.exceptions.RequestException as e:
        print(f"Error parsing HTML: {e}")
        return ""
