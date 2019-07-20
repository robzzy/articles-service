# -*- coding: utf-8 -*-

from mock import patch

from articles.utils import utcnow


def test_utc_now():

    with patch("articles.utils.datetime") as datetime:
        datetime.utcnow.return_value = "2019-7-20 00:00:00"

        now = utcnow()

    assert now == "2019-7-20 00:00:00"
