# api/views.py

from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Avg, Count, Q
from .models import Wine
from .serializers import WineSerializer
from django_filters.rest_framework import DjangoFilterBackend

class WineViewSet(viewsets.ModelViewSet):
    queryset = Wine.objects.all().order_by('id')
    serializer_class = WineSerializer
    
    # ADD THIS LINE:
    filter_backends = [DjangoFilterBackend]
    
    # Enable filtering, searching, ordering (for browsable API and marks)
    filterset_fields = ['type', 'quality']
    search_fields = ['type']
    ordering_fields = ['alcohol', 'quality', 'pH']

    # Interesting custom endpoint 1: High quality wines (quality >= 7)
    @action(detail=False, methods=['get'])
    def high_quality(self, request):
        high = self.get_queryset().filter(quality__gte=7)
        page = self.paginate_queryset(high)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    # Interesting custom endpoint 2: Average stats by type
    @action(detail=False, methods=['get'])
    def stats_by_type(self, request):
        stats = Wine.objects.values('type').annotate(
            avg_quality=Avg('quality'),
            avg_alcohol=Avg('alcohol'),
            count=Count('id')
        )
        return Response(stats)

    # Interesting custom endpoint 3: Wines with high alcohol and low acidity
    @action(detail=False, methods=['get'])
    def premium(self, request):
        premium_wines = self.get_queryset().filter(
            alcohol__gte=11,
            volatile_acidity__lte=0.4
        ).order_by('-quality')
        page = self.paginate_queryset(premium_wines)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    # POST is already included via ModelViewSet (create method)