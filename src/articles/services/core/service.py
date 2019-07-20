# -*- coding: utf-8 -*-

import json

from nameko.web.handlers import http

from articles.services.core.base import Base


class ArticleService(Base):

    name = "articles"

    @http("GET", "/healthcheck")
    def health_check(self, request):
        return json.dumps({"status": "ok"})
