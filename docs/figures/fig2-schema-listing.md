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

**Caption:** *A complete application. The schema declares data (typed fields),
conditional structure (`rating` appears only once `visited` is true), and
presentation (a model-authored custom view with a declared read-only capability
set). The host renders, validates, and sandboxes from this declaration; the model
authored it — and its companion operating manual — from one sentence of
conversation. Fields abridged; from the authors' own workspace.*
