from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'MDlogger'
urlpatterns = [
    path ('', views.index, name='index'),
    path ('logout', views.logout_request, name='logout'),
    path ('associate_home', views.associate_home, name='associate_home'),
    path ('lp_entry', views.lp_entry, name='lp_entry'),
    path ('sku_entry', views.sku_entry, name='sku_entry'),
    path ('add_repair', views.add_repair, name='add_repair'),
 ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)




