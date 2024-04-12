from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.index, name='index'),
    path('ajax_login/', views.ajax_login, name='ajax_login'),
    path('logout/', views.logout_view, name='logout'),
    path('sells/', views.sells, name='sells'),
    path('upload/', views.sells_upload, name='upload'),
    path('detail/<int:id>/', views.detail, name='detail'),
    path('jisan/', views.jisan, name='jisan'),
    path('apart/', views.apart, name='apart'),
    path('officetel/', views.officetel, name='officetel'),
    path('sanga/', views.sanga, name='sanga'),
    path('office/', views.office, name='office'),
    path('multi/', views.multi, name='multi'),
    path('store/', views.store, name='store'),
    path('land/', views.land, name='land'),
    path('delete_property/', views.delete_property, name='delete_property'),
    path('search/', views.search, name='search'),
    path('sell_update/<int:id>/', views.sell_update, name='sell_update'),
    path('robots.txt/', TemplateView.as_view(template_name="robots.txt", content_type='text/plain')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)