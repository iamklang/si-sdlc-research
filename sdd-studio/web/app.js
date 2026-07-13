"use strict";
const $ = (s, r = document) => r.querySelector(s);
const el = (tag, cls, txt) => { const e = document.createElement(tag); if (cls) e.className = cls; if (txt != null) e.textContent = txt; return e; };

let STAGES = [], STATE = null, ENGINE = "template", CLAUDE_AVAIL = false;
const cache = new Map();               // path -> content

async function api(path, opts) {
  const r = await fetch(path, opts);
  if (!r.ok) {
    let msg = "HTTP " + r.status;
    try { const e = await r.json(); msg = e.detail || msg; } catch (_) {}
    throw new Error(msg);
  }
  return r.json();
}

function toast(msg) {
  const t = $("#toast"); t.textContent = "⚠ " + msg; t.classList.add("show");
  setTimeout(() => t.classList.remove("show"), 4200);
}

/* ---------- theme ---------- */
(function () { const t = localStorage.getItem("sdd-theme"); if (t) document.documentElement.setAttribute("data-theme", t); })();

/* ---------- boot ---------- */
async function boot() {
  try {
    STAGES = (await api("/api/stages")).stages;
    await refresh();
    wireControls();
  } catch (e) { toast(e.message); }
}

async function refresh() {
  const s = await api("/api/state");
  STATE = s.state; CLAUDE_AVAIL = s.claudeAvailable; ENGINE = STATE.engine || "template";
  $("#feature").value = STATE.feature || "";
  updateEngineUI();
  render();
}

/* ---------- controls ---------- */
function wireControls() {
  $("#eng-template").onclick = () => setEngine("template");
  $("#eng-claude").onclick = () => setEngine("claude");
  $("#reset").onclick = async () => {
    if (!confirm("เริ่มใหม่? artifact ใน workspace จะถูกลบ")) return;
    try { await api("/api/reset", { method: "POST" }); cache.clear(); await refresh(); }
    catch (e) { toast(e.message); }
  };
  $("#theme").onclick = () => {
    const cur = document.documentElement.getAttribute("data-theme");
    const dark = cur ? cur === "dark" : matchMedia("(prefers-color-scheme:dark)").matches;
    const next = dark ? "light" : "dark";
    document.documentElement.setAttribute("data-theme", next);
    localStorage.setItem("sdd-theme", next);
  };
  $("#feature").onchange = async (e) => {
    try { await api("/api/config", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ feature: e.target.value }) }); }
    catch (err) { toast(err.message); }
  };
}

async function setEngine(eng) {
  if (eng === "claude" && !CLAUDE_AVAIL) { toast("ยังไม่มี ANTHROPIC_API_KEY — ตั้ง key แล้วรีสตาร์ตเซิร์ฟเวอร์"); return; }
  ENGINE = eng;
  try { await api("/api/config", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ engine: eng }) }); }
  catch (e) { toast(e.message); }
  updateEngineUI();
}

function updateEngineUI() {
  $("#eng-template").setAttribute("aria-pressed", ENGINE === "template");
  $("#eng-claude").setAttribute("aria-pressed", ENGINE === "claude");
  $("#eng-claude").disabled = !CLAUDE_AVAIL;
  $("#enginenote").textContent = ENGINE === "claude"
    ? "engine: claude (เรียก Anthropic API — ส่งข้อมูลออกนอกเครื่อง)"
    : "engine: template (offline · ไม่มี network call)" + (CLAUDE_AVAIL ? "" : " · Claude ปิดอยู่ (ไม่มี key)");
}

/* ---------- state helpers ---------- */
function stageState(id) {
  const st = STATE.stages[id];
  if (st && st.status === "done") return "done";
  const idx = STAGES.findIndex(s => s.id === id);
  const prev = idx > 0 ? STAGES[idx - 1].id : null;
  const ready = !prev || (STATE.stages[prev] && STATE.stages[prev].status === "done");
  return ready ? "ready" : "locked";
}

/* ---------- render ---------- */
function render() {
  const root = $("#pipeline"); root.innerHTML = "";
  STAGES.forEach(stage => root.appendChild(renderStage(stage)));
}

function renderStage(stage) {
  const state = stageState(stage.id);
  const done = STATE.stages[stage.id];
  const sec = el("section", "stage"); sec.dataset.state = state; sec.dataset.stage = stage.id;

  const node = el("div", "node", String(stage.num));
  const card = el("div", "card");

  const top = el("div", "card-top");
  top.appendChild(el("span", "cmd", stage.cmd));
  top.appendChild(el("span", "role", stage.title));
  const pill = el("span", "status-pill", state === "done" ? "เสร็จ" : state === "ready" ? "พร้อม" : "รอ");
  top.appendChild(pill);
  card.appendChild(top);

  // flow3: input | action | output
  const flow = el("div", "flow3");
  const inCell = el("div", "fcell in"); inCell.appendChild(el("span", "fl", "Input"));
  const getInput = renderInput(inCell, stage, done);
  const chev1 = el("div", "fchev", "▶");

  const actCell = el("div", "fcell act"); actCell.appendChild(el("span", "fl", "Action"));
  const actors = el("div", "actors");
  stage.actors.forEach(a => actors.appendChild(el("span", "actor " + a, a === "human" ? "คน" : "AI")));
  actCell.appendChild(actors);
  const btn = el("button", "run-btn", state === "done" ? "✓ " + stage.cmd : "Run " + stage.cmd);
  btn.disabled = state !== "ready";
  actCell.appendChild(btn);
  const chev2 = el("div", "fchev", "▶");

  const outCell = el("div", "fcell out"); outCell.appendChild(el("span", "fl", "Output"));
  const outFiles = el("div", "out-files");
  outCell.appendChild(outFiles);

  flow.append(inCell, chev1, actCell, chev2, outCell);
  card.appendChild(flow);

  if (stage.flag) {
    const flag = el("div", "flag " + stage.flag.kind);
    flag.appendChild(el("b", null, stage.flag.label));
    flag.appendChild(el("span", null, stage.flag.text));
    card.appendChild(flag);
  }

  const viewer = el("div", "viewer hidden");
  card.appendChild(viewer);

  // extra: test runner on implement
  let testRow = null;
  if (stage.id === "implement") {
    testRow = el("div", "test-row");
    const tbtn = el("button", "test-btn", "▶ Run tests (pytest)");
    const tout = el("pre", "test-out");
    tbtn.onclick = () => runTests(tbtn, tout);
    testRow.appendChild(tbtn); card.appendChild(testRow); card.appendChild(tout);
    testRow.style.display = state === "done" ? "flex" : "none";
    tout.dataset.k = "";
  }

  // if already done (persisted), show its files
  if (done) {
    fillOutput(outFiles, viewer, done.files.map(p => ({ path: p })));
  } else {
    outFiles.appendChild(el("span", "out-empty", "— ยังไม่ทำ —"));
  }

  btn.onclick = () => runStage(stage, getInput, { btn, outFiles, viewer, pill, testRow });

  sec.append(node, card);
  return sec;
}

function renderInput(cell, stage, done) {
  const spec = stage.input, prev = done ? done.input : null;
  if (spec.type === "idea") {
    const f = el("div", "field");
    const ta = el("textarea"); ta.placeholder = spec.placeholder || ""; if (prev && prev.idea) ta.value = prev.idea;
    f.append(labelEl(spec.label), ta); cell.appendChild(f);
    return () => ({ idea: ta.value.trim() || spec.placeholder });
  }
  if (spec.type === "principles") {
    const f = el("div", "field");
    const ta = el("textarea"); ta.placeholder = "เว้นว่าง = ใช้ template มาตรฐาน"; if (prev && prev.principles) ta.value = prev.principles;
    f.append(labelEl(spec.label), ta); cell.appendChild(f);
    return () => { const v = ta.value.trim(); return v ? { principles: v } : {}; };
  }
  if (spec.type === "questions") {
    const getters = [];
    spec.questions.forEach(q => {
      const f = el("div", "qrow");
      f.appendChild(el("span", "q", q.q));
      const inp = el("input"); inp.value = (prev && prev[q.id]) || q.default;
      f.appendChild(inp); cell.appendChild(f);
      getters.push([q.id, () => inp.value]);
    });
    return () => Object.fromEntries(getters.map(([k, g]) => [k, g()]));
  }
  if (spec.type === "tech") {
    const getters = [];
    spec.fields.forEach(fld => {
      const f = el("div", "field");
      const inp = el("input"); inp.value = (prev && prev[fld.id]) || fld.default;
      f.append(labelEl(fld.label), inp); cell.appendChild(f);
      getters.push([fld.id, () => inp.value]);
    });
    return () => Object.fromEntries(getters.map(([k, g]) => [k, g()]));
  }
  // auto
  cell.appendChild(el("span", "auto-note", spec.label));
  return () => ({});
}

function labelEl(t) { return el("label", null, t); }

/* ---------- run a stage ---------- */
async function runStage(stage, getInput, ui) {
  ui.btn.disabled = true; ui.btn.classList.add("busy"); ui.btn.textContent = "…กำลังรัน";
  try {
    const res = await api("/api/run/" + stage.id, {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ input: getInput(), engine: ENGINE }),
    });
    res.files.forEach(f => cache.set(f.path, f.content));
    await refresh();   // re-render: marks done, unlocks next, shows output
  } catch (e) {
    toast(e.message);
    ui.btn.disabled = false; ui.btn.classList.remove("busy"); ui.btn.textContent = "Run " + stage.cmd;
  }
}

/* ---------- output viewer ---------- */
function fillOutput(outFiles, viewer, files) {
  outFiles.innerHTML = "";
  files.forEach(f => outFiles.appendChild(el("span", "file-chip", f.path.split("/").pop())));
  buildViewer(viewer, files);
}

function buildViewer(viewer, files) {
  viewer.innerHTML = ""; viewer.classList.remove("hidden");
  const tabs = el("div", "filetabs"); tabs.setAttribute("role", "tablist");
  const bar = el("div", "codebar");
  const pre = el("pre", "code");
  const btns = [];
  async function select(i) {
    btns.forEach((b, j) => b.setAttribute("aria-selected", j === i));
    bar.textContent = files[i].path;
    pre.textContent = "…";
    try { pre.textContent = await loadContent(files[i]); }
    catch (e) { pre.textContent = "(โหลดไม่ได้: " + e.message + ")"; }
  }
  files.forEach((f, i) => {
    const b = el("button", "ftab", f.path.split("/").pop());
    b.setAttribute("role", "tab"); b.onclick = () => select(i);
    tabs.appendChild(b); btns.push(b);
  });
  viewer.append(tabs, bar, pre);
  select(0);
}

async function loadContent(f) {
  if (f.content != null) return f.content;
  if (cache.has(f.path)) return cache.get(f.path);
  const r = await api("/api/artifact?path=" + encodeURIComponent(f.path));
  cache.set(f.path, r.content);
  return r.content;
}

/* ---------- test runner ---------- */
async function runTests(btn, out) {
  btn.disabled = true; btn.textContent = "…รัน pytest";
  try {
    const r = await api("/api/implement/test", { method: "POST" });
    out.className = "test-out " + (r.ok ? "pass" : "fail");
    out.textContent = (r.ok ? "✓ ผ่าน " : "✕ ล้มเหลว ") + `(passed=${r.passed}, failed=${r.failed})\n\n` + r.output;
  } catch (e) { out.className = "test-out fail"; out.textContent = e.message; }
  btn.disabled = false; btn.textContent = "▶ Run tests (pytest)";
}

boot();
