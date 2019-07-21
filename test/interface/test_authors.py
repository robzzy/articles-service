# -*- coding: utf-8 -*-

import pytest
from mock import Mock, call
from marshmallow import ValidationError

from articles.exceptions import AuthorNotFound
from articles.models import Author


class TestAuthorService:

    @pytest.fixture
    def author(self, setup_author):
        setup_author(id=1)

    def test_handle_user_created(self, article_service):
        article_service.create_author = Mock()

        payload = {
            "data": {"uuid": "uuid1"}
        }

        article_service.handle_user_created(payload)

        assert article_service.create_author.call_args == call(
            {"uuid": "uuid1"}
        )

    def test_handle_user_updated(self, article_service):
        article_service.update_author = Mock()

        payload = {
            "uuid": "uuid1",
            "data": {"nickname": "nick"}
        }
        article_service.handle_user_updated(payload)

        assert article_service.update_author.call_args == call(
            "uuid1", {"nickname": "nick"}
        )

    def test_handle_user_deleted(self, article_service):
        article_service.get_author = Mock()
        article_service.delete_author = Mock()

        article_service.get_author.return_value = (
            type("Author", (), {"id": 1})
        )

        article_service.handle_user_deleted({"uuid": "uuid1"})

        assert article_service.delete_author.call_args == call(1)

    @pytest.mark.parametrize(
        "id_, uuid",
        (
            (1, None),
            (None, "uuid1")
        )
    )
    def test_get_author(self, article_service, author, id_, uuid):

        author = article_service.get_author(id_=id_, uuid=uuid)

        assert author == {
            "id": 1,
            "nickname": "iamdavidzeng",
            "gender": "male",
            "birth": "2000-01-01T00:00:00+00:00",
            "location": "099 Street",
            "user_uuid": "uuid1",
        }

    def test_get_author_not_found(self, article_service):

        with pytest.raises(AuthorNotFound):
            article_service.get_author(1)

    def test_create_author(self, article_service):

        author_data = {
            "nickname": "iamzzy",
            "gender": "male",
            "birth": "2000-01-01 00:00:00",
            "location": "100 Street",
            "uuid": "new_uuid",
        }

        author = article_service.create_author(author_data)

        assert author == {
            "id": 2,
            "nickname": "iamzzy",
            "gender": "male",
            "birth": "2000-01-01T00:00:00+00:00",
            "location": "100 Street",
            "user_uuid": "new_uuid",
        }

    def test_create_author_validate_failed(self, article_service):

        author_data = {
            "uuid": None
        }
        with pytest.raises(ValidationError):
            article_service.create_author(author_data)

    def test_update_author(self, article_service, author):

        update_data = {"location": "Nowhere to hide"}

        author = article_service.update_author(1, update_data)

        assert author == {
            "id": 1,
            "nickname": "iamdavidzeng",
            "gender": "male",
            "birth": "2000-01-01T00:00:00+00:00",
            "location": "Nowhere to hide",
            "user_uuid": "uuid1",
        }

    def test_list_authors(self, article_service, setup_author):

        setup_author(id=2)
        setup_author(id=3)

        authors = article_service.list_authors(
            filters={"field": "gender", "op": "==", "value": "male"},
            sort={"field": "id", "direction": "desc"},
            offset=1,
            limit=1,
        )

        assert authors == [{
            "id": 2,
            "nickname": "iamdavidzeng",
            "gender": "male",
            "birth": "2000-01-01T00:00:00+00:00",
            "location": "099 Street",
            "user_uuid": "uuid2",
        }]

    def test_delete_author(self, article_service, setup_author):

        setup_author(id=4)

        article_service.delete_author(4)

        author = article_service.session.query(Author.id == 4).first()

        assert not author
