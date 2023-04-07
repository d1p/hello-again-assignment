import pytest

from apps.review.models import ReviewURL
from apps.review.tasks import index_all_reviews


@pytest.mark.django_db
class TestTasks:
    @pytest.fixture
    def review_url(self):
        return ReviewURL.objects.create(url='https://play.google.com/store/apps/details?id=co.wishroll')

    @pytest.fixture
    def invalid_review_url(self):
        return ReviewURL.objects.create(url='https://play.google.com/store/apps/details?id=com.example.app')

    def test_index_all_reviews_success(self, review_url):
        # index_all_reviews should be called with review_url_id as a kwarg and this should create more than 0 reviews
        index_all_reviews.delay(review_url_id=review_url.id)
        assert review_url.reviews.count() > 0, 'index_all_reviews should create more than 0 reviews'

    def test_index_all_reviews_failure(self, invalid_review_url):
        # index_all_reviews should be called with review_url_id as a kwarg and this should create 0 reviews
        index_all_reviews.delay(review_url_id=invalid_review_url.id)
        assert invalid_review_url.reviews.count() == 0, 'index_all_reviews should create 0 reviews'

