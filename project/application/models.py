from django.db import models
import uuid
import os

# Constants
APPLICATION_FOLDER = 'application_files'

def application_file_path(instance, filename):
    """
    Generate a unique file path for application files.
    
    This function creates a deterministic path structure and uses UUIDs
    to prevent filename collisions and ensure secure file storage.
    
    Args:
        instance: The Application model instance
        filename (str): The original filename uploaded by the user
        
    Returns:
        str: A unique file path in the format: 'data/application_files/{uuid}.{ext}'
    
    Example:
        Input: 'document.pdf'
        Output: 'data/application_files/a1b2c3d4e5f6.pdf'
    """
    # Extract file extension from original filename
    ext = filename.split('.')[-1]
    
    # Generate unique filename using UUID to prevent collisions
    unique_filename = f"{uuid.uuid4().hex}.{ext}"
    
    # Construct the full path
    subdirectory = APPLICATION_FOLDER
    return os.path.join('data', subdirectory, unique_filename)


class Application(models.Model):
    """
    Represents an application submission with associated metadata and file.
    
    Tracks the lifecycle of an application through various status states
    and stores relevant submission information.
    """
    
    class Status(models.TextChoices):
        """Defines possible states of an application throughout its lifecycle."""
        PENDING = 'pending', 'Pending'
        IN_REVIEW = 'in_review', 'In Review'
        APPROVED = 'approved', 'Approved'
        REJECTED = 'rejected', 'Rejected'
    
    # Basic application information
    name = models.CharField(
        max_length=120,
        help_text="Name of the application or applicant (max 120 characters)"
    )
    
    description = models.TextField(
        help_text="Detailed description of the application"
    )
    
    # Timestamp tracking
    submission_date = models.DateTimeField(
        auto_now_add=True,
        help_text="Date and time when the application was submitted"
    )
    
    # Application state
    status = models.CharField(
        max_length=120,
        choices=Status.choices,
        default=Status.PENDING,
        help_text="Current status of the application in the review process"
    )
    
    # File attachment (optional)
    file = models.FileField(
        upload_to=application_file_path,
        blank=True,
        null=True,
        help_text="Optional file attachment related to the application"
    )
    
    def __str__(self):
        """String representation of the Application model."""
        return f"{self.name} - {self.status}"
    
    class Meta:
        """Metadata options for the Application model."""
        ordering = ['-submission_date'] 