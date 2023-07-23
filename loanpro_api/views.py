""" API views module """

from rest_framework import generics, mixins, permissions
from rest_framework.authentication import (
    BasicAuthentication,
    SessionAuthentication,
    TokenAuthentication,
)

from loanpro_api.models import Customer, Loan, Payment
from loanpro_api.serializers import (
    CustomerBalanceSerializer,
    CustomerSerializer,
    LoanCreateSerializer,
    LoanSerializer,
    PaymentSerializer,
)


class CustomerCreateRead(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):
    """
    List and register customers.
    """

    queryset = Customer.objects.all()
    authentication_classes = (
        TokenAuthentication,
        BasicAuthentication,
        SessionAuthentication,
    )
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CustomerSerializer

    def get(self, request, *args, **kwargs):
        """
        Get all objects.
        """
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Create an object.
        """
        return self.create(request, *args, **kwargs)


class CustomerBalanceRead(mixins.RetrieveModelMixin, generics.GenericAPIView):
    """Return customer balance."""

    lookup_field = "external_id"
    queryset = Customer.objects.all()
    authentication_classes = (
        TokenAuthentication,
        BasicAuthentication,
        SessionAuthentication,
    )
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CustomerBalanceSerializer

    def get(self, request, *args, **kwargs):
        """Customer balance info"""
        return self.retrieve(request, *args, **kwargs)


class CustomerDetail(
    mixins.RetrieveModelMixin,
    generics.GenericAPIView,
):
    """
    Return Customer details.
    """

    lookup_field = "external_id"
    queryset = Customer.objects.all()
    authentication_classes = (
        TokenAuthentication,
        BasicAuthentication,
        SessionAuthentication,
    )
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CustomerSerializer

    def get(self, request, *args, **kwargs):
        """
        Get certain object.
        """
        return self.retrieve(request, *args, **kwargs)


class LoanCreateRead(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):
    """
    List and register Loans.
    """

    queryset = Loan.objects.all()
    authentication_classes = (
        TokenAuthentication,
        BasicAuthentication,
        SessionAuthentication,
    )
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = LoanSerializer
    serializer_action_class = {
        "post": LoanCreateSerializer,
    }

    def get_serializer_class(self):
        """
        Select certain serializer depending on request method.
        """
        try:
            return self.serializer_action_class[self.request.method]
        except KeyError:
            return super().get_serializer_class()

    def get(self, request, *args, **kwargs):
        """
        Get all objects.
        """
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Create an object.
        """
        return self.create(request, *args, **kwargs)


class LoanDetail(
    mixins.RetrieveModelMixin,
    generics.GenericAPIView,
):
    """
    Return Loan details.
    """

    lookup_field = "external_id"
    queryset = Loan.objects.all()
    authentication_classes = (
        TokenAuthentication,
        BasicAuthentication,
        SessionAuthentication,
    )
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = LoanSerializer

    def get(self, request, *args, **kwargs):
        """
        Get certain object.
        """
        return self.retrieve(request, *args, **kwargs)
