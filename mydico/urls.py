from django.urls import path, include
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('', views.index, name='index'),
    path('history/', views.history, name='history'),
    path('search/', views.search, name='search'),
    path('favourite/', views.favourite, name='favourite'),
    path('setting/', views.setting, name='setting'),
    path('developer/', views.developer, name='developer'),
    path('help/', views.help, name='help'),
    path('about/', views.about, name='about'),
    path('pronounce/<str:wordSearch>/', views.pronunce, name='pronounce_word'),
]
