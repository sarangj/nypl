import collections
import dataclasses
import os

import flask

import nypl.api as api


app = flask.Flask(__name__)
app.config["API_TOKEN"] = os.environ["API_TOKEN"]


@app.route('/api/collections/<uid>/asset-summary')
def get_collection_asset_summary(uid: str) -> flask.Response:
    client = api.Client(token=app.config["API_TOKEN"])
    summary = {}
    for capture in api.get_all_items_in_collection(client, uid):
        asset_type_summary = summary.get(capture.type_of_resource, {})
        if asset_type_summary:
            asset_type_summary["count"] += 1
        else:
            summary[capture.type_of_resource] = {
                "count": 1,
                "example_uid": capture.uid,
                "example_api_uri": capture.api_uri,
                "example_item_link": capture.item_link,
            }

    data = flask.jsonify({"asset_summary": asset_type_summary})
    response = app.make_response(data)
    response.content_type = "application/json"
    return response
