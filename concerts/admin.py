from django.contrib import admin

from .models import Band, Event, FavoriteBand, Performance, Venue


@admin.register(Band)
class BandAdmin(admin.ModelAdmin):
    list_display = ("name", "genre", "website")
    search_fields = ("name", "genre")
    ordering = ("name",)


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "state", "country")
    list_filter = ("country", "state")
    search_fields = ("name", "address", "city")
    ordering = ("name", "city")


class PerformanceInline(admin.TabularInline):
    model = Performance
    extra = 1
    autocomplete_fields = ("band",)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("name", "venue", "date_time", "status", "submitted_by")
    list_filter = ("status", "date_time")
    list_select_related = ("venue", "submitted_by")
    search_fields = ("name", "venue__name", "venue__city")
    ordering = ("-date_time",)
    autocomplete_fields = ("venue", "submitted_by")
    readonly_fields = ("created_at",)
    inlines = (PerformanceInline,)


@admin.register(Performance)
class PerformanceAdmin(admin.ModelAdmin):
    list_display = ("band", "event", "set_time", "is_headliner")
    list_filter = ("is_headliner",)
    list_select_related = ("band", "event")
    search_fields = ("band__name", "event__name")
    autocomplete_fields = ("band", "event")


@admin.register(FavoriteBand)
class FavoriteBandAdmin(admin.ModelAdmin):
    list_display = ("user", "band")
    list_select_related = ("user", "band")
    search_fields = ("user__username", "band__name")
    autocomplete_fields = ("user", "band")
