from django.conf.urls import url
from app import views


urlpatterns = [

    #initialize states database table
    url(r'^initialize', views.Initialize.as_view(), name="initialize"),
    #download states layer
    url(r'^getstates', views.GetStates.as_view(), name="getstates"),
    #addpoint to database
    url(r'^addpoint', views.AddPoint.as_view(), name="addpoint"),
    #download all points
    url(r'^allpoints', views.GetAllPoints.as_view(), name="getallpoints")

]
