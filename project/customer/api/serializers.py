from rest_framework import serializers
from django.contrib.auth.models import User, Group
from django.db import transaction
from customer.models import CustomerProfile, Company

class CustomerProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for creating customer profiles with associated user accounts.
    Creates User, assigns to Customer group, links to Company, and creates CustomerProfile.
    """
    company_id = serializers.IntegerField(write_only=True)
    first_name = serializers.CharField(max_length=30, write_only=True)
    last_name = serializers.CharField(max_length=30, write_only=True)
    email = serializers.EmailField(write_only=True)
    username = serializers.CharField(max_length=150, write_only=True)
    phone_number = serializers.CharField(max_length=20, required=False, allow_blank=True)
    
    class Meta:
        model = CustomerProfile
        fields = ['company_id', 'first_name', 'last_name', 'email', 'username', 'phone_number']
    
    def validate_company_id(self, value):
        try:
            company = Company.objects.get(id=value)
            self.context['company'] = company
            return value
        except Company.DoesNotExist:
            raise serializers.ValidationError("Company with this ID does not exist.")
    
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        return value
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value
    
    @transaction.atomic
    def create(self, validated_data):
        company_id = validated_data.pop('company_id')
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        email = validated_data.pop('email')
        username = validated_data.pop('username')
        phone_number = validated_data.get('phone_number', '')
        
        company = self.context['company']
        
        customer_group, created = Group.objects.get_or_create(name='Customer')
        
        user = User.objects.create_user(
            username=username,
            password=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            is_active=True
        )
        
        user.groups.add(customer_group)
        company.users.add(user)
        
        customer_profile = CustomerProfile.objects.create(
            user=user,
            company=company,
            phone_number=phone_number
        )
        
        return customer_profile
    
    def to_representation(self, instance):
        group_names = list(instance.user.groups.values_list('name', flat=True))
        
        return {
            'id': instance.id,
            'user_id': instance.user.id,
            'username': instance.user.username,
            'email': instance.user.email,
            'first_name': instance.user.first_name,
            'last_name': instance.user.last_name,
            'company': instance.company.name,
            'company_id': instance.company.id,
            'phone_number': instance.phone_number,
            'groups': group_names,
            'role': 'Customer',
            'message': f'User "{instance.user.username}" created successfully with Customer role'
        }

class CompanySerializer(serializers.ModelSerializer):
    """
    Serializer for Company model with basic information.
    """
    class Meta:
        model = Company
        fields = ['id', 'name', 'address', 'users', 'customer_profiles']
        