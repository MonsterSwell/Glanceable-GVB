from django.conf.urls.defaults import *

urlpatterns = patterns('govi.views',
    (r'^$', 'index'),
    (r'^pick/$', 'pick'),
    
    # Pass through method, parses XML and returns JSON
    (r'^dris/(?P<halteid>\d+)/$', 'dris'),
    
    # API methods, currently not used
    (r'^haltes/(?P<halteid>\d+)/$', 'halte'),
    (r'^haltes/$', 'haltes'),
    
    # (r'^conversations/(?P<cid>\d+)/$', 'conversation'),
    #    (r'^conversations/(?P<cid>\d+)/say/$', 'conversation_say'),
    #    (r'^conversations/(?P<cid>\d+)/say/thanks/$', 'conversation_say_thanks'),
    #    (r'^conversations/(?P<cid>\d+)/lastlineid/', 'conversation_lastlineid')
    
    # (r'^unit/(?P<slug>\w.+?)/$', 'unit_detail'),
)

urlpatterns += patterns('',
    (r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'essence/login.html'}),
    (r'^logout/$', 'django.contrib.auth.views.logout'),
    
    (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/static/images/favicon.ico'}),
)