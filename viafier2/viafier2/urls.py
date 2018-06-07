"""viafier2 URL Configuration
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse
from django.urls import include
from django.urls import path

urlpatterns = [
    path('', include('common.urls')),
    path('admin/', admin.site.urls),
    path('inventory/', include('inventory.urls')),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('robots.txt', lambda r: HttpResponse("User-agent: *\nDisallow: /",
                                              content_type="text/plain")),
    path('taggit/', include('taggit_selectize.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns + static(settings.MEDIA_URL,
                             document_root=settings.MEDIA_ROOT)
