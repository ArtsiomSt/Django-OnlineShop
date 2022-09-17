from django.conf.urls.static import static
from django.urls import path, include, re_path
from .views import *
from django.conf import settings
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', cache_page(60*15)(HomePage), name = 'home'),
    path('about/', about),
    path('create/', create),
    path('order/<int:tovar_id>', order, name='order'),
    path('category/<int:category_id>/', TovarByCat.as_view(), name='category'),
    path('category/<slug:category_id>/',cache_page(60)(TovarByCat.as_view()), name='category'),
    path('tovar/<int:tovar_id>/', tovar_page, name='tovar'),
    path('packet', user_Packet, name='Packet'),
    path('registrate', register, name='registrate'),
    path('tgqa/', include('tgQA.urls')),
    path('orderingproc', orderingprocess, name='orderingproc'),
    path('loginbyapi/', loginbyapi, name='loginbyapi'),
    path('logoutbyapi/', logoutbyapi, name='logoutbyapi'),
    re_path(r'^study/(?P<number>[A-z][0-9]{3})/', study, name='study'),
    path('testofpag/', pagonationtest, name='pag'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

