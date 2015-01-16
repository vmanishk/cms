from django.conf.urls import patterns, include, url
# from django.contrib.auth.views import login, logout
#from views import login_view, logout_view, auth_view, loggedin, invalid_login, loggedout_view, loginpage_view
# Uncomment the next two lines to enable the admin:
from django.contrib import admin


admin.autodiscover()
from views import *


urlpatterns = patterns('',

    # user attendence

    url(r'^$',  attendence_view),
    url(r'^subjectselected/$',  subjectselected_view),
    url(r'^takeattendance/$',  takeattendance_view),
    url(r'^takenewattendance/$',  takenewattendance_view),
    url(r'^attendanceteacher/$',  attendanceteacher_view),
    url(r'^attendancelist/$',  attendancelist_view),
    url(r'^succesful/$',  succesful_view),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
