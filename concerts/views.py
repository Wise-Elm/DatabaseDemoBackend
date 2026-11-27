from django.db.models.deletion import ProtectedError
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Band, Event, Venue
from .permissions import CanManageCatalog, CanManageEvent
from .serializers import (
    BandSerializer,
    EventSerializer,
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
