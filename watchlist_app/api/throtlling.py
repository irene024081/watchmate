from rest_framework.throttling import UserRateThrottle

class ReviewListThrottle(UserRateThrottle):
    scope = 'review_list'




