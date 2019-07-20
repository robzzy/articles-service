# -*- coding: utf-8 -*-

import os

import pytest

from articles.models import DeclarativeBase


@pytest.fixture(scope="session")
def db_url():
    return "mysql+mysqlconnector://{}:{}@{}/{}?charset=utf8mb4".format(
        os.getenv("DB_USER", "root"),
        os.getenv("DB_PASSWORD", ""),
        os.getenv("DB_SERVER", "localhost"),
        os.getenv("DB_NAME", "articles_test"),
    )


@pytest.fixture(scope="session")
def model_base():
    return DeclarativeBase
