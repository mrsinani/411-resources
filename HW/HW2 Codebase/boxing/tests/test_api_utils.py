import pytest
import requests

from boxing.utils.api_utils import get_random


@pytest.fixture
def mock_random_org(mocker):
    """Fixture that mocks the random.org API response."""
    mock_response = mocker.Mock()
    mock_response.text = "0.74"
    mock_response.raise_for_status.return_value = None
    mocker.patch("requests.get", return_value=mock_response)
    return mock_response


def test_get_random_success(mock_random_org):
    """Test successfully getting a random number from the API."""
    result = get_random()
    assert result == 0.74
    requests.get.assert_called_once()


def test_get_random_timeout(mocker):
    """Test that a timeout from the API raises the expected error."""
    mocker.patch("requests.get", side_effect=requests.exceptions.Timeout)
    with pytest.raises(RuntimeError, match="Request to random.org timed out."):
        get_random()


def test_get_random_request_failure(mocker):
    """Test that a request failure from the API raises the expected error."""
    mocker.patch(
        "requests.get",
        side_effect=requests.exceptions.RequestException("Connection error"),
    )
    with pytest.raises(
        RuntimeError, match="Request to random.org failed: Connection error"
    ):
        get_random()


def test_get_random_invalid_response(mocker):
    """Test that an invalid response from the API raises the expected error."""
    mock_response = mocker.Mock()
    mock_response.text = "not_a_number"
    mock_response.raise_for_status.return_value = None
    mocker.patch("requests.get", return_value=mock_response)

    with pytest.raises(
        ValueError, match="Invalid response from random.org: not_a_number"
    ):
        get_random()
