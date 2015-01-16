from django.conf.urls import patterns, include, url
# from django.contrib.auth.views import login, logout
# from views import *
from views import *
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

	# course and material urls
	(r'^courseselection/$', courseselection_view),
	(r'^courseselection/submit/$', course_selected_submit_view),
	(r'^courses/$', courses_view),
	(r'^coursematerial/$', coursematerial_view),
	(r'^material_details/$', material_details_view),
	(r'^upload_material/$', upload_material_view),
	#url(r'^download/$', download_view),
	
	# calendar urls
	(r'^calendar/', include('django_bootstrap_calendar.urls')),
	(r'^add_event/$', add_event_view),
	(r'^edit_event/event_details/$', edit_event_details_view),
	(r'^edit_event/update/$', edit_event_update_view),
	#(r'^get_events/$', get_events_view),
	(r'^edit_event/$', edit_event_view),
	(r'^remove_event/$', remove_event_view),
	(r'^remove_event/event_delete/$', delete_event_view),
	
	# user field modification urls
	(r'^changepassword/$', changepasswordpage_view),
	(r'^changepassword/auth/$', changepassword_view),
	(r'^changepassword/successfull/$', changepassword_successfull_view),
	
	# sending the mail in forgot password
	(r'^sendmail/$',  sendmail_view),
	
	# help urls
	(r'^loginpage/contact_us/$',  contact_us2_view),
	(r'^help/$',  contact_us1_view),
	(r'^documentation/$',  documentation_view),

    # user auth urls
    (r'^loginpage/$',  loginpage_view),
    (r'^accounts/login/$',  login_view),
    (r'^accounts/auth/$',  auth_view),
    (r'^home/$',  loggedin_view),
    (r'^accounts/invalid/$',  invalid_login_view),
    (r'^accounts/logout/$', logout_view),
    (r'^loggedout/$', loggedout_view),
	(r'^forgotpassword/$', forgotpassword_view),
	(r'^onlinemanual/$', onlinemanual_view),
	
	url(r'^attendance/', include('attendance.urls')),
	url(r'^discussion/', discussion_view),
	url(r'^polls/', polls_view),
	url(r'^app/', include('db.urls')),
	
    # Examples:
    # url(r'^$', 'cms.views.home', name='home'),
    # url(r'^cms/', include('cms.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
