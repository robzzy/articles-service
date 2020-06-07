# -*- coding: utf-8 -*-

from nameko_autocrud import AutoCrud

from articles.schemas import ReviewSchema
from articles.models import Review


class ReviewMixin:

    reviews_autocrud = AutoCrud(
        "db_session",
        model_cls=Review,
        get_method_name="get_review",
        create_method_name="create_review",
        update_method_name="update_review",
        list_method_name="list_reviews",
        count_method_name="count_reviews",
        from_serializable=lambda obj: ReviewSchema(strict=True).load(obj).data,
        to_serializable=lambda obj: ReviewSchema(strict=True).dump(obj).data,
    )
