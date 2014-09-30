# Create your views here.
from django.conf.urls import patterns, url
from main import views

urlpatterns = patterns('',

	url(r'^$', views.index, name='index'),
	url(r'^closed/', views.closed, name='closed'),
	url(r'^login/', views.user_login, name='login'),
	url(r'^logout/', views.user_logout, name='logout'),
	url(r'^tindakan/', views.tindakan, name='tindakan'),
	url(r'^perangkat/', views.perangkat, name='perangkat'),
	url(r'^hapus_perangkat/', views.hapus_perangkat, name='hapus_perangkat'),
	url(r'^hapus_tindakan/', views.hapus_tindakan, name='hapus_tindakan'),
	url(r'^perangkat_detail/', views.perangkat_detail, name='perangkat_detail'),
	url(r'^perangkat_update/', views.perangkat_update, name='perangkat_update'),
	url(r'^tindakan_detail/', views.tindakan_detail, name='tindakan_detail'),
	url(r'^tindakan_status/', views.tindakan_status, name='tindakan_status'),
	url(r'^gtd_get_json/', views.gtd_get_json, name='gtd_get_json'),

		)
