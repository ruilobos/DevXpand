from django.conf.urls import url
from django.contrib.auth.views import LoginView, LogoutView
from devxpand.accounts import views

app_name="accounts"

urlpatterns = [
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^login/$', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^edit/$', views.edit, name='edit'),
    url(r'^edit-password/$', views.edit_password, name='edit_password'),
    url(r'^reset-password/$', views.password_reset, name='password_reset'),
    url(r'^confirm-new-password/(?P<key>\w+)/$', views.password_reset_confirm, name='password_reset_confirm'),
]