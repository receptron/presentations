"""Idea: a news show written by a script from live public data (GitHub search + Open-Meteo), narrated by TTS.

Run this right before rendering and the video is about *now*: every headline, number and
quake below comes from the JSON fetched at build time, and the narration is generated from it.
"""
import datetime
import html as H
import json
import pathlib

HERE = pathlib.Path(__file__).parent
repos = {r["name"]: r for r in json.load(open(HERE / "data" / "gh.json"))}
temps = json.load(open(HERE / "data" / "temps.json"))
# Hand-picked from the fetched list: neutral topics only (no chat-reading, crypto, politics, disasters).
PICK = [("dgreenheck/tidewater", "a coastal town, built with Opus 5.5"),
        ("852wa/JIZURA", "a browser app that turns song lyrics into a lyric video"),
        ("tobi/disktree", "a treemap for finding what fills your disk")]
stories = [{"title": f"{n}: {d}", "name": n, "desc": d, "score": repos[n]["stars"], "comments": repos[n]["forks"], "lang": repos[n]["lang"]} for n, d in PICK]
TICK = ["dgreenheck/tidewater", "852wa/JIZURA", "tobi/disktree", "yetone/magpie", "unreallabsai/unreal-agent", "mikehasa/golive-skill", "riba2534/claude-opus-5-5-demo"]
stamp = datetime.datetime.fromisoformat(temps[0]["time"]).strftime("%b %d, %Y · %H:%M UTC")
cold, hot = min(temps, key=lambda x: x["temp"]), max(temps, key=lambda x: x["temp"])
ticker = "   ◆   ".join(H.escape(f"{n} ★{repos[n]['stars']:,}") for n in TICK)

HELPERS = """
function clamp01(x) { return Math.max(0, Math.min(1, x)); }
function P(t, a, b) { return clamp01((t - a) / (b - a)); }
function eout(x) { return 1 - Math.pow(1 - x, 3); }
function eback(x) { var c1 = 1.70158, c3 = c1 + 1; return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2); }
function $(id) { return document.getElementById(id); }
"""
FONT = "<style>.t{font-family:'Helvetica Neue',Helvetica,Arial,sans-serif}.cond{font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;font-stretch:condensed}</style>"
NAVY = "#0b1a33"


def chrome(inner):
    """Broadcast frame shared by every beat: bug, clock, ticker."""
    return (f"{FONT}<div class='t relative overflow-hidden' style='width:1280px;height:720px;background:radial-gradient(1200px 700px at 30% 20%,#17305c,{NAVY} 70%);color:#fff'>"
            f"{inner}"
            "<div class='absolute left-0 right-0 bottom-0 flex items-center' style='height:54px;background:#fff;color:#0b1a33'>"
            "<div class='h-full flex items-center px-6 font-extrabold text-xl' style='background:#e11d48;color:#fff'>LIVE DATA</div>"
            f"<div class='relative flex-1 h-full overflow-hidden'><div id='tick' class='absolute whitespace-nowrap font-bold text-xl' style='top:14px;left:0'>{ticker}   ◆   {ticker}</div></div></div>"
            f"<div class='absolute right-6 top-5 text-right font-bold' style='font-size:18px;opacity:.85'>GITHUB WEEKLY<br><span style='font-weight:400'>{stamp}</span></div>"
            "</div>")


TICK_JS = "function tick(t) { $('tick').style.transform = 'translateX(' + (-t * 140) + 'px)'; }\n"


def beat(label, text, inner, script):
    return {"id": label, "text": text,
            "image": {"type": "html_tailwind", "html": chrome(inner), "script": HELPERS + TICK_JS + script, "animation": {"fps": 30}}}


opening = beat("news-open",
               "Good evening. These are the week's fastest-rising new projects on GitHub, and this whole show was generated automatically from live data.",
               """
<div id='bars' class='absolute inset-0'></div>
<div class='absolute inset-0 flex flex-col items-center justify-center'>
  <div id='logo' class='font-black tracking-tight' style='font-size:130px;line-height:1'>GITHUB<span style='color:#e11d48'>WEEKLY</span></div>
  <div id='sub' class='mt-4 font-bold tracking-[0.5em] text-2xl' style='opacity:0'>AUTOMATICALLY GENERATED</div>
</div>""", """
var bars = $('bars');
for (var i = 0; i < 12; i++) { var b = document.createElement('div'); b.style.cssText = 'position:absolute;left:0;height:60px;width:0;top:' + (i * 60) + 'px;background:' + (i % 3 ? '#1e3a8a' : '#e11d48'); bars.appendChild(b); }
function render(frame, total, fps) {
  var t = frame / fps; tick(t);
  for (var i = 0; i < 12; i++) { var p = P(t, i * 0.03, 0.45 + i * 0.03), q = P(t, 0.7 + i * 0.02, 1.1 + i * 0.02); var el = bars.children[i]; el.style.width = (eout(p) * 100) + '%'; el.style.left = (eout(q) * 100) + '%'; }
  var l = P(t, 0.9, 1.4); $('logo').style.transform = 'scale(' + (0.4 + eback(l) * 0.6) + ')'; $('logo').style.opacity = l;
  $('sub').style.opacity = P(t, 1.5, 2.0); $('sub').style.letterSpacing = (1.2 - 0.7 * eout(P(t, 1.5, 2.3))) + 'em';
}""")


def story(rank, s):
    title = H.escape(s["title"])
    return beat(f"news-story-{rank}",
                f"Number {['one', 'two', 'three'][rank - 1]}. {s['name'].replace('/', ' slash ')}: {s['desc']}. {s['score']:,} stars in its first week.",
                f"""
<div id='wipe' class='absolute inset-y-0 left-0' style='width:0;background:#e11d48'></div>
<div id='rank' class='absolute font-black' style='left:70px;top:70px;font-size:260px;line-height:1;color:#e11d48;opacity:0'>{rank}</div>
<div class='absolute' style='left:300px;right:80px;top:120px'>
  <div id='kick' class='font-bold tracking-[0.3em] text-xl' style='color:#93c5fd;opacity:0'>RISING · #{rank} · {H.escape(s['lang'] or '')}</div>
  <div id='head' class='font-extrabold mt-3' style='font-size:52px;line-height:1.12'></div>
</div>
<div class='absolute flex gap-16' style='left:300px;top:430px'>
  <div><div id='pts' class='font-black' style='font-size:84px;line-height:1'>0</div><div class='text-xl opacity-70'>stars</div></div>
  <div><div id='cmt' class='font-black' style='font-size:84px;line-height:1'>0</div><div class='text-xl opacity-70'>forks</div></div>
</div>
<div id='lt' class='absolute flex items-center' style='left:0;top:586px;height:56px;transform:translateX(-100%)'>
  <div class='h-full px-5 flex items-center font-bold' style='background:#e11d48'>{H.escape(s['name'].split('/')[0])}</div>
  <div class='h-full px-5 flex items-center' style='background:#fff;color:#0b1a33'>github.com/{H.escape(s['name'])}</div>
</div>""", f"""
var HEAD = {json.dumps(s['title'])}, PTS = {s['score']}, CMT = {s['comments']};
function render(frame, total, fps) {{
  var t = frame / fps; tick(t);
  var w = P(t, 0, 0.35), w2 = P(t, 0.35, 0.7);
  $('wipe').style.width = (eout(w) * 100 - eout(w2) * 100) + '%'; $('wipe').style.left = (eout(w2) * 100) + '%';
  var r = P(t, 0.45, 0.8); $('rank').style.opacity = r; $('rank').style.transform = 'scale(' + (2.2 - 1.2 * eback(r)) + ')';
  $('kick').style.opacity = P(t, 0.7, 1.0);
  $('head').textContent = HEAD.substring(0, Math.floor(P(t, 0.8, 2.2) * HEAD.length));
  $('pts').textContent = Math.round(PTS * eout(P(t, 1.2, 3.0))).toLocaleString('en-US');
  $('cmt').textContent = Math.round(CMT * eout(P(t, 1.4, 3.2))).toLocaleString('en-US');
  $('lt').style.transform = 'translateX(' + (-100 + eout(P(t, 1.8, 2.4)) * 100) + '%)';
}}""")


t_js = json.dumps([[t["lon"], t["lat"], t["temp"], t["city"]] for t in temps])
globe = beat("news-weather",
             f"And the weather right now, across {len(temps)} cities: from {cold['temp']} degrees in {cold['city']}, to {hot['temp']} in {hot['city']}.",
             f"""
<script src='https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js'></script>
<canvas id='gl' width='1280' height='720' class='absolute inset-0'></canvas>
<div class='absolute' style='left:60px;top:80px'>
  <div class='font-bold tracking-[0.3em] text-xl' style='color:#93c5fd'>OPEN-METEO · NOW · {len(temps)} CITIES</div>
  <div class='mt-4 flex items-end gap-3'><div id='lo' class='font-black' style='font-size:96px;line-height:1;color:#60a5fa'>0</div><div class='text-2xl mb-2'>°C · {H.escape(cold['city'])}</div></div>
  <div class='mt-2 flex items-end gap-3'><div id='hi' class='font-black' style='font-size:96px;line-height:1;color:#f97316'>0</div><div class='text-2xl mb-2'>°C · {H.escape(hot['city'])}</div></div>
</div>
<div id='tagH' class='absolute px-3 py-1 font-bold text-lg' style='background:#f97316;opacity:0;transform:translate(10px,-50%)'>{H.escape(hot['city'])} {hot['temp']}°</div>
<div id='tagC' class='absolute px-3 py-1 font-bold text-lg' style='background:#3b82f6;opacity:0;transform:translate(10px,-50%)'>{H.escape(cold['city'])} {cold['temp']}°</div>""", f"""
var T = {t_js}, LO = {cold['temp']}, HI = {hot['temp']};
var R3 = new THREE.WebGLRenderer({{ canvas: $('gl'), antialias: true, alpha: true, preserveDrawingBuffer: true }}); R3.setSize(1280, 720, false);
var scene = new THREE.Scene(), cam = new THREE.PerspectiveCamera(35, 16 / 9, 0.1, 100); cam.position.set(0, 0.6, 6.2); cam.lookAt(0, 0, 0);
var world = new THREE.Group(); world.position.x = 1.2; scene.add(world);
world.add(new THREE.Mesh(new THREE.SphereGeometry(1.5, 64, 48), new THREE.MeshBasicMaterial({{ color: 0x0f2548 }})));
var gm = new THREE.LineBasicMaterial({{ color: 0x3b6fb6, transparent: true, opacity: 0.45 }});
function ll(lon, lat, r) {{ var f = (90 - lat) * Math.PI / 180, l = (lon + 180) * Math.PI / 180; return new THREE.Vector3(-r * Math.sin(f) * Math.cos(l), r * Math.cos(f), r * Math.sin(f) * Math.sin(l)); }}
for (var la = -60; la <= 60; la += 30) {{ var pts = []; for (var lo = -180; lo <= 180; lo += 4) pts.push(ll(lo, la, 1.502)); world.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints(pts), gm)); }}
for (var lo2 = -180; lo2 < 180; lo2 += 30) {{ var p2 = []; for (var la2 = -90; la2 <= 90; la2 += 4) p2.push(ll(lo2, la2, 1.502)); world.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints(p2), gm)); }}
function tcol(v) {{ var u = (v - LO) / (HI - LO); return new THREE.Color().setHSL(0.62 - 0.6 * u, 0.85, 0.55); }}
var pins = T.map(function (c, i) {{
  var h = 0.12 + 0.55 * (c[2] - LO) / (HI - LO);
  var g = new THREE.CylinderGeometry(0.03, 0.03, 1, 10); g.translate(0, 0.5, 0);
  var m = new THREE.Mesh(g, new THREE.MeshBasicMaterial({{ color: tcol(c[2]) }}));
  var p = ll(c[0], c[1], 1.5); m.position.copy(p); m.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), p.clone().normalize());
  world.add(m); return {{ m: m, h: h, i: i }};
}});
function tip(i) {{ var c = T[i]; return ll(c[0], c[1], 1.5 + pins[i].m.scale.y + 0.03); }}
var iH = 0, iC = 0; T.forEach(function (c, i) {{ if (c[2] > T[iH][2]) iH = i; if (c[2] < T[iC][2]) iC = i; }});
// Search the end angle instead of deriving it: try every 0.02 rad and keep the one where the hottest
// city faces the camera most. (Hottest and coldest are ~100 deg apart, so both cannot face front at once;
// the coldest gets its label whenever it swings past during the turn.)
function score(ry) {{
  world.rotation.set(0.2, ry, 0); world.updateMatrixWorld(true);
  var worst = 1e9;
  [iH].forEach(function (i) {{
    var w = ll(T[i][0], T[i][1], 1.5).applyMatrix4(world.matrixWorld);
    var n = w.clone().sub(world.position).normalize(), v = cam.position.clone().sub(w).normalize();
    var sx = w.clone().project(cam).x;                       // -1..1 across the frame
    worst = Math.min(worst, n.dot(v) - Math.max(0, Math.abs(sx) - 0.75) * 4);
  }});
  return worst;
}}
var end = 0, best = -1e9;
for (var a = 0; a < Math.PI * 2; a += 0.02) {{ var sc = score(a); if (sc > best) {{ best = sc; end = a; }} }}
function render(frame, total, fps) {{
  var t = frame / fps, dur = total / fps; tick(t);
  world.rotation.y = end - (1 - eout(P(t, 0, dur - 1.0))) * 3.0; world.rotation.x = 0.2;
  pins.forEach(function (p) {{ var g = eout(P(t, 0.4 + p.i * 0.05, 1.0 + p.i * 0.05)); p.m.scale.set(1, Math.max(0.001, g) * p.h, 1); }});
  $('lo').textContent = (LO * eout(P(t, 0.6, 2.2))).toFixed(1); $('hi').textContent = (HI * eout(P(t, 0.6, 2.2))).toFixed(1);
  R3.render(scene, cam);
  [['tagH', iH], ['tagC', iC]].forEach(function (tg) {{
    var w = tip(tg[1]).applyMatrix4(world.matrixWorld), facing = w.clone().sub(new THREE.Vector3(1.2, 0, 0)).dot(cam.position.clone().sub(w)) > 0;
    var v = w.project(cam); $(tg[0]).style.left = ((v.x + 1) / 2 * 1280) + 'px'; $(tg[0]).style.top = ((1 - v.y) / 2 * 720) + 'px';
    $(tg[0]).style.opacity = facing ? P(t, 1.2, 1.6) : 0;
  }});
}}""")

closing = beat("news-close",
               "That's the show. Nobody wrote this script: it was assembled from two public data feeds and rendered straight to video.",
               f"""
<div class='absolute inset-0 flex flex-col items-center justify-center text-center'>
  <div id='c1' class='font-black' style='font-size:72px;opacity:0'>Nobody wrote this script.</div>
  <div id='c2' class='mt-6 text-3xl' style='opacity:0;color:#93c5fd'>api.github.com · api.open-meteo.com → MulmoScript → video</div>
  <div id='c3' class='mt-6 text-2xl opacity-70' style='opacity:0'>data fetched {stamp}</div>
</div>""", """
function render(frame, total, fps) {
  var t = frame / fps; tick(t);
  [['c1', 0.2], ['c2', 1.2], ['c3', 2.0]].forEach(function (c) { var p = P(t, c[1], c[1] + 0.5); $(c[0]).style.opacity = p; $(c[0]).style.transform = 'translateY(' + (1 - eout(p)) * 30 + 'px)'; });
}""")

deck = {
    "$mulmocast": {"version": "1.1"},
    "canvasSize": {"width": 1280, "height": 720},
    "title": "Idea: a news show generated from live data",
    "description": f"GitHub search + Open-Meteo fetched {stamp}; script, narration and graphics generated from the data.",
    "lang": "en",
    "speechParams": {"speakers": {"Anchor": {"voiceId": "Charon", "isDefault": True, "provider": "gemini", "model": "gemini-3.1-flash-tts-preview",
                                             "speechOptions": {"instruction": "Crisp, confident evening-news anchor. Clear and measured, slightly upbeat."}}}},
    "audioParams": {"bgm": {"kind": "path", "path": "assets/news-bed.mp3"}, "bgmVolume": 0.18, "audioVolume": 1.0,
                    "padding": 0.4, "introPadding": 0.6, "closingPadding": 0.8, "outroPadding": 1.0},
    "beats": [opening] + [story(i + 1, s) for i, s in enumerate(stories)] + [globe, closing],
}
(HERE / "ideas-news.json").write_text(json.dumps(deck, indent=1))
print("ok", [s["name"] for s in stories], cold["city"], hot["city"])
