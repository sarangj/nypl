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
    summary = {"type_summary": {}, "availability_summary": {}}
    for capture in api.get_all_items_in_collection(client, uid):
        asset_type_summary = summary["type_summary"].get(capture.type_of_resource, {})
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


    data = flask.jsonify({"asset_summary": summary})
    response = app.make_response(data)
    response.content_type = "application/json"
    return response


@app.errorhandler(api.APIError)
def not_found(e) -> flask.Response:
    data = flask.jsonify({"error": {"msg": "Could not talk to NYPL"}})
    response = app.make_response(data)
    response.content_type = "application/json"
    response.status = 500
    return response


@app.errorhandler(api.APINotFound)
def not_found(e) -> flask.Response:
    data = flask.jsonify({"error": {"msg": "UID Not Found"}})
    response = app.make_response(data)
    response.content_type = "application/json"
    response.status = 404
    return response


def _default_summary(capture: api.GenericCapture) -> dict:
    return {
        "count": 1,
        "example_uid": capture.uid,
        "example_api_uri": capture.api_uri,
        "example_item_link": capture.item_link,
    }
