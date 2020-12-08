# -*- coding: utf-8 -*-
import uuid

from marshmallow import Schema, fields, pre_dump, pre_load

from articles.constants import Gender, ArticleStatus


class AuthorSchema(Schema):

    id = fields.Integer()
    nickname = fields.String()
    gender = fields.String()
    birth = fields.DateTime()
    location = fields.String()
    user_uuid = fields.String(allow_none=False)

    @pre_load
    def generate_user_uuid(self, data):
        if not data.get("user_uuid"):
            data["user_uuid"] = str(uuid.uuid4())
        return data

    @pre_dump
    def handle_gender_to_enum(self, author):
        if isinstance(author.gender, Gender):
            author.gender = author.gender.value
        return author


class ArticleSchema(Schema):

    id = fields.Integer()
    title = fields.String(allow_none=False)
    content = fields.String(allow_none=True)
    status = fields.String(allow_none=True)
    click_num = fields.Integer(dump_only=True)
    author_id = fields.Integer(required=True)

    @pre_dump
    def handle_status_to_enum(self, article):
        if isinstance(article.status, ArticleStatus):
            article.status = article.status.value
        return article


class ReviewSchema(Schema):

    id = fields.Integer(dump_only=True)
    content = fields.String()
    author_id = fields.Integer(allow_none=False)
    article_id = fields.Integer(allow_none=False)
