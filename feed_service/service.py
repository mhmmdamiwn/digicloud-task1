from nameko.rpc import rpc, RpcProxy
from nameko_sqlalchemy import DatabaseSession
from models import Base, Feed, FeedItem, Bookmark
from scraper import fetch_feed_updates,fetch_feed_updates_sync
from sqlalchemy import create_engine

class FeedService:
    name = "feed_service"

    db = DatabaseSession(Base)
    auth_service = RpcProxy("auth_service")  

    def __init__(self):
        engine = create_engine("mysql+pymysql://myuser:mypassword@mysql/mydatabase")
        Base.metadata.create_all(engine)

    @rpc
    def follow_feed(self, token, feed_url):
        """Allow users to follow a new feed"""
        user_id = self._verify_user(token)
        if not user_id:
            return {"message": "Unauthorized"}

        feed = Feed(url=feed_url, user_id=user_id)
        self.db.add(feed)
        self.db.commit()
        return {"message": "Feed followed successfully"}

    @rpc
    def list_feeds(self, token):
        """List all feeds followed by the user"""
        user_id = self._verify_user(token)
        if not user_id:
            return {"message": "Unauthorized"}

        feeds = self.db.query(Feed).filter_by(user_id=user_id).all()
        return [{"id": feed.id, "url": feed.url} for feed in feeds]

    @rpc
    def add_bookmark(self, token, feed_item_id):
        """Allow users to bookmark a feed item"""
        user_id = self._verify_user(token)
        if not user_id:
            return {"message": "Unauthorized"}

        bookmark = Bookmark(user_id=user_id, feed_item_id=feed_item_id)
        self.db.add(bookmark)
        self.db.commit()
        return {"message": "Feed item bookmarked"}

    @rpc
    def list_bookmarks(self, token):
        """List all bookmarks for a user"""
        user_id = self._verify_user(token)
        if not user_id:
            return {"message": "Unauthorized"}

        bookmarks = self.db.query(Bookmark).filter_by(user_id=user_id).all()
        return [{"id": bookmark.id, "feed_item": bookmark.feed_item.title} for bookmark in bookmarks]

    @rpc
    def update_feeds(self,asynchronous = True):
        """Trigger the asynchronous feed update process"""
        if asynchronous:
            fetch_feed_updates()
            return {"message": "Feed updates triggered"}
        # For testing purposes
        else :
            fetch_feed_updates_sync()
            return {"message": "Feed updates triggered synchronously"}
    
    def _verify_user(self, token):
        """Call the Auth Service to verify the token and return the user_id"""
        response = self.auth_service.verify_token(token)
        if "user_id" in response:
            return response["user_id"]
        return None