# users/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_login, name='login'),  # Redirect users/ to login page
    path('login/', views.user_login, name='login'),  # Login page URL
    path('dashboard/', views.dashboard, name='dashboard'),  # Dashboard page URL
    path('logout/', views.user_logout, name='logout'),  # Logout page URL
    path('start/', views.start_work, name='start_work'),
    path('stop/', views.stop_work, name='stop_work'),
    path('test-log/', views.test_logging, name='test_log'),
    path('register/', views.register, name='register'),
    path('people/', views.people_view, name='people'),
    path('contact/', views.contact_view, name='contact'),
]

#path('', views.user_login, name='login'),  # Redirect users/ to login page