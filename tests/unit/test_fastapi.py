# -*- coding: utf-8 -*-
__author__ = "Jairo Leon, Luis Rueda"
__email__ = "jlr060@gmail.com, userlerueda@gmail.com"

import typing

from fastapi import Request

from fastapi_mongodb_utils.fastapi import CustomFastAPI, FastAPIRequest


class TestFastAPI:
    """Test FastAPI."""

    def test_custom_fastapi_initialization(self):
        """Test CustomFastAPI initialization."""
        app = CustomFastAPI()
        assert isinstance(app, CustomFastAPI)

    def test_fastapi_request_typing(self):
        """Test FastAPIRequest typing."""
        if typing.TYPE_CHECKING:
            assert issubclass(FastAPIRequest, Request)
            assert hasattr(FastAPIRequest, "app")
            assert FastAPIRequest.app == CustomFastAPI
        else:
            assert FastAPIRequest == Request
