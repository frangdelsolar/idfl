from django.contrib.auth import get_user_model
from django.utils import timezone
from application.models import (
    Application, 
    ApplicationCompanyInfo,
    ApplicationSupplyChainPartner,
    ApplicationProduct, 
    BulkSubmission
)
from customer.models import Company, Address, SupplyChainCompany, CertificationBody, CustomerProfile

def create_company_info():
    """Create dummy company data for testing and demonstration."""
    
    # Create addresses first
    address1 = Address.objects.create(
        address="123 Green Street",
        city="Portland",
        state="Oregon",
        zip_code="97205",
        country="United States"
    )
    
    address2 = Address.objects.create(
        address="456 Eco Avenue",
        city="Seattle",
        state="Washington",
        zip_code="98101",
        country="United States"
    )
    
    address3 = Address.objects.create(
        address="789 Sustainable Lane",
        city="Austin",
        state="Texas",
        zip_code="73301",
        country="United States"
    )
    
    address4 = Address.objects.create(
        address="321 Innovation Drive",
        city="San Francisco",
        state="California",
        zip_code="94107",
        country="United States"
    )
    
    # Create companies
    company1 = Company.objects.create(
        name="EcoFiber Textiles Inc.",
        address=address1
    )
    
    company2 = Company.objects.create(
        name="Sustainable Materials Co.",
        address=address2
    )
    
    company3 = Company.objects.create(
        name="Green Manufacturing Partners",
        address=address3
    )
    
    company4 = Company.objects.create(
        name="BioTech Fabrics Corp.",
        address=address4
    )
    
    # Create supply chain companies
    supply_company1 = SupplyChainCompany.objects.create(
        name="Organic Cotton Co-op",
        is_valid=True,
        address=address1
    )
    
    supply_company2 = SupplyChainCompany.objects.create(
        name="Recycled Polyester Ltd.",
        is_valid=True,
        address=address2
    )
    
    supply_company3 = SupplyChainCompany.objects.create(
        name="Natural Dyes International",
        is_valid=False,
        address=address3
    )
    
    supply_company4 = SupplyChainCompany.objects.create(
        name="Sustainable Packaging Solutions",
        is_valid=True,
        address=address4
    )
    
    # Create certification bodies
    cert_body1 = CertificationBody.objects.create(
        name="Global Organic Textile Standard (GOTS)",
        address=address1
    )
    
    cert_body2 = CertificationBody.objects.create(
        name="Fair Trade Certified",
        address=address2
    )
    
    cert_body3 = CertificationBody.objects.create(
        name="Cradle to Cradle Certified",
        address=address3
    )
    
    # Create some customer profiles
    User = get_user_model()
    
    # Create demo users if they don't exist
    demo_user1, created = User.objects.get_or_create(
        username="demo_customer1",
        defaults={
            'email': 'customer1@ecofiber.com',
            'first_name': 'John',
            'last_name': 'Greenfield',
            'is_active': True
        }
    )
    demo_user1.set_password('demo123')
    demo_user1.save()
    
    demo_user2, created = User.objects.get_or_create(
        username="demo_customer2",
        defaults={
            'email': 'customer2@sustainable.com',
            'first_name': 'Sarah',
            'last_name': 'Ecofield',
            'is_active': True
        }
    )
    demo_user2.set_password('demo123')
    demo_user2.save()
    
    # Add users to companies
    company1.users.add(demo_user1)
    company2.users.add(demo_user2)
    
    # Create customer profiles
    customer_profile1 = CustomerProfile.objects.create(
        user=demo_user1,
        company=company1,
        phone_number="+1-503-555-0101"
    )
    
    customer_profile2 = CustomerProfile.objects.create(
        user=demo_user2,
        company=company2,
        phone_number="+1-206-555-0102"
    )
    
    return {
        'companies': [company1, company2, company3, company4],
        'supply_chain_companies': [supply_company1, supply_company2, supply_company3, supply_company4],
        'certification_bodies': [cert_body1, cert_body2, cert_body3],
        'customer_profiles': [customer_profile1, customer_profile2],
        'addresses': [address1, address2, address3, address4]
    }

def create_dummy_bulk_submissions():
    """Create dummy bulk submissions with applications."""
    application_file = "application_files/application_form.xlsx"
    
    draft_submission = BulkSubmission.objects.create(
        name="📦 BULK - Q4 Sustainability Applications Batch",
        description="Quarter 4 sustainability certification applications from various textile companies",
        status=BulkSubmission.Status.DRAFT
    )
    
    app1 = Application.objects.create(
        name="BULK - EcoWear Collective - Fall Collection",
        description="Sustainable fall fashion line using organic cotton and recycled materials",
        status=Application.Status.PENDING,
        bulk_submissions=draft_submission,
        file=application_file
    )
    
    app2 = Application.objects.create(
        name="BULK - Green Threads Manufacturing", 
        description="Bulk application for manufacturing facility certification",
        status=Application.Status.PENDING,
        bulk_submissions=draft_submission,
        file=application_file
    )
    
    processing_submission = BulkSubmission.objects.create(
        name="🚀 BULK - Active Processing - Textile Partners",
        description="Currently processing applications from supply chain partners",
        status=BulkSubmission.Status.PROCESSING
    )
    
    app3 = Application.objects.create(
        name="BULK - Sustainable Dye House Ltd.",
        description="Application for eco-friendly dyeing processes certification",
        status=Application.Status.IN_REVIEW,
        bulk_submissions=processing_submission,
        file=application_file
    )
    
    success_submission = BulkSubmission.objects.create(
        name="✅ BULK - Completed - Q3 Approvals",
        description="Successfully processed and approved Q3 applications",
        status=BulkSubmission.Status.SUCCESS
    )
    
    app4 = Application.objects.create(
        name="BULK - Organic Cotton Co-op",
        description="Organic cotton farming cooperative certification",
        status=Application.Status.APPROVED,
        bulk_submissions=success_submission,
        file=application_file
    )
    
    app5 = Application.objects.create(
        name="BULK - Recycled Polyester Inc.",
        description="Post-consumer polyester recycling facility",
        status=Application.Status.APPROVED, 
        bulk_submissions=success_submission,
        file=application_file
    )
    
    failed_submission = BulkSubmission.objects.create(
        name="❌ BULK - Failed - Compliance Issues",
        description="Batch failed due to documentation and compliance problems",
        status=BulkSubmission.Status.FAIL,
        error_message="Multiple applications missing required sustainability documentation",
        error_details={"missing_docs": 3, "compliance_issues": 5}
    )
    
    app6 = Application.objects.create(
        name="BULK - Problematic Textiles LLC",
        description="Application with multiple compliance violations",
        status=Application.Status.REJECTED,
        bulk_submissions=failed_submission
    )
    
    return [draft_submission, processing_submission, success_submission, failed_submission]

def create_to_be_submitted_application():
    """Create a dummy application for Customer Service to submit."""
    application = Application.objects.create(
        name="📝 TO BE SUBMITTED - Fresh Start Apparel Application",
        description="New application ready for Customer Service review and submission.",
        status='pending'
    )
    
    ApplicationCompanyInfo.objects.create(
        application=application,
        name="Fresh Start Apparel Co.",
        address="111 New Beginnings Lane",
        city="Austin",
        state="Texas",
        zip_code="73301",
        country="United States"
    )
    
    ApplicationSupplyChainPartner.objects.create(
        application=application,
        name="Eco Threads Manufacturing",
        address="222 Sustainable Street",
        city="Denver",
        state="Colorado", 
        zip_code="80202",
        country="United States"
    )
    
    ApplicationSupplyChainPartner.objects.create(
        application=application,
        name="Green Stitch Workshops",
        address="333 Eco-Friendly Avenue",
        city="Portland",
        state="Oregon",
        zip_code="97201", 
        country="United States"
    )
    
    ApplicationProduct.objects.create(
        application=application,
        supply_chain_partner_name_raw="Eco Threads Manufacturing",
        product_name="Bamboo Fiber T-Shirt",
        product_category="Men's apparel",
        raw_materials_list="Organic bamboo, Recycled polyester labels, Natural dyes"
    )
    
    ApplicationProduct.objects.create(
        application=application,
        supply_chain_partner_name_raw="Eco Threads Manufacturing", 
        product_name="Recycled Denim Jeans",
        product_category="Bottoms",
        raw_materials_list="Recycled cotton, Recycled metal buttons, Plant-based indigo"
    )
    
    ApplicationProduct.objects.create(
        application=application,
        supply_chain_partner_name_raw="Green Stitch Workshops",
        product_name="Organic Linen Dress",
        product_category="Women's apparel", 
        raw_materials_list="Organic linen, Recycled silk trim, Natural pigments"
    )
    
    return application

def create_to_be_approved_application():
    """Create a dummy application that will be easily approved."""
    application = Application.objects.create(
        name="✅ TO BE APPROVED - EcoFiber Textiles Application",
        description="Well-prepared application with all sustainable materials and proper documentation.",
        submission_date=timezone.now(),
        status='in_review'
    )
    
    ApplicationCompanyInfo.objects.create(
        application=application,
        name="EcoFiber Textiles Inc.",
        address="123 Green Street",
        city="Portland",
        state="Oregon",
        zip_code="97205",
        country="United States",
        is_approved=True
    )
    
    ApplicationSupplyChainPartner.objects.create(
        application=application,
        name="Sustainable Yarn Co.",
        address="456 Eco Avenue",
        city="Seattle",
        state="Washington", 
        zip_code="98101",
        country="United States",
        is_approved=True
    )
    
    ApplicationSupplyChainPartner.objects.create(
        application=application,
        name="Green Weavers Ltd.",
        address="789 Renewable Road",
        city="Vancouver",
        state="British Columbia",
        zip_code="V6B 1A1", 
        country="Canada",
        is_approved=True
    )
    
    ApplicationProduct.objects.create(
        application=application,
        supply_chain_partner_name_raw="Sustainable Yarn Co.",
        product_name="Organic Cotton T-Shirt",
        product_category="Men's apparel",
        raw_materials_list="Organic cotton, Recycled polyester tags, Natural dyes",
        is_approved=True
    )
    
    ApplicationProduct.objects.create(
        application=application,
        supply_chain_partner_name_raw="Sustainable Yarn Co.", 
        product_name="Recycled Polyester Jacket",
        product_category="Outerwear",
        raw_materials_list="Recycled post-consumer polyester, Recycled nylon zippers, Waterproof coating",
        is_approved=True
    )
    
    ApplicationProduct.objects.create(
        application=application,
        supply_chain_partner_name_raw="Green Weavers Ltd.",
        product_name="Hemp Blend Scarf",
        product_category="Accessories", 
        raw_materials_list="Organic hemp, Recycled silk, Natural plant dyes",
        is_approved=True
    )
    
    return application

def create_to_be_rejected_application():
    """Create a dummy application that will be rejected."""
    application = Application.objects.create(
        name="❌ TO BE REJECTED - BioTech Fabrics Application",
        description="Application with several compliance issues including non-approved materials.",
        submission_date=timezone.now(),
        status='in_review'
    )
    
    ApplicationCompanyInfo.objects.create(
        application=application,
        name="BioTech Fabrics Corp.",
        address="321 Innovation Drive",
        city="San Francisco",
        state="California",
        zip_code="94107",
        country="United States",
        is_approved=True
    )
    
    ApplicationSupplyChainPartner.objects.create(
        application=application,
        name="Algae Fiber Producers",
        address="654 Bio Park Road",
        city="San Diego",
        state="California", 
        zip_code="92121",
        country="United States",
        is_approved=True
    )
    
    ApplicationSupplyChainPartner.objects.create(
        application=application,
        name="❌ Uncertified Textiles Inc.",
        address="999 Non-Compliant Road",
        city="Problem City",
        state="Texas",
        zip_code="75001", 
        country="United States",
        is_approved=False,
        rejection_reason="Supplier lacks proper sustainability certifications."
    )
    
    ApplicationProduct.objects.create(
        application=application,
        supply_chain_partner_name_raw="Algae Fiber Producers",
        product_name="Algae-Based Activewear",
        product_category="Sportswear",
        raw_materials_list="Algae-based polymer, Recycled elastane, Moisture-wicking finish",
        is_approved=True
    )
    
    ApplicationProduct.objects.create(
        application=application,
        supply_chain_partner_name_raw="Algae Fiber Producers", 
        product_name="Biodegradable Running Shoes",
        product_category="Footwear",
        raw_materials_list="Algae foam, Recycled rubber sole, Plant-based adhesives",
        is_approved=True
    )
    
    ApplicationProduct.objects.create(
        application=application,
        supply_chain_partner_name_raw="❌ Uncertified Textiles Inc.",
        product_name="❌ Polyester Blend Shirt",
        product_category="Men's apparel", 
        raw_materials_list="Virgin polyester, Synthetic dyes, Plastic buttons",
        is_approved=False,
        rejection_reason="Contains virgin polyester and synthetic dyes which violate sustainability standards."
    )
    
    ApplicationProduct.objects.create(
        application=application,
        supply_chain_partner_name_raw="Mushroom Leather Co.",
        product_name="Mycelium Leather Bag",
        product_category="Bags & Luggage",
        raw_materials_list="Mycelium leather, Recycled brass hardware, Organic cotton lining",
        is_approved=False,
        rejection_reason="Supply chain partner not listed in application."
    )
    
    return application

def create_dummy_data():
    """Create dummy data for testing and demonstration."""
    company_data = create_company_info()
    submitted_app = create_to_be_submitted_application()
    approved_app = create_to_be_approved_application()
    rejected_app = create_to_be_rejected_application()
    bulk_submissions = create_dummy_bulk_submissions()
    
    return {
        'company_data': company_data,
        'applications': {
            'submitted': submitted_app,
            'approved': approved_app,
            'rejected': rejected_app
        },
        'bulk_submissions': bulk_submissions
    }