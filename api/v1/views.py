from rest_framework.response import Response
from rest_framework.decorators import api_view

from api.models import Category
from api.v1.serializers import CategorySerializer

@api_view(['GET', 'POST'])
def category_list(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.error)

@api_view(['GET', 'PUT', 'DELETE'])
def category_detail(request, pk):
    if request.method == 'GET':
        category = Category.objects.get(pk=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    
    if request.method == 'PUT':
        category = Category.objects.get(pk=pk)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    if request.method == 'DELETE':
        category = Category.objects.get(pk=pk)
        category.delete()
        return Response()

                      
