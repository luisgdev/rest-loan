""" REST API URLs """

from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from loanpro_api import views

urlpatterns = [
    path("customer/", views.CustomerCreateRead.as_view()),
    path("customer/<str:external_id>/", views.CustomerDetail.as_view()),
    path("customer/<str:external_id>/balance", views.CustomerBalanceRead.as_view()),
    path("customer/<str:external_id>/loans", views.CustomerLoansRead.as_view()),
    path("loan/", views.LoanCreateRead.as_view()),
    path("loan/<str:external_id>/", views.LoanDetail.as_view()),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"),
]
