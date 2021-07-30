from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("<int:pattern_id>", views.pattern, name = "pattern"),
    path("categories", views.categories, name = "categories"),
    path("categories/<int:cate_id>", views.category, name="category")
]