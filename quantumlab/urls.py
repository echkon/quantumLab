# quantumlab/urls.py
from django.contrib import admin
from django.urls import path, include
from users import views  # Import the views from the users app

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),  # Include users app URLs
    path('', views.home, name='home'),  # Root path for home page
    path('login/', views.user_login, name='login'),  # Login page URL
    path('people/', views.people, name='people'),  # people.html
]