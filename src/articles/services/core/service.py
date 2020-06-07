# -*- coding: utf-8 -*-

import json

from nameko_tracer import Tracer
from nameko.events import EventDispatcher
from nameko_sqlalchemy import DatabaseSession
from nameko.rpc import rpc
from nameko.web.handlers import http

from articles.models import DeclarativeBase
from articles.services.core.authors import AuthorMixin
from articles.services.core.reviews import ReviewMixin
from articles.services.core.articles import ArticleMixin


class ArticleService(AuthorMixin, ReviewMixin, ArticleMixin):

    name = "articles"

    tracer = Tracer()
    db_session = DatabaseSession(DeclarativeBase)
    event_dispatch = EventDispatcher()

    @http("GET", "/healthcheck")
    def health_check_http(self, request):
        return json.dumps(self.health_check())

    @rpc
    def health_check(self):
        return {"status": "ok"}
