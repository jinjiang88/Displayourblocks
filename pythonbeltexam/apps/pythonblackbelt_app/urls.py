from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^main$', views.index),
    url(r'^reg$', views.reg),
    url(r'^travels$', views.travels),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^add$', views.add),
    url(r'^addplan$', views.addplan),
    url(r'^destination(?P<Trip_id>\d+)$', views.destination),
]
