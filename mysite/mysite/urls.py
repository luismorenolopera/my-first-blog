from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^accounts/logout/$',
        'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'', include('blog.urls')),
]
