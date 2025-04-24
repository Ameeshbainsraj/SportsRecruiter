from django.contrib import admin
from django.urls import path, include
from home import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Admin panel URL
    path('admin/', admin.site.urls),

    # Include URLs from your 'home' app
    path('', include('home.urls')),  # This includes all URLs from your home app



    # Search path (custom search view)
    path('search/', views.search, name='search'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
