"""dzmo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from accounts import urls as accounts_urls

from lessons import urls as lessons_urls
from problems import urls as problems_urls
from control import urls as control_urls
from control.views import MainPage
from tests import urls as tests_urls
from tasks import urls as tasks_urls
urlpatterns = [
    path('', MainPage.as_view(), name ='main'),
    path('problems/', include(problems_urls)),
    path('lessons/', include(lessons_urls)),
    path('accounts/', include(accounts_urls)),
    path('control/', include(control_urls)),
    path('tasks/', include(tasks_urls)),
    path('tests/', include(tests_urls)),
    path('admin/', admin.site.urls),
    #path('', include('django.contrib.auth.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
