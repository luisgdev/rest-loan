from django.contrib import admin

from loanpro_api.models import Customer, Loan, Payment, PaymentDetail

# Register your models here.
admin.site.register(Customer)
admin.site.register(Loan)
admin.site.register(Payment)
admin.site.register(PaymentDetail)
