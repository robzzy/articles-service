# -*- coding: utf-8 -*-

import json

from nameko.rpc import rpc
from nameko.web.handlers import http
from marshmallow.exceptions import ValidationError
from sqlalchemy_filters import apply_sort, apply_filters

from articles.models import Article
from articles.exceptions import ArticleNotFound, AuthorNotFound
from articles.services.core.authors import AuthorService
from articles.services.core.reviews import ReviewService
from articles.schemas import ArticleSchema


class ArticleService(AuthorService, ReviewService):

    name = "articles"

    @http("GET", "/healthcheck")
    def health_check(self, request):
        return json.dumps({"status": "ok"})

    def _get_article(self, id_):
        query = self.session.query(Article)

        article = query.filter(Article.id == id_).first()

        if not article:
            raise ArticleNotFound(
                f"Article with id: {id_} do not exists."
            )
        return article

    @rpc
    def get_article(self, id_):
        article = self._get_article(id_)

        return ArticleSchema().dump(article).data

    @rpc
    def update_article(self, id_, data):

        article = self._get_article(id_)

        try:
            article_data = ArticleSchema(strict=True).load(data).data
        except ValidationError as err:
            raise ValidationError(*err.args)

        for key, value in article_data.items():
            setattr(article, key, value)
        self.session.commit()

        return ArticleSchema().dump(article).data

    @rpc
    def create_article(self, data):
        try:
            schema = ArticleSchema(strict=True)
            article_data = schema.load(data).data
        except ValidationError as err:
            raise ValidationError(*err.args)

        user = data.get("user", {})

        try:
            author = self.get_author(uuid=user["uuid"])
        except AuthorNotFound:

            author = self.create_author(data["user"])

        article_data["author_id"] = author["id"]

        article = Article(**article_data)

        self.session.add(article)
        self.session.commit()

        return ArticleSchema().dump(article).data

    @rpc
    def list_articles(self, filters=None, sort=None, offset=None, limit=None):
        query = self.session.query(Article)
        if filters:
            query = apply_filters(query, filters)
        if sort:
            query = apply_sort(query, sort)
        if offset:
            query = query.offset(offset)
        if limit:
            query = query.limit(limit)

        articles = query.all()

        return ArticleSchema(many=True).dump(articles).data

    @rpc
    def delete_article(self, id_):

        article = self._get_article(id_)

        self.session.delete(article)
        self.session.commit()
