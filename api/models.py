import uuid
import json
from django.db import models

# Create your models here.
class Booking(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    IDUser = models.UUIDField()
    StartTime = models.DateTimeField()
    EndTime = models.DateTimeField()
    CreatedAt = models.DateTimeField(auto_now=True)
    UsedAt = models.DateTimeField(null=True)
    CancelledAt = models.DateTimeField(null=True)

    def toJSON(self):
        return {
            "IDUser": self.IDUser,
            "StartTime": self.StartTime,
            "EndTime": self.EndTime,
            "CreatedAt": self.CreatedAt,
            "UsedAt": self.UsedAt,
            "CancelledAt": self.CancelledAt,
        }
