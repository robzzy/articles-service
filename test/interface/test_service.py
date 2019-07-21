# -*- coding: utf-8 -*-

import pytest
from marshmallow import ValidationError

from articles.exceptions import ArticleNotFound


class TestArticleService:

    @pytest.fixture
    def article(self, setup_author, setup_article):
        setup_author(id=1)
        setup_article(id=1)

    def test_health_check(self, article_service):

        response = article_service.health_check({})

        assert response == '{"status": "ok"}'

    def test_get_article(self, article_service, article):

        article = article_service.get_article(1)

        assert article == {
            "id": 1,
            "title": "article1",
            "content": "article1 looks great.",
            "status": "published",
            "click_num": 0,
            "author_id": 1,
        }

    def test_get_article_not_found(self, article_service):

        with pytest.raises(ArticleNotFound) as err:

            article_service.get_article(1)

        assert str(err.value) == "Article with id: 1 do not exists."

    def test_update_article(self, article_service, article):

        article = article_service.update_article(1, {"title": "new_title"})

        assert article == {
            "id": 1,
            "title": "new_title",
            "content": "article1 looks great.",
            "status": "published",
            "click_num": 0,
            "author_id": 1,
        }

    def test_update_article_validate_failed(self, article_service, article):

        with pytest.raises(ValidationError) as err:
            article_service.update_article(1, {"title": None})

        assert str(err.value) == str({"title": ["Field may not be null."]})

    def test_create_article(self, article_service, article):

        article_data = {
            "title": "article1",
            "content": "article1 looks great.",
            "status": "published",
            "user": {"uuid": "uuid1"},
        }

        article = article_service.create_article(article_data)

        assert article == {
            "id": 2,
            "title": "article1",
            "content": "article1 looks great.",
            "status": "published",
            "click_num": 0,
            "author_id": 1,
        }

    def test_create_article_author_not_found(self, article_service):

        article_data = {
            "title": "article1",
            "content": "article1 looks great.",
            "status": "published",
            "user": {"uuid": "uuid_not_exists"},
        }
        article = article_service.create_article(article_data)

        assert article == {
            "id": 3,
            "title": "article1",
            "content": "article1 looks great.",
            "status": "published",
            "click_num": 0,
            "author_id": 5,
        }

    def test_create_article_validate_failed(self, article_service):
        article_data = {
            "title": None,
            "content": "article1 looks great.",
            "status": "published",
            "user": {"uuid": "uuid1"},
        }

        with pytest.raises(ValidationError):
            article_service.create_article(article_data)

    def test_list_articles(self, article_service, article, setup_article):

        setup_article(id=2)
        setup_article(id=3)
        setup_article(id=4)

        articles = article_service.list_articles(
            filters={"field": "author_id", "op": "==", "value": 1},
            sort={"field": "id", "direction": "asc"},
            offset=2,
            limit=1,
        )

        assert articles == [{
            "id": 3,
            "title": "article1",
            "content": "article1 looks great.",
            "status": "published",
            "click_num": 0,
            "author_id": 1,
        }]

    def test_delete_article(self, article_service, article):

        article_service.delete_article(1)

        with pytest.raises(ArticleNotFound):
            article_service.get_article(1)
