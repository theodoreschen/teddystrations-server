from unittest import TestCase, main
from unittest.mock import MagicMock
try:
    from .data_types import Player
except ImportError:
    from data_types import Player
import uuid
import json


class TestPlayer(TestCase):
    def test_to_dict(self):
        test_uid = uuid.uuid4()
        p = Player(name="test")

        pd = p.to_dict()
        self.assertNotEqual(pd["uid"], str(test_uid))
        self.assertEqual(pd["name"], "test")

    def test_to_json(self):
        test_uid = uuid.uuid4()
        p = Player(name="test")

        j = json.loads(p.to_json())
        self.assertNotEqual(j["uid"], str(test_uid))
        self.assertEqual(j["name"], "test")

    def test_from_json(self):
        test_uid = uuid.uuid4()
        test_name = "test"
        test_obj = json.dumps({
            "name": test_name,
            "uid": str(test_uid)
        })

        p = Player.from_json(test_obj)

        self.assertEqual(p.name, test_name)
        self.assertEqual(p.uid, test_uid)


if __name__ == "__main__":
    main()