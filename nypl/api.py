import typing as t

import requests


class Client:

    BASE_URL = "https://api.repo.nypl.org/api/v2"

    def __init__(self, token: str):
        self.session = requests.Session()
        self.session.headers["Authorization"] = f"Token token=\"{token}\""

    def get(self, path: str, params: dict[str, t.Any]) -> dict:
        response = self.session.get(self.BASE_URL + path, params=params)
        response.raise_for_status()
        response_data = response.json()["nyplAPI"]["response"]
        if response_data["headers"]["status"] != "success":
            # TODO: Make more granular
            raise Exception()

        return response_data


def get_item_page_for_collection(client: Client, uid: str, page: int = 0) -> dict:
    # Max out the page size for now
    params = {"page": page, "per_page": 500}
    return client.get(f"/items/{uid}", params=params)


def get_all_items_in_collection(client: Client, uid: str) -> t.Iterator:
    response_data = get_item_page_for_collection(client, uid)
    page = 0
    # I would use `numResults` in the response, but it seems to sometimes not match up
    # to the total number of available results?
    # Upside, it's my first time using the ol' walrus...
    while captures := response_data.get("capture"):
        for capture in captures:
            yield capture

        page += 1
        response_data = get_item_page_for_collection(client, uid, page=page)
