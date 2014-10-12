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
	url(r'^gtd_get_json_by_id/', views.gtd_get_json_by_id, name='gtd_get_json_by_id'),
	url(r'^gtd_post_kanban_update/', views.gtd_post_kanban_update, name='gtd_post_kanban_update'),
	url(r'^gtd_get_json_ticket_owner_by_id/', views.gtd_get_json_ticket_owner_by_id, name='gtd_get_json_ticket_owner_by_id'),
	url(r'^gtd_update_json_ticket_owner/', views.gtd_update_json_ticket_owner, name='gtd_update_json_ticket_owner'),
	url(r'^gtd_update_json_ticket/', views.gtd_update_json_ticket, name='gtd_update_json_ticket'),
	url(r'^tindakan_kanban_populate/', views.tindakan_kanban_populate, name='tindakan_kanban_populate'),
		)
