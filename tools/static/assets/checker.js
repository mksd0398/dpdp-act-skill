/* DPDP readiness self-check.
 * Runs entirely in the browser: no network calls, no cookies, no analytics. Answers are kept in
 * localStorage on this device only, so a visitor can come back to them. Questions come from the
 * JSON block #checker-data, which tools/build_site.py writes from CHECKER_QUESTIONS.
 */
(function () {
  "use strict";

  var root = document.querySelector("[data-checker]");
  var dataEl = document.getElementById("checker-data");
  if (!root || !dataEl) return;

  var data = JSON.parse(dataEl.textContent);
  var base = root.getAttribute("data-base") || "./";
  var KEY = "dpdp-readiness-v1";
  var reduceMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  var OPTS = {
    yes: { label: "Yes", key: "1" },
    partly: { label: "Partly", key: "2" },
    no: { label: "No", key: "3" },
    unsure: { label: "Not sure", key: "4" }
  };
  var STATUS = { no: "Gap", partly: "Partly there", unsure: "Not sure" };

  var state = load() || { answers: {}, view: "intro", i: 0 };

  function load() {
    try {
      var s = JSON.parse(window.localStorage.getItem(KEY));
      return s && s.answers ? s : null;
    } catch (e) {
      return null;
    }
  }

  function save() {
    try {
      window.localStorage.setItem(KEY, JSON.stringify(state));
    } catch (e) {
      /* private mode or storage blocked: the check still works, it just won't be remembered */
    }
  }

  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  /* Questions that apply, given the profile answers so far. A conditional question applies
   * unless its profile question was answered "no". */
  function activeQuestions() {
    return data.questions.filter(function (q) {
      if (!q.cond) return true;
      var a = state.answers[q.cond];
      return a !== undefined && a !== "no";
    });
  }

  function refsHtml(q) {
    return q.refs
      .map(function (r) {
        return '<a href="' + esc(base + r[1]) + '">' + esc(r[0]) + "</a>";
      })
      .join(" ");
  }

  function ceilingText(q) {
    if (!q.ceiling) return "Other law, not a DPDP penalty";
    return "Penalty ceiling up to Rs " + q.ceiling + " crore";
  }

  function daysLeft() {
    var ms = new Date(data.deadline).getTime() - Date.now();
    return Math.max(0, Math.floor(ms / 86400000));
  }

  /* ------------------------------------------------------------------ views */

  function renderIntro() {
    var resumable = Object.keys(state.answers).length > 0;
    return (
      '<div class="ck-panel ck-intro">' +
      '<p class="ck-kicker">Free readiness self-check</p>' +
      '<h3 class="ck-title" tabindex="-1">How ready are you for 14 May 2027?</h3>' +
      "<p>Answer up to " + data.questions.length + " quick questions about your organisation. " +
      "You get a readiness score, your gaps ranked by the penalty ceiling behind them, and the " +
      "section or rule behind every one.</p>" +
      '<ul class="ck-meta"><li>About 3 minutes</li><li>Answers never leave your browser</li>' +
      "<li>Every question cites the law</li></ul>" +
      '<div class="ck-actions">' +
      '<button type="button" class="btn primary" data-act="start">' +
      (resumable ? "Resume where you left off" : "Start the self-check") + "</button>" +
      (resumable ? '<button type="button" class="btn ghost" data-act="restart">Start over</button>' : "") +
      "</div></div>"
    );
  }

  function renderQuestion() {
    var qs = activeQuestions();
    if (state.i >= qs.length) {
      state.view = "result";
      return renderResult();
    }
    var q = qs[state.i];
    var opts = q.kind === "check" ? ["yes", "partly", "no", "unsure"] : q.opts || ["yes", "no"];
    var pct = Math.round((state.i / qs.length) * 100);
    var current = state.answers[q.id];
    var btns = opts
      .map(function (o, n) {
        return (
          '<button type="button" class="ck-opt ck-' + o + '" data-answer="' + o + '" aria-pressed="' +
          (current === o) + '"><kbd>' + (n + 1) + "</kbd>" + OPTS[o].label + "</button>"
        );
      })
      .join("");
    return (
      '<div class="ck-panel">' +
      '<div class="ck-top"><span class="ck-step">Question ' + (state.i + 1) + " of " + qs.length +
      "</span>" + '<button type="button" class="ck-link" data-act="restart">Start over</button></div>' +
      '<div class="ck-bar" role="progressbar" aria-label="Progress" aria-valuemin="0" ' +
      'aria-valuemax="100" aria-valuenow="' + pct + '"><span style="width:' + pct + '%"></span></div>' +
      '<div class="ck-card">' +
      '<p class="ck-area">' + esc(q.area) + "</p>" +
      '<h3 class="ck-q" id="ck-q" tabindex="-1">' + esc(q.q) + "</h3>" +
      (q.help ? '<p class="ck-help">' + esc(q.help) + "</p>" : "") +
      '<div class="ck-opts" role="group" aria-labelledby="ck-q">' + btns + "</div>" +
      '<p class="ck-refs">The law: ' + refsHtml(q) + "</p>" +
      "</div>" +
      '<div class="ck-nav">' +
      '<button type="button" class="ck-link" data-act="back">&larr; Back</button>' +
      '<span class="ck-hint">Tip: press 1 to ' + opts.length + "</span></div>" +
      "</div>"
    );
  }

  function renderOut() {
    var q = data.questions.filter(function (x) { return x.id === state.outId; })[0];
    return (
      '<div class="ck-panel ck-intro">' +
      '<p class="ck-kicker">Probably out of scope</p>' +
      '<h3 class="ck-title" tabindex="-1">The DPDP Act may not apply to you</h3>' +
      "<p>" + esc(q ? q.out : "") + "</p>" +
      '<p class="ck-fine">This turns on facts. If anything changes, for example you start digitising ' +
      "records or selling to people in India, run the check again.</p>" +
      '<div class="ck-actions"><button type="button" class="btn ghost" data-act="back">&larr; Change my answer</button>' +
      '<a class="btn ghost" href="' + esc(base) + 'act/section-3/">Read section 3</a></div></div>'
    );
  }

  function score(items) {
    var pts = 0;
    items.forEach(function (q) {
      var a = state.answers[q.id];
      if (a === "yes") pts += 1;
      else if (a === "partly") pts += 0.5;
    });
    return items.length ? Math.round((pts / items.length) * 100) : 0;
  }

  function band(s) {
    if (s >= 80) return ["Well prepared", "good"];
    if (s >= 50) return ["Getting there", "mid"];
    return ["Early days", "low"];
  }

  function renderResult() {
    var checks = activeQuestions().filter(function (q) { return q.kind === "check"; });
    var s = score(checks);
    var b = band(s);
    var counts = { yes: 0, partly: 0, no: 0, unsure: 0 };
    checks.forEach(function (q) { counts[state.answers[q.id] || "unsure"]++; });

    var areas = [];
    var byArea = {};
    checks.forEach(function (q) {
      if (!byArea[q.group]) { byArea[q.group] = []; areas.push(q.group); }
      byArea[q.group].push(q);
    });
    var bars = areas
      .map(function (a) {
        var v = score(byArea[a]);
        return (
          '<li><span class="ck-bar-label">' + esc(a) + '</span><span class="ck-meter" aria-hidden="true">' +
          '<span class="ck-meter-fill ck-' + band(v)[1] + '" style="width:' + v + '%"></span></span>' +
          '<span class="ck-bar-val">' + v + "%</span></li>"
        );
      })
      .join("");

    var rank = { no: 0, partly: 1, unsure: 2 };
    var gaps = checks
      .filter(function (q) { var a = state.answers[q.id]; return a && a !== "yes"; })
      .sort(function (x, y) {
        return (y.ceiling || 0) - (x.ceiling || 0) ||
          rank[state.answers[x.id]] - rank[state.answers[y.id]];
      });
    var gapHtml = gaps
      .map(function (q) {
        var a = state.answers[q.id];
        return (
          '<li class="ck-gap"><span class="ck-chip ck-' + a + '">' + STATUS[a] + "</span>" +
          "<div><strong>" + esc(q.label) + "</strong>" +
          "<p>" + esc(q.fix) + "</p>" +
          '<p class="ck-refs">' + refsHtml(q) + ' <span class="ck-ceiling">' + ceilingText(q) +
          "</span></p></div></li>"
        );
      })
      .join("");

    var R = 52;
    var C = 2 * Math.PI * R;
    return (
      '<div class="ck-panel ck-result">' +
      '<div class="ck-score">' +
      '<svg viewBox="0 0 120 120" class="ck-ring ck-' + b[1] + '" role="img" aria-label="Readiness ' + s + ' percent">' +
      '<circle cx="60" cy="60" r="' + R + '" class="ck-ring-bg"></circle>' +
      '<circle cx="60" cy="60" r="' + R + '" class="ck-ring-fg" stroke-dasharray="' + C.toFixed(1) +
      '" stroke-dashoffset="' + C.toFixed(1) + '" data-target="' + (C * (1 - s / 100)).toFixed(1) + '"></circle>' +
      '<text x="60" y="58" text-anchor="middle" class="ck-ring-num">' + s + '%</text>' +
      '<text x="60" y="78" text-anchor="middle" class="ck-ring-sub">ready</text></svg>' +
      "<div>" +
      '<p class="ck-kicker">Your readiness</p>' +
      '<h3 class="ck-title" tabindex="-1">' + b[0] + "</h3>" +
      '<p class="ck-counts"><span>' + counts.yes + " ready</span><span>" + counts.partly +
      " partly</span><span>" + counts.no + " gaps</span><span>" + counts.unsure + " not sure</span></p>" +
      "<p><b>" + daysLeft() + " days</b> until 14 May 2027, when the substantive DPDP Rules commence.</p>" +
      "</div></div>" +
      '<ul class="ck-bars">' + bars + "</ul>" +
      (gaps.length
        ? '<h4>Fix these first</h4><p class="ck-fine">Ranked by the Schedule penalty ceiling behind each one, ' +
          "then by how far off you are. Ceilings are maximums, not fines.</p>" +
          '<ol class="ck-gaps">' + gapHtml + "</ol>"
        : "<h4>No gaps reported</h4><p>On your own answers you are in good shape. Test that against the " +
          "full checklist, which goes deeper on every area.</p>") +
      '<div class="ck-cta">' +
      "<p><strong>Turn this into a real audit.</strong> Paste your results into Claude with the free " +
      "dpdp-analyze skill installed, and it will work through each gap against the actual sections.</p>" +
      '<div class="ck-actions">' +
      '<button type="button" class="btn primary" data-act="copy">Copy results as a prompt for Claude</button>' +
      '<a class="btn ghost" href="' + esc(base) + 'claude-code-skill/">Get the AI skill</a>' +
      '<a class="btn ghost" href="' + esc(base) + 'compliance-checklist/">Full 78-point checklist</a>' +
      '<button type="button" class="ck-link" data-act="restart">Retake</button>' +
      '</div><p class="ck-status" role="status" aria-live="polite"></p></div>' +
      '<p class="ck-fine">Based only on your own answers. Not legal advice and not a compliance ' +
      "certificate. Verify against the Gazette text and consult qualified Indian legal counsel.</p>" +
      "</div>"
    );
  }

  function promptText() {
    var checks = activeQuestions().filter(function (q) { return q.kind === "check"; });
    var lines = [
      "I ran the DPDP readiness self-check (" + score(checks) + "% ready). Using the dpdp-analyze skill, " +
        "help me close these gaps, most serious first. For each one, cite the section or rule, explain " +
        "what good looks like, and give me concrete steps.",
      "",
      "Context:"
    ];
    data.questions
      .filter(function (q) { return q.kind === "profile"; })
      .forEach(function (q) {
        var a = state.answers[q.id];
        if (a) lines.push("- " + q.label + ": " + OPTS[a].label);
      });
    lines.push("", "Answers:");
    checks.forEach(function (q) {
      var a = state.answers[q.id] || "unsure";
      lines.push("- [" + OPTS[a].label + "] " + q.label + " (" + q.refs.map(function (r) { return r[0]; }).join(", ") + ")");
    });
    return lines.join("\n");
  }

  function copy(text, done) {
    function fallback() {
      var ta = document.createElement("textarea");
      ta.value = text;
      ta.setAttribute("readonly", "");
      ta.style.position = "fixed";
      ta.style.opacity = "0";
      document.body.appendChild(ta);
      ta.select();
      var ok = false;
      try { ok = document.execCommand("copy"); } catch (e) { ok = false; }
      document.body.removeChild(ta);
      done(ok);
    }
    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(text).then(function () { done(true); }, fallback);
    } else {
      fallback();
    }
  }

  /* ------------------------------------------------------------------ render + events */

  function render(focus) {
    var html =
      state.view === "q" ? renderQuestion()
      : state.view === "out" ? renderOut()
      : state.view === "result" ? renderResult()
      : renderIntro();
    root.innerHTML = html;
    var ring = root.querySelector(".ck-ring-fg");
    if (ring) {
      var target = ring.getAttribute("data-target");
      if (reduceMotion) ring.setAttribute("stroke-dashoffset", target);
      else requestAnimationFrame(function () {
        requestAnimationFrame(function () { ring.setAttribute("stroke-dashoffset", target); });
      });
    }
    if (focus) {
      var h = root.querySelector(".ck-q, .ck-title");
      if (h) h.focus({ preventScroll: true });
      var top = root.getBoundingClientRect().top;
      if (top < 0 || top > window.innerHeight * 0.6) {
        root.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "start" });
      }
    }
  }

  function answer(v) {
    var qs = activeQuestions();
    var q = qs[state.i];
    if (!q) return;
    state.answers[q.id] = v;
    if (q.kind === "scope" && v === "no") {
      state.view = "out";
      state.outId = q.id;
    } else {
      state.i += 1;
      if (state.i >= activeQuestions().length) state.view = "result";
    }
    save();
    render(true);
  }

  root.addEventListener("click", function (e) {
    var t = e.target.closest("[data-answer], [data-act]");
    if (!t || !root.contains(t)) return;
    var v = t.getAttribute("data-answer");
    if (v) return answer(v);
    var act = t.getAttribute("data-act");
    if (act === "start") {
      state.view = "q";
      var qs = activeQuestions();
      if (state.i >= qs.length) state.view = "result";
    } else if (act === "restart") {
      state = { answers: {}, view: "q", i: 0 };
    } else if (act === "back") {
      if (state.view === "out") state.view = "q";
      else if (state.view === "result") { state.view = "q"; state.i = activeQuestions().length - 1; }
      else if (state.i > 0) state.i -= 1;
      else state.view = "intro";
    } else if (act === "copy") {
      var status = root.querySelector(".ck-status");
      copy(promptText(), function (ok) {
        status.textContent = ok
          ? "Copied. Paste it into Claude Code or Claude.ai with the dpdp-analyze skill installed."
          : "Copy failed. Select and copy manually from the list above.";
      });
      return;
    }
    save();
    render(true);
  });

  root.addEventListener("keydown", function (e) {
    if (state.view !== "q" || e.altKey || e.ctrlKey || e.metaKey) return;
    var btn = root.querySelectorAll(".ck-opt")[parseInt(e.key, 10) - 1];
    if (btn) {
      e.preventDefault();
      btn.click();
    }
  });

  root.classList.add("ck-live");
  render(false);
})();
