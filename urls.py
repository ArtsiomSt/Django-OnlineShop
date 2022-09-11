from django.contrib import admin
from django.urls import path, include, re_path
from tgQA.views import *
from glpage.views import catAPI

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('glpage.urls')),
    path('api/v1/questions/', Createtgq.as_view()),
    path('api/v1/getcategories/', catAPI.as_view()),
    path('api/v1/questions/<str:username>', Createtgq.as_view()),
    path('api/v1/auth', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]
