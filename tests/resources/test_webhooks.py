import pytest

from nylas.models.webhooks import Webhook, WebhookTriggers
from nylas.resources.webhooks import Webhooks, extract_challenge_parameter


class TestWebhooks:
    def test_webhook_deserialization(self, http_client):
        webhook_json = {
            "id": "UMWjAjMeWQ4D8gYF2moonK4486",
            "description": "Production webhook destination",
            "trigger_types": ["calendar.created"],
            "webhook_url": "https://example.com/webhooks",
            "status": "active",
            "notification_email_addresses": ["jane@example.com", "joe@example.com"],
            "status_updated_at": 1234567890,
            "created_at": 1234567890,
            "updated_at": 1234567890,
        }

        webhook = Webhook.from_dict(webhook_json)

        assert webhook.id == "UMWjAjMeWQ4D8gYF2moonK4486"
        assert webhook.description == "Production webhook destination"
        assert webhook.trigger_types == ["calendar.created"]
        assert webhook.webhook_url == "https://example.com/webhooks"
        assert webhook.status == "active"
        assert webhook.notification_email_addresses == [
            "jane@example.com",
            "joe@example.com",
        ]
        assert webhook.status_updated_at == 1234567890
        assert webhook.created_at == 1234567890
        assert webhook.updated_at == 1234567890

    def test_webhook_deserialization_all(self, http_client):
        trigger_types = [
            "booking.created",
            "booking.pending",
            "booking.rescheduled",
            "booking.cancelled",
            "booking.reminder",
            "calendar.created",
            "calendar.updated",
            "calendar.deleted",
            "contact.updated",
            "contact.deleted",
            "event.created",
            "event.updated",
            "event.deleted",
            "grant.created",
            "grant.updated",
            "grant.deleted",
            "grant.expired",
            "message.send_success",
            "message.send_failed",
            "message.bounce_detected",
            "message.created",
            "message.updated",
            "message.opened",
            "message.link_clicked",
            "message.opened.legacy",
            "message.link_clicked.legacy",
            "message.intelligence.order",
            "message.intelligence.tracking",
            "message.intelligence.return",
            "thread.replied",
            "thread.replied.legacy",
            "folder.created",
            "folder.updated",
            "folder.deleted"
        ]

        webhook_json = {
            "id": "UMWjAjMeWQ4D8gYF2moonK4486",
            "description": "Production webhook destination",
            "trigger_types": trigger_types,
            "webhook_url": "https://example.com/webhooks",
            "status": "active",
            "notification_email_addresses": ["jane@example.com", "joe@example.com"],
            "status_updated_at": 1234567890,
            "created_at": 1234567890,
            "updated_at": 1234567890,
        }

        webhook = Webhook.from_dict(webhook_json)

        assert webhook.id == "UMWjAjMeWQ4D8gYF2moonK4486"
        assert webhook.description == "Production webhook destination"
        assert webhook.trigger_types == trigger_types
        assert webhook.webhook_url == "https://example.com/webhooks"
        assert webhook.status == "active"
        assert webhook.notification_email_addresses == [
            "jane@example.com",
            "joe@example.com",
        ]
        assert webhook.status_updated_at == 1234567890
        assert webhook.created_at == 1234567890
        assert webhook.updated_at == 1234567890

    def test_list_webhooks(self, http_client_list_response):
        webhooks = Webhooks(http_client_list_response)

        webhooks.list()

        http_client_list_response._execute.assert_called_once_with(
            "GET", "/v3/webhooks", None, None, None, overrides=None
        )

    def test_find_webhook(self, http_client_response):
        webhooks = Webhooks(http_client_response)

        webhooks.find("webhook-123")

        http_client_response._execute.assert_called_once_with(
            "GET", "/v3/webhooks/webhook-123", None, None, None, overrides=None
        )

    def test_create_webhook(self, http_client_response):
        webhooks = Webhooks(http_client_response)
        request_body = {
            "trigger_types": [WebhookTriggers.EVENT_CREATED],
            "webhook_url": "https://example.com/webhooks",
            "description": "Production webhook destination",
            "notification_email_addresses": ["jane@test.com"],
        }

        webhooks.create(request_body=request_body)

        http_client_response._execute.assert_called_once_with(
            "POST", "/v3/webhooks", None, None, request_body, overrides=None
        )

    def test_update_webhook(self, http_client_response):
        webhooks = Webhooks(http_client_response)
        request_body = {
            "trigger_types": [WebhookTriggers.EVENT_CREATED],
            "webhook_url": "https://example.com/webhooks",
            "description": "Production webhook destination",
            "notification_email_addresses": ["jane@test.com"],
        }

        webhooks.update(
            webhook_id="webhook-123",
            request_body=request_body,
        )

        http_client_response._execute.assert_called_once_with(
            "PUT", "/v3/webhooks/webhook-123", None, None, request_body, overrides=None
        )

    def test_destroy_webhook(self, http_client_delete_response):
        webhooks = Webhooks(http_client_delete_response)

        webhooks.destroy("webhook-123")

        http_client_delete_response._execute.assert_called_once_with(
            "DELETE", "/v3/webhooks/webhook-123", None, None, None, overrides=None
        )

    def test_rotate_secret(self, http_client_response):
        webhooks = Webhooks(http_client_response)

        webhooks.rotate_secret("webhook-123")

        http_client_response._execute.assert_called_once_with(
            method="PUT",
            path="/v3/webhooks/webhook-123/rotate-secret",
            request_body={},
            overrides=None,
        )

    def test_ip_addresses(self, http_client_response):
        webhooks = Webhooks(http_client_response)

        webhooks.ip_addresses()

        http_client_response._execute.assert_called_once_with(
            method="GET", path="/v3/webhooks/ip-addresses", overrides=None
        )

    def test_extract_challenge_parameter(self, http_client):
        url = "https://example.com/webhooks?challenge=abc123"

        challenge = extract_challenge_parameter(url)

        assert challenge == "abc123"

    def test_extract_challenge_parameter_no_challenge(self, http_client):
        url = "https://example.com/webhooks"

        with pytest.raises(ValueError) as e:
            extract_challenge_parameter(url)

        assert str(e.value) == "Invalid URL or no challenge parameter found."
