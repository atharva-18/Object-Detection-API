from django.conf import settings
from django.views.static import serve

urlpatterns = [
    url(r'^detect_image/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    }),
]