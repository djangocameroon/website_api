from django.utils import translation
from django.utils.deprecation import MiddlewareMixin


class APILanguageMiddleware(MiddlewareMixin):
    """
    Middleware to set the language for the current request based on the 'Accept-Language' or custom header.
    """

    def process_request(self, request):
        lang_code = request.headers.get('Accept-Language')

        if lang_code:
            lang_code = lang_code.split(',')[0].strip()

        if lang_code and translation.check_for_language(lang_code):
            translation.activate(lang_code)
            request.LANGUAGE_CODE = lang_code
        else:
            translation.activate(translation.get_language())

    def process_response(self, request, response):
        response['Content-Language'] = translation.get_language()
        translation.deactivate()
        return response
