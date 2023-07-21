from django.db import models


class BaseModel(models.Model):  # TODO: Fix fields with datetime.
    """ Common properties among our models """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.SmallIntegerField()
    external_id = models.CharField(max_length=60, unique=True)

    class Meta:
        """ No table will be created for this model """
        abstract = True


class Customer(BaseModel):
    """ Customers model """
    score = models.DecimalField(max_digits=12, decimal_places=2)
    preapproved_at = models.DateTimeField(auto_now=False, auto_now_add=False)


class Loan(BaseModel):
    """ Loan model """
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    contract_version = models.CharField(max_length=30, blank=True)
    maximum_payment_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    taken_at = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    outstanding = models.DecimalField(max_digits=12, decimal_places=2)


class Payment(BaseModel):
    """ Payment model """
    total_amount = models.DecimalField(max_digits=20, decimal_places=10)
    paid_at = models.DateTimeField(auto_now=False, auto_now_add=False)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)


class PaymentDetail(BaseModel):
    """ Payment detail model """
    amount = models.DecimalField(max_digits=20, decimal_places=10)
    loan_id = models.ForeignKey(Loan, on_delete=models.CASCADE)
    payment_id = models.ForeignKey(Payment, on_delete=models.CASCADE)
    external_id = None
    status = None
