const fs = require("fs");
const path = require("path");
const { mulmoScriptSchema } = require("mulmocast");

const roots = ["mulmoclaude", "mulmoterminal"].map((d) => path.join(__dirname, "..", d));
const files = roots
  .filter((root) => fs.existsSync(root))
  .flatMap((root) =>
    fs
      .readdirSync(root, { recursive: true })
      .filter((f) => f.endsWith(".json"))
      .map((f) => path.join(root, f)),
  )
  .sort();

if (files.length === 0) {
  console.error("No MulmoScript files found under mulmoclaude/ or mulmoterminal/");
  process.exit(1);
}

let failures = 0;
for (const file of files) {
  const rel = path.relative(process.cwd(), file);
  let script;
  try {
    script = JSON.parse(fs.readFileSync(file, "utf8"));
  } catch (e) {
    console.error(`✗ ${rel} — invalid JSON: ${e.message}`);
    failures++;
    continue;
  }
  const result = mulmoScriptSchema.safeParse(script);
  if (result.success) {
    console.log(`✓ ${rel}`);
  } else {
    console.error(`✗ ${rel}`);
    for (const issue of result.error.issues) {
      console.error(`    ${issue.path.join(".")}: ${issue.message}`);
    }
    failures++;
  }
}

console.log(`\n${files.length - failures}/${files.length} valid`);
process.exit(failures ? 1 : 0);
