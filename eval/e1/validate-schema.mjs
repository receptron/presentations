#!/usr/bin/env node
// E1 harness: validate a model-authored collection schema with the PRODUCTION
// validator from @mulmoclaude/core (CollectionSchemaZ + acceptParsedSchema).
// Usage: node validate-schema.mjs <schema.json> [...more]
// Output: one JSON line per input file:
//   { file, parse: "ok"|"json-error", zod: "pass"|"fail", zodIssues: [...],
//     gates: "pass"|"fail"|"skipped", gateReason }
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

const CORE = resolve(
  process.env.MULMOCLAUDE_REPO ?? `${process.env.HOME}/git/ai/mulmoclaude`,
  "packages/core/dist/collection/server/index.js",
);
const { CollectionSchemaZ, acceptParsedSchema } = await import(CORE);

// Acceptance gates check dataPath containment against a workspace root; any
// root works for that purpose since authored dataPaths are workspace-relative.
const WORKSPACE_ROOT = process.env.E1_WORKSPACE_ROOT ?? "/tmp/e1-workspace";

const out = [];
for (const file of process.argv.slice(2)) {
  const row = { file };
  let raw;
  try {
    raw = JSON.parse(readFileSync(file, "utf8"));
    row.parse = "ok";
  } catch (e) {
    row.parse = "json-error";
    row.parseError = String(e.message).slice(0, 200);
    out.push(row);
    continue;
  }
  const parsed = CollectionSchemaZ.safeParse(raw);
  if (parsed.success) {
    row.zod = "pass";
    try {
      const acceptance = acceptParsedSchema(parsed.data, {
        source: "user",
        workspaceRoot: WORKSPACE_ROOT,
      });
      row.gates = acceptance?.ok === false ? "fail" : "pass";
      if (acceptance?.ok === false) row.gateReason = acceptance.reason ?? acceptance;
    } catch (e) {
      row.gates = "skipped";
      row.gateReason = String(e.message).slice(0, 200);
    }
  } else {
    row.zod = "fail";
    row.zodIssues = parsed.error.issues.map((i) => ({
      path: i.path.join("."),
      code: i.code,
      message: i.message,
    }));
  }
  out.push(row);
}
for (const row of out) console.log(JSON.stringify(row));
