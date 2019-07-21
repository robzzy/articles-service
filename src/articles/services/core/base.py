# -*- coding: utf-8 -*-

from nameko_tracer import Tracer
from nameko.events import EventDispatcher
from nameko_sqlalchemy import DatabaseSession

from articles.models import DeclarativeBase


class Base:

    tracer = Tracer()
    session = DatabaseSession(DeclarativeBase)
    event_dispatch = EventDispatcher()
