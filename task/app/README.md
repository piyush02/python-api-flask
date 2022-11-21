### API app code

Python flask based app that stores and returns JSON record with HTTP Status Code appropriate to each request/response.
This api app returns valid JSON response for all the API requests.

## Prerequisites

- Python3.X
- pip3
- flask

## Assumption

- Every POST entery with unique name.
- In memory DB is used to keep the records. Nosql db is required for Production env.

## Following are the endpoints are supported:

| Name   | Method      | URL
| ---    | ---         | ---
| List   | `GET`       | `/configs`
| Create | `POST`      | `/configs`
| Get    | `GET`       | `/configs/{name}`
| Update | `PUT/PATCH` | `/configs/{name}`
| Delete | `DELETE`    | `/configs/{name}`
| Query  | `GET`       | `/search?metadata.key=value`

#### Query

The query endpoint return all configs that satisfy the query argument.

Query example:

```sh
curl http://config-service/search?metadata.monitoring.enabled=true
```
