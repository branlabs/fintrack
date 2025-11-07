from django.contrib import admin

# Register your models here.
from api.models import Category, Transaction, User

# Register your models here
admin.site.register(Category)
admin.site.register(Transaction)
admin.site.register(User)