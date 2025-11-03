from rest_framework import serializers
from application.models import (
    Application, 
    ApplicationCompanyInfo, 
    ApplicationSupplyChainPartner, 
    ApplicationProduct
)


class ApplicationProductSerializer(serializers.ModelSerializer):
    """
    Serializer for ApplicationProduct model.
    
    Handles serialization/deserialization of product information within applications,
    including product details, raw materials, and approval status.
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
    
    Handles serialization/deserialization of supply chain partner information
    including their location details and associated products.
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
    including company location details and approval status.
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
    Main Application serializer that handles complete application data.
    
    Manages the nested structure of applications including company information
    and multiple supply chain partners with their respective products.
    Provides creation of entire application hierarchy in a single operation.
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
                    application=application,
                    **product_data
                )
        
        return application