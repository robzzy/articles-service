# -*- coding: utf-8 -*-

from nameko.rpc import rpc, RpcProxy
from nameko.events import event_handler
from marshmallow import ValidationError
from sqlalchemy_filters import apply_filters, apply_sort

from articles.services.core.base import Base
from articles.exceptions import AuthorNotFound
from articles.models import Author
from articles.schemas import AuthorSchema


class AuthorService(Base):

    users_rpc = RpcProxy("users")

    @event_handler("users", "user_created")
    def handle_user_created(self, payload):

        self.create_author(payload["data"])

    @event_handler("users", "user_updated")
    def handle_user_updated(self, payload):

        self.update_author(payload["uuid"], payload["data"])

    @event_handler("users", "user_deleted")
    def handle_user_deleted(self, payload):

        author = self.get_author(uuid=payload["uuid"])

        self.delete_author(author.id)

    def _get_author(self, id_=None, uuid=None):
        query = self.session.query(Author)
        if id_:
            query = query.filter(Author.id == id_)
        if uuid:
            query = query.filter(Author.user_uuid == uuid)

        author = query.first()

        if not author:
            raise AuthorNotFound(f"Author not found.")

        return author

    @rpc
    def get_author(self, id_=None, uuid=None):

        author = self._get_author(id_, uuid)

        return AuthorSchema().dump(author).data

    @rpc
    def create_author(self, data):

        try:
            author_data = AuthorSchema(strict=True).load(data).data
        except ValidationError as err:
            raise ValidationError(*err.args)

        author = Author(**author_data)

        self.session.add(author)
        self.session.commit()

        return AuthorSchema().dump(author).data

    @rpc
    def update_author(self, id_, data):

        author = self._get_author(id_)

        for key, value in data.items():
            setattr(author, key, value)
        self.session.commit()

        return AuthorSchema().dump(author).data

    @rpc
    def list_authors(self, filters=None, sort=None, offset=None, limit=None):
        query = self.session.query(Author)
        if filters:
            query = apply_filters(query, filters)
        if sort:
            query = apply_sort(query, sort)
        if offset:
            query = query.offset(offset)
        if limit:
            query = query.limit(limit)
        authors = query.all()

        return AuthorSchema(many=True).dump(authors).data

    @rpc
    def delete_author(self, id_):

        author = self._get_author(id_)

        self.session.delete(author)
        self.session.commit()
