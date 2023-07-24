""" Test Customer endpoints """

import pytest
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient

from loanpro_api.constants import StatusForCustomer
from tests.constants import CUSTOMER_ENDPOINT, VALID_DATE, SampleAuth

client = APIClient()


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("ext_id", "score", "date", "status_code"),
    (
        # Valid input
        ("id1", "1", VALID_DATE, status.HTTP_201_CREATED),
        ("001", "2", VALID_DATE, status.HTTP_201_CREATED),
        ("ct_01", "3", VALID_DATE, status.HTTP_201_CREATED),
        ("x", "100.00", VALID_DATE, status.HTTP_201_CREATED),
        ("1", "1000.0", VALID_DATE, status.HTTP_201_CREATED),
        # Invalid id
        ("", "210.00", VALID_DATE, status.HTTP_400_BAD_REQUEST),
        # Invalid score
        ("id1", "x", VALID_DATE, status.HTTP_400_BAD_REQUEST),
        ("id1", "-10.00", VALID_DATE, status.HTTP_400_BAD_REQUEST),
        ("id1", "", VALID_DATE, status.HTTP_400_BAD_REQUEST),
        # Invalid date
        ("id1", "300", "23-01-01", status.HTTP_400_BAD_REQUEST),
        ("id1", "300", "3-01-01", status.HTTP_400_BAD_REQUEST),
        ("id1", "300", "01-01", status.HTTP_400_BAD_REQUEST),
    ),
)
def test_api_customer(ext_id, score, date, status_code):
    """
    Test customer endpoints
    """
    User.objects.create_user(username=SampleAuth.USER, password=SampleAuth.PASS)
    client.login(username=SampleAuth.USER, password=SampleAuth.PASS)
    params = {
        "external_id": ext_id,
        "score": score,
        "preapproved_at": date,
    }
    post_response = client.post(CUSTOMER_ENDPOINT, data=params)
    get_response = client.get(f"{CUSTOMER_ENDPOINT}{ext_id}")
    balance_response = client.get(f"{CUSTOMER_ENDPOINT}{ext_id}/balance")
    assert post_response.status_code == status_code
    if status == status.HTTP_201_CREATED:
        assert get_response.status_code == status.HTTP_200_OK
        assert get_response.data.status == StatusForCustomer.ACTIVE
        assert balance_response.status_code == status.HTTP_200_OK
    if status == status.HTTP_400_BAD_REQUEST:
        assert get_response.status_code == status.HTTP_404_NOT_FOUND
        assert balance_response.status_code == status.HTTP_404_NOT_FOUND
    client.logout()
