import pytest
import requests

from boxing.utils.api_utils import get_random


@pytest.fixture
def mock_random_org(mocker):
    mock_response = mocker.Mock()
    mock_response.text = "0.74"
    mock_response.raise_for_status.return_value = None
    mocker.patch("requests.get", return_value=mock_response)
    return mock_response


def test_get_random_success(mock_random_org):
    result = get_random()
    assert result == 0.74
    requests.get.assert_called_once()


def test_get_random_timeout(mocker):
    mocker.patch("requests.get", side_effect=requests.exceptions.Timeout)
    with pytest.raises(RuntimeError, match="Request to random.org timed out."):
        get_random()


def test_get_random_request_failure(mocker):
    mocker.patch(
        "requests.get",
        side_effect=requests.exceptions.RequestException("Connection error"),
    )
    with pytest.raises(
        RuntimeError, match="Request to random.org failed: Connection error"
    ):
        get_random()


def test_get_random_invalid_response(mocker):
    mock_response = mocker.Mock()
    mock_response.text = "not_a_number"
    mock_response.raise_for_status.return_value = None
    mocker.patch("requests.get", return_value=mock_response)

    with pytest.raises(
        ValueError, match="Invalid response from random.org: not_a_number"
    ):
        get_random()
