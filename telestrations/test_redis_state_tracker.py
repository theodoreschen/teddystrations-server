from unittest import TestCase, main
from unittest.mock import MagicMock
try:
    from .data_types import Player
except ImportError:
    from data_types import Player
import uuid
import json


class TestRedisStateTracker(TestCase):
    @classmethod
    def setUp(self):
        return super().setUp()


if __name__ == "__main__":
    main()