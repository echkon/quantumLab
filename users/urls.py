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
    path('member/', views.member_view, name='member'),
    path('publication/', views.publication_view, name='publication'),
    path('visitor/', views.visitor_view, name='visitor'),
    path('contact/', views.contact_view, name='contact'),
    path('position/', views.position_view, name='position'),
    path('event/', views.event_view, name='event'),
    path('resource/', views.resource_view, name='resource'),
    path('me/', views.me_view, name='me'),
    path('upload/', views.upload_file, name='upload_file'),
]

#path('', views.user_login, name='login'),  # Redirect users/ to login page