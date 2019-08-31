"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from django.views.generic import RedirectView
from detect_image.views import detect, yolo_detect_api
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('detect/', detect),
    path('', RedirectView.as_view(url='detect/')),
    path('detect/api/', yolo_detect_api),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
