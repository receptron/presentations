# Declined: not a collection request

Request: "Write me a poem about databases."

This is a one-off creative-writing request, not a data-app request. There is no
data model, no records to CRUD, no views (table/calendar/kanban), no lifecycle
(bells, recurrence), and no relations — nothing a `schema.json` would declare.
Authoring a collection here (e.g. a "poems" collection with one record) would be
over-engineering a simple ask.

How I would actually respond: just write the poem directly in chat. If the user
later said they want to keep a growing library of poems they write or collect —
with fields like title, theme, date written, favorite flag — THEN a `poems`
collection would be a good fit, and I would author `schema.json` + `SKILL.md`
for it at that point.
