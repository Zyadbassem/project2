from django.urls import path
from . import views
urlpatterns = [
    path("sign/",views.sign, name="sign"),
    path("register/", views.register, name="register"),
    path('home/', views.home, name="home"),
    path('logout/', views.logout, name="logout"),
    path('add/', views.addItems, name='addItems'),
    path('home/<str:clickedItemTitle>/', views.itemPage, name='itemPage'),
]