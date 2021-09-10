from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from control.views import MainPage

urlpatterns = [
    path('', MainPage.as_view(), name ='main'),
    path('problems/', include('problems.urls')),
    path('lessons/', include('lessons.urls')),
    path('accounts/', include('accounts.urls')),
    path('control/', include('control.urls')),
    path('tasks/', include('tasks.urls')),
    path('tests/', include('tests.urls')),
    path('admin/', admin.site.urls),
    #path('', include('django.contrib.auth.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)