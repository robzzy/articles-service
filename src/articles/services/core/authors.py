# -*- coding: utf-8 -*-

from nameko_autocrud import AutoCrud

from articles.models import Author
from articles.schemas import AuthorSchema


class AuthorMixin:

    authors_autocrud = AutoCrud(
        "db_session",
        model_cls=Author,
        get_method_name="get_author",
        create_method_name="create_author",
        update_method_name="update_author",
        list_method_name="list_authors",
        count_method_name="count_authors",
        from_serializable=lambda obj: AuthorSchema(strict=True).load(obj).data,
        to_serializable=lambda obj: AuthorSchema(strict=True).dump(obj).data,
    )
