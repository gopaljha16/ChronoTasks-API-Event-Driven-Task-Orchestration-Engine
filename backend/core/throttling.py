from rest_framework.throttling import UserRateThrottle


class BurstRateThrottle(UserRateThrottle):
    """
    Throttle for burst requests (short time window)
    """
    scope = 'burst'


class TaskCreateThrottle(UserRateThrottle):
    """
    Custom throttle for task creation
    """
    rate = '100/hour'
    
    def allow_request(self, request, view):
        if request.method != 'POST':
            return True
        return super().allow_request(request, view)
