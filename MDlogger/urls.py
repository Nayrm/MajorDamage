from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
from django.contrib import admin
from .views import mark_project_complete

app_name = 'MDlogger'
urlpatterns = [
    path ('', views.index, name='index'),
    path ('admin/', admin.site.urls, name='admin'),
    path ('logout', views.logout_request, name='logout'),
    path ('associate_home', views.associate_home, name='associate_home'),
    path('mark_project_complete/<int:project_id>/', mark_project_complete, name='project_complete'),
    path ('lp_entry', views.lp_entry, name='lp_entry'),
    path ('sku_entry', views.sku_entry, name='sku_entry'),
    path ('add_repair', views.add_repair, name='add_repair'),
    path ('metrics', views.metrics, name='metrics'),
    path ('data', views.data, name='data'),
    path ('dashboard', views.dashboard, name='dashboard'),
    path ('projects', views.projects, name='projects'),
    
 ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)




