# -*- coding: utf-8 -*-

from marshmallow import Schema, fields, pre_dump


class AuthorSchema(Schema):

    id = fields.Integer()
    nickname = fields.String()
    gender = fields.String()
    birth = fields.DateTime()
    location = fields.String()
    user_uuid = fields.String(load_from="uuid", allow_none=False)

    @pre_dump
    def handle_gender_to_enum(self, author):
        if author.gender:
            author.gender = author.gender.value
        return author


class ArticleSchema(Schema):

    id = fields.Integer()
    title = fields.String(allow_none=False)
    content = fields.String(allow_none=True)
    status = fields.String(allow_none=True)
    click_num = fields.Integer(dump_only=True)
    author_id = fields.Integer()

    @pre_dump
    def handle_status_to_enum(self, article):
        article.status = article.status.value
        return article


class ReviewSchema(Schema):

    id = fields.Integer(dump_only=True)
    content = fields.String()
    author_id = fields.Integer(allow_none=False)
    article_id = fields.Integer(allow_none=False)
