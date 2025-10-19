from django.shortcuts import render
from api.models import Category
from django.http import JsonResponse

def catagory_list(request):
    catagory = Category.objects.all()
    data = {
        'catagory': list(catagory.values())
    }
    print(data)
    return JsonResponse(data)