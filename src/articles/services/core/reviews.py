# -*- coding: utf-8 -*-


from nameko.rpc import rpc
from marshmallow import ValidationError
from sqlalchemy_filters import apply_sort, apply_filters

from articles.schemas import ReviewSchema
from articles.models import Review
from articles.exceptions import ReviewNotFound
from articles.services.core.base import Base


class ReviewService(Base):

    def _get_review(self, id_):

        query = self.session.query(Review)

        review = query.filter(Review.id == id_).first()

        if not review:
            raise ReviewNotFound(
                "Review not found."
            )
        return review

    @rpc
    def get_review(self, id_):

        review = self._get_review(id_)

        return ReviewSchema().dump(review).data

    @rpc
    def update_review(self, id_, data):

        review = self._get_review(id_)

        for key, value in data.items():
            setattr(review, key, value)

        self.session.commit()

        return ReviewSchema().dump(review).data

    @rpc
    def create_review(self, data):

        try:
            review_data = ReviewSchema(strict=True).load(data).data
        except ValidationError as err:
            raise ValidationError(*err.args)

        review = Review(**review_data)

        self.session.add(review)
        self.session.commit()

        return ReviewSchema().dump(review).data

    @rpc
    def list_reviews(self, filters=None, sort=None, offset=None, limit=None):
        query = self.session.query(Review)
        if filters:
            query = apply_filters(query, filters)
        if sort:
            query = apply_sort(query, sort)
        if offset:
            query = query.offset(offset)
        if limit:
            query = query.limit(limit)
        articles = query.all()

        return ReviewSchema(many=True).dump(articles).data

    @rpc
    def delete_review(self, id_):

        review = self._get_review(id_)

        self.session.delete(review)
        self.session.commit()
