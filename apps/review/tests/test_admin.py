from unittest.mock import patch

import pytest

from apps.review.models import ReviewURL
from apps.review.tasks import index_all_reviews
from ..admin import ReviewURLAdmin


@pytest.mark.django_db
class TestReviewURLAdmin:
    @pytest.fixture
    def review_url(self):
        return ReviewURL.objects.create(url='https://play.google.com/store/apps/details?id=com.example.app')

    @patch('apps.review.tasks.index_all_reviews.delay')
    def test_create_pushes_new_job_to_celery(self, review_url):
        admin = ReviewURLAdmin(ReviewURL, None)
        admin.save_model(None, review_url, None, False)
        assert index_all_reviews.delay.called, 'index_all_reviews.delay should be called'
