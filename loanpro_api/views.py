""" API views module """

from rest_framework import generics, mixins, permissions
from rest_framework.authentication import (
    BasicAuthentication,
    SessionAuthentication,
    TokenAuthentication,
)
from rest_framework.response import Response

from loanpro_api.models import Customer, Loan
from loanpro_api.serializers import (
    CustomerBalanceSerializer,
    CustomerLoansSerializer,
    CustomerSerializer,
    LoanSerializer,
)


class CustomerCreateRead(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):
    """ List and register customers. """

    queryset = Customer.objects.all()
    authentication_classes = (
        TokenAuthentication,
        BasicAuthentication,
        SessionAuthentication,
    )
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CustomerSerializer

    def get(self, request, *args, **kwargs):
        """ List objects. """
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """ Create an object. """
        return self.create(request, *args, **kwargs)


class CustomerBalanceRead(mixins.RetrieveModelMixin, generics.GenericAPIView):
    """ Return customer balance information. """

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
        """ Get Customer balance info. """
        return self.retrieve(request, *args, **kwargs)


class CustomerLoansRead(mixins.ListModelMixin, generics.GenericAPIView):
    """ List Customer loans. """

    lookup_field = "external_id"
    queryset = Loan.objects.all()
    authentication_classes = (
        TokenAuthentication,
        BasicAuthentication,
        SessionAuthentication,
    )
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CustomerLoansSerializer

    def list(self, request, *args, **kwargs):
        """ Override function. """
        self.queryset = self.queryset.filter(
            customer_id=Customer.objects.get(
                external_id=self.kwargs.get("external_id")
            ).id
        )
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get(self, request, *args, **kwargs):
        """ Customer loans info. """
        return self.list(request, *args, **kwargs)


class CustomerDetail(
    mixins.RetrieveModelMixin,
    generics.GenericAPIView,
):
    """ Return Customer details. """

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
        """ Get customer details. """
        return self.retrieve(request, *args, **kwargs)


class LoanCreateRead(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):
    """ List and register Loans. """

    queryset = Loan.objects.all()
    authentication_classes = (
        TokenAuthentication,
        BasicAuthentication,
        SessionAuthentication,
    )
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = LoanSerializer

    def get(self, request, *args, **kwargs):
        """ Get all objects. """
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """ Create an object. """
        return self.create(request, *args, **kwargs)


class LoanDetail(
    mixins.RetrieveModelMixin,
    generics.GenericAPIView,
):
    """ Return Loan details. """

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
        """ Get certain object. """
        return self.retrieve(request, *args, **kwargs)
