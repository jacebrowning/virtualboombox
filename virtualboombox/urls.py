from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = [
    url(r'', include('player.urls')),
    url(r'^api/', include('api.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt',
                                                content_type='text/plain')),
]
