from typing_extensions import TypedDict, NotRequired


class ListQueryParams(TypedDict):
    """
    Interface of the query parameters for listing resources.

    Attributes:
        limit: The maximum number of objects to return.
            This field defaults to 50. The maximum allowed value is 200.
        page_token: An identifier that specifies which page of data to return.
            This value should be taken from a ListResponse object's next_cursor parameter.
    """

    limit: NotRequired[int]
    page_token: NotRequired[str]
