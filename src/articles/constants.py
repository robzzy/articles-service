# -*- coding: utf-8 -*-

from enum import Enum


class ArticleStatus(Enum):

    WRITING = "writing"
    """author are writing article, not ready to display."""

    UNPUBLISHED = "unpublished"
    """author finished, but he/she do not want to display right now."""

    PUBLISHED = "published"
    """Ready to display!!!"""


class Gender(Enum):

    MALE = "male"

    FEMALE = "female"
