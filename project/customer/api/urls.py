from django.urls import path
from .views import CustomerProfileCreateAPIView, CompanyViewSet

urlpatterns = [
    path('customer-profiles/create/', CustomerProfileCreateAPIView.as_view(), name='customer-profile-create'),
    path('companies/', CompanyViewSet.as_view({'get': 'list'}), name='company-list'),
]