/**
 * Vrutha Sahayi web UI — structured results (no raw JSON in main view).
 * Optional: set window.__API_BASE__ before this script (e.g. https://your-api.onrender.com)
 * for GitHub Pages; leave unset for same-origin (local uvicorn).
 */
function apiUrl(path) {
  const p = path.startsWith("/") ? path : "/" + path;
  const raw =
    typeof window !== "undefined" && window.__API_BASE__ != null
      ? String(window.__API_BASE__).trim()
      : "";
  const base = raw.replace(/\/$/, "");
  return base ? base + p : p;
}

function $(id) {
  return document.getElementById(id);
}

async function loadVruthams() {
  const r = await fetch(apiUrl("/api/vruthams"));
  const j = await r.json();
  const sel = $("vrutham");
  sel.innerHTML = "";
  const opt0 = document.createElement("option");
  opt0.value = "";
  opt0.textContent = "Select a meter…";
  sel.appendChild(opt0);
  for (const n of j.names || []) {
    const o = document.createElement("option");
    o.value = n;
    o.textContent = n;
    sel.appendChild(o);
  }
}

function syncMode() {
  const check = document.querySelector('input[name="mode"]:checked').value === "check";
  $("vrutham").disabled = !check;
}

function resetResultView() {
  $("result-error").hidden = true;
  $("result-find").hidden = true;
  $("result-check").hidden = true;
  $("result-raw").hidden = true;
  $("result-loading").hidden = true;
  $("result-sub").textContent = "";
}

function showError(message) {
  $("result-empty").classList.add("hidden");
  const el = $("result-error");
  el.hidden = false;
  el.textContent = message;
}

function markerLabel(m) {
  const map = {
    v: "Laghu (short syllable)",
    "-": "Guru (long syllable)",
    x: "Mismatch",
    t: "Yathi (caesura)",
    g: "Gana match",
    a: "Position",
    "|": "Line break",
  };
  return map[m] || `Symbol “${m}”`;
}

function statusLabel(s) {
  const map = {
    y: "OK",
    n: "Problem",
    t: "Yathi",
    g: "Gana",
  };
  return map[s] || s;
}

function renderFind(data) {
  const container = $("result-find");
  container.innerHTML = "";

  const lines = data.lines || [];
  const bySloka = new Map();
  for (const row of lines) {
    const k = row.sloka;
    if (!bySloka.has(k)) bySloka.set(k, []);
    bySloka.get(k).push(row);
  }

  for (const [slokaId, rows] of bySloka) {
    const block = document.createElement("div");
    block.className = "sloka-block";

    const head = document.createElement("div");
    head.className = "sloka-head";
    head.textContent = `Śloka ${slokaId}`;
    block.appendChild(head);

    for (const row of rows) {
      const lineRow = document.createElement("div");
      lineRow.className = "line-row";

      const num = document.createElement("div");
      num.className = "line-num";
      num.textContent = `L${row.line}`;
      lineRow.appendChild(num);

      const main = document.createElement("div");
      const name = document.createElement("div");
      name.className = "meter-name";
      const vid = row.lineVruthamId;
      const mlName = row.lineVruthamNameMl || "";
      const pattern = row.glPattern || "";
      if (vid >= 0 && mlName) {
        name.textContent = mlName;
      } else if (vid >= 0) {
        name.textContent = "—";
      } else {
        name.classList.add("meter-unknown");
        const lbl = document.createElement("div");
        lbl.className = "meter-unknown-title";
        lbl.textContent = "No exact meter in catalog";
        name.appendChild(lbl);
        const why = document.createElement("p");
        why.className = "meter-unknown-why";
        why.textContent =
          "The engine matches your line’s laghu/guru string to fixed classical patterns only—not every poem uses one verbatim.";
        name.appendChild(why);
        if (pattern) {
          const wrap = document.createElement("div");
          wrap.className = "gl-pattern-wrap";
          const hint = document.createElement("span");
          hint.className = "gl-pattern-hint";
          hint.textContent = "Your line’s pattern:";
          const code = document.createElement("code");
          code.className = "gl-pattern";
          code.textContent = pattern;
          code.title = "v = laghu (short), − = guru (long); c = special cluster";
          wrap.appendChild(hint);
          wrap.appendChild(code);
          name.appendChild(wrap);

          const near = row.nearestMatches || [];
          if (near.length > 0) {
            const nh = document.createElement("div");
            nh.className = "nearest-head";
            nh.textContent = "Closest catalog shapes (by similarity):";
            name.appendChild(nh);
            const ul = document.createElement("ul");
            ul.className = "nearest-list";
            for (const m of near) {
              const li = document.createElement("li");
              li.className = "nearest-item";
              const strong = document.createElement("strong");
              strong.className = "nearest-name";
              strong.textContent = m.lineVruthamNameMl || "(unnamed)";
              const pct = Math.round((m.similarity || 0) * 100);
              const cp = document.createElement("code");
              cp.className = "nearest-pattern";
              cp.textContent = m.catalogPattern || "";
              cp.title = "Pattern stored in the catalog for this meter";
              li.appendChild(strong);
              li.appendChild(document.createTextNode(" · " + pct + "% · "));
              li.appendChild(cp);
              ul.appendChild(li);
            }
            name.appendChild(ul);
          } else {
            const none = document.createElement("div");
            none.className = "meter-unknown-note";
            none.textContent = "No similar catalog pattern above the confidence cutoff.";
            name.appendChild(none);
          }
        } else {
          const fall = document.createElement("div");
          fall.className = "meter-unknown-note";
          fall.textContent = "Engine could not derive a pattern for this line.";
          name.appendChild(fall);
        }
      }
      if (vid >= 0 && mlName && pattern) {
        const sub = document.createElement("div");
        sub.className = "gl-pattern-sub";
        const code = document.createElement("code");
        code.className = "gl-pattern gl-pattern-compact";
        code.textContent = pattern;
        sub.appendChild(code);
        name.appendChild(sub);
      }
      main.appendChild(name);

      const meta = document.createElement("div");
      meta.className = "line-meta";

      const yathi = document.createElement("span");
      yathi.className = "badge " + (row.yathiOk === "y" ? "badge-yathi-ok" : "badge-yathi-no");
      yathi.textContent = row.yathiOk === "y" ? "Yathi OK" : "Check yathi";
      meta.appendChild(yathi);

      if (row.slokaVruthamId != null && row.slokaVruthamId !== -2 && row.slokaVruthamId !== -1) {
        const sb = document.createElement("span");
        sb.className = "badge badge-sloka";
        sb.textContent = "Śloka meter resolved";
        meta.appendChild(sb);
      }

      main.appendChild(meta);
      lineRow.appendChild(main);
      block.appendChild(lineRow);
    }

    container.appendChild(block);
  }

  container.hidden = false;
}

function renderCheck(data) {
  const container = $("result-check");
  container.innerHTML = "";

  const raw = data.rawErrors || [];
  const issues = data.issues || [];

  const summary = document.createElement("div");
  summary.className = "check-summary";
  const problemCount = issues.filter((i) => i.status === "n").length;
  if (problemCount === 0 && issues.length > 0) {
    summary.innerHTML = "No syllable mismatches flagged in this pass. <strong>Patterns align</strong> with the chosen meter where the engine could evaluate.";
  } else if (issues.length === 0) {
    summary.textContent = "Analysis complete. See footnotes if the poem uses complex feet.";
  } else {
    summary.innerHTML = `<strong>${problemCount}</strong> position${problemCount === 1 ? "" : "s"} may need attention (see below).`;
  }
  container.appendChild(summary);

  if (issues.length > 0) {
    const ul = document.createElement("ul");
    ul.className = "issue-list";

    for (const issue of issues) {
      const li = document.createElement("li");
      li.className = "issue-item";

      const mark = document.createElement("div");
      mark.className = "issue-marker " + (issue.status === "n" ? "bad" : "ok");
      mark.textContent = issue.marker === "|" ? "¶" : issue.marker;
      li.appendChild(mark);

      const body = document.createElement("div");
      body.className = "issue-body";

      const sn = document.createElement("div");
      sn.className = "issue-snippet";
      sn.textContent = issue.snippet || "—";
      body.appendChild(sn);

      const note = document.createElement("div");
      note.className = "issue-note";
      note.textContent = `${markerLabel(issue.marker)} · ${statusLabel(issue.status)}`;
      body.appendChild(note);

      li.appendChild(body);
      ul.appendChild(li);
    }
    container.appendChild(ul);
  }

  const legend = document.createElement("div");
  legend.className = "check-legend";
  legend.innerHTML =
    "Symbols follow the classic engine: <code>v</code> laghu, <code>-</code> guru, <code>x</code> mismatch. Line breaks appear as <code>|</code> in the raw sequence.";
  container.appendChild(legend);

  container.hidden = false;
}

document.querySelectorAll('input[name="mode"]').forEach((el) => {
  el.addEventListener("change", syncMode);
});

$("go").addEventListener("click", async () => {
  const btn = $("go");
  const mode = document.querySelector('input[name="mode"]:checked').value;
  const text = $("text").value;
  const vrutham = $("vrutham").value;

  btn.classList.add("loading");
  btn.disabled = true;
  resetResultView();
  $("result-empty").classList.add("hidden");
  $("result-loading").hidden = false;

  try {
    const res = await fetch(apiUrl("/api/analyze"), {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text, mode, vrutham }),
    });
    const data = await res.json();

    $("raw-json").textContent = JSON.stringify(data, null, 2);
    $("result-raw").hidden = false;
    $("result-loading").hidden = true;

    if (data.error) {
      showError(data.error);
      $("result-sub").textContent = "Something prevented a full analysis.";
      return;
    }

    if (data.mode === "find") {
      $("result-sub").textContent = `${data.lines?.length || 0} line(s) analyzed · Find meter`;
      renderFind(data);
    } else if (data.mode === "check") {
      $("result-sub").textContent = "Check meter · Syllable-by-syllable markers";
      renderCheck(data);
    }
  } catch (e) {
    $("result-loading").hidden = true;
    $("result-raw").hidden = true;
    showError("Network error — please try again.");
    $("result-sub").textContent = "";
  } finally {
    btn.classList.remove("loading");
    btn.disabled = false;
  }
});

loadVruthams();
syncMode();
