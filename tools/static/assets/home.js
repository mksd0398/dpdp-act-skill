/* Home page interactions: live countdown, count-up stats, myth/fact cards, the AI answer demo,
 * the commencement timeline, and scroll reveals. No network calls. Everything degrades to static
 * content without JavaScript, and motion is skipped when the visitor prefers reduced motion. */
(function () {
  "use strict";

  var reduceMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var io = "IntersectionObserver" in window;

  function onVisible(el, fn, threshold) {
    if (!io || reduceMotion) return fn();
    var obs = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          obs.disconnect();
          fn();
        }
      });
    }, { threshold: threshold || 0.3 });
    obs.observe(el);
  }

  function pad(n) { return (n < 10 ? "0" : "") + n; }

  /* ---------------------------------------------------------------- countdown */
  document.querySelectorAll("[data-countdown]").forEach(function (el) {
    var target = new Date(el.getAttribute("data-countdown")).getTime();
    var d = el.querySelector("[data-unit=d]");
    var h = el.querySelector("[data-unit=h]");
    var m = el.querySelector("[data-unit=m]");
    var s = el.querySelector("[data-unit=s]");
    function tick() {
      var left = Math.max(0, target - Date.now());
      var secs = Math.floor(left / 1000);
      if (d) d.textContent = Math.floor(secs / 86400);
      if (h) h.textContent = pad(Math.floor((secs % 86400) / 3600));
      if (m) m.textContent = pad(Math.floor((secs % 3600) / 60));
      if (s) s.textContent = pad(secs % 60);
    }
    tick();
    setInterval(tick, 1000);
  });

  document.querySelectorAll("[data-days-left]").forEach(function (el) {
    var t = new Date(el.getAttribute("data-days-left")).getTime();
    el.textContent = Math.max(0, Math.floor((t - Date.now()) / 86400000));
  });

  /* ---------------------------------------------------------------- timeline */
  document.querySelectorAll("[data-timeline]").forEach(function (tl) {
    var steps = tl.querySelectorAll("[data-date]");
    var now = Date.now();
    var first = new Date(steps[0].getAttribute("data-date")).getTime();
    var last = new Date(steps[steps.length - 1].getAttribute("data-date")).getTime();
    var nextMarked = false;
    steps.forEach(function (st) {
      var t = new Date(st.getAttribute("data-date")).getTime();
      st.classList.remove("done", "next");
      if (t <= now) st.classList.add("done");
      else if (!nextMarked) { st.classList.add("next"); nextMarked = true; }
    });
    var p = Math.min(1, Math.max(0, (now - first) / (last - first)));
    tl.style.setProperty("--p", p.toFixed(3));
  });

  /* ---------------------------------------------------------------- count-up stats */
  document.querySelectorAll("[data-count]").forEach(function (el) {
    var end = parseInt(el.getAttribute("data-count"), 10);
    if (reduceMotion) { el.textContent = end; return; }
    el.textContent = "0";
    onVisible(el, function () {
      var start = null;
      var dur = 900;
      function step(ts) {
        if (start === null) start = ts;
        var k = Math.min(1, (ts - start) / dur);
        var eased = 1 - Math.pow(1 - k, 3);
        el.textContent = Math.round(end * eased);
        if (k < 1) requestAnimationFrame(step);
      }
      requestAnimationFrame(step);
    });
  });

  /* ---------------------------------------------------------------- myth / fact cards */
  document.querySelectorAll("[data-myth]").forEach(function (card) {
    var btn = card.querySelector("button");
    var fact = card.querySelector(".fact");
    card.classList.add("closed");
    btn.setAttribute("aria-expanded", "false");
    btn.addEventListener("click", function () {
      var open = card.classList.toggle("closed") === false;
      btn.setAttribute("aria-expanded", String(open));
      btn.textContent = open ? "Hide the law" : "Show what the Act says";
      if (open && fact) fact.focus({ preventScroll: true });
    });
  });

  /* ---------------------------------------------------------------- AI answer demo */
  document.querySelectorAll("[data-demo]").forEach(function (demo) {
    var prompt = demo.querySelector("[data-type]");
    var lines = demo.querySelectorAll("[data-line]");
    var replay = demo.querySelector("[data-replay]");
    var full = prompt.getAttribute("data-type");
    var timers = [];

    function clear() { timers.forEach(clearTimeout); timers = []; }
    function showAll() {
      prompt.textContent = full;
      lines.forEach(function (l) { l.classList.add("shown"); });
      demo.classList.add("done");
    }
    function play() {
      clear();
      demo.classList.remove("done");
      lines.forEach(function (l) { l.classList.remove("shown"); });
      prompt.textContent = "";
      var i = 0;
      (function type() {
        prompt.textContent = full.slice(0, ++i);
        if (i < full.length) timers.push(setTimeout(type, 28 + Math.random() * 40));
        else {
          lines.forEach(function (l, n) {
            timers.push(setTimeout(function () { l.classList.add("shown"); }, 450 + n * 420));
          });
          timers.push(setTimeout(function () { demo.classList.add("done"); }, 450 + lines.length * 420));
        }
      })();
    }

    if (reduceMotion || !io) showAll();
    else {
      showAll();               /* content is present even before the animation starts */
      onVisible(demo, play, 0.4);
    }
    if (replay) replay.addEventListener("click", function () { reduceMotion ? showAll() : play(); });
  });

  /* ---------------------------------------------------------------- copy buttons */
  document.querySelectorAll("[data-copy]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var text = btn.getAttribute("data-copy");
      var label = btn.textContent;
      function done(ok) {
        btn.textContent = ok ? "Copied" : "Press Ctrl+C";
        setTimeout(function () { btn.textContent = label; }, 1600);
      }
      if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(text).then(function () { done(true); }, function () { done(false); });
      } else done(false);
    });
  });

  /* ---------------------------------------------------------------- scroll reveal */
  var reveals = document.querySelectorAll(".reveal");
  if (reduceMotion || !io) {
    reveals.forEach(function (el) { el.classList.add("in"); });
  } else {
    var obs = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          en.target.classList.add("in");
          obs.unobserve(en.target);
        }
      });
    }, { threshold: 0.12 });
    reveals.forEach(function (el) { obs.observe(el); });
  }
})();
