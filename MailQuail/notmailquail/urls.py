from django.conf.urls import patterns, include, url

import notmailquail.views
import notmailquail.android_views

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^$', "notmailquail.views.index", name='index'), 
    url(r'^login/$', "notmailquail.views.login_request", name="login_request"),
    url(r'^gmail_login_request/$', "notmailquail.views.test_auth", name="gmail_login_request"),
#    url(r'^test/$', "notmailquail.views.testmail", name="testmail"),
    url(r'^test/$', "notmailquail.views.save", name="save"),
    url(r'^logout/$', "notmailquail.views.logout_request", name="logout_request"),
    url(r'^logback/$', "notmailquail.views.logback_request", name="logback_request"),
    url(r'^change/$', "notmailquail.views.change", name="change"),
    url(r'^archive/$', "notmailquail.views.archive", name="archive"),
    url(r'^a_login/$', "notmailquail.android_views.a_login", name="a_login"),
    url(r'^a_accounts/$', "notmailquail.android_views.a_accounts", name="a_accounts"),
    url(r'^a_mail/$', "notmailquail.android_views.a_mail", name="a_mail"),
    url(r'^search/$', "notmailquail.views.search", name="search"),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url('', include('django.contrib.auth.urls', namespace='auth'))
)

#urlpatterns = patterns('',
    # Examples: 
    # url(r'^$', 'notmailquail.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

 #   url(r'^admin/', include(admin.site.urls)) , url(r'^$', views.index, name='index'),
#)