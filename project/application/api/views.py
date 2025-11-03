from rest_framework import viewsets
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiExample
from application.api.serializers import ApplicationSerializer
from application.models import Application


@extend_schema_view(
    list=extend_schema(
        summary="List all applications",
        description="Retrieve a list of all certification applications with their nested data.",
        examples=[
            OpenApiExample(
                'Success Response',
                value=[
                    {
                        "id": 1,
                        "name": "EcoFiber Textiles Application",
                        "description": "Well-prepared application with sustainable materials",
                        "submission_date": "2025-11-03T13:12:37.824203Z",
                        "status": "in_review",
                        "file": None,
                        "rejection_reason": None,
                        "company_info": {
                            "id": 1,
                            "name": "EcoFiber Textiles Inc.",
                            "address": "123 Green Street",
                            "city": "Portland",
                            "state": "Oregon", 
                            "zip_code": "97205",
                            "country": "United States",
                            "is_approved": True,
                            "rejection_reason": None
                        },
                        "supply_chain_partners": [
                            {
                                "id": 1,
                                "name": "Sustainable Yarn Co.",
                                "address": "456 Eco Avenue",
                                "city": "Seattle", 
                                "state": "Washington",
                                "zip_code": "98101",
                                "country": "United States",
                                "is_approved": True,
                                "rejection_reason": None,
                                "products": [
                                    {
                                        "id": 1,
                                        "supply_chain_partner_name_raw": "Sustainable Yarn Co.",
                                        "product_name": "Organic Cotton T-Shirt",
                                        "product_category": "Apparel",
                                        "raw_materials_list": "Organic cotton, Natural dyes",
                                        "is_approved": True,
                                        "rejection_reason": None
                                    }
                                ]
                            }
                        ]
                    }
                ],
                response_only=True
            )
        ]
    ),
    create=extend_schema(
        summary="Create new application",
        description="Create a new product certification application with nested company info and supply chain partners.",
        examples=[
            OpenApiExample(
                'Create Request',
                value={
                    "name": "API DEMO - Eco Fabrics Inc Application",
                    "description": "Sustainable textile company - Submitted via REST API",
                    "company_info": {
                        "name": "API DEMO - Eco Fabrics Inc", 
                        "address": "123 API Integration Street",
                        "city": "Portland",
                        "state": "Oregon",
                        "zip_code": "97205",
                        "country": "United States"
                    },
                    "supply_chain_partners": [
                        {
                            "name": "API DEMO - Organic Cotton Co-op",
                            "address": "456 RESTful Road", 
                            "city": "Austin",
                            "state": "Texas",
                            "zip_code": "73301",
                            "country": "United States",
                            "products": [
                                {
                                    "supply_chain_partner_name_raw": "API DEMO - Organic Cotton Co-op",
                                    "product_name": "Organic Cotton T-Shirt",
                                    "product_category": "Apparel",
                                    "raw_materials_list": "Organic cotton, Natural dyes"
                                }
                            ]
                        }
                    ]
                },
                request_only=True
            )
        ]
    ),
    retrieve=extend_schema(
        summary="Retrieve application",
        description="Get detailed information about a specific application by ID."
    ),
    update=extend_schema(
        summary="Update application", 
        description="Full update of an existing application."
    ),
    partial_update=extend_schema(
        summary="Partial update application",
        description="Update specific fields of an application."
    ),
    destroy=extend_schema(
        summary="Delete application",
        description="Remove an application from the system."
    )
)
class ApplicationViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing product certification applications.
    
    Provides complete CRUD operations for applications including nested
    company information, supply chain partners, and their products.
    """
    
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer