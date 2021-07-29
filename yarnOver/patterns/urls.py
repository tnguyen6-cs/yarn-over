from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    #path("<int:pid>", views.pattern, name = "pattern")
]