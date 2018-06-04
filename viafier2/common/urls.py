from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from common.views import IndexView

app_name = 'common'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', IndexView.as_view(), name='home'),
]
