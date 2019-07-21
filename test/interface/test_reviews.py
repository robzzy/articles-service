# -*- coding: utf-8 -*-

import pytest
from marshmallow import ValidationError

from articles.exceptions import ReviewNotFound
from articles.models import Review


class TestReviewService:

    @pytest.fixture
    def review(self, setup_author, setup_article, setup_review):

        setup_author(id=1)
        setup_article(id=1)
        setup_review(id=1)

    def test_get_review(self, article_service, review):

        review = article_service.get_review(1)

        assert review == {
            "id": 1,
            "content": "LGTM",
            "author_id": 1,
            "article_id": 1,
        }

    def test_get_review_not_found(self, article_service):

        with pytest.raises(ReviewNotFound):
            article_service.get_review(2)

    def test_update_review(self, article_service, review):

        review = article_service.update_review(1, {"content": "LGTM too."})

        assert review == {
            "id": 1,
            "content": "LGTM too.",
            "author_id": 1,
            "article_id": 1,
        }

    def test_create_review(self, article_service, review):

        review = article_service.create_review({
            "content": "This article is terrible.",
            "author_id": 1,
            "article_id": 1,
        })

        assert review == {
            "id": 2,
            "content": "This article is terrible.",
            "author_id": 1,
            "article_id": 1,
        }

    @pytest.mark.parametrize(
        "author_id, article_id",
        (
            (1, None),
            (None, 1),
        )
    )
    def test_create_review_validate_failed(
        self, article_service, author_id, article_id
    ):

        with pytest.raises(ValidationError):
            article_service.create_review({
                "content": "Woo, such great!",
                "author_id": author_id,
                "article_id": article_id,
            })

    def test_list_reviews(self, article_service, review, setup_review):

        setup_review(id=2, content="Terrible.")
        setup_review(id=3, content="Woo, such great!")

        reviews = article_service.list_reviews(
            filters={"field": "content", "op": "!=", "value": None},
            sort={"field": "id", "direction": "asc"},
            offset=1,
            limit=10,
        )
        assert reviews == [
            {
                "id": 2,
                "content": "Terrible.",
                "author_id": 1,
                "article_id": 1,
            },
            {
                "id": 3,
                "content": "Woo, such great!",
                "author_id": 1,
                "article_id": 1,
            }
        ]

    def test_delete_review(self, article_service, review):

        article_service.delete_review(1)

        review = article_service.session.query(Review.id == 1).first()

        assert not review
