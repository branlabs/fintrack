from django.urls import path, include
from api.views import catagory_list

urlpatterns = [
    path('catagory/list/', catagory_list, name='catagory-list'),
]