from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'django_project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^api/getVolatility', 'kensoDataStore.views.display_volatility', name='cor_api'),
    url(r'^api/getData', 'kensoDataStore.views.get_data', name='raw_data'),
    url(r'^', 'kensoDataStore.views.temp_home', name="samp"),
)
