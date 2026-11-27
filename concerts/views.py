from django.db.models.deletion import ProtectedError
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Band, Event, FavoriteBand, Venue
from .permissions import CanManageCatalog, CanManageEvent
from .serializers import (
    BandSerializer,
    EventSerializer,
    FavoriteBandSerializer,
    PerformanceSerializer,
    VenueSerializer,
)


class CatalogViewSet(viewsets.ModelViewSet):
    permission_classes = (CanManageCatalog,)

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError:
            return Response(
                {"detail": "This record is in use and cannot be deleted."},
                status=status.HTTP_409_CONFLICT,
            )


class BandViewSet(CatalogViewSet):
    queryset = Band.objects.order_by("name", "pk")
    serializer_class = BandSerializer


class VenueViewSet(CatalogViewSet):
    queryset = Venue.objects.order_by("name", "pk")
    serializer_class = VenueSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.prefetch_related("performances").order_by("date_time", "pk")
    serializer_class = EventSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, CanManageEvent)

    def get_queryset(self):
        queryset = super().get_queryset()
        params = self.request.query_params
        if band := params.get("band"):
            queryset = queryset.filter(performances__band_id=band)
        if venue := params.get("venue"):
            queryset = queryset.filter(venue_id=venue)
        if city := params.get("city"):
            queryset = queryset.filter(venue__city__icontains=city)
        if date := params.get("date"):
            queryset = queryset.filter(date_time__date=date)
        if params.get("upcoming") == "true":
            queryset = queryset.filter(date_time__gte=timezone.now())
        return queryset.distinct()

    def perform_create(self, serializer):
        serializer.save(submitted_by=self.request.user)

    @action(
        detail=True,
        methods=["post"],
        serializer_class=PerformanceSerializer,
    )
    def performances(self, request, pk=None):
        event = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(event=event)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
        detail=False,
        methods=["get"],
        url_path="favorite-upcoming",
        permission_classes=[IsAuthenticated],
    )
    def favorite_upcoming(self, request):
        events = self.get_queryset().filter(
            date_time__gte=timezone.now(),
            performances__band__followers__user=request.user,
        ).distinct()
        return Response(self.get_serializer(events, many=True).data)


class FavoriteBandViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteBandSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ("get", "post", "delete", "head", "options")

    def get_queryset(self):
        return FavoriteBand.objects.filter(user=self.request.user).select_related("band")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
