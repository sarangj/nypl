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
    total_items = int(response_data["numResults"])
    items_collected = 0
    page = 0
    print(total_items)
    while True:
        for capture in response_data["capture"]:
            items_collected += 1
            yield capture

        if items_collected >= total_items:
            break
        page += 1

        print(f"Page {page}")
        print(f"{items_collected} collected")
        response_data = get_item_page_for_collection(client, uid, page=page)
