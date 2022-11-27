import os

import flask

import nypl.api
import nypl.summary

app = flask.Flask(__name__)


@app.route('/api/collections/<uid>/asset-summary')
def get_collection_asset_summary(uid: str) -> flask.Response:
    client = nypl.api.Client(token=os.environ["API_TOKEN"])
    summary = nypl.summary.build_asset_summary(client, uid)

    data = flask.jsonify({"asset_summary": summary})
    response = app.make_response(data)
    response.content_type = "application/json"
    return response


@app.errorhandler(nypl.api.APIError)
def not_found(e) -> flask.Response:
    data = flask.jsonify({"error": {"msg": "Could not talk to NYPL"}})
    response = app.make_response(data)
    response.content_type = "application/json"
    response.status = 500
    return response


@app.errorhandler(nypl.api.APINotFound)
def not_found(e) -> flask.Response:
    data = flask.jsonify({"error": {"msg": "UID Not Found"}})
    response = app.make_response(data)
    response.content_type = "application/json"
    response.status = 404
    return response
