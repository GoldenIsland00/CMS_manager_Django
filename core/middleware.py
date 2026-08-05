THEME_COOKIE_NAME = "theme"
DEFAULT_THEME = "light"
VALID_THEMES = {"light", "dark"}


class ThemeMiddleware:
    """
    Reads the visitor's preferred theme (dark/light) from a cookie and
    attaches it to the request so templates and views can use it.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        theme = request.COOKIES.get(THEME_COOKIE_NAME, DEFAULT_THEME)
        if theme not in VALID_THEMES:
            theme = DEFAULT_THEME
        request.theme = theme
        return self.get_response(request)
