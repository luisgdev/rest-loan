""" Serializers module """

from rest_framework import serializers

from loanpro_api.constants import LoanStatus
from loanpro_api.models import Customer, Loan, Payment, PaymentDetail


class CustomerSerializer(serializers.ModelSerializer):
    """Serializer for customer objects"""

    class Meta:
        model = Customer
        fields = (
            "external_id",
            "status",
            "score",
            "preapproved_at",
        )
        read_only_fields = (
            "created_at",
            "status",
        )

    def validate(self, attrs):
        """
        Custom attrs validation.
        """
        if attrs.get("score") < 0:  # TODO: Definir valor minimo para `score`.
            raise serializers.ValidationError("Score cannot be a negative number.")
        return attrs


class CustomerBalanceSerializer(serializers.ModelSerializer):
    """Serializer for customer objects"""

    class Meta:
        model = Customer
        fields = (
            "external_id",
            "score",
        )
        read_only_fields = ("created_at",)

    def to_representation(self, instance):
        """Override function."""
        data = super().to_representation(instance)
        total_debt = _get_customer_total_debt(customer_id=instance.id)
        data["available_amount"] = f"{float(instance.score) - total_debt:.2f}"
        data["total_debt"] = str(_get_customer_total_debt(customer_id=instance.id))
        return data


class LoanSerializer(serializers.ModelSerializer):
    """Serializer to read loan objects"""

    class Meta:
        model = Loan
        fields = (
            "external_id",
            "customer_id",
            "amount",
            "outstanding",
            "status",
            "maximum_payment_date",
        )
        read_only_fields = (
            "created_at",
            "status",
            "outstanding",
        )

    def validate(self, attrs):
        """
        Custom validation to create a Loan.
        """
        if attrs.get("amount") <= 0:
            raise serializers.ValidationError("Invalid amount value.")
        attrs["outstanding"] = attrs.get("amount")

        customer = Customer.objects.get(id=attrs.get("customer_id").id)
        customer_total_debt = _get_customer_total_debt(
            customer_id=attrs.get("customer_id").id
        )
        if float(attrs.get("amount")) + customer_total_debt > customer.score:
            raise serializers.ValidationError(
                f"Available amount is: {float(customer.score) - customer_total_debt}"
            )
        return attrs


class LoanCreateSerializer(serializers.ModelSerializer):
    """Serializer to create loan objects"""

    class Meta:
        model = Loan
        fields = (
            "external_id",
            "customer_id",
            "amount",
            "status",
            "maximum_payment_date",
        )
        read_only_fields = ("created_at",)


class PaymentSerializer(serializers.ModelSerializer):
    """Serializer for payment"""

    class Meta:
        model = Payment
        fields = "__all__"
        read_only_fields = ("created_at",)


class PaymentDetailSerializer(serializers.ModelSerializer):
    """Serializer for payment detail"""

    class Meta:
        model = PaymentDetail
        fields = "__all__"
        read_only_fields = ("created_at",)


def _get_customer_total_debt(customer_id: int) -> float:
    """
    Calculate the total debt for a given user.
    """
    return float(
        sum(
            loan.outstanding
            for loan in Loan.objects.filter(customer_id=customer_id)
            if loan.status in (LoanStatus.PENDING, LoanStatus.ACTIVE)
        )
    )
