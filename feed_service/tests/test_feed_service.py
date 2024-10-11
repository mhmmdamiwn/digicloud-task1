import pytest
from service import FeedService  
from unittest.mock import Mock

@pytest.fixture
def feed_service():
    return FeedService()

def test_fetch_feed(feed_service, mocker):
    mock_response = Mock()
    mock_response.status = 200
    mock_response.text = "<rss><channel><title>Test Feed</title></channel></rss>"
    mocker.patch('aiohttp.ClientSession.get', return_value=mock_response)

    feed = feed_service.fetch_feed("https://api.domainsdb.info/v1/domains/search?domain=facebook")
    assert feed['title'] == "Test Feed"  

def test_fetch_feed_invalid_url(feed_service, mocker):
    mock_response = Mock()
    mock_response.status = 404
    mocker.patch('aiohttp.ClientSession.get', return_value=mock_response)

    feed = feed_service.fetch_feed("https://invalid-url.com/rss")
    assert feed is None  

def test_update_feed(feed_service, mocker):
    mocker.patch('feed_service.FeedService.fetch_feed', return_value={"title": "Updated Feed"})
    result = feed_service.update_feed("https://api.domainsdb.info/v1/domains/search?domain=facebook")
    assert result is True  

def test_update_feed_failure(feed_service, mocker):
    mocker.patch('feed_service.FeedService.fetch_feed', return_value=None)
    result = feed_service.update_feed("https://invalid-url.com/rss")
    assert result is False 
