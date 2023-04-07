from google_play_scraper import Sort, reviews_all, reviews

from conf.celery import app
from .models import PlayStoreReview, ReviewURL

import logging

logger = logging.getLogger(__name__)


@app.task(bind=True, max_retries=3, default_retry_delay=60)
def index_all_reviews(*args, **kwargs):
    """Index all reviews for a given review url."""
    review_url_id = kwargs.get("review_url_id")
    logger.debug(f"Indexing all reviews for review url id {review_url_id}")

    try:
        review_url = ReviewURL.objects.get(id=review_url_id)
    except ReviewURL.DoesNotExist:
        return

    url: str = review_url.url

    # get all reviews
    try:
        app_id: str = url.split("id=")[1]
    except IndexError:
        return

    all_reviews = reviews_all(
        app_id,
        sleep_milliseconds=0,
        lang="en",
        country="us",
        sort=Sort.NEWEST,
    )
    logger.debug(f"Found {len(all_reviews)} reviews")

    # save all reviews
    PlayStoreReview.objects.bulk_create(
        [PlayStoreReview(
            review_url=review_url,
            user_name=review["userName"],
            rating=review["score"],
            review_text=review["content"],
        ) for review in all_reviews])

    logger.debug(f"Saved {len(all_reviews)} reviews")


@app.task
def index_latest_reviews(review_url_id: int):
    try:
        review_url = ReviewURL.objects.get(id=review_url_id)
    except ReviewURL.DoesNotExist:
        return

    url: str = review_url.url

    # get all reviews
    try:
        app_id: str = url.split("id=")[1]
    except IndexError:
        return

    last_review_time = review_url.playstorereview_set.last().created_at

    latest_reviews = reviews(
        app_id,
        lang="en",
        country="us",
        sort=Sort.NEWEST,
        count=100,
    )
    logger.debug(f"Found {len(latest_reviews)} reviews")

    # filter out reviews that are older than the last review
    latest_reviews = [review for review in latest_reviews if review["at"] > last_review_time]
    if len(latest_reviews) == 0:
        return

    # save all reviews
    PlayStoreReview.objects.bulk_create(
        [PlayStoreReview(
            review_url=review_url,
            user_name=review["userName"],
            rating=review["score"],
            review_text=review["content"],
        ) for review in latest_reviews])


@app.task
def index_review_urls():
    """Index all review urls."""
    logger.debug("Indexing all review urls")

    review_urls = ReviewURL.objects.all()

    for review_url in review_urls:
        index_latest_reviews.delay(review_url.id)

    logger.debug("Done indexing all review urls")
