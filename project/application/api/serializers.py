from rest_framework import serializers
from application.models import (
    Application, 
    ApplicationCompanyInfo, 
    ApplicationSupplyChainPartner, 
    ApplicationProduct,
    BulkSubmission
)


class ApplicationProductSerializer(serializers.ModelSerializer):
    """
    Serializer for ApplicationProduct model.
    
    Handles serialization/deserialization of product information within applications,
    including supply chain partner relationships and approval status.
    """
    
    class Meta:
        model = ApplicationProduct
        fields = [
            'id',
            'supply_chain_partner_name_raw',
            'product_name', 
            'product_category',
            'raw_materials_list',
            'is_approved',
            'rejection_reason'
        ]
        read_only_fields = ['id', 'is_approved', 'rejection_reason']


class ApplicationSupplyChainPartnerSerializer(serializers.ModelSerializer):
    """
    Serializer for ApplicationSupplyChainPartner model.
    
    Handles serialization/deserialization of supply chain partner data
    including nested product information and location details.
    """
    
    products = ApplicationProductSerializer(many=True, required=False)
    
    class Meta:
        model = ApplicationSupplyChainPartner
        fields = [
            'id',
            'name',
            'address',
            'city',
            'state', 
            'zip_code',
            'country',
            'products',
            'is_approved',
            'rejection_reason'
        ]
        read_only_fields = ['id', 'is_approved', 'rejection_reason']


class ApplicationCompanyInfoSerializer(serializers.ModelSerializer):
    """
    Serializer for ApplicationCompanyInfo model.
    
    Handles serialization/deserialization of company information
    including business location and approval status.
    """
    
    class Meta:
        model = ApplicationCompanyInfo
        fields = [
            'id',
            'name',
            'address',
            'city',
            'state',
            'zip_code',
            'country',
            'is_approved',
            'rejection_reason'
        ]
        read_only_fields = ['id', 'is_approved', 'rejection_reason']


class ApplicationSerializer(serializers.ModelSerializer):
    """
    Serializer for Application model.
    
    Handles complete application serialization including nested company information
    and supply chain partners with their products. Supports creation of complex
    nested application structures.
    """
    
    company_info = ApplicationCompanyInfoSerializer()
    supply_chain_partners = ApplicationSupplyChainPartnerSerializer(many=True)
    
    class Meta:
        model = Application
        fields = [
            'id',
            'name',
            'description',
            'submission_date',
            'status',
            'file',
            'rejection_reason',
            'company_info',
            'supply_chain_partners'
        ]
        read_only_fields = [
            'id', 
            'submission_date', 
            'status', 
            'rejection_reason'
        ]
    
    def create(self, validated_data):
        """
        Create an Application instance with nested company information,
        supply chain partners, and their associated products.
        
        Args:
            validated_data: Validated data containing application information
                          and nested company_info and supply_chain_partners data
            
        Returns:
            Application: The created Application instance with all nested relationships
        """
        company_info_data = validated_data.pop('company_info')
        supply_chain_partners_data = validated_data.pop('supply_chain_partners')
        
        application = Application.objects.create(**validated_data)
        
        ApplicationCompanyInfo.objects.create(
            application=application,
            **company_info_data
        )
        
        for partner_data in supply_chain_partners_data:
            products_data = partner_data.pop('products', [])
            
            partner = ApplicationSupplyChainPartner.objects.create(
                application=application,
                **partner_data
            )
            
            for product_data in products_data:
                ApplicationProduct.objects.create(
                    supply_chain_partner=partner,
                    **product_data
                )
        
        return application
