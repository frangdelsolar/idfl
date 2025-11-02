from django.contrib.auth import get_user_model
from django.utils import timezone
from application.models import (
    Application, 
    ApplicationCompanyInfo,
    ApplicationSupplyChainPartner,
    ApplicationProduct
)

def create_to_be_submitted_application():
    """Create a dummy application for Customer Service to submit."""
    User = get_user_model()
    
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
    User = get_user_model()
    
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
    User = get_user_model()
    
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
    submitted_app = create_to_be_submitted_application()
    approved_app = create_to_be_approved_application()
    rejected_app = create_to_be_rejected_application()
    
    return submitted_app, approved_app, rejected_app