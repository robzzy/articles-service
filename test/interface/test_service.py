# -*- coding: utf-8 -*-

import pytest

from nameko.testing.services import worker_factory

from articles.services.core.service import ArticleService


@pytest.fixture
def article_service(db_session):
    service = worker_factory(ArticleService, **{"session": db_session})
    return service


class TestArticleService:

    def test_health_check(self, article_service):

        response = article_service.health_check({})

        assert response == '{"status": "ok"}'
