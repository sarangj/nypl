import collections
import os

import flask

import nypl.api as api


app = flask.Flask(__name__)
app.config["API_TOKEN"] = os.environ["API_TOKEN"]


@app.route('/api/collections/<uid>/asset-summary')
def get_collection_asset_summary(uid: str) -> flask.Response:
    client = api.Client(token=app.config["API_TOKEN"])
    asset_type_count = collections.defaultdict(int)
    for capture in api.get_all_items_in_collection(client, uid):
        asset_type_count[capture["typeOfResource"]] += 1

    data = flask.jsonify(
        {
            "asset_summary": {
                "asset_types": dict(asset_type_count),
            },
        },
    )
    response = app.make_response(data)
    response.content_type = "application/json"
    return response
