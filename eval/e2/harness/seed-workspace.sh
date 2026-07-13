#!/bin/zsh
# Seed a scratch MulmoClaude workspace with a synthetic collection that
# exercises the reconciler semantics (completion bell, trigger lead,
# spawn recurrence). All data synthetic per eval/DISCLOSURE.md.
# Usage: ./seed-workspace.sh <workspace-dir> [due-date] [done-date] [far-date]
set -eu
W="$1"
DUE="${2:-}"    # a date within triggerLeadDays of "now" → bell expected
DONE="${3:-}"   # a completed record's trigger → spawn successor expected
FAR="${4:-}"    # a far-future trigger → nothing at real now
mkdir -p "$W/.claude/skills/maintenance-tasks" "$W/data/maintenance-tasks/items"

cat > "$W/.claude/skills/maintenance-tasks/SKILL.md" <<'EOF'
---
name: maintenance-tasks
description: synthetic evaluation fixture (E2 harness)
---
Synthetic fixture. Records at data/maintenance-tasks/items.
EOF

cat > "$W/.claude/skills/maintenance-tasks/schema.json" <<'EOF'
{
  "title": "Maintenance Tasks",
  "icon": "build",
  "dataPath": "data/maintenance-tasks/items",
  "primaryKey": "id",
  "displayField": "title",
  "fields": {
    "id": { "type": "string", "label": "ID", "primary": true, "required": true },
    "title": { "type": "string", "label": "Title", "required": true },
    "status": { "type": "enum", "label": "Status", "values": ["pending", "done"] },
    "nextDue": { "type": "date", "label": "Next due" }
  },
  "completionField": "status",
  "completionDoneValues": ["done"],
  "triggerField": "nextDue",
  "triggerLeadDays": 3,
  "spawn": {
    "when": { "field": "status", "in": ["done"] },
    "every": { "unit": "month", "interval": 1 },
    "carry": ["title"]
  }
}
EOF

emit() { printf '{"id":"%s","title":"%s","status":"%s","nextDue":"%s"}\n' "$1" "$2" "$3" "$4" > "$W/data/maintenance-tasks/items/$1.json"; }
[ -n "$DUE" ]  && emit m-due  "Replace filter" pending "$DUE"
[ -n "$DONE" ] && emit m-done "Clean gutters"  done    "$DONE"
[ -n "$FAR" ]  && emit m-far  "Service boiler" pending "$FAR"
echo "seeded $W"
