// Live preview: regenerate the mulmo viewer whenever the script file changes
// and auto-reload the browser via server-sent events.
//
// Usage: npm run preview -- mulmoclaude/vision/<name>.json
const { execFile } = require("child_process");
const fs = require("fs");
const http = require("http");
const path = require("path");

const args = process.argv.slice(2);
const noOpen = args.includes("--no-open");
const file = args.find((a) => !a.startsWith("--"));
if (!file || !file.endsWith(".json")) {
  console.error("Usage: npm run preview -- <script>.json [--no-open]");
  process.exit(1);
}
const scriptPath = path.resolve(file);
const basename = path.basename(scriptPath, ".json");
const viewerPath = path.resolve("output", basename, `${basename}_viewer.html`);
const port = Number(process.env.PORT) || 8787;

const CLIENT_SNIPPET = `
<script>
(() => {
  const es = new EventSource("/events");
  es.addEventListener("reload", () => location.reload());
  es.addEventListener("generating", () => banner("Regenerating…", "#1e3a5f"));
  es.addEventListener("error", (e) => banner(JSON.parse(e.data), "#7f1d1d"));
  function banner(text, bg) {
    let el = document.getElementById("mulmo-live-banner");
    if (!el) {
      el = document.createElement("div");
      el.id = "mulmo-live-banner";
      el.style.cssText = "position:fixed;top:0;left:0;right:0;z-index:99999;" +
        "padding:8px 16px;font:13px Menlo,monospace;color:#fff;white-space:pre-wrap";
      document.body.appendChild(el);
    }
    el.style.background = bg;
    el.textContent = text;
  }
})();
</script>`;

let html = "<p>Generating first preview…</p>" + CLIENT_SNIPPET;
let generating = false;
let pending = false;
const clients = new Set();

// Exit when the last tab closes. Reloads drop the connection briefly before
// reconnecting, so only shut down after a grace period with no clients.
const SHUTDOWN_GRACE_MS = 5000;
let everConnected = false;
let shutdownTimer;
function maybeShutdown() {
  if (!everConnected || clients.size > 0) return;
  clearTimeout(shutdownTimer);
  shutdownTimer = setTimeout(() => {
    if (clients.size === 0) {
      console.log("All preview tabs closed — shutting down.");
      process.exit(0);
    }
  }, SHUTDOWN_GRACE_MS);
}

function broadcast(event, data) {
  for (const res of clients) res.write(`event: ${event}\ndata: ${data}\n\n`);
}

function generate(onDone) {
  if (generating) {
    pending = true;
    return;
  }
  generating = true;
  broadcast("generating", "1");
  console.log(`[${new Date().toLocaleTimeString()}] regenerating…`);
  execFile("mulmo", ["viewer", "-g", scriptPath], { cwd: path.resolve(__dirname, "..") }, (err, stdout, stderr) => {
    generating = false;
    if (err) {
      const msg = (stderr || stdout || err.message)
        .replace(/\x1b\[[0-9;]*m/g, "")
        .split(/\n\s+at /)[0]
        .trim()
        .slice(-2000);
      console.error(msg);
      broadcast("error", JSON.stringify("Generation failed:\n" + msg));
    } else {
      html = fs.readFileSync(viewerPath, "utf8").replace(/<\/body>/i, CLIENT_SNIPPET + "</body>");
      console.log(`[${new Date().toLocaleTimeString()}] updated`);
      broadcast("reload", "1");
      if (onDone) onDone();
    }
    if (pending) {
      pending = false;
      generate();
    }
  });
}

const server = http.createServer((req, res) => {
  if (req.url === "/events") {
    res.writeHead(200, {
      "Content-Type": "text/event-stream",
      "Cache-Control": "no-cache",
      Connection: "keep-alive",
    });
    res.write("\n");
    clients.add(res);
    everConnected = true;
    clearTimeout(shutdownTimer);
    res.on("close", () => {
      clients.delete(res);
      maybeShutdown();
    });
    return;
  }
  res.writeHead(200, { "Content-Type": "text/html; charset=utf-8" });
  res.end(html);
});

let debounce;
fs.watch(path.dirname(scriptPath), (eventType, filename) => {
  if (filename !== path.basename(scriptPath)) return;
  clearTimeout(debounce);
  debounce = setTimeout(() => generate(), 300);
});

server.listen(port, () => {
  const url = `http://localhost:${port}`;
  console.log(`Live preview of ${path.relative(process.cwd(), scriptPath)} at ${url}`);
  let opened = noOpen;
  generate(() => {
    if (!opened) {
      opened = true;
      execFile("open", [url]);
    }
  });
});
