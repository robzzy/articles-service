# -*- coding: utf-8 -*-

import pytest

from nameko.testing.services import worker_factory

from articles.services.core.service import ArticleService
from articles.models import Article, Author, Review


@pytest.fixture
def article_service(db_session):
    service = worker_factory(ArticleService, **{"session": db_session})
    yield service


@pytest.fixture
def make_article():
    def _make(**kwargs):

        article_data = {
            "title": "article1",
            "content": "article1 looks great.",
            "status": "published",
            "author_id": 1,
        }
        article_data.update(**kwargs)

        return article_data

    return _make


@pytest.fixture
def setup_article(db_session, make_article):
    def insert(**overrides):
        article_data = make_article(**overrides)
        article = Article(**article_data)

        db_session.add(article)
        db_session.commit()
        return article

    return insert


@pytest.fixture
def make_author():
    def _make(**kwargs):

        author_data = {
            "nickname": "iamdavidzeng",
            "gender": "male",
            "birth": "2000-1-1 00:00:00",
            "location": "099 Street",
            "user_uuid": "uuid",
        }
        if "id" in kwargs:
            author_data["user_uuid"] += str(kwargs["id"])
        author_data.update(**kwargs)
        return author_data

    return _make


@pytest.fixture
def setup_author(db_session, make_author):
    def insert(**overrides):

        author_data = make_author(**overrides)
        author = Author(**author_data)

        db_session.add(author)
        db_session.commit()
        return author

    return insert


@pytest.fixture
def make_review():
    def _make(**kwargs):

        review_data = {
            "content": "LGTM",
            "author_id": 1,
            "article_id": 1,
        }
        review_data.update(**kwargs)
        return review_data

    return _make


@pytest.fixture
def setup_review(db_session, make_review):
    def insert(**overrides):

        review_data = make_review(**overrides)
        review = Review(**review_data)

        db_session.add(review)
        db_session.commit()
        return review

    return insert
