// The in-page rule set: walks a HyperFrames short's GSAP timeline and turns visual events into sound cues.
// extract_cues.mjs (the runner) loads the page in headless Chrome and evaluates this function.
// Returns [{t, s, g}] sorted by time: t = seconds, s = kit sound name, g = relative gain (1 = normal).
// Captions (.cg) never make sound; nor does anything inside [data-sfx="off"] or a tween with data: "nosfx".
// Hand-placed cues in window.__sfx ([{t, s, g}], pushed by the composition's sfx() helper) are merged in
// and win over any automatic cue within 70 ms.
() => {
  const tl = (window.__timelines || {})["main"];
  if (!tl) return { error: "no main timeline" };
  const cues = [];
  const add = (t, s, g = 1) => cues.push({ t: +t.toFixed(3), s, g });
  const els = (tw) => (tw.targets ? tw.targets() : []).filter((e) => e && e.nodeType === 1);
  const has = (e, c) => e.classList && e.classList.contains(c);
  const within = (e, sel) => e.closest && e.closest(sel);
  const word = (id, words) => new RegExp("(^|-)(" + words + ")(-|\\d|$)", "i").test(id);
  const BLIPS = ["blip+0", "blip+2", "blip+4", "blip+7", "blip+9", "blip+12"];
  let blipStep = 0, lastFlow = -9;
  const nextBlip = () => BLIPS[blipStep++ % BLIPS.length];
  const deg = (x) => (typeof x === "number" ? Math.abs(x) : Math.abs(parseFloat(String(x || "0").replace(/^[+-]=/, "")) || 0));

  for (const tw of tl.getChildren(true, true, false)) {
    const t0 = tw.startTime(), d = tw.duration(), v = tw.vars || {}, f = v.startAt || {};
    if (v.data === "nosfx") continue;
    const targets = els(tw);
    const keys = Object.keys(v).concat(Object.keys(f));

    // Plain-object tweens with onUpdate: counters tick per digit (10/s), anything else is one stepping blip.
    if (!targets.length && typeof v.onUpdate === "function" && d > 0.15) {
      const isCounter = v.data === "counter" || /textContent\s*=\s*fmt\(/.test(String(v.onUpdate));
      if (isCounter) {
        const n = Math.min(Math.round(d * 10), 40);
        for (let i = 0; i < n; i++) add(t0 + (i * d) / n, ["digit", "digit-hi", "digit-lo"][i % 3], 0.8);
        add(t0 + d, "tick", 0.9);
      } else if (d > 0.4 && t0 - lastFlow > 0.6) { add(t0, nextBlip(), 0.7); lastFlow = t0; }
      continue;
    }

    // Staggers: each target gets its own start; at most 10 cues per second and 6 per tween.
    const n = targets.length, st = v.stagger;
    const each = n > 1 ? (typeof st === "number" ? st : st ? st.each || (st.amount ? st.amount / (n - 1) : 0) : 0) : 0;
    const dItem = each ? d - each * (n - 1) : d;
    const step = each ? Math.max(1, Math.ceil(0.1 / each)) : n;   // no stagger: one cue for the whole tween

    let placed = 0;
    for (let i = 0; i < n && placed < 6; i += step) {
      const e = targets[i], t = t0 + i * each;
      if (within(e, ".cg") || within(e, "#captions") || within(e, '[data-sfx="off"]')) continue;
      const id = e.id || "";
      const entering = v.runBackwards || "opacity" in f || "scale" in f;
      let cue = null;
      if (id === "wipe" && "yPercent" in v && v.yPercent === 0) cue = ["wipe", 1];
      else if (has(e, "dot") && keys.includes("scale")) cue = ["dot", 0.8];
      else if ((has(e, "tag") || has(e, "minitag")) && keys.includes("opacity")) cue = ["tick", 1];
      else if (keys.includes("strokeDashoffset") && dItem > 0.4) {      // flow line: one blip, stepping up
        if (t - lastFlow > 0.6) { cue = [nextBlip(), 0.7]; lastFlow = t; } else continue;
      }
      else if (word(id, "shell|cover|lid|casing|case|door|flap") && keys.includes("rotation")) cue = ["lift", 1];
      else if ((has(e, "stamp") || word(id, "stamp|check|cross|ok|no|nomatch")) &&
               (entering || keys.includes("scale") || keys.includes("strokeDashoffset"))) cue = ["stamp", 0.8];
      else if (word(id, "lockup|so-big|lock|things") && entering) cue = ["lockup", 0.9];
      else if (/(^|-)(so-)?mark/i.test(id) && (keys.includes("scaleX") || keys.includes("backgroundSize"))) cue = ["marker", 0.7];
      else if (keys.includes("rotation") && deg(v.rotation != null ? v.rotation : f.rotation) >= 90) cue = ["lift", 0.6];
      // generic entrances (from-tweens), quieter than the named events
      else if (!entering) continue;
      else if (keys.includes("clipPath") && dItem <= 1.2) cue = ["marker", 0.45];
      else if (keys.includes("scaleY") && dItem <= 0.8) cue = [nextBlip(), 0.55];
      else if (keys.includes("scale") && dItem <= 0.8) cue = ["tick-hi", 0.65];
      else if (keys.includes("x") && dItem > 1.0) cue = ["lift", 0.45];
      else if (keys.includes("opacity") && dItem <= 0.8 && (keys.includes("y") || keys.includes("x"))) cue = ["tick-lo", 0.55];
      if (cue) { add(t, cue[0], cue[1]); placed++; }
    }
  }

  for (const c of window.__sfx || []) cues.push({ t: +(+c.t).toFixed(3), s: c.s, g: c.g == null ? 1 : c.g, hand: true });
  // one end-card chord per episode (the first), nothing in the first 0.15 s,
  // and no two cues within 70 ms (the earlier wins, unless the later one was placed by hand)
  cues.sort((a, b) => a.t - b.t);
  const firstLock = cues.findIndex((c) => c.s === "lockup" && !c.hand);
  const out = [];
  cues.forEach((c, i) => {
    if (c.t < 0.15 || (c.s === "lockup" && !c.hand && i !== firstLock)) return;
    const last = out[out.length - 1];
    if (!last || c.t - last.t >= 0.07) out.push(c);
    else if (c.hand && !last.hand) out[out.length - 1] = c;
  });
  // Burst cap: at most 6 automatic cues in any 1 s window. Counter ticks, hand cues and the
  // structural sounds (wipe, reveal, lockup) are exempt and always kept.
  const exempt = (c) => c.hand || c.s.startsWith("digit") || c.s === "wipe" || c.s === "reveal" || c.s === "lockup";
  const kept = [], recent = [];
  for (const c of out) {
    if (exempt(c)) { kept.push(c); continue; }
    while (recent.length && c.t - recent[0] >= 1.0) recent.shift();
    if (recent.length >= 6) continue;
    recent.push(c.t); kept.push(c);
  }
  return kept.map(({ t, s, g }) => ({ t, s, g }));
}
