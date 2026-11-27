# Music Performance Tracking API

A Django REST Framework backend for tracking live music events. SQLite stores
the catalog, event lineups, submissions, and users' favorite bands.

## Local setup

From the repository root, with Python 3.9 or later and uv installed:

```sh
uv sync --locked
uv run manage.py migrate
uv run manage.py createsuperuser
uv run manage.py runserver
```

Open the [browsable API](http://127.0.0.1:8000/api/) to explore the routes,
[Django Admin](http://127.0.0.1:8000/admin/) to manage records, or the
[API login page](http://127.0.0.1:8000/api-auth/login/) to sign in with a
Django account.

## API routes

| Route | Methods | Access |
| --- | --- | --- |
| `/api/bands/`, `/api/venues/` | GET, POST | Public reads and signed-in creation |
| `/api/bands/<id>/`, `/api/venues/<id>/` | GET, PUT, PATCH, DELETE | Public reads and staff-only changes |
| `/api/events/` | GET, POST | Public reads and signed-in creation |
| `/api/events/<id>/` | GET, PUT, PATCH, DELETE | Public reads and changes by the submitter or staff |
| `/api/events/<id>/performances/` | POST | Add a band to the lineup as the event submitter or staff |
| `/api/favorites/` | GET, POST | List or follow bands as the signed-in user |
| `/api/favorites/<id>/` | GET, DELETE | Read or remove one of your own favorite records |
| `/api/events/favorite-upcoming/` | GET | List future events featuring bands you follow |

Event responses include the lineup. The server sets the event submitter from
the authenticated request. To add a performance, post a band ID and optionally
`set_time` and `is_headliner` to the lineup route. To follow a band, post
`{"band": 3}` to `/api/favorites/`, replacing `3` with the band's ID.

Filter the event list with `band` or `venue` IDs, a partial `city` name, a
`date` in `YYYY-MM-DD` format (UTC), or `upcoming=true`. For example:

```text
/api/events/?city=St.%20Paul&upcoming=true
```

The upcoming filter uses the event time. Event statuses are `scheduled`,
`canceled`, and `postponed`.

## Database and demo

Each event links to a venue and can record a submitting user. `Performance`
links bands to events with optional set times and headliner flags.
`FavoriteBand` links users to the bands they follow. The database enforces
unique band names, venue name and city pairs, event and band pairs, and user
and band pairs.

In Django Admin, create a venue, two bands, and a future event. Add both bands
through the event's inline performance form, then open `/api/events/` to see
the lineup. Create two regular users in Admin to demonstrate how event
ownership affects API edits.

## Checks

```sh
uv run manage.py check
uv run manage.py test
```
