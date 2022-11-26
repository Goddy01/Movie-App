from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('sign-in/', views.sign_in, name='sign_in')
]