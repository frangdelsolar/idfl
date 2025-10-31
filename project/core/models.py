from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class TimestampMixin(models.Model):
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)
    
    class Meta:
        abstract = True


class UserHistoryMixin(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        editable=False,
        related_name='%(class)s_created_by',
        null=True,
        blank=True,
        verbose_name=_('Created by'),
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        editable=False,
        related_name='%(class)s_updated_by',
        null=True,
        blank=True,
        verbose_name=_('Updated by'),
    )

    class Meta:
        abstract = True


