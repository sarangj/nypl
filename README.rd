# NYPL Collection Asset Summary

This endpoint summarizes the all the physical assets in a collection

## Data

  - Path: /api/collections/<uid>/asset-summary

```json
{
  "asset_summary": {
    "type_summary": {
      <type>: {
        "count": "int",
        "example_uid": "str",
        "example_api_uri": "str",
        "example_item_link": "str",
      }
    },
    "availability_summary": {
      "public": {
        "count": "int",
        "example_uid": "str",
        "example_api_uri": "str",
        "example_item_link": "str",
      },
      "private": {
        "count": "int",
        "example_uid": "str",
        "example_api_uri": "str",
        "example_item_link": "str",
      }
    }
  }
}
```

## Development

  - Clone the repo
  - Install poetry: https://python-poetry.org/docs/#installing-with-the-official-installer
  - Run `poetry install` from the repo
  - Set the $API_TOKEN env var in a `.env` file at the repo root
  - Run `$ poetry run flask -A nypl/server.py run` to run the server locally
  - Run `$ poetry run pytest` to run tests

## Potential improvements

  - More / better testing
  - Linting
  - A cache
  - Async or threads to make requests concurrently (we could use `numResults` or something to batch page requests)

