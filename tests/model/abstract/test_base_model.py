from unittest import TestCase, mock
from unittest.mock import MagicMock, Mock

import ornitho
from ornitho.api_exception import APIException
from ornitho.model.abstract import BaseModel
from ornitho.model.abstract.base_model import check_raw_data, check_refresh

ornitho.consumer_key = "ORNITHO_CONSUMER_KEY"
ornitho.consumer_secret = "ORNITHO_CONSUMER_SECRET"
ornitho.user_email = "ORNITHO_USER_EMAIL"
ornitho.user_pw = "ORNITHO_USER_PW"
ornitho.api_base = "ORNITHO_API_BASE"


class TestBaseModel(TestCase):
    class MyModel(BaseModel):
        ENDPOINT = "my_model"

    # noinspection PyUnusedLocal
    @staticmethod
    def fake_request(**kwargs):
        return [["data"], "paginationKey"]

    # noinspection PyUnusedLocal
    @staticmethod
    def fake_empty_request(**kwargs):
        return [[], None]

    def setUp(self):
        self.my_model = self.MyModel.create_from_ornitho_json({"id": "1"})
        self.my_model_2 = self.MyModel.create_from_ornitho_json({"@id": "2"})

    def test_id_(self):
        self.assertEqual(1, self.my_model.id_)
        self.assertEqual(2, self.my_model_2.id_)

        my_model_3 = self.MyModel()
        self.assertIsNone(my_model_3.id_)
        my_model_3._raw_data = {"id": 3}
        self.assertEqual(3, my_model_3.id_)

        my_model_4 = self.MyModel()
        self.assertIsNone(my_model_4.id_)
        my_model_4._raw_data = {"@id": 4}
        self.assertEqual(4, my_model_4.id_)

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
        model = self.MyModel.create_from_ornitho_json({"id": "1", "foo": "bar"})
        self.assertEqual(1, model.id_)
        self.assertEqual({"id": "1", "foo": "bar"}, model._raw_data)

    @mock.patch.object(ornitho.api_requester.APIRequester, "request", fake_request)
    def test_refresh(self):
        self.my_model.refresh()

        self.assertEqual({"id": "1"}, self.my_model._previous)
        self.assertEqual("data", self.my_model._raw_data)

    @mock.patch.object(
        ornitho.api_requester.APIRequester, "request", fake_empty_request
    )
    def test_refresh_exception(self):
        self.assertRaises(
            APIException,
            lambda: self.my_model.refresh(),
        )

    def test_instance_url(self):
        self.assertEqual("my_model/1", self.my_model.instance_url())


def test_check_refresh():
    func = Mock()
    func.__name__ = "foo"
    base_mode_mock = MagicMock()
    base_mode_mock._raw_data = {"bar": 1}
    base_mode_mock._refreshed = False
    decorated_func = check_refresh(func)
    decorated_func(base_mode_mock)
    assert func.called
    assert base_mode_mock.refresh.called

    func2 = Mock()
    func2.__name__ = "foo"
    base_mode_mock2 = MagicMock()
    base_mode_mock2._raw_data = {"foo": 1}
    base_mode_mock._refreshed = False
    decorated_func = check_refresh(func2)
    decorated_func(base_mode_mock2)
    assert func2.called
    assert not base_mode_mock2.refresh.called


def test_check_raw_data():
    func = Mock()
    base_mode_mock = MagicMock()
    base_mode_mock._raw_data = {"bar": 1}
    base_mode_mock._refreshed = False
    decorated_func = check_raw_data("foo")(func)
    decorated_func(base_mode_mock)
    assert func.called
    assert base_mode_mock.refresh.called

    func2 = Mock()
    base_mode_mock2 = MagicMock()
    base_mode_mock2._raw_data = {"foo": 1}
    base_mode_mock._refreshed = False
    decorated_func = check_raw_data("foo")(func2)
    decorated_func(base_mode_mock2)
    assert func2.called
    assert not base_mode_mock2.refresh.called
