class EnsureTokenPrefixMiddleware:
    """
    Middleware to ensure the Authorization header includes the 'Token' prefix.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if auth_header and not auth_header.startswith('Token '):
            request.META['HTTP_AUTHORIZATION'] = f'Token {auth_header}'
        return self.get_response(request)