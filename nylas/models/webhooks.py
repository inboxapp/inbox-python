from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Literal

from dataclasses_json import dataclass_json
from typing_extensions import TypedDict, NotRequired

WebhookStatus = Literal["active", "failing", "failed", "pause"]
""" Literals representing the possible webhook statuses. """


class WebhookTriggers(str, Enum):
    """Enum representing the available webhook triggers."""
    BOOKING_CREATED = "booking.created"
    BOOKING_PENDING = "booking.pending"
    BOOKING_RESCHEDULED = "booking.rescheduled"
    BOOKING_CANCELLED = "booking.cancelled"
    BOOKING_REMINDER = "booking.reminder"
    CALENDAR_CREATED = "calendar.created"
    CALENDAR_UPDATED = "calendar.updated"
    CALENDAR_DELETED = "calendar.deleted"
    CONTACT_UPDATED = "contact.updated"
    CONTACT_DELETED = "contact.deleted"
    EVENT_CREATED = "event.created"
    EVENT_UPDATED = "event.updated"
    EVENT_DELETED = "event.deleted"
    GRANT_CREATED = "grant.created"
    GRANT_UPDATED = "grant.updated"
    GRANT_DELETED = "grant.deleted"
    GRANT_EXPIRED = "grant.expired"
    MESSAGE_SEND_SUCCESS = "message.send_success"
    MESSAGE_SEND_FAILED = "message.send_failed"
    MESSAGE_BOUNCE_DETECTED = "message.bounce_detected"
    MESSAGE_CREATED = "message.created"
    MESSAGE_UPDATED = "message.updated"
    MESSAGE_OPENED = "message.opened"
    MESSAGE_LINK_CLICKED = "message.link_clicked"
    MESSAGE_OPENED_LEGACY = "message.opened.legacy"
    MESSAGE_LINK_CLICKED_LEGACY = "message.link_clicked.legacy"
    MESSAGE_INTELLIGENCE_ORDER = "message.intelligence.order"
    MESSAGE_INTELLIGENCE_TRACKING = "message.intelligence.tracking"
    MESSAGE_INTELLIGENCE_RETURN = "message.intelligence.return"
    THREAD_REPLIED = "thread.replied"
    THREAD_REPLIED_LEGACY = "thread.replied.legacy"
    FOLDER_CREATED = "folder.created"
    FOLDER_UPDATED = "folder.updated"
    FOLDER_DELETED = "folder.deleted"


@dataclass_json
@dataclass
class Webhook:
    """
    Class representing a Nylas webhook.

    Attributes:
        id: Globally unique object identifier.
        trigger_types: The event that triggers the webhook.
        webhook_url: The URL to send webhooks to.
        status: The status of the new destination.
        notification_email_addresses: The email addresses that Nylas notifies when a webhook is down for a while.
        status_updated_at: The time when the status field was last updated, represented as a Unix timestamp in seconds.
        created_at: The time when the status field was created, represented as a Unix timestamp in seconds.
        updated_at: The time when the status field was last updated, represented as a Unix timestamp in seconds.
        description: A human-readable description of the webhook destination.
    """

    id: str
    trigger_types: List[WebhookTriggers]
    webhook_url: str
    status: WebhookStatus
    notification_email_addresses: List[str]
    status_updated_at: int
    created_at: int
    updated_at: int
    description: Optional[str] = None


@dataclass_json
@dataclass
class WebhookWithSecret(Webhook):
    """
    Class representing a Nylas webhook with secret.

    Attributes:
        webhook_secret: A secret value used to encode the X-Nylas-Signature header on webhook requests.
    """

    webhook_secret: str = ""


@dataclass_json
@dataclass
class WebhookDeleteData:
    """
    Class representing the object enclosing the webhook deletion status.

    Attributes:
        status: The status of the webhook deletion.
    """

    status: str


@dataclass_json
@dataclass
class WebhookDeleteResponse:
    """
    Class representing a Nylas webhook delete response.

    Attributes:
        request_id: The request's ID.
        data: Object containing the webhook deletion status.
    """

    request_id: str
    data: Optional[WebhookDeleteData] = None


@dataclass_json
@dataclass
class WebhookIpAddressesResponse:
    """
    Class representing the response for getting a list of webhook IP addresses.

    Attributes:
        ip_addresses: The IP addresses that Nylas send your webhook from.
        updated_at: Unix timestamp representing the time when Nylas last updated the list of IP addresses.
    """

    ip_addresses: List[str]
    updated_at: int


class CreateWebhookRequest(TypedDict):
    """
    Class representation of a Nylas create webhook request.

    Attributes:
        trigger_types: List of events that triggers the webhook.
        webhook_url: The url to send webhooks to.
        description: A human-readable description of the webhook destination.
        notification_email_addresses: The email addresses that Nylas notifies when a webhook is down for a while.
    """

    trigger_types: List[WebhookTriggers]
    webhook_url: str
    description: NotRequired[str]
    notification_email_addresses: NotRequired[List[str]]


class UpdateWebhookRequest(TypedDict):
    """
    Class representation of a Nylas update webhook request.

    Attributes:
        trigger_types: List of events that triggers the webhook.
        webhook_url: The url to send webhooks to.
        description: A human-readable description of the webhook destination.
        notification_email_addresses: The email addresses that Nylas notifies when a webhook is down for a while.
    """

    trigger_types: NotRequired[List[WebhookTriggers]]
    webhook_url: NotRequired[str]
    description: NotRequired[str]
    notification_email_addresses: NotRequired[List[str]]
