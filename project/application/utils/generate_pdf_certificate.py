import logging
import pdfkit
from django.template.loader import render_to_string
from django.utils import timezone

def generate_pdf_certificate(application):
    """
    Generate PDF certificate for approved or rejected applications.
    
    Note: In production, we could implement logic to store the generated certificate
    as a file when the application is completed/rejected, rather than generating
    it dynamically on each download request. This would improve performance and
    ensure certificate consistency.
    """
    logging.info(f"Generating PDF certificate for application: {application.name}")
    
    try:
        # Prepare context data for the template
        context = {
            'application': application,
            'generation_date': timezone.now().strftime("%B %d, %Y at %H:%M %Z"),
            
            # Approved items
            'approved_company_info': [application.company_info] if application.company_info.is_approved else [],
            'approved_partners': application.supply_chain_partners.filter(is_approved=True),
            'approved_products': application.products.filter(is_approved=True),
            
            # Rejected items
            'rejected_company_info': [application.company_info] if not application.company_info.is_approved else [],
            'rejected_partners': application.supply_chain_partners.filter(is_approved=False),
            'rejected_products': application.products.filter(is_approved=False),
        }
        
        # Render HTML template
        html_content = render_to_string('application/certificate_template.html', context)
        
        # PDF generation options
        options = {
            'page-size': 'Letter',
            'margin-top': '1in',
            'margin-right': '1in',
            'margin-bottom': '1in',
            'margin-left': '1in',
            'encoding': "UTF-8",
            'no-outline': None,
            'enable-local-file-access': None,
        }
        
        # Generate PDF from HTML
        pdf = pdfkit.from_string(html_content, False, options=options)
        
        logging.info(f"Successfully generated PDF for application: {application.name}")
        return pdf
        
    except Exception as e:
        logging.error(f"Failed to generate PDF for application {application.name}: {str(e)}")
        return None