from django.urls import path

from authentication.views import signup_view

app_name = 'authentication'

urlpatterns = [
    path('signup', signup_view, name="signup"),
]