""" Constants for tests """

from enum import Enum


class SampleAuth(str, Enum):
    """ Sample temporary user for testing purposes. """
    USER: str = "user1"
    PASS: str = "pass123"


VALID_DATE: str = "2023-07-20"
MAX_AMOUNT_SAMPLE: str = "100"

GET: str = "get"
POST: str = "post"
CUSTOMER_ENDPOINT: str = "/api/customer/"
DOCS_ENDPOINT: str = "/api/docs/"
LOAN_ENDPOINT: str = "/api/loan/"

AUTH_MISSING: str = "Authentication credentials were not provided."
INVALID_AMOUNT: str = "A valid number is required."
INVALID_DATE: str = "Datetime has wrong format."
REQUIRED_IS_BLANK: str = "This field may not be blank."
REQUIRED_IS_MISSING: str = "This field is required."
AMOUNT_LIMITED: str = f"Available amount is: {MAX_AMOUNT_SAMPLE}"
CUSTOMER_SAMPLE: dict = {
    "external_id": "c1",
    "score": MAX_AMOUNT_SAMPLE,
    "preapproved_at": VALID_DATE,
}
