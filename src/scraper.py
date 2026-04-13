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


def _clean_env_value(name: str) -> str | None:
    """Return a normalized env var value with surrounding quotes removed."""
    value = os.getenv(name)
    if value is None:
        return None

    cleaned = value.strip()
    if len(cleaned) >= 2 and cleaned[0] == cleaned[-1] and cleaned[0] in {'"', "'"}:
        cleaned = cleaned[1:-1].strip()

    return cleaned or None


def _to_float(value: str | None) -> float | None:
    """Convert API string values into floats when possible."""
    if value in (None, "", "None"):
        return None

    try:
        return float(str(value).replace(",", ""))
    except (TypeError, ValueError):
        return None


def get_market_snapshot() -> List[Dict]:
    """
    Fetch a small pre-market snapshot using SearchAPI Google Finance.

    Environment:
        SEARCHAPI_API_KEY: API key for SearchAPI
        MARKET_SYMBOLS: Optional comma-separated watchlist

    Returns:
        List of symbol snapshots with price and change data
    """
    api_key = _clean_env_value("SEARCHAPI_API_KEY")
    if not api_key or api_key == "your_searchapi_api_key_here":
        return []

    raw_symbols = _clean_env_value("MARKET_SYMBOLS") or "QQQ:NYSEARCA,SPY:NYSEARCA,VIX:INDEXCBOE,TLT:NASDAQ"
    symbols = [symbol.strip().upper() for symbol in raw_symbols.split(",") if symbol.strip()]
    snapshot = []

    for raw_symbol in symbols:
        try:
            response = requests.get(
                "https://www.searchapi.io/api/v1/search",
                params={"engine": "google_finance", "q": raw_symbol, "hl": "en", "api_key": api_key},
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()

            if data.get("error"):
                print(f"Market data error for {raw_symbol}: {data.get('message', 'unknown error')}")
                continue

            summary = data.get("summary") or {}
            price_change = summary.get("price_change") or {}
            price = _to_float(summary.get("price"))
            change = _to_float(price_change.get("amount"))
            percent_change = _to_float(price_change.get("percentage"))

            if price is None:
                continue

            symbol = raw_symbol.split(":", 1)[0]
            snapshot.append(
                {
                    "symbol": symbol,
                    "name": summary.get("title", symbol),
                    "price": price,
                    "change": change,
                    "percent_change": percent_change,
                }
            )
        except requests.exceptions.RequestException as e:
            print(f"Market data request failed for {raw_symbol}: {e}")
        except Exception as e:
            print(f"Unexpected market data error for {raw_symbol}: {e}")

    return snapshot


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
    Fetch breaking news from SearchAPI Google News when configured,
    otherwise fall back to Google News RSS.
    
    Returns:
        List of breaking news headlines matching keywords
    """
    searchapi_key = _clean_env_value("SEARCHAPI_API_KEY")
    if searchapi_key and searchapi_key != "your_searchapi_api_key_here":
        try:
            response = requests.get(
                "https://www.searchapi.io/api/v1/search",
                params={
                    "engine": "google_news",
                    "q": "Nasdaq futures OR Fed OR Powell OR CPI OR NFP OR earnings",
                    "location": "New York,United States",
                    "hl": "en",
                    "gl": "us",
                    "api_key": searchapi_key,
                },
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()
            results = data.get("organic_results", [])

            breaking = []
            for item in results[:5]:
                title = item.get("title", "").strip()
                link = item.get("link", "").strip()
                source = item.get("source", "SearchAPI Google News")

                if not title or not link:
                    continue

                breaking.append(
                    {
                        "title": title,
                        "link": link,
                        "source": source,
                        "timestamp": datetime.now(TIMEZONE),
                    }
                )

            if breaking:
                return breaking
        except requests.exceptions.RequestException as e:
            print(f"SearchAPI news request failed: {e}")
        except Exception as e:
            print(f"SearchAPI news error: {e}")

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
