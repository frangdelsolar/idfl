from . import process_xlsx_application_form
import logging
import time

logger = logging.getLogger(__name__)

import threading


def process_bulk_submission(bulk_submission):
    """
    Process a bulk submission by processing each application individually
    
    Args:
        bulk_submission: The BulkSubmission instance to process
        
    Returns:
        bool: True if all applications processed successfully, False otherwise
    """
    try:
        applications = bulk_submission.applications.all()
        successful_processing = 0
        failed_processing = 0
        
        for application in applications:
            try:
                if application.file:
                    success = process_xlsx_application_form(application)
                    if success:
                        successful_processing += 1
                    else:
                        failed_processing += 1
                else:
                    failed_processing += 1  
                    
            except Exception as e:
                logger.error(f"Failed to process application {application.name}: {str(e)}")
                failed_processing += 1

            # Simulate this takes a some time
            WAIT_SECONDS = 15
            for second in range(WAIT_SECONDS):
                logger.info(f"Waiting {WAIT_SECONDS-second} seconds before processing next application...")
                time.sleep(1)
        
        return failed_processing == 0 and successful_processing > 0
        
    except Exception as e:
        logger.error(f"Error processing bulk submission {bulk_submission.name}: {str(e)}")
        return False
    
def process_bulk_submission_async(bulk_submission_id):
    """Process in background thread"""
    def _process():
        try:
            from application.models import BulkSubmission
            bulk_submission = BulkSubmission.objects.get(id=bulk_submission_id)
            success = process_bulk_submission(bulk_submission)

            logger.info(f"Processed bulk submission {bulk_submission.name}, success: {success}")
            
            if success:
                bulk_submission.status = BulkSubmission.Status.SUCCESS
            else:
                bulk_submission.status = BulkSubmission.Status.FAIL
            bulk_submission.save()
            
        except Exception as e:
            # Log error or send email notification
            logger.error(f"Error processing bulk submission {bulk_submission_id}: {str(e)}")
    
    thread = threading.Thread(target=_process)
    thread.daemon = True
    thread.start()
