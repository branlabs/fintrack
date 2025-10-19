from django.urls import path, include
from api.v1.views import category_list, category_detail

urlpatterns = [
    path('category/list/', category_list, name='category-list'),
    path('category/<int:pk>', category_detail, name='category-detail'),
]