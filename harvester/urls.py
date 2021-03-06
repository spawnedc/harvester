from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
import dbindexer
dbindexer.autodiscover() #This needs to happen before anything else, hence strange import ordering

urlpatterns = patterns('harvester.views',
    url(r'^$', 'home', name='home'),
    url(r'^settings/', 'settings', name='settings'),
    # Examples:
    # url(r'^$', 'harvester.views.home', name='home'),
    # url(r'^harvester/', include('harvester.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
