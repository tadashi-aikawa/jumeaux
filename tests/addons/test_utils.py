#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pytest

from jumeaux.addons import utils


class TestExactMatch:
    @pytest.mark.parametrize(
        'expected, target, regexp', [
            (True, '123', '[0-9]+'),
            (False, 'a123b', '[0-9]+'),
            (True, 'a123b', '([0-9]|[a-b])+'),
            (True, 'aaa', 'aaa|bbb'),
            (False, 'caaa', 'aaa|bbb'),
            (False, 'aaac', 'aaa|bbb'),
            (True, 'bbb', 'aaa|bbb'),
            (False, 'cbbb', 'aaa|bbb'),
            (False, 'bbbc', 'aaa|bbb'),
        ]
    )
    def test_normal(self, expected, target, regexp):
        actual = utils.exact_match(target, regexp)
        assert expected == actual


class TestWhenFilter:
    data = {
        "id": 1,
        "name": "一朗",
        "age": 44,
        "carrier": {
            "2010": "web",
            "2015": "aws"
        },
        "favorites": [
            {
                "rank": 2,
                "name": "Orange"
            },
            {
                "rank": 1,
                "name": "Apple"
            }
        ],
        "nicknames": [
            "Ichi",
            "イチロー"
        ]
    }

    @pytest.mark.parametrize(
        'expected, expression', [
            (True, 'id == 1'),
            (False, 'id != 1'),
            (False, 'id == 2'),
            (True, 'age > 40'),
            (False, 'age > 45'),
            (True, '40 < age < 45'),
            (True, '"イチロー" in nicknames'),
            (True, '"イチ" not in nicknames'),
            (True, 'favorites.1.name == "Apple"'),
            (True, 'favorites[1].name == "Apple"'),
            (False, 'favorites.0.name == "Apple"'),
            (False, 'favorites[0].name == "Apple"'),
            (True, 'favorites|length == 2'),
            (False, 'favorites|length == 3'),
            (True, 'id == 1 and age == 44'),
            (False, 'id == 1 and age == 45'),
            (True, 'id == 1 or age == 44'),
            (True, 'id == 1 or age == 45'),
            (False, 'id == 2 or age == 45'),
            (True, 'age|string|reg("[0-9]{2}")'),
            (False, 'age|string|reg("[0-9]{3}")'),
            (False, '(id == 1 or not name) and (favorites|length == 0 or nicknames|length == 0)'),
            (True, 'id == 1 or (not name and favorites|length == 0) or nicknames|length == 0'),
            (True, '"Apple" in favorites|map(attribute="name")'),
            (False, '"Grape" in favorites|map(attribute="name")'),
            (True, 'carrier["2010"]|default("neet") == "web"'),
            (True, 'carrier["2011"]|default("neet") == "neet"'),
            (4, 'calc_distance_km(35.664131, 139.759302, 35.694253, 139.784099)|int')
        ]
    )
    def test_normal(self, expected, expression):
        actual = utils.when_filter(expression, self.data)
        assert expected == actual


class TestGetJinja2FormatError:
    @pytest.mark.parametrize(
        'expected, fmt', [
            (None, 'I am {{ name }}'),
            (None, 'I am { name }'),
            ("unexpected '}'", 'I am {{ name }'),
        ]
    )
    def test_normal(self, expected, fmt):
        actual = utils.get_jinja2_format_error(fmt)
        assert expected == actual.get()
