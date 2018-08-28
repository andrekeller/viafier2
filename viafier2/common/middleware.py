from django.conf import settings
from django.utils import translation
from django.middleware.common import MiddlewareMixin

class ForceLanguageMiddleware(MiddlewareMixin):

    def process_request(self, request):
        request.LANG = settings.LANGUAGE_CODE
        translation.activate(request.LANG)
        request.LANGUATE_CODE = request.LANG
