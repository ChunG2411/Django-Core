from django.utils.deprecation import MiddlewareMixin


class AcceptRangesMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        response['Accept-Ranges'] = 'bytes'
        return response