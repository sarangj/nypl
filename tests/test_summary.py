import json
import pytest

import nypl.api
import nypl.summary


def test_get_collection_summary(mocker):
    get_all_items = mocker.patch(
        "nypl.api.get_all_items_in_collection",
        return_value=[
            nypl.api.GenericCapture(
                uid=mocker.sentinel.image_1_uid,
                type_of_resource="still image",
                api_uri=mocker.sentinel.image_1_api_uri,
                item_link=mocker.sentinel.image_1_item_link,
                rights_statement_uri=nypl.api.GenericCapture.private_uri,
            ),
            nypl.api.GenericCapture(
                uid=mocker.sentinel.image_2_uid,
                type_of_resource="still image",
                api_uri=mocker.sentinel.image_2_api_uri,
                item_link=mocker.sentinel.image_2_item_link,
                rights_statement_uri="",
            ),
            nypl.api.GenericCapture(
                uid=mocker.sentinel.music_uid,
                type_of_resource="notated music",
                api_uri=mocker.sentinel.music_api_uri,
                item_link=mocker.sentinel.music_item_link,
                rights_statement_uri="some uri",
            ),
        ],
    )
    client = mocker.create_autospec(nypl.api.Client)
    summary = nypl.summary.build_asset_summary(
        client,
        mocker.sentinel.collection_uid,
    )
    assert summary == {
        "type_summary": {
            "still image": {
                "count": 2,
                "example_uid": mocker.sentinel.image_1_uid,
                "example_api_uri": mocker.sentinel.image_1_api_uri,
                "example_item_link": mocker.sentinel.image_1_item_link,
            },
            "notated music": {
                "count": 1,
                "example_uid": mocker.sentinel.music_uid,
                "example_api_uri": mocker.sentinel.music_api_uri,
                "example_item_link": mocker.sentinel.music_item_link,
            },
        },
        "availability_summary": {
            "public": {
                "count": 2,
                "example_uid": mocker.sentinel.image_2_uid,
                "example_api_uri": mocker.sentinel.image_2_api_uri,
                "example_item_link": mocker.sentinel.image_2_item_link,
            },
            "private": {
                "count": 1,
                "example_uid": mocker.sentinel.image_1_uid,
                "example_api_uri": mocker.sentinel.image_1_api_uri,
                "example_item_link": mocker.sentinel.image_1_item_link,
            },
        },
    }
