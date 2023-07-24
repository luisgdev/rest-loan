""" Test API endpoints """

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from tests.constants import (
    AUTH_MISSING,
    CUSTOMER_ENDPOINT,
    DOCS_ENDPOINT,
    GET,
    LOAN_ENDPOINT,
    POST,
)

client = APIClient()


@pytest.mark.parametrize(
    ("endpoint", "data", "method", "result"),
    (
        (LOAN_ENDPOINT, None, GET, AUTH_MISSING),
        (LOAN_ENDPOINT, None, POST, AUTH_MISSING),
        (CUSTOMER_ENDPOINT, None, GET, AUTH_MISSING),
        (CUSTOMER_ENDPOINT, None, POST, AUTH_MISSING),
    ),
)
def test_auth(endpoint, data, method, result):
    """
    Test GET endpoints
    """
    if method == GET:
        response = client.get(endpoint, data=data)
    else:
        response = client.post(endpoint, data=data)
    assert result in response.data.get("detail")


@pytest.mark.parametrize(
    ("endpoint", "data", "method", "status_code"),
    (
        ("/", None, GET, status.HTTP_404_NOT_FOUND),
        ("/aaaa", None, POST, status.HTTP_404_NOT_FOUND),
        ("/index", None, POST, status.HTTP_404_NOT_FOUND),
        (CUSTOMER_ENDPOINT, None, GET, status.HTTP_401_UNAUTHORIZED),
        (CUSTOMER_ENDPOINT, None, POST, status.HTTP_401_UNAUTHORIZED),
        (LOAN_ENDPOINT, None, GET, status.HTTP_401_UNAUTHORIZED),
        (LOAN_ENDPOINT, None, POST, status.HTTP_401_UNAUTHORIZED),
        (DOCS_ENDPOINT, None, GET, status.HTTP_200_OK),
        ("/api/redoc/", None, GET, status.HTTP_404_NOT_FOUND),
        ("/admin/", None, GET, status.HTTP_302_FOUND),
        ("/admin/", None, POST, status.HTTP_302_FOUND),
        ("/docs/", None, GET, status.HTTP_404_NOT_FOUND),
        ("/redoc", None, POST, status.HTTP_404_NOT_FOUND),
    ),
)
def test_status_codes(endpoint, data, method, status_code):
    """
    Test GET endpoints
    """
    if method == GET:
        response = client.get(endpoint, data=data)
    else:
        response = client.post(endpoint, data=data)
    assert response.status_code == status_code
