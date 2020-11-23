# -*- coding: utf-8 -*-
from typing import Any

from owlmixin import TOption


class NotificationHandler:
    def notify(self, message: str) -> TOption[str]:
        """
        :param message: Message to send
        :return: Error message
        """
        raise NotImplementedError()
