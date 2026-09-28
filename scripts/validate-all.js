const fs = require("fs");
const path = require("path");
const { mulmoScriptSchema } = require("mulmocast");

// samples/ also holds data JSON next to its decks (beat tables, fetched data, music plans),
// so there only files carrying the "$mulmocast" key are treated as MulmoScripts.
const roots = [
  { dir: "mulmoclaude", scriptsOnly: false },
  { dir: "mulmoterminal", scriptsOnly: false },
  { dir: "samples", scriptsOnly: true },
];
const isMulmoScript = (file) => {
  try {
    return Object.prototype.hasOwnProperty.call(JSON.parse(fs.readFileSync(file, "utf8")), "$mulmocast");
  } catch {
    return true; // unreadable JSON is reported by the validation below
  }
};
const files = roots
  .map(({ dir, scriptsOnly }) => ({ root: path.join(__dirname, "..", dir), scriptsOnly }))
  .filter(({ root }) => fs.existsSync(root))
  .flatMap(({ root, scriptsOnly }) =>
    fs
      .readdirSync(root, { recursive: true })
      .filter((f) => f.endsWith(".json"))
      .map((f) => path.join(root, f))
      .filter((file) => !scriptsOnly || isMulmoScript(file)),
  )
  .sort();

if (files.length === 0) {
  console.error("No MulmoScript files found under mulmoclaude/, mulmoterminal/ or samples/");
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
