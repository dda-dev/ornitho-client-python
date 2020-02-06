from unittest import TestCase, mock
from unittest.mock import MagicMock

import ornitho
from ornitho.model.abstract import BaseModel


class TestBaseModel(TestCase):
    class MyModel(BaseModel):
        ENDPOINT = "my_model"

    # noinspection PyUnusedLocal
    @staticmethod
    def fake_request(**kwargs):
        return [["data"], "paginationKey"]

    def setUp(self):
        self.my_model = self.MyModel.create_from({"id": "1"})

    def test_id_(self):
        self.assertEqual(1, self.my_model.id_)

    def test_retrieve(self):
        self.MyModel.refresh = MagicMock()
        model = self.MyModel.get(1)
        self.MyModel.refresh.assert_called()
        self.assertEqual(1, model.id_)

    @mock.patch.object(ornitho.api_requester.APIRequester, "request", fake_request)
    def test_request(self):
        model = self.MyModel.request(method="get", url=self.MyModel.ENDPOINT)[0]
        self.assertEqual("data", model)

    def test_create_from(self):
        model = self.MyModel.create_from({"id": "1", "foo": "bar"})
        self.assertEqual(1, model.id_)
        self.assertEqual({"id": "1", "foo": "bar"}, model._raw_data)

    @mock.patch.object(ornitho.api_requester.APIRequester, "request", fake_request)
    def test_refresh(self):
        self.my_model.refresh()

        self.assertEqual({"id": "1"}, self.my_model._previous)
        self.assertEqual("data", self.my_model._raw_data)

    def test_instance_url(self):
        self.assertEqual("my_model/1", self.my_model.instance_url())
