from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url('^$', views.welcome, name = 'welcome'),
    url('^home/', views.home, name = 'home'),
    url('^accounts/profile/', views.user_profile, name = 'user_profile'),
    url(r'^search/', views.search_results, name='search_results'),
    url(r'^image/(\d+)',views.image, name ='image'),
    url(r'^new/image$',views.new_image, name ='new_image'),
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)


