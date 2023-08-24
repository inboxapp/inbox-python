import urllib.parse

from nylas.handler.api_resources import (
    ListableApiResource,
    FindableApiResource,
    CreatableApiResource,
    UpdatableApiResource,
    DestroyableApiResource,
)
from nylas.models.list_response import ListResponse
from nylas.models.response import Response
from nylas.models.webhooks import (
    Webhook,
    WebhookWithSecret,
    WebhookDeleteResponse,
    WebhookIpAddressesResponse,
)


class Webhooks(
    ListableApiResource[Webhook],
    FindableApiResource[Webhook],
    CreatableApiResource[WebhookWithSecret],
    UpdatableApiResource[Webhook],
    DestroyableApiResource[WebhookDeleteResponse],
):
    def __init__(self, http_client):
        super(Webhooks, self).__init__("webhooks", http_client)

    def list(self) -> ListResponse[Webhook]:
        """
        List all webhook destinations

        Returns:
            Response[Webhook]: The list of webhook destinations
        """
        return super(Webhooks, self).list(path=f"/v3/webhooks")

    def find(self, webhook_id: str) -> Response[Webhook]:
        """
        Get a webhook destination

        Parameters:
            webhook_id (str): The ID of the webhook destination to get

        Returns:
            Response[Webhook]: The webhook destination
        """
        return super(Webhooks, self).find(path=f"/v3/webhooks/{webhook_id}")

    def create(self, request_body: dict) -> Response[WebhookWithSecret]:
        """
        Create a webhook destination

        Parameters:
            request_body (dict): The request body to create the webhook destination

        Returns:
            Response[WebhookWithSecret]: The created webhook destination
        """
        return super(Webhooks, self).create(
            path=f"/v3/webhooks", request_body=request_body
        )

    def update(self, webhook_id: str, request_body: dict) -> Response[Webhook]:
        """
        Update a webhook destination

        Parameters:
            webhook_id (str): The ID of the webhook destination to update
            request_body (dict): The request body to update the webhook destination

        Returns:
            Response[Webhook]: The updated webhook destination
        """
        return super(Webhooks, self).update(
            path=f"/v3/webhooks/{webhook_id}", request_body=request_body
        )

    def destroy(self, webhook_id: str) -> WebhookDeleteResponse:
        """
        Delete a webhook destination

        Parameters:
            webhook_id (str): The ID of the webhook destination to delete

        Returns:
            WebhookDeleteResponse: The response from deleting the webhook destination
        """
        return super(Webhooks, self).destroy(path=f"/v3/webhooks/{webhook_id}")

    def rotate_secret(self, webhook_id: str) -> Response[Webhook]:
        """
        Update the webhook secret value for a destination

        Parameters:
            webhook_id (str): The ID of the webhook destination to update

        Returns:
            Response[Webhook]: The updated webhook destination
        """
        res = self._http_client._execute(
            method="PUT",
            path=f"/v3/webhooks/{webhook_id}/rotate-secret",
            request_body={},
        )
        return Response.from_dict(res, Webhook)

    def ip_addresses(self) -> Response[WebhookIpAddressesResponse]:
        """
        Get the current list of IP addresses that Nylas sends webhooks from

        Returns:
            Response[WebhookIpAddressesResponse]: The list of IP addresses that Nylas sends webhooks from
        """
        res = self._http_client._execute(method="GET", path="/v3/webhooks/ip-addresses")
        return Response.from_dict(res, WebhookIpAddressesResponse)


def extract_challenge_parameter(url: str) -> str:
    """
    Extract the challenge parameter from a URL

    Parameters:
        url (str): The URL sent by Nylas containing the challenge parameter

    Returns:
        str: The challenge parameter
    """
    url_object = urllib.parse.urlparse(url)
    query = urllib.parse.parse_qs(url_object.query)
    challenge_parameter = query.get("challenge")
    if not challenge_parameter:
        raise ValueError("Invalid URL or no challenge parameter found.")

    return challenge_parameter[0]
