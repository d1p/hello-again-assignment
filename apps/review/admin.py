from django.contrib import admin

from apps.review.models import PlayStoreReview, ReviewURL
from apps.review.tasks import index_all_reviews


@admin.register(ReviewURL)
class ReviewURLAdmin(admin.ModelAdmin):
    list_display = ('url', 'site', 'created_at', 'updated_at')
    list_filter = ('site', 'created_at', 'updated_at')
    search_fields = ('url',)

    class Meta:
        fields = '__all__'

    # call the task to index all reviews on new review url creation
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if change:
            return
        index_all_reviews.delay(review_url_id=obj.id)


@admin.register(PlayStoreReview)
class PlayStoreReviewAdmin(admin.ModelAdmin):
    list_display = ('review_url', 'user_name', 'rating', 'review_text', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user_name', 'review_text')

    class Meta:
        fields = '__all__'
