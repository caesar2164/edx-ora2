"""
Trackchanges models used as part of the (optional) "Track Changes" feature,
which allows basic collaborative editing of student submissions.

NOTE: If you make any edits to this file, you can generate migrations using:
    ./manage.py schemamigration openassessment.workflow --auto
"""
import logging

from django.db import models
from django_extensions.db.fields import UUIDField

from submissions.models import Submission as submission_model

logger = logging.getLogger(__name__)


class ChangeTracker(models.Model):
    """Store copies of student submission texts with inline editing marks."""
    MAX_SIZE = submission_model.MAXSIZE * 3 # We only expect 2x, 3x seems ok

    #submission_uuid = UUIDField(version=1, db_index=True, unique=True)
    assessmentworkflow_uuid = UUIDField(version=1, db_index=True, unique=True)
    edited_content = models.TextField(blank=True)

