# -*- coding: utf-8 -*-

from nameko_autocrud import AutoCrudWithEvents

from articles.models import Article
from articles.schemas import ArticleSchema


class ArticleMixin:

    articles_autocurd = AutoCrudWithEvents(
        "db_session",
        "event_dispatcher",
        "article",
        model_cls=Article,
        get_method_name="get_article",
        create_method_name="create_article",
        update_method_name="update_article",
        list_method_name="list_articles",
        count_method_name="count_articles",
        create_event_name="article_created",
        update_event_name="article_updated",
        delete_event_name="article_deleted",
        from_serializable=lambda obj: ArticleSchema(strict=True).load(obj).data,
        to_serializable=lambda obj: ArticleSchema(strict=True).dump(obj).data,
    )
