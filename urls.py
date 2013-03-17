from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^foo/$', 'views.home'),
    url(r'^foo/cookie/$', 'views.cookie'),
    url(r'^foo/set_cookie/$', 'views.set_cookie'),
    url(r'^foo/session_set/$', 'views.set_session'),
    url(r'^foo/session_get/$', 'views.get_session'),
    url(r'^foo/session_del/$', 'views.del_session'),
    url(r'^foo/seed/$', 'views.seed_task'),

    # Examples:
    # url(r'^$', 'hola.views.home', name='home'),
    # url(r'^hola/', include('hola.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
