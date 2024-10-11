import requests
import asyncio
import aiohttp
import time
import json
import feedparser
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Feed, FeedItem, Base

engine = create_engine("mysql+pymysql://myuser:mypassword@mysql/mydatabase")
Session = sessionmaker(bind=engine)

async def fetch_feed(session, feed_url):
    """Fetch a single feed asynchronously and handle different content types"""
    async with session.get(feed_url) as response:
        content_type = response.headers.get('Content-Type', '').lower()

        if 'application/json' in content_type:
            data = await response.json()
            entries = []
            if isinstance(data, dict):
                domains = data.get('domains', [])
                for domain in domains:
                    entries.append({
                        'title': domain.get('domain'),
                        'description': f"Created: {domain.get('create_date')}, Updated: {domain.get('update_date')}",
                        'link': domain.get('domain')
                    })
            return entries
        elif 'application/rss+xml' in content_type or 'application/xml' in content_type or 'text/xml' in content_type:
            feed_data = await response.text()
            parsed_feed = feedparser.parse(feed_data)
            return parsed_feed.entries
        else:
            print(f"Unsupported content type: {content_type}")
            return None
        
async def update_feed(feed_id, feed_url):
    """Update a single feed and store the items in the database asynchronously"""
    async with aiohttp.ClientSession() as session:
        try:
            entries = await fetch_feed(session, feed_url)
            if not entries:
                print(f"No entries found in the feed {feed_url}", flush=True)
                return

            db_session = Session()
            for entry in entries:
                feed_item = FeedItem(
                    title=entry.get('title'),
                    description=entry.get('description'),
                    link=entry.get('link'),
                    feed_id=feed_id
                )
                db_session.add(feed_item)

            db_session.commit()
            print(f"Feed {feed_url} updated successfully", flush=True)
        except Exception as e:
            print(f"Error updating feed {feed_url}: {e}", flush=True)
        finally:
            db_session.close()  

async def retry_update_feed(feed_id, feed_url, retries=3, delay=1):
    """Retry updating a feed with exponential back-off in case of failure"""
    for attempt in range(retries):
        try:
            await update_feed(feed_id, feed_url)
            return  
        except Exception as e:
            print(f"Attempt {attempt + 1} failed for {feed_url}: {e}")
            await asyncio.sleep(delay)
            delay *= 2  

    print(f"Failed to update feed {feed_url} after {retries} attempts")

def update_feed_sync(feed_id, feed_url):
    """Update a single feed and store the items in the database synchronously"""
    try:
        response = requests.get(feed_url)
        response.raise_for_status()  
        feed_data = response.content
        parsed_feed = feedparser.parse(feed_data)

        db_session = Session()
        for entry in parsed_feed.entries:
            feed_item = FeedItem(
                title=entry.title,
                description=entry.description,
                link=entry.link,
                feed_id=feed_id
            )
            db_session.add(feed_item)
        db_session.commit()

    except Exception as e:
        print(f"Error fetching {feed_url}: {e}")

async def update_all_feeds():
    """Update all feeds in the database asynchronously with back-off"""
    db_session = Session()
    feeds = db_session.query(Feed).all()
    db_session.close()

    tasks = []
    try:
        for feed in feeds:
            task = retry_update_feed(feed.id,feed.url)
            tasks.append(task)
    except Exception as e:
        print(f"Error updating feeds: {e}",flush=True)
    try:
        await asyncio.gather(*tasks)
    except Exception as e:
        print(f"Error gathering tasks : {e}",flush=True)

def update_all_feeds_sync():
    """Update all feeds in the database synchronously with no back-off"""
    db_session = Session()
    feeds = db_session.query(Feed).all()

    for feed in feeds:
        update_feed_sync(feed.id, feed.url)

def fetch_feed_updates():
    """Entry point for triggering feed updates, blocking call"""
    asyncio.run(update_all_feeds())
    
def fetch_feed_updates_sync():
    """Entry point for triggering feed updates, blocking call (synchronous version)"""
    update_all_feeds_sync()

# Retry mechanism 
async def retry_update_feed(feed_id, feed_url, retries=3, delay=1):
    for attempt in range(retries):
        try:
            await update_feed(feed_id, feed_url)
            break
        except Exception as e:
            print(f"Attempt {attempt + 1} failed for {feed_url}, retrying...",flush=True)
            await asyncio.sleep(delay)
            delay *= 2  