# -*- coding: utf-8 -*-

from nameko_autocrud import AutoCrud

from articles.models import Article
from articles.schemas import ArticleSchema


class ArticleMixin:

    articles_autocurd = AutoCrud(
        "db_session",
        model_cls=Article,
        get_method_name="get_article",
        create_method_name="create_article",
        update_method_name="update_article",
        list_method_name="list_articles",
        count_method_name="count_articles",
        from_serializable=lambda obj: ArticleSchema(strict=True).load(obj).data,
        to_serializable=lambda obj: ArticleSchema(strict=True).dump(obj).data,
    )
