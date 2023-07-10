from nylas.config import DEFAULT_SERVER_URL
from nylas.handler.http_client import HttpClient
from nylas.resources.applications import Applications
from nylas.resources.auth import Auth
from nylas.resources.availability import Availability
from nylas.resources.calendars import Calendars
from nylas.resources.events import Events


class Client(object):
    """API client for the Nylas API."""

    def __init__(
        self, api_key: str, api_server: str = DEFAULT_SERVER_URL, timeout: int = 30
    ):
        self.api_key = api_key
        self.api_server = api_server
        self.http_client = HttpClient(self.api_server, self.api_key, timeout)

    def auth(self, client_id: str, client_secret: str) -> Auth:
        return Auth(self.http_client, client_id, client_secret)

    @property
    def applications(self) -> Applications:
        return Applications(self.http_client)

    @property
    def availability(self) -> Availability:
        return Availability(self.http_client)

    @property
    def calendars(self) -> Calendars:
        return Calendars(self.http_client)

    @property
    def events(self) -> Events:
        return Events(self.http_client)
