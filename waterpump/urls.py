from django.urls import path
from . import views

app_name = 'waterpump'

urlpatterns = [
	path('', views.index, name='index'),
	path('node/<int:node_id>/', views.nodePage, name='nodePage'),
	path('<int:node_id>/', views.contentPage, name='contentPage'),
]
