from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static

# This function tells Django to render your index.html file
def home_view(request):
    return render(request, 'index.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('contact/', include('contact.urls')),  # Contact form API
    path('', home_view, name='home'),
]

# Let Django automatically serve static files from STATIC_URL in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
