#!/bin/zsh
# E3 transfer-matrix inventory: enumerate a MulmoClaude workspace's state by
# artifact type, using the directory layout itself as the coding scheme.
# AGGREGATE COUNTS ONLY — never prints record contents.
# Usage: ./inventory.sh [workspace-root]   (default ~/mulmoclaude)
set -u
W="${1:-$HOME/mulmoclaude}"
count() { print -r -- "$2:	$1"; }

n() { local c; c=$(eval "$1" 2>/dev/null | wc -l | tr -d ' '); echo "$c"; }

echo "# Workspace inventory: $W ($(date +%Y-%m-%d))"
echo
echo "## Conversational / memory layer (what portability protocols target)"
count "$(n "ls $W/conversations/chat/*.jsonl")" "chat session transcripts (jsonl)"
count "$(n "find $W/conversations/memory -name '*.md'")" "memory topic files"
count "$(n "find $W/conversations/summaries -type f")" "conversation summaries"
echo
echo "## Application layer (schema-as-application)"
count "$(n "ls $W/data/skills/*/schema.json")" "collection schemas (applications)"
count "$(n "ls $W/data/skills/*/SKILL.md")" "SKILL.md operating manuals"
count "$(n "ls $W/data/skills/*/views/*.html")" "custom view files (model-authored code)"
count "$(n "ls -d $W/data/*/items")" "collections with record stores"
count "$(n "find $W/data/*/items -name '*.json'")" "collection records"
echo
echo "## Knowledge layer"
count "$(n "ls $W/data/wiki/pages/*.md")" "wiki pages"
count "$(n "ls $W/data/wiki/.history")" "wiki pages with snapshot history"
count "$(n "find $W/data/wiki/.history -name '*.md'")" "wiki history snapshots"
echo
echo "## Host-executed state (behavioral)"
count "$(n "find $W/data/scheduler -type f")" "scheduler/automation entries"
count "$(n "find $W/data/notifier -type f")" "notifier (reminder bell) state files"
count "$(n "find $W/feeds -name '_state.json'")" "feed ingest state files"
count "$(n "ls -d $W/data/feeds/* 2>/dev/null; ls -d $W/feeds/* 2>/dev/null | grep -v _state")" "feed definitions (approx)"
echo
echo "## Media / documents"
count "$(n "find $W/data/attachments -type f")" "attachments"
count "$(n "find $W/artifacts -type f")" "generated artifacts (charts/docs/etc.)"
