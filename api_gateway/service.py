from nameko.rpc import RpcProxy
from nameko.web.handlers import http
from werkzeug.wrappers import Response
import json

class APIGateway:
    name = "api_gateway"

    auth_service = RpcProxy("auth_service")
    feed_service = RpcProxy("feed_service")

    @http('POST', '/register')
    def register(self, request):
        """Register a new user"""
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        result = self.auth_service.register(username, password)
        return Response(json.dumps(result), status=200, mimetype='application/json')

    @http('POST', '/login')
    def login(self, request):
        """Login a user and return a JWT token"""
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        result = self.auth_service.login(username, password)
        return Response(json.dumps(result), status=200, mimetype='application/json')

    @http('GET', '/feeds')
    def list_feeds(self, request):
        """List all feeds for a logged-in user"""
        token = request.headers.get('Authorization')
        if not token:
            return Response(json.dumps({"message": "Unauthorized"}), status=401, mimetype='application/json')

        result = self.feed_service.list_feeds(token)
        return Response(json.dumps(result), status=200, mimetype='application/json')

    @http('POST', '/feeds')
    def follow_feed(self, request):
        """Allow a user to follow a new feed"""
        token = request.headers.get('Authorization')
        if not token:
            return Response(json.dumps({"message": "Unauthorized"}), status=401, mimetype='application/json')

        data = request.get_json()
        feed_url = data.get('feed_url')
        result = self.feed_service.follow_feed(token, feed_url)
        return Response(json.dumps(result), status=200, mimetype='application/json')

    @http('POST', '/bookmarks')
    def add_bookmark(self, request):
        """Add a bookmark for a feed item"""
        token = request.headers.get('Authorization')
        if not token:
            return Response(json.dumps({"message": "Unauthorized"}), status=401, mimetype='application/json')

        data = request.get_json()
        feed_item_id = data.get('feed_item_id')
        result = self.feed_service.add_bookmark(token, feed_item_id)
        return Response(json.dumps(result), status=200, mimetype='application/json')

    @http('GET', '/bookmarks')
    def list_bookmarks(self, request):
        """List all bookmarks for a user"""
        token = request.headers.get('Authorization')
        if not token:
            return Response(json.dumps({"message": "Unauthorized"}), status=401, mimetype='application/json')

        result = self.feed_service.list_bookmarks(token)
        return Response(json.dumps(result), status=200, mimetype='application/json')

    @http('POST', '/feeds/update')
    def update_feeds(self, request):
        """Trigger feed update (async or sync based on payload)"""
        data = request.get_json()
        asynchronous = data.get("asynchronous", True)

        result = self.feed_service.update_feeds(asynchronous)
        return Response(json.dumps(result), status=200, mimetype='application/json')