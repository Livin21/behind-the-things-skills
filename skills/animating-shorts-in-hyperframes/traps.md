# Traps (every one has happened)

| # | Symptom | Cause | Fix |
|---|---|---|---|
| 1 | Text "occluded" by `#wipe` mid-scene; the panel sits over the frame | A CSS `transform` plus GSAP `yPercent`/`x`/`scale` on the same element are **summed** | Never give a tweened element a CSS transform. Use `gsap.set`, or centre it with a wrapper (flex) |
| 2 | StaticGuard: "Font families used without @font-face" | Font named in CSS only | Local `@font-face` plus woff2 in `assets/fonts/` |
| 3 | Objects slide under the captions late in a long scene | Push-in growth | Keep the 7% cap; lay out inside x 104–912, y 258–1211 before the push |
| 4 | An SVG part scales or rotates from its corner | GSAP's default origin for SVG is the top-left | `transformOrigin: "50% 50%"` in the tween |
| 5 | Items peek in at the frame edge before they should | The `from` offset is too small | The start state must be fully off canvas; snapshot each scene's first frame |
| 6 | Labels wrap inside fixed-width boxes | Box narrower than the label | `white-space: nowrap`; size the box to the longest label |
| 7 | A tag beside a centred object runs past x 940 | 32 px mono ≈ 19 px per character, plus 40 px padding | Measure; put the tag above or below, or run the leader down to it |
| 8 | A moving dot or packet covers labels | A shared lane | Give the mover its own lane beside the labels |
| 9 | Blank default cover on the platforms | The hook object fades in | No opacity entrance on the hook; check `frame0.png` from the render. A t = 0.3 snapshot won't catch it |
| 10 | `content_overlap` on a stamp over text, or on stacked swap tags | An intentional overlap | `data-layout-allow-overlap` on both elements |
| 11 | Type-floor warning on tiny text | Decorative text, or normal text inside something later scaled down (a shrunken casing) | `data-layout-ignore` on it |
| 12 | A fake barcode or QR code | Drawn by eye | Generate it from the spec in code; decode-test a rendered frame (for example with jsQR) |
| 13 | A missing glyph (□) in a tag | The font lacks `→`, `−`, `≈` or `✓` | Check the glyphs in the font; draw arrows as SVG |
| 14 | "Inactive" icon parts are invisible | Shade-coloured fills on the paper background | Give inactive parts an ink-2 outline |
| 15 | SVG `<text>` in the wrong font | `.tag` styles don't reach into SVG | Give SVG text its own font class |
| 16 | Contrast or type check flags a counter or readout | `check` measures text at whatever value it holds at the sample time | Expected; confirm the final value visually |
