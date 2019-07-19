# -*- coding: utf-8 -*-

from enum import Enum

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType

from articles.utils import utcnow


class ModelBase:

    created_at = Column(DateTime, nullable=False, default=utcnow)
    updated_at = Column(DateTime, nullable=False, default=utcnow, onupdate=utcnow)


DeclarativeBase = declarative_base(cls=ModelBase)


class ArticleStatus(Enum):

    WRITING = "writing"
    """author are writing article, not ready to display."""

    UN_PUBLISH = "un_publish"
    """author finished, but he/she do not want to display right now."""

    PUBLISHED = "published"
    """Ready to display!!!"""


class Gender(Enum):

    MALE = "male"

    FEMALE = "female"


class Author(DeclarativeBase):

    __tablename__ = "authors"

    id = Column(Integer, primary_key=True)
    nickname = Column(String(64), nullable=True)
    gender = Column(ChoiceType(Gender), nullable=True)
    birth = Column(DateTime, nullable=True)
    location = Column(String(64), nullable=True)
    user_uuid = Column(String(36), nullable=False, unique=True)


class Article(DeclarativeBase):

    __tablename__ = "articles"

    id = Column(Integer, primary_key=True)
    title = Column(String(32), nullable=False)
    content = Column(Text, nullable=True)
    status = Column(
        ChoiceType(ArticleStatus, impl=String(16)),
        nullable=False,
        default=ArticleStatus.WRITING,
    )
    click_num = Column(Integer, nullable=True, default=0)
    author_id = Column(
        Integer,
        ForeignKey("authors.id", name="fk_articles_authors"),
        nullable=False,
    )
    author = relationship("Author", backref="articles")


class Tag(DeclarativeBase):

    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    key = Column(String(16), nullable=False, unique=True)


class Review(DeclarativeBase):

    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True)
    content = Column(String(256), nullable=True)

    author_id = Column(
        Integer,
        ForeignKey("author.id", name="fk_reviews_authors"),
        nullable=False,
    )
    author = relationship("Author", backref="reviews")

    article_id = Column(
        Integer,
        ForeignKey("article.id", name="fk_reviews_articles"),
        nullable=False
    )
    article = relationship("Article", backref="reviews")
