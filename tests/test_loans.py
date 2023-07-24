""" Test Customer endpoints """

import pytest
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient

from loanpro_api.constants import StatusForLoan
from tests.constants import (
    AMOUNT_LIMITED,
    CUSTOMER_ENDPOINT,
    CUSTOMER_SAMPLE,
    INVALID_AMOUNT,
    INVALID_DATE,
    LOAN_ENDPOINT,
    MAX_AMOUNT_SAMPLE,
    REQUIRED_IS_BLANK,
    REQUIRED_IS_MISSING,
    SampleAuth,
)

client = APIClient()

# Constants


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("loan", "status_code", "error_field", "error_message"),
    (
        # Valid input, accepted amount: Loan amount <= Customer score
        (
            {
                "external_id": "ln01",
                "amount": "54",
                "maximum_payment_date": "20230823",
            },
            status.HTTP_201_CREATED,
            None,
            None,
        ),
        (
            {
                "external_id": "ln03",
                "amount": "28",
                "maximum_payment_date": "20230823",
            },
            status.HTTP_201_CREATED,
            None,
            None,
        ),
        (
            {
                "external_id": "ln03",
                "amount": MAX_AMOUNT_SAMPLE,
                "maximum_payment_date": "20230823",
            },
            status.HTTP_201_CREATED,
            None,
            None,
        ),
        # Valid input, unaccepted amount: Loan amount > Customer score
        (
            {
                "external_id": "ln02",
                "amount": "110",
                "maximum_payment_date": "20230823",
            },
            status.HTTP_400_BAD_REQUEST,
            "non_field_errors",
            AMOUNT_LIMITED,
        ),
        (
            {
                "external_id": "ln04",
                "amount": "100.01",
                "maximum_payment_date": "20230823",
            },
            status.HTTP_400_BAD_REQUEST,
            "non_field_errors",
            AMOUNT_LIMITED,
        ),
        # Invalid input
        (
            {
                "external_id": "ln04",
                "amount": "10",
                "maximum_payment_date": "bar",
            },
            status.HTTP_400_BAD_REQUEST,
            "maximum_payment_date",
            INVALID_DATE,
        ),
        (
            {
                "external_id": "ln04",
                "amount": "foo",
                "maximum_payment_date": "20230823",
            },
            status.HTTP_400_BAD_REQUEST,
            "amount",
            INVALID_AMOUNT,
        ),
        (
            {
                "external_id": "ln04",
                "amount": "",
                "maximum_payment_date": "20230823",
            },
            status.HTTP_400_BAD_REQUEST,
            "amount",
            INVALID_AMOUNT,
        ),
        (
            {
                "external_id": "1",
                "amount": "22",
                "maximum_payment_date": "",
            },
            status.HTTP_400_BAD_REQUEST,
            "maximum_payment_date",
            INVALID_DATE,
        ),
        (
            {
                "external_id": "",
                "amount": "22",
                "maximum_payment_date": "20230823",
            },
            status.HTTP_400_BAD_REQUEST,
            "external_id",
            REQUIRED_IS_BLANK,
        ),
        # Missing fields
        (
            {
                "external_id": "ln04",
                "maximum_payment_date": "20230823",
            },
            status.HTTP_400_BAD_REQUEST,
            "amount",
            REQUIRED_IS_MISSING,
        ),
        (
            {
                "amount": "22",
                "maximum_payment_date": "20230823",
            },
            status.HTTP_400_BAD_REQUEST,
            "external_id",
            REQUIRED_IS_MISSING,
        ),
        (
            {
                "external_id": "ln04",
                "amount": "22",
            },
            status.HTTP_400_BAD_REQUEST,
            "maximum_payment_date",
            REQUIRED_IS_MISSING,
        ),
    ),
)
def test_api_loan(loan, status_code, error_message, error_field):
    """
    Test customer endpoints
    """
    User.objects.create_user(username=SampleAuth.USER, password=SampleAuth.PASS)
    client.login(username=SampleAuth.USER, password=SampleAuth.PASS)
    create_customer = client.post(
        CUSTOMER_ENDPOINT,
        data=CUSTOMER_SAMPLE,
    )
    loan["customer_id"] = create_customer.data["id"]
    create_loan = client.post(LOAN_ENDPOINT, data=loan)
    assert create_customer.status_code == status.HTTP_201_CREATED
    assert create_loan.status_code == status_code
    if status_code == status.HTTP_201_CREATED:
        assert create_loan.data["outstanding"] == create_loan.data["amount"]
        assert create_loan.data["status"] == StatusForLoan.PENDING
    if status_code == status.HTTP_400_BAD_REQUEST:
        assert error_message in create_loan.data[error_field][0]
    client.logout()
