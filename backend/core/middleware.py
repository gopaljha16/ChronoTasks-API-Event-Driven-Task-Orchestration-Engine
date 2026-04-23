import time
import logging
from django.db import connection
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger('performance')


class QueryCountDebugMiddleware(MiddlewareMixin):
    """
    Middleware to log database query count and execution time
    """
    def process_request(self, request):
        request.start_time = time.time()
        request.query_count_start = len(connection.queries)
    
    def process_response(self, request, response):
        if hasattr(request, 'start_time'):
            # Calculate request duration
            duration = time.time() - request.start_time
            
            # Calculate query count
            query_count = len(connection.queries) - request.query_count_start
            
            # Log if duration is significant or query count is high
            if duration > 1.0 or query_count > 10:
                logger.warning(
                    f"Slow request: {request.method} {request.path} "
                    f"Duration: {duration:.2f}s Queries: {query_count}"
                )
            
            # Add headers for debugging
            response['X-Query-Count'] = str(query_count)
            response['X-Response-Time'] = f"{duration:.3f}s"
        
        return response


class CacheHeaderMiddleware(MiddlewareMixin):
    """
    Middleware to add cache-related headers
    """
    def process_response(self, request, response):
        # Add cache control headers for API responses
        if request.path.startswith('/api/'):
            if request.method == 'GET':
                response['Cache-Control'] = 'private, max-age=300'
            else:
                response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        
        return response
