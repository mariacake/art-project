from django.urls import path
from arts.views import upload_artwork, gallery, contact, search
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', gallery, name='home'),
    path('upload/', upload_artwork, name='upload'),
    path('gallery/', gallery, name='gallery'),
    path('contact/', contact, name='contact'),
    path('search/', search, name='search')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
