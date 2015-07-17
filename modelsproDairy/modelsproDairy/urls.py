#from django.conf.urls import patterns, include, url
#from django.contrib import admin

#urlpatterns = patterns('',
#    # Examples:
#    # url(r'^$', 'modelspro.views.home', name='home'),
#    # url(r'^blog/', include('blog.urls')),
#
#    url(r'^admin/', include(admin.site.urls)),
#)
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
urlpatterns = patterns('',
    (r'^', include('modelsapp.urls')),
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


