from django.conf.urls import url
from courses import views

app_name="courses"
app_name="details"

urlpatterns = [
    url(r'^$',views.index, name='index'),
    url(r'^(?P<slug>[\w_-]+)/$',views.details, name='details'),
    url(r'^(?P<slug>[\w_-]+)/subscription/$',views.enrollment, name='enrollment'),
    url(r'^(?P<slug>[\w_-]+)/announcements/$',views.announcements, name='announcements'),
    url(r'^(?P<slug>[\w_-]+)/announcements/(?P<pk>\d+)/$',views.show_announcement, name='show_announcement'),
    url(r'^(?P<slug>[\w_-]+)/cancel-subscription/$',views.undo_enrollment, name='undo_enrollment'),
    url(r'^(?P<slug>[\w_-]+)/lectures/$',views.lessons, name='lessons'),
    url(r'^(?P<slug>[\w_-]+)/lectures/(?P<pk>\d+)/$',views.lesson, name='lesson'),
    url(r'^(?P<slug>[\w_-]+)/resources/(?P<pk>\d+)/$',views.material, name='material'),
]