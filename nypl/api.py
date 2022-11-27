import dataclasses
import typing as t

import requests
import requests.exceptions


class Client:

    BASE_URL = "https://api.repo.nypl.org/api/v2"

    def __init__(self, token: str):
        self.session = requests.Session()
        self.session.headers["Authorization"] = f"Token token=\"{token}\""

    def get(self, path: str, params: dict[str, t.Any]) -> dict:
        response = self.session.get(self.BASE_URL + path, params=params)
        try:
            response.raise_for_status()
        except request.errors.HTTPError:
            raise APIError()
        response_data = response.json()["nyplAPI"]["response"]
        if response_data["headers"]["status"] != "success":
            # TODO: Make more granular
            raise APIError()

        return response_data


@dataclasses.dataclass
class GenericCapture:
    """Generic data about a capture"""
    uid: str
    type_of_resource: str
    api_uri: str
    item_link: str
    rights_statement_uri: str

    private_uri: t.ClassVar[str] = "http://rightsstatements.org/vocab/UND/1.0/"

    def is_public(self) -> bool:
        # This is kind of a guess tbh
        return not self.rights_statement_uri.startswith(self.private_uri)


def get_item_page_for_collection(client: Client, uid: str, page: int = 0) -> dict:
    # Max out the page size for now
    params = {"page": page, "per_page": 500}
    return client.get(f"/items/{uid}", params=params)


def get_all_items_in_collection(client: Client, uid: str) -> t.Iterator[GenericCapture]:
    response_data = get_item_page_for_collection(client, uid)
    captures = response_data.get("capture")
    # If the first page is missing stuff, this seems to be like a 404
    if not captures:
        raise APINotFound()

    page = 0
    # I would use `numResults` in the response, but it seems to sometimes not match up
    # to the total number of available results?
    while captures:
        for capture in captures:
            try:
                yield _parse_capture(capture)
            except KeyError:
                raise APIParseError()

        page += 1
        captures = get_item_page_for_collection(client, uid, page=page).get("capture")


def _parse_capture(c: dict) -> GenericCapture:
    return GenericCapture(
        uid=c["uuid"],
        type_of_resource=c["typeOfResource"],
        api_uri=c["apiUri"],
        item_link=c["itemLink"],
        rights_statement_uri=c["rightsStatementURI"],
    )


class APIError(Exception):
    pass


class APINotFound(APIError):
    pass


class APIParseError(APIError):
    pass
