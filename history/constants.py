from collections import namedtuple


ACTIVITY_CONSTANT = namedtuple(
    "ACTIVITY", ["activity_code", "activity_display", "description"]
)

LOGGED_IN = ACTIVITY_CONSTANT(
    activity_code="logged_in",
    activity_display="Logged In",
    description="Logged in from {device}.",
)

QR_GENERATED = ACTIVITY_CONSTANT(
    activity_code="qr_generated",
    activity_display="Generated a QR Code",
    description="Generated a QR code to share your {document} details.",
)

QR_SCANNED = ACTIVITY_CONSTANT(
    activity_code="qr_scanned",
    activity_display="Scanned a QR Code",
    description="You scanned a QR Code from {source}.",
    # "You Scanned a QR Code from NIC Asia (nicasia.com).",
)

APPROVED_ACCESS_REQUEST = ACTIVITY_CONSTANT(
    activity_code="approved_access_request",
    activity_display="Approved Identity Access Request.",
    description="You approved a request from {requester} to view your identity details.",
    # "You approved a request from NIC Asia to view your identity details.",
)

VIEWED_SHARED_DETAILS = ACTIVITY_CONSTANT(
    activity_code="viewed_shared_details",
    activity_display="Viewed Shared Identity Details",
    description="{viewer} viewed your {document} details.",
    # "Hawaldar viewed your Driving License details.",
)

DOCUMENT_CODE_AGE = "Proof of Age"
DOCUMENT_CODE_DVL = "Driving License"

ACTIVITY_CHOICES = (
    (LOGGED_IN.activity_code, LOGGED_IN.activity_display),
    (QR_GENERATED.activity_code, QR_GENERATED.activity_display),
    (QR_SCANNED.activity_code, QR_SCANNED.activity_display),
    (APPROVED_ACCESS_REQUEST.activity_code, APPROVED_ACCESS_REQUEST.activity_display),
    (VIEWED_SHARED_DETAILS.activity_code, VIEWED_SHARED_DETAILS.activity_display),
)
