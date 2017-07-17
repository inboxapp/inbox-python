import re
import json
from six.moves.urllib.parse import parse_qs
import pytest
from urlobject import URLObject
import responses
from nylas.client import APIClient
from nylas.client.restful_models import Contact


def urls_equal(url1, url2):
    """
    Compare two URLObjects, without regard to the order of their query strings.
    """
    return (
        url1.without_query() == url2.without_query() and
        url1.query_dict == url2.query_dict
    )


def test_custom_client():
    # Can specify API server
    custom = APIClient(api_server="http://example.com")
    assert custom.api_server == "http://example.com"
    # Must be a valid URL
    with pytest.raises(Exception) as exc:
        APIClient(api_server="invalid")
    assert exc.value.args[0] == (
        "When overriding the Nylas API server address, "
        "you must include https://"
    )


def test_client_access_token():
    client = APIClient(access_token="foo")
    assert client.access_token == "foo"
    assert client.session.headers['Authorization'] == "Bearer foo"
    client.access_token = "bar"
    assert client.access_token == "bar"
    assert client.session.headers['Authorization'] == "Bearer bar"
    client.access_token = None
    assert client.access_token is None
    assert 'Authorization' not in client.session.headers


def test_client_app_secret():
    client = APIClient(app_secret="foo")
    headers = client.admin_session.headers
    assert headers['Authorization'] == "Basic Zm9vOg=="
    assert headers['X-Nylas-API-Wrapper'] == "python"
    assert "Nylas Python SDK" in headers['User-Agent']


def test_client_authentication_url(api_client, api_url):
    expected = (
        URLObject(api_url)
        .with_path("/oauth/authorize")
        .set_query_params([
            ('login_hint', ''),
            ('state', ''),
            ('redirect_uri', '/redirect'),
            ('response_type', 'code'),
            ('client_id', 'None'),
            ('scope', 'email'),
        ])
    )
    actual = URLObject(api_client.authentication_url("/redirect"))
    assert urls_equal(expected, actual)

    actual2 = URLObject(
        api_client.authentication_url("/redirect", login_hint="hint")
    )
    expected2 = expected.set_query_param("login_hint", "hint")
    assert urls_equal(expected2, actual2)


@responses.activate
def test_client_token_for_code(api_client, api_url):
    endpoint = re.compile(api_url + '/oauth/token')
    response_body = json.dumps({"access_token": "hooray"})
    responses.add(
        responses.POST,
        endpoint,
        content_type='application/json',
        status=200,
        body=response_body,
    )

    assert api_client.token_for_code("foo") == "hooray"
    assert len(responses.calls) == 1
    request = responses.calls[0].request
    body = parse_qs(request.body)
    assert body["grant_type"] == ["authorization_code"]
    assert body["code"] == ["foo"]


def test_client_opensource_api(api_client):
    # pylint: disable=singleton-comparison
    assert api_client.is_opensource_api() == True
    api_client.app_id = "foo"
    api_client.app_secret = "super-sekrit"
    assert api_client.is_opensource_api() == False
    api_client.app_id = api_client.app_secret = None
    assert api_client.is_opensource_api() == True


@responses.activate
def test_client_revoke_token(api_client, api_url):
    endpoint = re.compile(api_url + '/oauth/revoke')
    responses.add(
        responses.POST,
        endpoint,
        status=200,
        body="",
    )

    api_client.auth_token = "foo"
    api_client.access_token = "bar"
    api_client.revoke_token()
    assert api_client.auth_token is None
    assert api_client.access_token is None
    assert len(responses.calls) == 1


@responses.activate
def test_create_resources(api_client, api_url):
    contacts_data = [
        {
            "id": 1,
            "name": "first",
            "email": "first@example.com",
        }, {
            "id": 2,
            "name": "second",
            "email": "second@example.com",
        }
    ]
    responses.add(
        responses.POST,
        api_url + "/contacts/",
        content_type='application/json',
        status=200,
        body=json.dumps(contacts_data),
    )

    post_data = contacts_data.copy()
    for contact in post_data:
        del contact["id"]

    contacts = api_client._create_resources(Contact, post_data)
    assert len(contacts) == 2
    assert all(isinstance(contact, Contact) for contact in contacts)
    assert len(responses.calls) == 1