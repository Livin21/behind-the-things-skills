/* Behind The Things — long-form shared helpers. Loaded once by the root/preview file.
   Usage inside a chapter's timeline script:
     var K = BTT.kit(tl, "ch03");      // tl = this chapter's paused timeline, prefix = id prefix
     K.push("#ch03-stage", 0, 20);      // slow push-in, capped at 5%
     K.callout("ch03-c1", 4.2);         // dot -> leader -> tag
     K.flow("#ch03-path", 6, 3);        // dashes travel along a path
     K.swap("#ch03-a", "#ch03-b", 9);   // readout change
     K.counter(el, 0, 20200, 10, 2, function (v) { return Math.round(v) + " KM"; });
     K.card("#ch03-l3", 0.4, 4);        // chapter lower-third: in at t, out after hold
     K.wipe("#ch03-wipe", 12.0);        // scene cut: panel rises by T, then K.wipeOut at T
   All times are chapter-local seconds. Deterministic: no Math.random, no Date. */
(function () {
  function kit(tl, prefix) {
    var K = {};
    K.push = function (stage, start, dur, cap) {
      var c = cap == null ? 0.05 : cap;
      tl.fromTo(stage, { scale: 1 }, { scale: 1 + Math.min(0.004 * dur, c), duration: dur, ease: "none" }, start);
    };
    K.enter = function (sel, t, opts) {
      tl.from(sel, Object.assign({ y: 40, opacity: 0, duration: 0.5, ease: "power3.out" }, opts || {}), t);
    };
    K.callout = function (id, t) {
      var el = document.getElementById(id);
      if (!el) { throw new Error("BTT.callout: missing #" + id); }
      var v = el.classList.contains("v"), rev = el.classList.contains("rev"), up = el.classList.contains("up");
      var origin = v ? (up ? "50% 100%" : "50% 0%") : rev ? "100% 50%" : "0% 50%";
      tl.from(el.querySelector(".dot"), { scale: 0, duration: 0.2, ease: "back.out(2.5)" }, t);
      tl.from(el.querySelector(".lead"), v ? { scaleY: 0, transformOrigin: origin, duration: 0.3, ease: "power2.inOut" } : { scaleX: 0, transformOrigin: origin, duration: 0.3, ease: "power2.inOut" }, t + 0.1);
      tl.from(el.querySelector(".tag"), Object.assign({ opacity: 0, duration: 0.3, ease: "power2.out" }, v ? { y: up ? -12 : 12 } : { x: rev ? -12 : 12 }), t + 0.36);
    };
    K.flow = function (sel, start, dur) {
      tl.fromTo(sel, { strokeDashoffset: 0 }, { strokeDashoffset: -240 * dur, duration: dur, ease: "none" }, start);
    };
    K.draw = function (sel, start, dur) {
      // Stroke draw-on for a path with a known length set in data-len (px).
      var el = document.querySelector(sel); var len = +(el && el.getAttribute("data-len")) || 1000;
      tl.fromTo(sel, { strokeDasharray: len, strokeDashoffset: len }, { strokeDashoffset: 0, duration: dur, ease: "power2.inOut" }, start);
    };
    K.swap = function (fromSel, toSel, t) {
      tl.fromTo(toSel, { opacity: 0, y: 10 }, { opacity: 1, y: 0, duration: 0.25, ease: "power2.out", immediateRender: true }, t);
      tl.to(fromSel, { opacity: 0, duration: 0.15, ease: "power1.in" }, t);
    };
    K.counter = function (el, from, to, start, dur, fmt, ease) {
      var o = { v: from }; el.textContent = fmt(from);
      tl.to(o, { v: to, duration: dur, ease: ease || "none", onUpdate: function () { el.textContent = fmt(o.v); } }, start);
    };
    K.marker = function (sel, t) {
      tl.fromTo(sel, { backgroundSize: "0% 100%" }, { backgroundSize: "100% 100%", duration: 0.35, ease: "expo.out" }, t);
    };
    K.card = function (sel, t, hold) {
      tl.from(sel, { x: -60, opacity: 0, duration: 0.4, ease: "power3.out" }, t);
      tl.to(sel, { x: -40, opacity: 0, duration: 0.3, ease: "power2.in" }, t + 0.4 + (hold == null ? 4 : hold));
    };
    K.title = function (sel, t, hold) {
      tl.from(sel + " .k", { y: 20, opacity: 0, duration: 0.35, ease: "power3.out" }, t);
      tl.from(sel + " .t", { y: 40, opacity: 0, duration: 0.5, ease: "power3.out" }, t + 0.1);
      tl.to(sel, { opacity: 0, duration: 0.3, ease: "power2.in" }, t + (hold == null ? 1.8 : hold));
    };
    // Wipe: panel rises over the frame ending exactly at T (cut point), then drops away after the swap.
    K.wipe = function (sel, T) {
      gsap.set(sel, { yPercent: 102 });
      tl.fromTo(sel, { yPercent: 102 }, { yPercent: 0, duration: 0.25, ease: "power3.in", immediateRender: false }, T - 0.25);
      tl.to(sel, { yPercent: -102, duration: 0.3, ease: "power3.out" }, T);
    };
    K.show = function (sel, t) { tl.set(sel, { visibility: "visible", opacity: 1 }, t); };
    K.hide = function (sel, t) { tl.set(sel, { opacity: 0, visibility: "hidden" }, t); };
    K.end = function (dur) { tl.set({}, {}, dur); };
    return K;
  }
  window.BTT = window.BTT || {};
  window.BTT.kit = kit;
})();
