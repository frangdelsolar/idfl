import logging
from django.db import transaction
from django.contrib.auth.models import User
from customer.models import Address, Company, SupplyChainCompany
from product.models import ProductCategory, ProductDetail, RawMaterial, Product

# Set up detailed logging
logger = logging.getLogger(__name__)

def complete_application(application):
    """
    Process an approved application and create permanent records.
    
    Only creates entities that are approved, ensuring nested components
    are only created if their parents are valid and approved.
    
    Args:
        application: The Application instance to process
        
    Returns:
        bool: True if successful, False if failed
    """
    logger.info("🚀 STARTING application completion process for: %s (ID: %s)", 
                application.name, application.id)
    logger.info("📊 Application status: %s", application.status)
    
    try:
        with transaction.atomic():
            logger.info("🔒 Database transaction started - all changes will be atomic")
            
            # Validate that all required components exist and are approved
            logger.info("📋 Step 1: Validating application components...")
            if not _validate_application_components(application):
                logger.error("❌ Application validation failed for: %s", application.name)
                return False
            logger.info("✅ Application validation passed")
            
            # Create company and address if approved
            logger.info("🏢 Step 2: Creating company records...")
            company = _create_company_from_application(application)
            if not company:
                logger.error("❌ Failed to create company for application: %s", application.name)
                return False
            logger.info("✅ Company created successfully: %s (ID: %s)", company.name, company.id)
            
            # Create supply chain partners if approved
            logger.info("🔗 Step 3: Creating supply chain partners...")
            supply_chain_companies = _create_supply_chain_partners(application)
            logger.info("✅ Created %s supply chain partners", len(supply_chain_companies))
            
            # Create products and related entities if approved
            logger.info("📦 Step 4: Creating products and related entities...")
            products_created = _create_products_from_application(application, supply_chain_companies)
            logger.info("✅ Created %s products", len(products_created))
            
            # Summary
            logger.info("📈 COMPLETION SUMMARY for %s:", application.name)
            logger.info("   • Company: %s (ID: %s)", company.name, company.id)
            logger.info("   • Supply Chain Partners: %s", len(supply_chain_companies))
            logger.info("   • Products: %s", len(products_created))
            logger.info("   • Total database records created: %s", 
                      1 + len(supply_chain_companies) + len(products_created))  # Company + partners + products
            
            logger.info("🎉 SUCCESS: Application %s completed successfully!", application.name)
            return True
            
    except Exception as e:
        logger.error("💥 CRITICAL ERROR in application completion for %s:", application.name)
        logger.error("   Error type: %s", type(e).__name__)
        logger.error("   Error message: %s", str(e))
        logger.error("   Stack trace:", exc_info=True)
        return False

def _validate_application_components(application):
    """Validate that all required application components exist and are approved."""
    logger.debug("🔍 Validating application components for: %s", application.name)
    
    # Check if company info exists and is approved
    if not hasattr(application, 'company_info') or not application.company_info:
        logger.error("❌ Application %s has no company info attached", application.name)
        return False
    
    company_info = application.company_info
    logger.debug("   Company info: %s (Approved: %s)", 
                company_info.name, company_info.is_approved)
    
    if not company_info.is_approved:
        logger.error("❌ Application %s company info is not approved", application.name)
        return False
    
    # Check supply chain partners
    all_partners = application.supply_chain_partners.all()
    approved_partners = application.supply_chain_partners.filter(is_approved=True)
    rejected_partners = application.supply_chain_partners.filter(is_approved=False)
    
    logger.debug("   Supply Chain Partners - Total: %s, Approved: %s, Rejected: %s", 
                all_partners.count(), approved_partners.count(), rejected_partners.count())
    
    for partner in approved_partners:
        logger.debug("     ✅ Approved: %s", partner.name)
    for partner in rejected_partners:
        logger.debug("     ❌ Rejected: %s - Reason: %s", 
                    partner.name, partner.rejection_reason or "No reason provided")
    
    if not approved_partners.exists():
        logger.warning("⚠️ Application %s has no approved supply chain partners", application.name)
    
    # Check products
    all_products = application.products.all()
    approved_products = application.products.filter(is_approved=True)
    rejected_products = application.products.filter(is_approved=False)
    
    logger.debug("   Products - Total: %s, Approved: %s, Rejected: %s", 
                all_products.count(), approved_products.count(), rejected_products.count())
    
    for product in approved_products:
        logger.debug("     ✅ Approved: %s", product.product_name)
    for product in rejected_products:
        logger.debug("     ❌ Rejected: %s - Reason: %s", 
                    product.product_name, product.rejection_reason or "No reason provided")
    
    if not approved_products.exists():
        logger.warning("⚠️ Application %s has no approved products", application.name)
    
    logger.info("✅ Application validation completed successfully")
    return True

def _create_company_from_application(application):
    """Create Company and Address from approved application company info."""
    company_info = application.company_info
    
    logger.debug("🏢 Creating company from: %s", company_info.name)
    logger.debug("   Address: %s, %s, %s %s, %s", 
                company_info.address, company_info.city, 
                company_info.state, company_info.zip_code, company_info.country)
    
    try:
        # Create address first
        logger.debug("   Creating address record...")
        address = Address.objects.create(
            address=company_info.address or '',
            city=company_info.city or '',
            state=company_info.state or '',
            zip_code=company_info.zip_code or '',
            country=company_info.country or ''
        )
        logger.debug("   ✅ Address created (ID: %s)", address.id)
        
        # Create company
        logger.debug("   Creating company record...")
        company = Company.objects.create(
            name=company_info.name or f"Company-{application.id}",
            address=address
        )
        logger.debug("   ✅ Company created (ID: %s)", company.id)
        
        # Note: Users would need to be associated later via admin or separate process
        logger.info("🏢 Created company: %s (ID: %s) with address ID: %s", 
                   company.name, company.id, address.id)
        return company
        
    except Exception as e:
        logger.error("❌ Failed to create company from application %s:", application.name)
        logger.error("   Error: %s", str(e))
        return None

def _create_supply_chain_partners(application):
    """Create SupplyChainCompany records from approved supply chain partners."""
    approved_partners = application.supply_chain_partners.filter(is_approved=True)
    created_companies = []
    
    logger.debug("🔗 Processing %s approved supply chain partners", approved_partners.count())
    
    for i, partner in enumerate(approved_partners, 1):
        logger.debug("   [%s/%s] Creating supply chain partner: %s", 
                    i, approved_partners.count(), partner.name)
        
        try:
            # Create address for supply chain partner
            logger.debug("      Creating address...")
            address = Address.objects.create(
                address=partner.address or '',
                city=partner.city or '',
                state=partner.state or '',
                zip_code=partner.zip_code or '',
                country=partner.country or ''
            )
            logger.debug("      ✅ Address created (ID: %s)", address.id)
            
            # Create supply chain company (mark as valid since they're approved)
            logger.debug("      Creating supply chain company...")
            supply_chain_company = SupplyChainCompany.objects.create(
                name=partner.name or f"Partner-{partner.id}",
                is_valid=True,  # Mark as valid since they passed approval
                address=address
            )
            logger.debug("      ✅ Supply chain company created (ID: %s)", supply_chain_company.id)
            
            created_companies.append(supply_chain_company)
            logger.info("🔗 Created supply chain company: %s (ID: %s)", 
                       supply_chain_company.name, supply_chain_company.id)
            
        except Exception as e:
            logger.error("❌ Failed to create supply chain partner %s:", partner.name)
            logger.error("   Error: %s", str(e))
            continue
    
    logger.info("🔗 Completed supply chain partner creation: %s successful, %s total attempted", 
               len(created_companies), approved_partners.count())
    return created_companies

def _create_products_from_application(application, supply_chain_companies):
    """Create Product records and related entities from approved products."""
    approved_products = application.products.filter(is_approved=True)
    created_products = []
    
    logger.debug("📦 Processing %s approved products", approved_products.count())
    
    # Create a mapping of supply chain partner names to their created companies
    partner_name_mapping = {company.name: company for company in supply_chain_companies}
    logger.debug("   Available supply chain companies: %s", list(partner_name_mapping.keys()))
    
    for i, app_product in enumerate(approved_products, 1):
        logger.debug("   [%s/%s] Creating product: %s", 
                    i, approved_products.count(), app_product.product_name)
        
        try:
            # Get or create product category
            logger.debug("      Processing product category...")
            category = _get_or_create_product_category(app_product)
            if not category:
                logger.warning("⚠️ Skipping product %s - could not create category", app_product.product_name)
                continue
            logger.debug("      ✅ Category: %s (ID: %s)", category.description, category.id)
            
            # Get or create product detail
            logger.debug("      Processing product detail...")
            product_detail = _get_or_create_product_detail(app_product)
            if not product_detail:
                logger.warning("⚠️ Skipping product %s - could not create product detail", app_product.product_name)
                continue
            logger.debug("      ✅ Product detail: %s (ID: %s)", product_detail.description, product_detail.id)
            
            # Create raw materials
            logger.debug("      Processing raw materials...")
            raw_materials = _create_raw_materials_from_product(app_product)
            logger.debug("      ✅ Created %s raw materials", len(raw_materials))
            
            # Create the main product
            logger.debug("      Creating main product record...")
            product = Product.objects.create(
                name=app_product.product_name,
                detail=product_detail,
                category=category
            )
            logger.debug("      ✅ Main product created (ID: %s)", product.id)
            
            # Add raw materials to the product
            if raw_materials:
                product.raw_materials.set(raw_materials)
                logger.debug("      ✅ Associated %s raw materials with product", len(raw_materials))
            
            created_products.append(product)
            logger.info("📦 Created product: %s (ID: %s) with %s raw materials", 
                       product.name, product.id, len(raw_materials))
            
        except Exception as e:
            logger.error("❌ Failed to create product %s:", app_product.product_name)
            logger.error("   Error: %s", str(e))
            continue
    
    logger.info("📦 Completed product creation: %s successful, %s total attempted", 
               len(created_products), approved_products.count())
    return created_products

def _get_or_create_product_category(app_product):
    """Get or create ProductCategory from application product data."""
    if not app_product.product_category:
        logger.warning("⚠️ No product category specified for product: %s", app_product.product_name)
        return None
    
    try:
        # Create a code from the category name (simple slugification)
        category_code = app_product.product_category.upper().replace(' ', '-').replace("'", "")[:50]
        category_code = f"CAT-{category_code}"
        
        logger.debug("      Looking up/creating category: %s -> %s", 
                    app_product.product_category, category_code)
        
        category, created = ProductCategory.objects.get_or_create(
            code=category_code,
            defaults={
                'description': app_product.product_category,
                'is_active': True
            }
        )
        
        if created:
            logger.debug("      ✅ Created NEW category: %s (ID: %s)", category_code, category.id)
        else:
            logger.debug("      ✅ Using EXISTING category: %s (ID: %s)", category_code, category.id)
        
        return category
        
    except Exception as e:
        logger.error("❌ Failed to create product category for %s:", app_product.product_category)
        logger.error("   Error: %s", str(e))
        return None

def _get_or_create_product_detail(app_product):
    """Get or create ProductDetail from application product data."""
    if not app_product.product_name:
        logger.warning("⚠️ No product name specified for product")
        return None
    
    try:
        # Create a code from the product name
        detail_code = app_product.product_name.upper().replace(' ', '-').replace("'", "")[:50]
        detail_code = f"PROD-{detail_code}"
        
        logger.debug("      Looking up/creating product detail: %s -> %s", 
                    app_product.product_name, detail_code)
        
        product_detail, created = ProductDetail.objects.get_or_create(
            code=detail_code,
            defaults={
                'description': app_product.product_name,
                'is_active': True
            }
        )
        
        if created:
            logger.debug("      ✅ Created NEW product detail: %s (ID: %s)", detail_code, product_detail.id)
        else:
            logger.debug("      ✅ Using EXISTING product detail: %s (ID: %s)", detail_code, product_detail.id)
        
        return product_detail
        
    except Exception as e:
        logger.error("❌ Failed to create product detail for %s:", app_product.product_name)
        logger.error("   Error: %s", str(e))
        return None

def _create_raw_materials_from_product(app_product):
    """Create RawMaterial records from product's raw materials list."""
    if not app_product.raw_materials_list:
        logger.debug("      No raw materials specified for product: %s", app_product.product_name)
        return []
    
    raw_materials = []
    
    logger.debug("      Processing raw materials list: %s", app_product.raw_materials_list)
    
    try:
        # Split the raw materials list (assuming comma-separated)
        material_names = [material.strip() for material in app_product.raw_materials_list.split(',')]
        logger.debug("      Found %s raw materials: %s", len(material_names), material_names)
        
        for j, material_name in enumerate(material_names, 1):
            if not material_name:
                logger.debug("      [%s/%s] Skipping empty material name", j, len(material_names))
                continue
                
            # Create a code from the material name
            material_code = material_name.upper().replace(' ', '-').replace("'", "")[:50]
            material_code = f"MAT-{material_code}"
            
            logger.debug("      [%s/%s] Processing material: %s -> %s", 
                        j, len(material_names), material_name, material_code)
            
            material, created = RawMaterial.objects.get_or_create(
                code=material_code,
                defaults={
                    'description': material_name,
                    'is_active': True
                }
            )
            
            raw_materials.append(material)
            
            if created:
                logger.debug("      ✅ Created NEW raw material: %s (ID: %s)", material_code, material.id)
            else:
                logger.debug("      ✅ Using EXISTING raw material: %s (ID: %s)", material_code, material.id)
        
        logger.debug("      ✅ Completed processing %s raw materials", len(raw_materials))
    
    except Exception as e:
        logger.error("❌ Failed to create raw materials for product %s:", app_product.product_name)
        logger.error("   Error: %s", str(e))
    
    return raw_materials