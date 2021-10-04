from django.contrib import admin

from .models import Reviews


class ReviewsAdmin(admin.ModelAdmin):
    pass


admin.site.register(Reviews, ReviewsAdmin)
