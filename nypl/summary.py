import typing as t

import nypl.api


def build_asset_summary(client: nypl.api.Client, collection_uid: str) -> dict:
    summary = {
        "type_summary": {},
        "availability_summary": {},
    }
    for capture in nypl.api.get_all_items_in_collection(client, collection_uid):
        asset_type_summary = summary["type_summary"].get(capture.type_of_resource)
        if asset_type_summary:
            asset_type_summary["count"] += 1
        else:
            summary["type_summary"][capture.type_of_resource] = _default_summary(capture)
        availability_key = "public" if capture.is_public() else "private"
        availability = summary["availability_summary"].get(availability_key)
        if availability:
            availability["count"] += 1
        else:
            summary["availability_summary"][availability_key] = _default_summary(capture)

    return summary


def _default_summary(capture: nypl.api.GenericCapture):
    return {
        "count": 1,
        "example_uid": capture.uid,
        "example_api_uri": capture.api_uri,
        "example_item_link": capture.item_link,
    }
