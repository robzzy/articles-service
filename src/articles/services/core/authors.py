# -*- coding: utf-8 -*-

from nameko_autocrud import AutoCrudWithEvents

from articles.models import Author
from articles.schemas import AuthorSchema


class AuthorMixin:

    authors_autocrud = AutoCrudWithEvents(
        "db_session",
        "event_dispatcher",
        "author",
        model_cls=Author,
        get_method_name="get_author",
        create_method_name="create_author",
        update_method_name="update_author",
        list_method_name="list_authors",
        count_method_name="count_authors",
        create_event_name="author_created",
        update_event_name="author_updated",
        delete_event_name="author_deleted",
        from_serializable=lambda obj: AuthorSchema(strict=True).load(obj).data,
        to_serializable=lambda obj: AuthorSchema(strict=True).dump(obj).data,
    )
