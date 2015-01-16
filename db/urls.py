from django.conf.urls import patterns, include, url
from db.views import *

urlpatterns = patterns('',
    url(r'^all/$',articles),                                                  # to view topics in discussion topic
    url(r'^get/(?P<article_id>\d+)/$',article),                                          # for viewing individual article
    url(r'^language/(?P<language>[a-z\-]+)/$',language), 
    url(r'^create/$',create,name="create"),                                             # for creating a topic in discussion forum
    url(r'^add/(?P<article_id>\d+)/$',add_comment),                                                     # for adding comments for topics
    url(r'^search/$',search_titles),                            # for searching topics in discussion forum
    url(r'^mytop/$',my_articles),                                   # for viewing topics made by himself
    url(r'^pop/$',pop_articles),                                    # for viewing  popular topics 
    url(r'^del/(?P<article_id>\d+)/$',del_article),                 # for deleting a topic
    url(r'^multiupvote/$',multiupvote),                             # if upvoted multiple times
    url(r'^usr/(?P<uname>[a-z]+)/$',user_articles),


    url(r'^polls/$',polls),                                         # to view all polls 
    url(r'^view/(?P<poll_id>\d+)/$',poll),                          # to view result of a particular poll
    url(r'^cpoll/$',cpoll),                                               # to create a poll
    url(r'^spolls/$',search_polls),     
    url(r'^mypolls/$',my_polls),                            # to view polls created by himself
    url(r'^ppolls/$',pop_polls),                            # to view popular polls
    url(r'^clr/(?P<poll_id>\d+)/$',del_poll),               # to delete a poll
    url(r'^multivote/$',multivote),                         # if vote mulltiple times
    url(r'^ur/(?P<unam>[a-z]+)/$',user_polls),


)