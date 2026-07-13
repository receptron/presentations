# Figure 2 — A complete application (listing, for typesetting as a code figure)

Abridged from the real `restaurants` collection in the author's workspace
(structure only, per the disclosure policy). Caption below.

```json
{
  "title": "Restaurants",
  "icon": "restaurant",
  "dataPath": "data/restaurants/items",
  "primaryKey": "id",
  "displayField": "name",
  "fields": {
    "id":       { "type": "string",  "label": "ID", "primary": true, "required": true },
    "name":     { "type": "string",  "label": "Name", "required": true },
    "cuisine":  { "type": "string",  "label": "Cuisine" },
    "visited":  { "type": "boolean", "label": "Visited" },
    "rating":   { "type": "enum",    "label": "Rating",
                  "values": ["★", "★★", "★★★", "★★★★", "★★★★★"],
                  "when":   { "field": "visited", "in": ["true"] } },
    "image":    { "type": "image",   "label": "Photo" },
    "notes":    { "type": "text",    "label": "Notes" }
  },
  "views": [
    { "id": "tokyo-map", "label": "Map", "icon": "map",
      "file": "views/tokyo-map.html", "capabilities": ["read"] }
  ]
}
```

A record the schema governs (one JSON file in `data/restaurants/items/`):

```json
{
  "id": "tartine-bakery",
  "name": "Tartine Bakery",
  "cuisine": "Bakery",
  "visited": true,
  "rating": "★★★★",
  "notes": "Go early; the morning bun sells out."
}
```

**Caption:** *A complete application: the schema (top) and a record it governs
(bottom). The schema declares data (typed fields), conditional structure
(`rating` appears — and is accepted — only once `visited` is true), and
presentation (a model-authored custom view with a declared read-only capability
set). From these declarations the host renders table, kanban, and map views,
validates writes on the managed path, and sandboxes the view code; the model
authored both artifacts — and the companion operating manual that guides its own
future sessions — from one sentence of conversation. Schema abridged; from the
authors' own workspace (record synthetic).*
