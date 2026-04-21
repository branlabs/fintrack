from datetime import date
from calendar import monthrange

from django.db.models import Sum, Case, When, Value, IntegerField
from django.db.models.functions import ExtractDay, ExtractMonth, ExtractYear
from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from api.models import Category, Transaction, User
from api.v1.serializers import CategorySerializer, TransactionSerializer, UserSerializer


@api_view(['GET','POST'])
def user_list(request):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])
def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)
    if request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        user.delete()
        return Response()

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
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'GET':
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    
    if request.method == 'PUT':
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        category.delete()
        return Response()


                      
# ---- TRANSACTION CRUD ----
@api_view(['GET', 'POST'])
def transaction_list(request):
    if request.method == 'GET':
        # Lọc theo month/year optional: /api/transaction/list/?month=11&year=2025&category=3
        qs = Transaction.objects.all().select_related('category')
        category_id = request.query_params.get('category')
        if category_id:
            qs = qs.filter(category_id=category_id)

        month = request.query_params.get('month')
        year = request.query_params.get('year')
        if year:
            qs = qs.filter(occurred_on__year=year)
        if month:
            qs = qs.filter(occurred_on__month=month)

        serializer = TransactionSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    else:  # POST
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            return Response(TransactionSerializer(obj).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def transaction_detail(request, pk):
    tx = get_object_or_404(Transaction, pk=pk)

    if request.method == 'GET':
        return Response(TransactionSerializer(tx).data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = TransactionSerializer(tx, data=request.data, partial=False)
        if serializer.is_valid():
            tx = serializer.save()
            return Response(TransactionSerializer(tx).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    else:  # DELETE
        tx.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ---- Tổng hợp: ngày / tuần / tháng / năm (lọc theo category & user) ----
@api_view(['GET'])
def transaction_summary(request):
    """
    /api/transaction/summary/?group=day&month=11&year=2025
    /api/transaction/summary/?group=week&month=11&year=2025
    /api/transaction/summary/?group=month&year=2025
    /api/transaction/summary/?group=year&year=2025

    Tuỳ chọn lọc:
      - ?category=3         hoặc ?category=2,5,7
      - ?user=4             hoặc ?user=1,2
    """
    group = request.query_params.get('group')  # 'day' | 'week' | 'month' | 'year'
    if group not in ('day', 'week', 'month', 'year'):
        return Response({'detail': 'group must be one of: day, week, month, year'},
                        status=status.HTTP_400_BAD_REQUEST)

    qs = Transaction.objects.all()

    def parse_id_list(raw):
        if not raw:
            return []
        ids = []
        for p in str(raw).split(','):
            p = p.strip()
            if not p:
                continue
            try:
                ids.append(int(p))
            except ValueError:
                pass
        return ids

    # Lọc category (1 hoặc nhiều id)
    category_ids = parse_id_list(request.query_params.get('category'))
    if category_ids:
        qs = qs.filter(category_id__in=category_ids)

    # Lọc user (1 hoặc nhiều id)
    user_ids = parse_id_list(request.query_params.get('user'))
    if user_ids:
        qs = qs.filter(user_id__in=user_ids)

    # ---- GROUP = DAY ----
    if group == 'day':
        year = request.query_params.get('year')
        month = request.query_params.get('month')
        if not (year and month):
            return Response({'detail': 'day summary requires year and month'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            year = int(year)
        except (TypeError, ValueError):
            return Response({'detail': 'invalid year'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            month = int(month)
        except (TypeError, ValueError):
            return Response({'detail': 'invalid month'}, status=status.HTTP_400_BAD_REQUEST)
        if month < 1 or month > 12:
            return Response({'detail': 'invalid month'}, status=status.HTTP_400_BAD_REQUEST)
        days_in_month = monthrange(year, month)[1]

        rows = (qs.filter(occurred_on__year=year, occurred_on__month=month)
                  .annotate(d=ExtractDay('occurred_on'))
                  .values('d')
                  .annotate(total=Sum('amount'))
                  .values('d', 'total'))

        result = {d: '0.00' for d in range(1, days_in_month + 1)}
        for r in rows:
            result[int(r['d'])] = str(r['total'] or 0)

        return Response({
            'group': 'day',
            'year': year,
            'month': month,
            'filters': {'category': category_ids or None, 'user': user_ids or None},
            'data': [{'day': d, 'total': result[d]} for d in range(1, days_in_month + 1)]
        }, status=status.HTTP_200_OK)

    # ---- GROUP = WEEK ----
    if group == 'week':
        year = request.query_params.get('year')
        month = request.query_params.get('month')
        if not (year and month):
            return Response({'detail': 'week summary requires year and month'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            year = int(year)
        except (TypeError, ValueError):
            return Response({'detail': 'invalid year'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            month = int(month)
        except (TypeError, ValueError):
            return Response({'detail': 'invalid month'}, status=status.HTTP_400_BAD_REQUEST)
        if month < 1 or month > 12:
            return Response({'detail': 'invalid month'}, status=status.HTTP_400_BAD_REQUEST)

        qs2 = qs.filter(occurred_on__year=year, occurred_on__month=month).annotate(day=ExtractDay('occurred_on'))
        week_bucket = Case(
            When(day__lte=7, then=Value(1)),
            When(day__lte=14, then=Value(2)),
            When(day__lte=21, then=Value(3)),
            default=Value(4),
            output_field=IntegerField()
        )
        rows = (qs2.annotate(week=week_bucket)
                    .values('week')
                    .annotate(total=Sum('amount'))
                    .values('week', 'total'))

        result = {1: '0.00', 2: '0.00', 3: '0.00', 4: '0.00'}
        for r in rows:
            result[int(r['week'])] = str(r['total'] or 0)

        return Response({
            'group': 'week',
            'year': year,
            'month': month,
            'filters': {'category': category_ids or None, 'user': user_ids or None},
            'data': [
                {'week': 1, 'total': result[1]},
                {'week': 2, 'total': result[2]},
                {'week': 3, 'total': result[3]},
                {'week': 4, 'total': result[4]},
            ]
        }, status=status.HTTP_200_OK)

    # ---- GROUP = MONTH ----
    if group == 'month':
        year = request.query_params.get('year')
        if not year:
            return Response({'detail': 'month summary requires year'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            year = int(year)
        except (TypeError, ValueError):
            return Response({'detail': 'invalid year'}, status=status.HTTP_400_BAD_REQUEST)

        rows = (qs.filter(occurred_on__year=year)
                  .annotate(m=ExtractMonth('occurred_on'))
                  .values('m')
                  .annotate(total=Sum('amount'))
                  .values('m', 'total'))

        result = {m: '0.00' for m in range(1, 13)}
        for r in rows:
            result[int(r['m'])] = str(r['total'] or 0)

        return Response({
            'group': 'month',
            'year': year,
            'filters': {'category': category_ids or None, 'user': user_ids or None},
            'data': [{'month': m, 'total': result[m]} for m in range(1, 13)]
        }, status=status.HTTP_200_OK)

    # ---- GROUP = YEAR ----
    if group == 'year':
        center_year = request.query_params.get('year')
        if not center_year:
            return Response({'detail': 'year summary requires year'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            center_year = int(center_year)
        except (TypeError, ValueError):
            return Response({'detail': 'invalid year'}, status=status.HTTP_400_BAD_REQUEST)
        years = [center_year - 1, center_year, center_year + 1]

        rows = (qs.filter(occurred_on__year__in=years)
                  .annotate(y=ExtractYear('occurred_on'))
                  .values('y')
                  .annotate(total=Sum('amount'))
                  .values('y', 'total'))

        result = {y: '0.00' for y in years}
        for r in rows:
            result[int(r['y'])] = str(r['total'] or 0)

        return Response({
            'group': 'year',
            'years': years,
            'filters': {'category': category_ids or None, 'user': user_ids or None},
            'data': [{'year': y, 'total': result[y]} for y in years]
        }, status=status.HTTP_200_OK)
