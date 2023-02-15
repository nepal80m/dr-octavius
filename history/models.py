from django.db import models
from core.models import TimeStampedModel
from django.contrib.auth import get_user_model
from history.constants import ACTIVITY_CHOICES

User = get_user_model()


class ActivityHistory(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.CharField(max_length=100, choices=ACTIVITY_CHOICES)
    description = models.CharField(max_length=255)
    extra_info = models.JSONField(null=True, blank=True)

    @property
    def title(self):
        return dict(ACTIVITY_CHOICES)[self.activity]

    """
    request
    
    """


"""
#* User Activity
Logged In
    Logged in from Android device.

    
#* NIC Asia Activity
Scanned a QR Code
    Scanned a QR Code from NIC Asia (nicasia.com).

Approved Identity Access Request.
    Approved request from NIC Asia to view your identity details.
        list of fields


#* Traffic Police Activity
Generated a QR Code
    - Generated a QR code to share your Driving License details.
    - Generated a QR code to share your proof of age details.

Viewed Shared Identity Details
    - Hawaldar viewed your Driving License details.
    - Hawaldar viewed your proof of age details.

Scanned a QR Code
    - Scanned a QR code to view Driving license details of Ram Lal.
    - Scanned a QR code to view proof of age details of Ram Lal.


    


Generated QR to share your Driving License details.

Shared NIN with NIC Asia 


Scanned QR Code from NIC Asia.

1. Access Request
You shared your details with NIC Asia.  
    fields, timestamp
2. Access Permit
Ram Lal viewed your driving licence details.
    fields, timestamp




"""
