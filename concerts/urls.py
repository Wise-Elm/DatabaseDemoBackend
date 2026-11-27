from rest_framework.routers import DefaultRouter

from .views import BandViewSet, EventViewSet, FavoriteBandViewSet, VenueViewSet

router = DefaultRouter()
router.register("bands", BandViewSet)
router.register("venues", VenueViewSet)
router.register("events", EventViewSet)
router.register("favorites", FavoriteBandViewSet, basename="favorite")

urlpatterns = router.urls
