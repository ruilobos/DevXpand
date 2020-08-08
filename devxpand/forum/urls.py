from django.conf.urls import url
from devxpand.forum import views

app_name="forum"
app_name="details"

urlpatterns = [
    url(r'^$',views.index, name='index'),
    url(r'^tag/(?P<tag>[\w_-]+)/$',views.index, name='index_tagged'),
    url(r'^answers/(?P<pk>\d+)/correct/$',views.reply_correct, name='reply_correct'),
    url(r'^answers/(?P<pk>\d+)/incorrect/$',views.reply_incorrect, name='reply_incorrect'),
    url(r'^(?P<slug>[\w_-]+)/$',views.thread, name='thread'),
]