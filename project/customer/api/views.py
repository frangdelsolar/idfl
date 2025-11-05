from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiExample, OpenApiResponse
from .serializers import CustomerProfileSerializer, CompanySerializer
from customer.models import Company


@extend_schema_view(
    post=extend_schema(
        summary="Create customer profile",
        description="Create a new customer profile with user account. The user will be assigned to the 'Customer' group and their password will be set to their username.",
        request=CustomerProfileSerializer,
        responses={
            201: OpenApiResponse(
                response=CustomerProfileSerializer,
                description="Customer profile created successfully",
                examples=[
                    OpenApiExample(
                        'Success Response',
                        value={
                            "id": 1,
                            "user_id": 5,
                            "username": "johndoe",
                            "email": "john.doe@example.com",
                            "first_name": "John",
                            "last_name": "Doe",
                            "company": "Example Company",
                            "company_id": 1,
                            "phone_number": "+1234567890",
                            "groups": ["Customer"],
                            "role": "Customer",
                            "message": "User \"johndoe\" created successfully with Customer role"
                        },
                        response_only=True
                    )
                ]
            ),
            400: OpenApiResponse(
                description="Bad request - validation error",
                examples=[
                    OpenApiExample(
                        'Validation Error',
                        value={
                            "company_id": ["Company with this ID does not exist."],
                            "username": ["A user with this username already exists."],
                            "email": ["A user with this email already exists."]
                        }
                    )
                ]
            ),
            401: OpenApiResponse(
                description="Authentication required"
            )
        },
        examples=[
            OpenApiExample(
                'Create Request Example',
                value={
                    "company_id": 1,
                    "first_name": "John",
                    "last_name": "Doe", 
                    "email": "john.doe@example.com",
                    "username": "johndoe",
                    "phone_number": "+1234567890"
                },
                request_only=True
            ),
            OpenApiExample(
                'Minimal Request Example',
                value={
                    "company_id": 1,
                    "first_name": "Jane",
                    "last_name": "Smith",
                    "email": "jane.smith@example.com", 
                    "username": "janesmith"
                },
                request_only=True
            )
        ]
    )
)
class CustomerProfileCreateAPIView(generics.CreateAPIView):
    """
    API endpoint for creating customer profiles with user accounts.
    
    Creates a new Django user account and links it to a customer profile with the following behavior:
    - Validates that the company exists
    - Checks for unique username and email
    - Creates user with password set to username
    - Assigns user to 'Customer' group
    - Links user to the specified company
    - Creates customer profile with optional phone number
    """
    
    serializer_class = CustomerProfileSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        customer_profile = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

@extend_schema_view(
    list=extend_schema(
        summary="List companies",
        description="Retrieve a list of all companies with basic information.",
        responses={
            200: OpenApiResponse(
                response=CompanySerializer,
                description="List of companies retrieved successfully",
                examples=[
                    OpenApiExample(
                        'Success Response',
                        value=[
                            {
                                "id": 1,
                                "name": "EcoFiber Textiles Inc.",
                                "address": {
                                    "id": 1,
                                    "address": "123 Green Street",
                                    "city": "Portland",
                                    "state": "Oregon",
                                    "zip_code": "97205",
                                    "country": "United States"
                                }
                            },
                            {
                                "id": 2,
                                "name": "Sustainable Materials Co.",
                                "address": {
                                    "id": 2,
                                    "address": "456 Eco Avenue",
                                    "city": "Seattle",
                                    "state": "Washington", 
                                    "zip_code": "98101",
                                    "country": "United States"
                                }
                            }
                        ],
                        response_only=True
                    )
                ]
            )
        }
    ),
    retrieve=extend_schema(
        summary="Retrieve company",
        description="Get detailed information about a specific company by ID.",
        responses={
            200: OpenApiResponse(
                response=CompanySerializer,
                description="Company details retrieved successfully",
                examples=[
                    OpenApiExample(
                        'Success Response',
                        value={
                            "id": 1,
                            "name": "EcoFiber Textiles Inc.",
                            "users": [
                                {
                                    "id": 1,
                                    "username": "admin",
                                    "first_name": "John",
                                    "last_name": "Doe",
                                    "email": "john.doe@ecofiber.com"
                                }
                            ],
                            "address": {
                                "id": 1,
                                "address": "123 Green Street",
                                "city": "Portland",
                                "state": "Oregon",
                                "zip_code": "97205",
                                "country": "United States"
                            },
                            "customer_profiles": [
                                {
                                    "id": 1,
                                    "user": {
                                        "id": 2,
                                        "username": "customer1",
                                        "first_name": "Jane",
                                        "last_name": "Smith",
                                        "email": "jane.smith@ecofiber.com"
                                    },
                                    "phone_number": "+1234567890"
                                }
                            ]
                        },
                        response_only=True
                    )
                ]
            ),
            404: OpenApiResponse(
                description="Company not found"
            )
        }
    )
)
class CompanyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for viewing companies.
    
    Provides read-only operations to list and retrieve company information.
    Companies can be associated with multiple users and customer profiles.
    """
    queryset = Company.objects.all()
    serializer_class = CompanySerializer