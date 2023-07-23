""" Constants module """

from enum import Enum


class CustomerStatus(int, Enum):
    """
    Valid status for customers.
    """

    ACTIVE = 1
    INACTIVE = 2

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_


class LoanStatus(int, Enum):
    """
    Valid status for Loans.
    """

    PENDING = 1
    ACTIVE = 2
    REJECTED = 3
    PAID = 4

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_


class PaymentStatus(int, Enum):
    """
    Valid status for payments.
    """

    COMPLETED = 1
    REJECTED = 2
