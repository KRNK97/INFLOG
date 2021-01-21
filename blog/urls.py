from django.contrib import admin
from django.urls import path, include

# configurations for using user uploaded files on dev server
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("blog_app.urls")),
]


# add urls if debug mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
