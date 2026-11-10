/* Behind The Things — L01 shared drawings (flat 2D, ink outlines, paper faces, hard shade offsets).
   Each function returns an SVG <g> string drawn around its own origin, with ids prefixed by `p`
   (use the chapter prefix, e.g. "ch02-sat"). Place it with a wrapping transform:
     svg.insertAdjacentHTML("beforeend", '<g transform="translate(960 400) scale(1)">' + BTT.draw.satellite("ch02-sat") + "</g>");
   Insert drawings synchronously, before building the timeline. Signal (accent) appears only where noted.
   TRAP: GSAP x/y/scale on a <g> that has a transform="translate(...)" attribute REPLACES that translate
   (the drawing jumps to the top-left). Always animate an outer wrapper with no transform attribute:
     '<g id="ch02-satw"><g transform="translate(960 470) scale(0.9)">' + BTT.draw.satellite("ch02-sat") + '</g></g>'
   then tween "#ch02-satw". Inner ids (e.g. "#ch02-sat-shell") can take x/y/rotation because they have no transform. */
(function () {
  var W = 6; // outline width
  function phoneFront(p, o) {
    o = o || {};
    var dot = o.dot !== false, ring = o.ring === true;
    // 300 x 600 body centred on (0,0)
    return '<g id="' + p + '">' +
      '<rect x="-144" y="-294" width="300" height="600" rx="46" class="f-shade"/>' +
      '<rect id="' + p + '-body" x="-150" y="-300" width="300" height="600" rx="46" class="f-hi s-ink" stroke-width="' + W + '"/>' +
      '<g id="' + p + '-screen">' +
        '<clipPath id="' + p + '-clip"><rect x="-128" y="-262" width="256" height="524" rx="22"/></clipPath>' +
        '<g clip-path="url(#' + p + '-clip)">' +
          '<rect x="-128" y="-262" width="256" height="524" class="f-paper"/>' +
          // blocks
          '<g class="f-hi s-ink2" stroke-width="3">' +
            '<rect x="-120" y="-250" width="92" height="120" rx="6"/><rect x="-6" y="-250" width="130" height="80" rx="6"/>' +
            '<rect x="-120" y="-100" width="92" height="150" rx="6"/><rect x="-6" y="-146" width="58" height="100" rx="6"/><rect x="74" y="-146" width="50" height="196" rx="6"/>' +
            '<rect x="-120" y="80" width="150" height="80" rx="6"/><rect x="54" y="80" width="70" height="170" rx="6"/><rect x="-120" y="186" width="150" height="70" rx="6"/>' +
          '</g>' +
          // roads
          '<g class="s-ink2" stroke-width="2" stroke-dasharray="10 10" fill="none"><path d="M-128 -115 H128"/><path d="M-17 -262 V262"/><path d="M-128 65 H128"/><path d="M42 65 V262"/></g>' +
        '</g>' +
      '</g>' +
      '<rect x="-36" y="-284" width="72" height="12" rx="6" class="f-ink"/>' +
      (ring ? '<circle id="' + p + '-ring" cx="-17" cy="-25" r="70" class="f-flow" opacity="0.18"/>' : '') +
      (dot ? '<circle id="' + p + '-halo" cx="-17" cy="-25" r="30" class="f-flow" opacity="0.22"/>' +
             '<circle id="' + p + '-dot" cx="-17" cy="-25" r="19" class="f-flow" stroke="#FBF7EE" stroke-width="6"/>' : '') +
      '</g>';
  }
  // Phone seen from the back. The cover (id p-cover) lifts away to reveal the board and the quartz crystal (Signal).
  function phoneBack(p) {
    return '<g id="' + p + '">' +
      '<rect x="-144" y="-294" width="300" height="600" rx="46" class="f-shade"/>' +
      '<rect x="-150" y="-300" width="300" height="600" rx="46" class="f-hi s-ink" stroke-width="' + W + '"/>' +
      '<g id="' + p + '-inside">' +
        '<rect x="-118" y="-262" width="236" height="300" rx="16" class="f-shade s-ink" stroke-width="4"/>' +
        '<rect x="-96" y="-236" width="96" height="96" rx="8" class="f-hi s-ink" stroke-width="4"/>' +
        '<text x="-48" y="-180" text-anchor="middle" class="svg-mono" data-layout-ignore font-size="24" fill="#17161B">CPU</text>' +
        '<rect x="22" y="-236" width="74" height="60" rx="8" class="f-hi s-ink" stroke-width="4"/>' +
        '<rect x="22" y="-160" width="74" height="40" rx="8" class="f-hi s-ink" stroke-width="4"/>' +
        '<g id="' + p + '-quartz"><rect x="-70" y="-96" width="64" height="34" rx="17" class="f-accent s-ink" stroke-width="4"/>' +
          '<path d="M-60 -62 v14 M-16 -62 v14" class="s-ink" stroke-width="4"/></g>' +
        '<rect x="20" y="-100" width="76" height="110" rx="8" class="f-hi s-ink" stroke-width="4"/>' +
        '<text x="58" y="-36" text-anchor="middle" class="svg-mono" data-layout-ignore font-size="24" fill="#17161B">GPS</text>' +
        '<rect x="-118" y="60" width="236" height="210" rx="16" class="f-paper s-ink2" stroke-width="3" stroke-dasharray="8 8"/>' +
        '<text x="0" y="172" text-anchor="middle" class="svg-mono" data-layout-ignore font-size="24" fill="#5B5662">BATTERY</text>' +
      '</g>' +
      '<g id="' + p + '-cover">' +
        '<rect x="-150" y="-300" width="300" height="600" rx="46" class="f-hi s-ink" stroke-width="' + W + '"/>' +
        '<rect x="-112" y="-262" width="96" height="110" rx="26" class="f-shade s-ink" stroke-width="4"/>' +
        '<circle cx="-64" cy="-234" r="18" class="f-hi s-ink" stroke-width="4"/><circle cx="-64" cy="-180" r="18" class="f-hi s-ink" stroke-width="4"/>' +
      '</g>' +
      '</g>';
  }
  // GPS satellite: body 180x140 centred, two solar wings, antenna face pointing DOWN (toward Earth).
  // o.clock: draw the Signal clock face on the body. The shell (p-shell) lifts to reveal three atomic clocks (p-clocks).
  function satellite(p, o) {
    o = o || {};
    var wing = function (x, id) {
      var s = '<g id="' + id + '"><rect x="' + (x + 6) + '" y="-34" width="220" height="80" class="f-shade"/>' +
        '<rect x="' + x + '" y="-40" width="220" height="80" class="f-hi s-ink" stroke-width="' + W + '"/>';
      for (var i = 1; i < 4; i++) s += '<path d="M' + (x + i * 55) + ' -40 V40" class="s-ink" stroke-width="3"/>';
      return s + '<path d="M' + x + ' 0 H' + (x + 220) + '" class="s-ink" stroke-width="3"/></g>';
    };
    var clocks = '<g id="' + p + '-clocks">';
    for (var k = 0; k < 3; k++) {
      var cx = -50 + k * 50;
      clocks += '<rect x="' + (cx - 18) + '" y="-44" width="36" height="72" rx="10" class="' + (o.accentClocks ? 'f-accent' : 'f-hi') + ' s-ink" stroke-width="4"/>' +
        '<path d="M' + (cx - 18) + ' -20 H' + (cx + 18) + '" class="s-ink" stroke-width="3"/>';
    }
    clocks += '</g>';
    return '<g id="' + p + '">' +
      '<path d="M-90 0 H-126 M90 0 H126" class="s-ink" stroke-width="' + W + '"/>' +
      wing(-346, p + '-wl') + wing(126, p + '-wr') +
      '<rect x="-84" y="-64" width="180" height="140" rx="10" class="f-shade"/>' +
      '<rect id="' + p + '-core" x="-90" y="-70" width="180" height="140" rx="10" class="f-paper s-ink" stroke-width="' + W + '"/>' +
      clocks +
      '<g id="' + p + '-shell"><rect x="-90" y="-70" width="180" height="140" rx="10" class="f-hi s-ink" stroke-width="' + W + '"/>' +
        (o.clock ? '<g id="' + p + '-clockface"><circle cx="0" cy="0" r="44" class="f-accent s-ink" stroke-width="5"/>' +
          '<path id="' + p + '-hand-m" d="M0 0 V-30" class="s-ink" stroke-width="5" stroke-linecap="round"/>' +
          '<path id="' + p + '-hand-h" d="M0 0 H20" class="s-ink" stroke-width="5" stroke-linecap="round"/><circle cx="0" cy="0" r="5" class="f-ink"/></g>'
          : '<path d="M-60 -40 H60 M-60 -14 H60 M-60 12 H60 M-60 38 H60" class="s-ink2" stroke-width="3"/>') +
      '</g>' +
      // antenna array on the Earth-facing (bottom) side
      '<rect x="-56" y="70" width="112" height="22" rx="4" class="f-hi s-ink" stroke-width="5"/>' +
      '<path d="M-36 92 v16 M-12 92 v16 M12 92 v16 M36 92 v16" class="s-ink" stroke-width="5" stroke-linecap="round"/>' +
      '</g>';
  }
  // Earth's edge: a huge arc whose top sits at y=0, spanning the frame width around x=0.
  function earth(p, o) {
    o = o || {}; var r = o.r || 2200;
    return '<g id="' + p + '">' +
      '<circle cx="0" cy="' + r + '" r="' + r + '" class="f-hi s-ink" stroke-width="' + W + '"/>' +
      '<g class="s-ink2" fill="none" stroke-width="3" stroke-dasharray="14 12">' +
        '<ellipse cx="0" cy="' + r + '" rx="' + (r * 0.55) + '" ry="' + (r - 1) + '"/>' +
        '<ellipse cx="0" cy="' + r + '" rx="' + (r * 0.9) + '" ry="' + (r - 1) + '"/>' +
        '<path d="M' + (-r) + ' ' + (r * 0.12) + ' Q0 ' + (r * 0.02) + ' ' + r + ' ' + (r * 0.12) + '"/>' +
      '</g></g>';
  }
  // A row of buildings standing on y=0, total width w, deterministic heights.
  function buildings(p, o) {
    o = o || {}; var hs = o.heights || [380, 520, 300, 610, 440];
    var bw = o.bw || 150, gap = o.gap || 20, s = '<g id="' + p + '">', x = 0;
    hs.forEach(function (h, i) {
      s += '<g id="' + p + '-b' + i + '"><rect x="' + (x + 6) + '" y="' + (-h + 6) + '" width="' + bw + '" height="' + h + '" class="f-shade"/>' +
        '<rect x="' + x + '" y="' + (-h) + '" width="' + bw + '" height="' + h + '" class="f-hi s-ink" stroke-width="' + W + '"/>';
      for (var yy = -h + 30; yy < -40; yy += 56) for (var xx = x + 24; xx < x + bw - 30; xx += 44)
        s += '<rect x="' + xx + '" y="' + yy + '" width="22" height="30" rx="3" class="f-shade"/>';
      s += '</g>'; x += bw + gap;
    });
    return s + '</g>';
  }
  function wifi(p) {
    return '<g id="' + p + '" fill="none" class="s-ink" stroke-width="' + W + '" stroke-linecap="round">' +
      '<path d="M-60 -20 A85 85 0 0 1 60 -20"/><path d="M-38 4 A54 54 0 0 1 38 4"/><path d="M-17 27 A24 24 0 0 1 17 27"/>' +
      '<circle cx="0" cy="44" r="8" class="f-ink"/></g>';
  }
  function tower(p) {
    return '<g id="' + p + '" fill="none" class="s-ink" stroke-width="' + W + '" stroke-linejoin="round" stroke-linecap="round">' +
      '<path d="M0 -90 L-46 90 M0 -90 L46 90 M-30 30 H30 M-18 -18 H18 M-38 60 L24 0 M38 60 L-24 0"/>' +
      '<circle cx="0" cy="-90" r="9" class="f-ink"/>' +
      '<path d="M-34 -120 A48 48 0 0 0 -34 -60 M34 -120 A48 48 0 0 1 34 -60"/></g>';
  }
  // Analog clock (r=radius). Hands: p-min, p-hr. Accent only when o.accent.
  function clock(p, o) {
    o = o || {}; var r = o.r || 90;
    var s = '<g id="' + p + '"><circle cx="6" cy="6" r="' + r + '" class="f-shade"/>' +
      '<circle cx="0" cy="0" r="' + r + '" class="' + (o.accent ? 'f-accent' : 'f-hi') + ' s-ink" stroke-width="' + W + '"/>';
    for (var i = 0; i < 12; i++) {
      var a = i * Math.PI / 6, r1 = r * 0.78, r2 = r * 0.9;
      s += '<path d="M' + (Math.sin(a) * r1).toFixed(1) + ' ' + (-Math.cos(a) * r1).toFixed(1) + ' L' + (Math.sin(a) * r2).toFixed(1) + ' ' + (-Math.cos(a) * r2).toFixed(1) + '" class="s-ink" stroke-width="4"/>';
    }
    return s + '<path id="' + p + '-min" d="M0 0 V' + (-r * 0.7) + '" class="s-ink" stroke-width="6" stroke-linecap="round"/>' +
      '<path id="' + p + '-hr" d="M0 0 H' + (r * 0.45) + '" class="s-ink" stroke-width="6" stroke-linecap="round"/>' +
      '<circle cx="0" cy="0" r="7" class="f-ink"/></g>';
  }
  // A signal pulse: concentric arcs travelling downward. p-0..p-2 are the arcs (animate y/opacity).
  function pulse(p, o) {
    o = o || {}; var w = o.w || 60, s = '<g id="' + p + '" fill="none" class="s-flow" stroke-width="6" stroke-linecap="round">';
    for (var i = 0; i < 3; i++) s += '<path id="' + p + '-' + i + '" d="M' + (-w + i * 12) + ' ' + (i * 22) + ' Q0 ' + (24 + i * 22) + ' ' + (w - i * 12) + ' ' + (i * 22) + '"/>';
    return s + '</g>';
  }
  window.BTT = window.BTT || {};
  window.BTT.draw = { phoneFront: phoneFront, phoneBack: phoneBack, satellite: satellite, earth: earth, buildings: buildings, wifi: wifi, tower: tower, clock: clock, pulse: pulse };
})();
