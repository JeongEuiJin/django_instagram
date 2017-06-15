from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login/$',views.login, name='login'),
    rul(r'^logout/$',views.logout, name='logout')
]