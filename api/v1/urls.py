from django.urls import path
from api.v1.views import (
    category_list, category_detail,
    transaction_list, transaction_detail,
    transaction_summary, user_list, user_detail
)

urlpatterns = [
    # Category
    path('category/list/', category_list, name='category-list'),
    path('category/<int:pk>', category_detail, name='category-detail'),
    
    # Transaction CRUD
    path('transaction/list/', transaction_list, name='transaction-list'),
    path('transaction/<int:pk>/', transaction_detail, name='transaction-detail'),

    # Summary
    path('transaction/summary/', transaction_summary, name='transaction-summary'),

    # User
    path('user/list/', user_list, name='user-list'),
    path('user/<int:pk>', user_detail, name="user-detail"),
]