from rest_framework.response import Response
from rest_framework.decorators import api_view


from api.models import Category
from api.v1.serializers import CategorySerializer

@api_view()
def category_list(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)

@api_view()
def category_detail(request, pk):
    category = Category.objects.get(pk=pk)
    serializer = CategorySerializer(category)
    return Response(serializer.data)