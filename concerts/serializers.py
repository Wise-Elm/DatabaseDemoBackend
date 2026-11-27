from rest_framework import serializers

from .models import Band, Event, FavoriteBand, Performance, Venue


class BandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Band
        fields = ("id", "name", "genre", "website")


class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = ("id", "name", "address", "city", "state", "country")


class PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = ("id", "band", "set_time", "is_headliner")

    def create(self, validated_data):
        band = validated_data.pop("band")
        event = validated_data.pop("event")
        performance, created = Performance.objects.get_or_create(
            event=event,
            band=band,
            defaults=validated_data,
        )
        if not created:
            raise serializers.ValidationError(
                {"band": "This band is already on the event lineup."}
            )
        return performance


class EventSerializer(serializers.ModelSerializer):
    performances = PerformanceSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = (
            "id",
            "name",
            "venue",
            "date_time",
            "status",
            "submitted_by",
            "ticket_url",
            "created_at",
            "performances",
        )
        read_only_fields = ("submitted_by", "created_at")


class FavoriteBandSerializer(serializers.ModelSerializer):
    band_name = serializers.CharField(source="band.name", read_only=True)

    class Meta:
        model = FavoriteBand
        fields = ("id", "band", "band_name")

    def validate_band(self, band):
        request = self.context["request"]
        if FavoriteBand.objects.filter(user=request.user, band=band).exists():
            raise serializers.ValidationError("You already follow this band.")
        return band
