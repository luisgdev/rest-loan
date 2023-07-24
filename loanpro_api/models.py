from django.db import models
from django.utils import timezone

from loanpro_api.constants import StatusForCustomer, StatusForLoan, StatusForPayment


class BaseModel(models.Model):
    """ Common properties among our models. """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    external_id = models.CharField(max_length=60, unique=True)

    class Meta:
        """ No table will be created for this model. """

        abstract = True


class Customer(BaseModel):
    """ Customer model. """

    status = models.SmallIntegerField(
        default=StatusForCustomer.ACTIVE,
        choices=[(item.value, item.name) for item in StatusForCustomer],
    )
    score = models.DecimalField(max_digits=12, decimal_places=2)
    preapproved_at = models.DateTimeField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return f"{self.external_id} ({self.id})"


class Loan(BaseModel):
    """ Loan model. """

    status = models.SmallIntegerField(
        default=StatusForLoan.PENDING,
        choices=[(item.value, item.name) for item in StatusForLoan],
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    contract_version = models.CharField(max_length=30, blank=True)
    maximum_payment_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    taken_at = models.DateTimeField(
        auto_now=False, auto_now_add=False, blank=True, default=timezone.now
    )
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    outstanding = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return self.external_id


class Payment(BaseModel):
    """ Payment model. """

    status = models.SmallIntegerField(
        choices=[(item.value, item.name) for item in StatusForPayment],
    )
    total_amount = models.DecimalField(max_digits=20, decimal_places=10)
    paid_at = models.DateTimeField(auto_now=False, auto_now_add=False)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)


class PaymentDetail(BaseModel):
    """ Payment detail model. """

    amount = models.DecimalField(max_digits=20, decimal_places=10)
    loan_id = models.ForeignKey(Loan, on_delete=models.CASCADE)
    payment_id = models.ForeignKey(Payment, on_delete=models.CASCADE)
    external_id = None
