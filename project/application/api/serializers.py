from rest_framework import serializers
from application.models import (
    Application, 
    ApplicationCompanyInfo, 
    ApplicationSupplyChainPartner, 
    ApplicationProduct,
    BulkSubmission
)


class ApplicationProductSerializer(serializers.ModelSerializer):
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
        Create Application with nested company_info and supply_chain_partners
        """
        # Extract nested data
        company_info_data = validated_data.pop('company_info')
        supply_chain_partners_data = validated_data.pop('supply_chain_partners')
        
        # Create main Application instance
        application = Application.objects.create(**validated_data)
        
        # Create CompanyInfo (OneToOne relationship)
        ApplicationCompanyInfo.objects.create(
            application=application,
            **company_info_data
        )
        
        # Create SupplyChainPartners and their Products
        for partner_data in supply_chain_partners_data:
            # Extract products data if it exists
            products_data = partner_data.pop('products', [])
            
            # Create SupplyChainPartner
            partner = ApplicationSupplyChainPartner.objects.create(
                application=application,
                **partner_data
            )
            
            # Create Products for this partner
            for product_data in products_data:
                ApplicationProduct.objects.create(
                    application=application,
                    **product_data
                )
        
        return application


class BulkSubmissionSerializer(serializers.ModelSerializer):
    applications = ApplicationSerializer(many=True, read_only=True)
    
    class Meta:
        model = BulkSubmission
        fields = [
            'id',
            'name',
            'description',
            'status',
            'created_at',
            'updated_at',
            'error_message',
            'error_details',
            'applications'
        ]
        read_only_fields = [
            'id', 
            'created_at', 
            'updated_at', 
            'error_message', 
            'error_details',
            'applications'
        ]