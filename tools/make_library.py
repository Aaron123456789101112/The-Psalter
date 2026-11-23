"""The Psalter's Library: the row of tab buttons becomes a "Library" button that opens a full-screen library where each
collection is an object you pick up.

usage: python3 make_library.py <index.html in> <out.html> <luxe|scrolls>
  luxe    - luxurious ancient leather books on a carved shelf (gilt tooling, brass caps, set stones)
  scrolls - historically accurate: Qumran-style parchment scrolls (linen wrappers, leather ties, a clay jar) for the
            Hebrew Bible books; early papyrus codices in leather wrappers for Matthew and Revelation; a miniature codex
            for Prayers; each labelled with a hanging parchment tag, in a cedar pigeonhole rack.
The old tab buttons stay in the page (hidden) and the library presses them, so the existing tab code is untouched.
"""
import sys, math

src, out, style = sys.argv[1], sys.argv[2], sys.argv[3]
assert style in ("luxe", "scrolls")
s = open(src, encoding="utf-8").read()

def once(old, new):
    global s
    assert s.count(old) == 1, ("expected exactly one", old[:80], s.count(old))
    s = s.replace(old, new, 1)

# ---------- the collections ----------
# key, short title, long title (top bar), mark, mark language, colours: cover-dark, cover-mid, gilt/ink, glow, gem
BOOKS = {
    "judges":   ("Judges", "Judges by the Fire", "שופטים", "he", "#2a1608", "#5a3212", "#f6b469", "#f0a04b", "#e8792a"),
    "mighty":   ("Mighty Men", "The Mighty Men", "הגבורים", "he", "#121212", "#36302a", "#dcb46a", "#d6a85a", "#b9bcc4"),
    "psalter":  ("The Psalter", "The Psalter", "תהלים", "he", "#14211a", "#30503f", "#e6b85c", "#d7a447", "#2f8f5b"),
    "proverbs": ("Proverbs", "Proverbs", "משלי", "he", "#0c1c1a", "#21524b", "#a6d8cf", "#8fcbc1", "#3fb5a5"),
    "prophets": ("Prophets", "The Prophets", "נביאים", "he", "#220d14", "#5a2333", "#eaa3b4", "#e08a9f", "#9b3a66"),
    "matthew":  ("Matthew", "Matthew", "מתי", "he", "#141b0e", "#43542c", "#d2dc98", "#c3cf86", "#6f9a3a"),
    "rev":      ("Revelation", "Revelation", "Ἀποκάλυψις", "grc", "#1d0907", "#5e2016", "#f09a7c", "#e0674a", "#b3261e"),
    "prayers":  ("Prayers", "Prayers", "תפילות", "he", "#10152a", "#2e3a68", "#c4d0f4", "#9fb2ec", "#4b62c4"),
}
SHELVES = [("Old Testament", ["judges", "mighty", "psalter", "proverbs", "prophets"]),
           ("New Testament & Prayers", ["matthew", "rev", "prayers"])]

stars = "".join(
    f'<circle cx="{12 + 7 * math.cos(2 * math.pi * i / 7 - math.pi / 2):.2f}" cy="{12 + 7 * math.sin(2 * math.pi * i / 7 - math.pi / 2):.2f}" r="1.3" fill="currentColor" stroke="none"/>'
    for i in range(7))
EM = {
    "psalter": '<path d="M7 4c-2.5 4-2.5 10 1 15h8c3.5-5 3.5-11 1-15"/><path d="M6 6.5h12M10 7v11M12 7v11M14 7v11"/>',
    "judges": '<path d="M12 3c3 4 6.5 6.5 6.5 11.5a6.5 6.5 0 0 1-13 0c0-3 1.5-5 3-7 0 3 1 4.5 3 5.5 0-4-1-6.5.5-10z"/>',
    "mighty": '<circle cx="11" cy="13" r="6.5"/><circle cx="11" cy="13" r="1.8"/><path d="M5 21L21 3M18 3h3v3"/>',
    "proverbs": '<path d="M7 4h10a2 2 0 0 1 2 2v13H9a2 2 0 0 1-2-2z"/><path d="M7 4a2 2 0 0 0-2 2v2h2M10 9h6M10 12h6M10 15h4"/>',
    "prophets": '<path d="M3 17c5 0 11-3 15-10l2.5 1.2c-3 7.5-10 12-17.5 12z"/><path d="M18 7l1.2-2.5"/>',
    "matthew": '<path d="M12 2l1.6 7.4L21 12l-7.4 1.6L12 22l-1.6-8.4L3 12l7.4-2.6z"/>',
    "rev": f'<circle cx="12" cy="12" r="2.2"/>{stars}',
    "prayers": '<path d="M3 14c3.5 3.2 11.5 3.2 15.5 0l2.5-3.2h-6c-3.5 0-9 .2-12 3.2z"/><path d="M19.5 9.5c-.6-2 .6-3.4.6-5.5 1.3 2 1.6 3.8-.6 5.5z"/>',
}
NOISE = ("url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='140' height='140'%3E%3Cfilter id='n'%3E"
         "%3CfeTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='3' stitchTiles='stitch'/%3E%3CfeColorMatrix values='0 0 0 0 0  0 0 0 0 0  "
         "0 0 0 0 0  0 0 0 .9 0'/%3E%3C/filter%3E%3Crect width='140' height='140' filter='url(%23n)' opacity='.33'/%3E%3C/svg%3E\")")
FIBRE = ("url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E%3Cfilter id='f'%3E"
         "%3CfeTurbulence type='fractalNoise' baseFrequency='.02 .9' numOctaves='2' stitchTiles='stitch'/%3E%3CfeColorMatrix values='0 0 0 0 0  0 0 0 0 0  "
         "0 0 0 0 0  0 0 0 .7 0'/%3E%3C/filter%3E%3Crect width='160' height='160' filter='url(%23f)' opacity='.25'/%3E%3C/svg%3E\")")

LAMP = ('<svg class="lamp" viewBox="0 0 64 44" aria-hidden="true">'
        '<ellipse cx="50" cy="12" rx="7" ry="11" fill="url(#lampglow)"/>'
        '<path d="M50 20c-2-3 0-6 0-11 2.5 4.5 3 7.5 0 11z" fill="#ffcf7a"/>'
        '<path d="M6 28c6 9 34 10 42 0l6-6H38c-10 0-26 0-32 6z" fill="#9a5a30"/><path d="M6 28c6 9 34 10 42 0" fill="none" stroke="#c98a55" stroke-width="1.5"/>'
        '<ellipse cx="27" cy="24" rx="7" ry="2" fill="#3b2213"/>'
        '<defs><radialGradient id="lampglow"><stop offset="0" stop-color="#ffd890" stop-opacity=".9"/><stop offset="1" stop-color="#ffb347" stop-opacity="0"/></radialGradient></defs></svg>')

# ======================================================================================================================
# Version A: luxurious ancient books
# ======================================================================================================================
LUXE_SIZES = {"judges": (64, 84), "mighty": (68, 90), "psalter": (88, 99), "proverbs": (62, 82), "prophets": (66, 92),
              "matthew": (72, 90), "rev": (68, 95), "prayers": (60, 80)}

def luxe_book(k):
    t, _, mark, lang, dark, mid, gilt, glow, gem = BOOKS[k]
    w, h = LUXE_SIZES[k]
    fam = " judges" if k == "judges" else ""
    return (f'<button class="pick book" type="button" data-tab="{k}" aria-label="{t}" '
            f'style="--dark:{dark};--mid:{mid};--gilt:{gilt};--glow:{glow};--gem:{gem};--w:{w}px;--h:{h}%">'
            f'<span class="cap"></span><span class="tool"></span>'
            f'<span class="mk" lang="{lang}"{"" if lang == "grc" else " dir=rtl"}>{mark}</span>'
            f'<span class="hub"></span>'
            f'<span class="lab"><span class="ttl{fam}">{t}</span></span>'
            f'<span class="hub"><i class="gem"></i></span>'
            f'<span class="roundel"><svg class="em" viewBox="0 0 24 24" aria-hidden="true">{EM[k]}</svg></span>'
            f'<span class="tool"></span><span class="cap bot"></span></button>')

def luxe_html():
    h = ""
    for i, (plate, keys) in enumerate(SHELVES):
        h += ('<div class="shelf"><div class="row">' + "".join(luxe_book(k) for k in keys) + (LAMP if i == 1 else "")
              + f'</div><div class="board"><i class="rail"></i></div><span class="plate">{plate}</span></div>')
    return h

LUXE_CSS = r'''
.lib.luxe { background:
    radial-gradient(110% 55% at 50% -5%, rgba(255, 196, 120, .24), transparent 62%),
    radial-gradient(80% 50% at 85% 78%, rgba(255, 170, 80, .10), transparent 70%),
    repeating-linear-gradient(90deg, #26170d 0 56px, #1d1109 56px 58px, #2a190e 58px 114px, #1e120a 114px 116px), #22140b; }
.luxe .shelf { position: relative; width: 100%; max-width: 440px; margin: 0 auto 26px; }
.luxe .row { display: flex; align-items: flex-end; justify-content: center; gap: 4px; height: clamp(292px, 44vh, 350px); padding: 0 4px; }
.luxe .board { position: relative; height: 22px; border-radius: 3px;
  background: linear-gradient(#7d4f2c, #5b3519 40%, #3a2010); box-shadow: 0 14px 22px rgba(0, 0, 0, .6), inset 0 1px 0 rgba(255, 220, 170, .3); }
.luxe .rail { position: absolute; left: 0; right: 0; top: 4px; height: 5px; background: linear-gradient(#f3d98c, #b0812e 55%, #6b4a17); box-shadow: 0 1px 1px rgba(0,0,0,.5); }
.luxe .plate { display: block; width: max-content; margin: 9px auto 0; padding: 3px 12px; border-radius: 2px;
  font: 700 11px var(--ui); letter-spacing: .16em; text-transform: uppercase; color: #3a2410;
  background: linear-gradient(#f3d690, #b98a40); box-shadow: 0 1px 2px rgba(0, 0, 0, .5), inset 0 0 0 1px rgba(90, 55, 15, .5); }
.book { --goldg: linear-gradient(180deg, #fff1bf, #e8c05e 30%, #9b6b1e 60%, #f0d27a 85%, #b38330);
  position: relative; flex: 0 1 var(--w); min-width: 50px; height: var(--h); margin: 0; padding: 0; border: 0; cursor: pointer;
  border-radius: 6px 6px 3px 3px; overflow: hidden; color: var(--gilt);
  display: flex; flex-direction: column; align-items: stretch;
  background:
    linear-gradient(90deg, rgba(0,0,0,.62), rgba(255,255,255,.13) 24%, rgba(255,255,255,.04) 44%, rgba(0,0,0,.22) 74%, rgba(0,0,0,.66)),
    radial-gradient(60% 18% at 30% 22%, rgba(255,255,255,.07), transparent 70%),
    radial-gradient(50% 12% at 70% 70%, rgba(0,0,0,.25), transparent 70%),
    __NOISE__,
    linear-gradient(180deg, var(--mid), var(--dark) 85%);
  box-shadow: 3px 0 5px rgba(0, 0, 0, .5), -1px 0 2px rgba(0, 0, 0, .4);
  transition: transform .45s cubic-bezier(.2, .8, .2, 1), box-shadow .45s; -webkit-tap-highlight-color: transparent; }
.book .cap { flex: none; height: 11px; background:
    radial-gradient(circle at 22% 55%, #fff3c4 0 1.3px, #6b4a17 1.6px 2.2px, transparent 2.4px),
    radial-gradient(circle at 78% 55%, #fff3c4 0 1.3px, #6b4a17 1.6px 2.2px, transparent 2.4px),
    linear-gradient(180deg, #f6dc8e, #c49440 45%, #7a5519 80%, #3b2508);
  box-shadow: 0 1px 2px rgba(0, 0, 0, .6); }
.book .cap.bot { transform: scaleY(-1); }
.book .tool { flex: none; height: 9px; margin: 4px 7px; opacity: .85;
  background: repeating-linear-gradient(45deg, var(--gilt) 0 1px, transparent 1px 5px), repeating-linear-gradient(-45deg, var(--gilt) 0 1px, transparent 1px 5px);
  -webkit-mask: linear-gradient(90deg, transparent, #000 15%, #000 85%, transparent); mask: linear-gradient(90deg, transparent, #000 15%, #000 85%, transparent);
  border-top: 1px solid color-mix(in srgb, var(--gilt) 70%, transparent); border-bottom: 1px solid color-mix(in srgb, var(--gilt) 70%, transparent); }
.book .mk { flex: none; text-align: center; font: 500 13px/1 Alegreya, Georgia, serif; white-space: nowrap; padding: 3px 0 5px;
  background: var(--goldg); -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent;
  filter: drop-shadow(0 1px 0 rgba(0, 0, 0, .7)); }
.book .mk[lang="grc"] { font-size: 10px; }
.book .hub { position: relative; flex: none; height: 8px; margin: 2px 0;
  background: linear-gradient(rgba(0,0,0,.55), rgba(255,255,255,.2) 45%, rgba(0,0,0,.5));
  box-shadow: 0 -2px 0 -1px color-mix(in srgb, var(--gilt) 75%, transparent), 0 2px 0 -1px color-mix(in srgb, var(--gilt) 75%, transparent); }
.book .gem { position: absolute; left: 50%; top: 50%; width: 11px; height: 11px; margin: -5.5px 0 0 -5.5px; border-radius: 50%;
  background: radial-gradient(circle at 35% 30%, #fff 0 1.2px, color-mix(in srgb, var(--gem) 55%, #fff) 2px, var(--gem) 55%, color-mix(in srgb, var(--gem) 50%, #000));
  box-shadow: 0 0 0 1.6px #d9ac4f, 0 0 0 2.6px #6b4a17, 0 1px 3px rgba(0, 0, 0, .7); }
.book .lab { flex: 1 1 auto; min-height: 0; margin: 6px 7px; display: flex; align-items: center; justify-content: center; overflow: hidden;
  border-radius: 2px; background: linear-gradient(90deg, rgba(0,0,0,.45), rgba(0,0,0,.18) 40%, rgba(0,0,0,.42));
  box-shadow: inset 0 0 0 1px color-mix(in srgb, var(--gilt) 85%, transparent), inset 0 0 0 3px rgba(0,0,0,.35), inset 0 0 0 4px color-mix(in srgb, var(--gilt) 45%, transparent), inset 0 2px 6px rgba(0,0,0,.6); }
.book .ttl { writing-mode: vertical-rl; font: 400 21px/1 Bellefair, Georgia, serif; letter-spacing: .08em; white-space: nowrap;
  background: var(--goldg); -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent;
  filter: drop-shadow(0 1px 0 rgba(0, 0, 0, .75)) drop-shadow(0 0 1px rgba(0, 0, 0, .5)); }
.book .ttl.judges { font-family: "IM Fell English", Georgia, serif; }
.book .roundel { flex: none; align-self: center; width: 32px; height: 32px; margin: 6px 0 4px; border-radius: 50%; display: grid; place-items: center;
  box-shadow: inset 0 0 0 1.4px color-mix(in srgb, var(--gilt) 85%, transparent), inset 0 0 0 3.5px rgba(0,0,0,.3), inset 0 0 0 4.4px color-mix(in srgb, var(--gilt) 45%, transparent); }
.book .em { width: 20px; height: 20px; fill: none; stroke: currentColor; stroke-width: 1.6; stroke-linecap: round; stroke-linejoin: round;
  filter: drop-shadow(0 1px 0 rgba(0, 0, 0, .7)); }
.book.current { transform: translateY(-16px); box-shadow: 3px 0 5px rgba(0, 0, 0, .5), 0 0 24px -3px var(--glow); }
.book.pull { transform: translateY(-74px) scale(1.05); box-shadow: 0 0 32px -2px var(--glow); z-index: 2; }
.book:focus-visible { outline: 2px solid #f1d9a8; outline-offset: 3px; }
.luxe .lamp { width: 64px; height: 44px; flex: none; margin-left: 8px; align-self: flex-end; filter: drop-shadow(0 0 10px rgba(255, 190, 90, .35)); }
@media (max-width: 380px) { .luxe .row { gap: 3px; } }
'''.replace("__NOISE__", NOISE)

# ======================================================================================================================
# Version B: historically accurate scrolls and codices
# ======================================================================================================================
def scroll_svg(k, length, dia, skin, wrap=None, tie="#5a3418", jar=False):
    """A parchment scroll lying on its side, seen from the front: a rolled cylinder of sewn sheets, the spiral of the
    roll at the left end, the edge of the outermost sheet, a leather thong (or a linen wrapper)."""
    W, H = 168, dia + 14
    x0 = (W - length) / 2 + 3; y0 = 5; r = dia / 2
    g = f'g{k}'
    out = [f'<svg class="obj" viewBox="0 0 {W} {H}" aria-hidden="true"><defs>'
           f'<linearGradient id="{g}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{skin}" stop-opacity=".55"/>'
           f'<stop offset=".18" stop-color="{skin}"/><stop offset=".55" stop-color="{skin}"/><stop offset="1" stop-color="#2b1a0c"/></linearGradient>'
           f'<linearGradient id="{g}w" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#cfc3a2"/><stop offset=".22" stop-color="#ddd1b1"/><stop offset=".6" stop-color="#c4b791"/><stop offset="1" stop-color="#5f5440"/></linearGradient>'
           f'<pattern id="{g}v" width="3" height="3" patternUnits="userSpaceOnUse"><path d="M0 1.5H3M1.5 0V3" stroke="rgba(90,75,50,.22)" stroke-width=".6"/></pattern>'
           f'</defs>']
    out.append(f'<ellipse cx="{W/2+3}" cy="{y0+dia+4}" rx="{length/2+4}" ry="3" fill="rgba(0,0,0,.45)"/>')
    # body
    out.append(f'<rect x="{x0}" y="{y0}" width="{length}" height="{dia}" rx="{r*0.35}" fill="url(#{g})"/>')
    # sewn seams between sheets (sinew stitches) and the slightly ragged outer edge
    for sx in (x0 + length * .34, x0 + length * .68):
        out.append(f'<path d="M{sx:.1f} {y0+2} V{y0+dia-2}" stroke="rgba(60,35,15,.45)" stroke-width="1" stroke-dasharray="2 3"/>')
    out.append(f'<path d="M{x0+length*.86:.1f} {y0} q-3 {dia*.3} 1 {dia*.55} t-1 {dia*.45}" stroke="rgba(50,28,10,.55)" stroke-width="1.2" fill="none"/>')
    # the spiral end
    cx = x0 + 1; cy = y0 + r
    out.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{r*0.42}" ry="{r}" fill="#c9ad7d" stroke="#5b3a1a" stroke-width=".8"/>')
    for i in range(1, 5):
        out.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{r*0.42*(1-i/5.5):.2f}" ry="{r*(1-i/5.5):.2f}" fill="none" stroke="rgba(80,50,20,.75)" stroke-width=".9"/>')
    out.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{r*0.06:.2f}" ry="{r*0.15:.2f}" fill="#3b2410"/>')
    if wrap:   # a linen wrapper (some Qumran wrappers had indigo-blue lines woven in) folded around most of the roll
        wx = x0 + length * .18; ww = length * .7
        out.append(f'<rect x="{wx}" y="{y0-1.5}" width="{ww}" height="{dia+3}" rx="3" fill="url(#{g}w)"/>')
        out.append(f'<rect x="{wx}" y="{y0-1.5}" width="{ww}" height="{dia+3}" rx="3" fill="url(#{g}v)"/>')
        for i, f in enumerate((.18, .42, .66, .86)):
            out.append(f'<path d="M{wx+ww*f:.1f} {y0-1} q2 {dia*.5} -1 {dia+2}" stroke="rgba(110,95,70,.45)" stroke-width="1" fill="none"/>')
        if wrap == "blue":
            for f in (.08, .9):
                out.append(f'<path d="M{wx+ww*f:.1f} {y0-1} V{y0+dia+1.5}" stroke="#3e5a86" stroke-width="1.8" opacity=".75"/>')
        out.append(f'<path d="M{wx+ww:.1f} {y0-1} l5 {dia*.45} -4 {dia*.6}" fill="#d9ccab" stroke="rgba(110,95,70,.5)" stroke-width=".8"/>')
    # leather thong tied round the middle, ends hanging
    tx = x0 + length * (0.62 if not wrap else 0.55)
    out.append(f'<path d="M{tx} {y0-1} V{y0+dia+1} M{tx+4} {y0-1} V{y0+dia+1}" stroke="{tie}" stroke-width="2.4"/>')
    out.append(f'<path d="M{tx+2} {y0+dia} q4 6 1 12 M{tx+2} {y0+dia} q-5 5 -3 11" stroke="{tie}" stroke-width="1.6" fill="none" stroke-linecap="round"/>')
    out.append('</svg>')
    return "".join(out)

def jar_svg(k):
    """A Qumran scroll jar: tall, cylindrical, buff clay with a bowl-shaped lid (set aside), the linen-wrapped scroll's head showing."""
    g = f'j{k}'
    return (f'<svg class="obj jar" viewBox="0 0 168 120" aria-hidden="true"><defs>'
            f'<linearGradient id="{g}" x1="0" x2="1"><stop offset="0" stop-color="#6e5434"/><stop offset=".3" stop-color="#d8c19a"/>'
            f'<stop offset=".55" stop-color="#c9ad80"/><stop offset="1" stop-color="#5f472b"/></linearGradient>'
            f'<linearGradient id="{g}l" x1="0" x2="1"><stop offset="0" stop-color="#7a5e3b"/><stop offset=".4" stop-color="#dcc6a0"/><stop offset="1" stop-color="#6a5133"/></linearGradient></defs>'
            f'<ellipse cx="72" cy="115" rx="34" ry="4" fill="rgba(0,0,0,.45)"/>'
            f'<path d="M60 22 q-2 -12 6 -14 h12 q8 2 6 14z" fill="#e7dcc1" stroke="#8a7b5c" stroke-width=".8"/>'
            f'<path d="M64 12 v10 M80 12 v10" stroke="#3b5f9b" stroke-width="1.4" opacity=".8"/>'
            f'<path d="M50 26 q-8 4 -9 20 v48 q0 12 10 18 h42 q10 -6 10 -18 v-48 q-1 -16 -9 -20z" fill="url(#{g})"/>'
            f'<path d="M50 26 h44 q4 3 2 6 h-48 q-2 -3 2 -6z" fill="#b89a6c"/>'
            f'<path d="M44 52 h56 M44 84 h56" stroke="rgba(80,55,30,.35)" stroke-width="1"/>'
            f'<ellipse cx="72" cy="27" rx="22" ry="4" fill="#3a2a18"/>'
            f'<path d="M112 98 q0 -12 20 -12 q20 0 20 12 q-20 8 -40 0z" fill="url(#{g}l)"/><ellipse cx="132" cy="97" rx="20" ry="3.4" fill="#4a3620"/>'
            f'<ellipse cx="132" cy="110" rx="22" ry="3" fill="rgba(0,0,0,.35)"/></svg>')

def codex_svg(k, w, h, leather, mini=False):
    """An early papyrus codex in a soft leather wrapper: a single gathering of papyrus leaves (fibres showing at the
    edge), the leather cover with its triangular flap folded over the fore-edge and a long thong wound round it."""
    W, H = w + 44, h + 16
    x0 = 26; y0 = 7
    g = f'c{k}'
    return (f'<svg class="obj" viewBox="0 0 {W} {H}" aria-hidden="true"><defs>'
            f'<linearGradient id="{g}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{leather}" stop-opacity=".75"/><stop offset=".45" stop-color="{leather}"/><stop offset="1" stop-color="#1a0f08"/></linearGradient>'
            f'<linearGradient id="{g}p" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e6cf98"/><stop offset="1" stop-color="#b8975c"/></linearGradient></defs>'
            f'<ellipse cx="{W/2}" cy="{H-4}" rx="{w/2+8}" ry="3.5" fill="rgba(0,0,0,.45)"/>'
            # page block seen at the head (papyrus)
            f'<rect x="{x0+3}" y="{y0-4}" width="{w-6}" height="6" rx="1" fill="url(#{g}p)"/>'
            + "".join(f'<path d="M{x0+4} {y0-3+i*1.2:.1f} H{x0+w-4}" stroke="rgba(120,90,45,.45)" stroke-width=".5"/>' for i in range(4)) +
            # cover
            f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" rx="3" fill="url(#{g})"/>'
            f'<path d="M{x0+4} {y0+3} h{w-8} v{h-6} h-{w-8}z" fill="none" stroke="rgba(0,0,0,.35)" stroke-width="1"/>'
            # the flap folded over the fore-edge (right), pointed, with the thong wound round the book
            f'<path d="M{x0+w} {y0+2} L{x0+w*.62} {y0+h*.5} L{x0+w} {y0+h-2}z" fill="{leather}" stroke="rgba(0,0,0,.45)" stroke-width=".8"/>'
            f'<path d="M{x0+w*.62} {y0+h*.5} H{x0-6}" stroke="#4b2c14" stroke-width="2"/>'
            f'<path d="M{x0-6} {y0+h*.5} q-6 4 -2 14 M{x0-6} {y0+h*.5} q-9 -1 -12 8" stroke="#4b2c14" stroke-width="1.5" fill="none" stroke-linecap="round"/>'
            f'<circle cx="{x0+w*.62}" cy="{y0+h*.5}" r="2" fill="#2a170a"/>'
            # stitching on the spine (left) from the single-quire binding
            + "".join(f'<path d="M{x0+2} {y0+h*f:.1f} h5" stroke="rgba(230,200,150,.45)" stroke-width="1"/>' for f in (.2, .4, .6, .8)) +
            '</svg>')

def tag(k):
    t, _, mark, lang, *_ = BOOKS[k]
    fam = ' style="font-family:\'IM Fell English\',serif"' if k == "judges" else ""
    return (f'<span class="tag"><span class="tmk" lang="{lang}"{"" if lang == "grc" else " dir=rtl"}>{mark}</span>'
            f'<span class="tnm"{fam}>{t}</span></span>')

def scroll_item(k):
    _, _, _, _, dark, mid, gilt, glow, gem = BOOKS[k]
    if k == "judges":   obj = scroll_svg(k, 118, 28, "#cdb185", tie="#6b3c18")                 # a small scroll (4QJudg)
    elif k == "mighty": obj = scroll_svg(k, 152, 42, "#bfa173", wrap="plain", tie="#4a2a12")    # a large scroll (4QSam-a)
    elif k == "psalter":obj = scroll_svg(k, 158, 32, "#d2b98d", wrap="blue", tie="#5a3418")     # long, slim (11QPs-a)
    elif k == "proverbs":obj = scroll_svg(k, 134, 32, "#c7a978", tie="#6e4120")
    elif k == "prophets":obj = jar_svg(k)                                                       # in a Qumran jar
    elif k == "matthew": obj = codex_svg(k, 66, 84, "#6b4a2a")                                   # papyrus codex, c. AD 200
    elif k == "rev":     obj = codex_svg(k, 70, 90, "#4b2318")                                   # papyrus codex, 3rd c.
    else:                obj = codex_svg(k, 46, 58, "#3e3a52", mini=True)                       # a miniature codex
    return (f'<button class="pick cub" type="button" data-tab="{k}" aria-label="{BOOKS[k][0]}" style="--glow:{glow}">'
            f'<span class="nest{" tall" if k == "prophets" else ""}">{obj}</span>{tag(k)}</button>')

SCRIBE = ('<span class="cub deco" aria-hidden="true"><span class="nest"><svg class="obj" viewBox="0 0 168 84">'
          '<ellipse cx="84" cy="80" rx="60" ry="3.5" fill="rgba(0,0,0,.4)"/>'
          '<path d="M40 52 h28 v22 q0 6 -14 6 q-14 0 -14 -6z" fill="#8a5a33"/><ellipse cx="54" cy="52" rx="14" ry="3.5" fill="#2a170a"/>'   # a clay inkwell
          '<path d="M60 22 L98 78" stroke="#c9b27a" stroke-width="3" stroke-linecap="round"/><path d="M60 22 l-2 -4" stroke="#2a170a" stroke-width="2"/>'  # a reed pen
          '<path d="M104 72 q12 -10 30 -4 l10 -10 q2 6 -2 10 l-10 6 q-14 6 -28 -2z" fill="#9a5a30"/>'  # a small oil lamp
          '<path d="M144 58 c-2 -4 1 -7 0 -12 c3 4 3 8 0 12z" fill="#ffcf7a"/><ellipse cx="144" cy="52" rx="6" ry="9" fill="rgba(255,200,110,.25)"/>'
          '</svg></span><span class="tag ghost">&nbsp;</span></span>')

def scrolls_html():
    h = ""
    for i, (plate, keys) in enumerate(SHELVES):
        cells = "".join(scroll_item(k) for k in keys)
        if len(keys) % 2: cells += SCRIBE
        h += f'<div class="rack"><div class="grid">{cells}</div><span class="plate">{plate}</span></div>'
    return h

SCROLL_CSS = r'''
.lib.scrolls { background:
    radial-gradient(90% 45% at 50% 0%, rgba(255, 205, 130, .22), transparent 65%),
    radial-gradient(60% 40% at 20% 90%, rgba(0, 0, 0, .35), transparent 70%),
    __NOISE__,
    linear-gradient(#5b4430, #3d2c1e); }
.scrolls h2, .scrolls .hint { color: #f3e2bf; }
.rack { width: 100%; max-width: 440px; margin: 0 auto 26px; padding: 8px; border-radius: 4px;
  background: linear-gradient(90deg, rgba(0,0,0,.25), transparent 12%, transparent 88%, rgba(0,0,0,.25)), __FIBRE__, linear-gradient(#8b4f2c, #6a3a1e);
  box-shadow: 0 14px 24px rgba(0, 0, 0, .55), inset 0 0 0 2px rgba(255, 210, 160, .12); }
.rack .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
.rack .plate { display: block; width: max-content; margin: 10px auto 2px; padding: 3px 12px; border-radius: 2px;
  font: 700 11px var(--ui); letter-spacing: .16em; text-transform: uppercase; color: #3a2410;
  background: linear-gradient(#ead9b0, #c9ad78); box-shadow: 0 1px 2px rgba(0, 0, 0, .5); }
.cub { position: relative; display: flex; flex-direction: column; align-items: stretch; padding: 0; margin: 0; border: 0; cursor: pointer;
  background: none; color: inherit; -webkit-tap-highlight-color: transparent; }
.cub .nest { position: relative; display: grid; place-items: center; height: 104px; padding: 6px 6px; border-radius: 3px;
  background: radial-gradient(90% 80% at 50% 20%, #3a2210, #1a0e06);
  box-shadow: inset 0 6px 12px rgba(0, 0, 0, .8), inset 0 -2px 0 rgba(255, 200, 150, .12); overflow: hidden; }
.cub .obj.jar { max-height: 96px; }
.cub .obj { width: auto; height: auto; max-width: 100%; max-height: 92px; transition: transform .45s cubic-bezier(.2, .8, .2, 1), filter .45s; }
.cub .tag { align-self: center; position: relative; margin-top: 7px; padding: 5px 10px 6px; min-width: 70%; text-align: center; border-radius: 2px;
  color: #3b2410; background: __FIBRE__, linear-gradient(#efe1bf, #d9c294); box-shadow: 0 2px 4px rgba(0, 0, 0, .45);
  clip-path: polygon(2% 0, 98% 3%, 100% 96%, 4% 100%, 0 40%); transform: rotate(-1.2deg); }
.cub:nth-child(even) .tag { transform: rotate(1deg); }
.cub .tag::before { content: ""; position: absolute; left: 50%; top: -9px; width: 1.5px; height: 10px; background: #6b4a2a; }
.cub .tag.ghost { visibility: hidden; }
.cub .tmk { display: block; font: 500 13px/1.1 Alegreya, Georgia, serif; color: #6b3f1c; }
.cub .tmk[lang="grc"] { font-size: 12px; }
.cub .tnm { display: block; font: 400 18px/1.15 Bellefair, Georgia, serif; letter-spacing: .03em; }
.cub.current .nest { box-shadow: inset 0 6px 12px rgba(0, 0, 0, .8), inset 0 0 0 2px var(--glow), 0 0 18px -4px var(--glow); }
.cub.current .obj { transform: translateY(-3px) scale(1.03); filter: drop-shadow(0 0 8px color-mix(in srgb, var(--glow) 60%, transparent)); }
.cub.pull .obj { transform: translateY(-6px) scale(1.14); filter: drop-shadow(0 0 14px var(--glow)); }
.cub:focus-visible { outline: 2px solid #f1d9a8; outline-offset: 3px; border-radius: 4px; }
.cub.deco { cursor: default; }
'''.replace("__NOISE__", NOISE).replace("__FIBRE__", FIBRE)

# ======================================================================================================================
COMMON_CSS = r'''
/* ---------- the Library: choosing a collection ---------- */
.tabs { flex-wrap: nowrap; justify-content: space-between; align-items: center; gap: 10px; padding: 8px max(14px, env(safe-area-inset-left, 0px)); }
.tabs .tab:not(.of-tab) { display: none; }   /* the old buttons stay in the page; the library presses them */
.lib-open { display: inline-flex; align-items: center; gap: 8px; min-height: 42px; padding: 6px 15px 6px 11px; border-radius: 999px;
  border: 1px solid var(--line); background: transparent; color: var(--fg); font: 500 15px var(--ui); cursor: pointer; flex: none; }
.lib-open svg { width: 22px; height: 22px; fill: var(--accent); }
.lib-open:focus-visible, .lib-close:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
.lib-now { flex: 1; min-width: 0; text-align: center; font-family: Bellefair, Georgia, serif; font-size: 20px; color: var(--accent);
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.lib { position: fixed; inset: 0; z-index: 60; display: none; flex-direction: column; align-items: center; overflow-y: auto;
  -webkit-overflow-scrolling: touch; color: #f3e6cf; padding: calc(16px + env(safe-area-inset-top)) 12px calc(28px + env(safe-area-inset-bottom)); }
.lib.on { display: flex; animation: lib-in .3s ease both; }
@keyframes lib-in { from { opacity: 0; } to { opacity: 1; } }
.lib h2 { font: 400 34px/1.1 Bellefair, Georgia, serif; letter-spacing: .05em; margin: 10px 0 2px; color: #f1d9a8; text-align: center; }
.lib .hint { font: 16px var(--ui); color: #cdb690; margin: 0 0 22px; text-align: center; }
.lib-close { position: absolute; top: calc(12px + env(safe-area-inset-top)); right: 12px; width: 44px; height: 44px; border-radius: 22px;
  border: 1px solid rgba(241, 217, 168, .35); background: rgba(0, 0, 0, .25); color: #f1d9a8; font-size: 20px; cursor: pointer; }
@media (prefers-reduced-motion: reduce) { .lib.on { animation: none; } .pick, .pick * { transition: none !important; } }
'''

JS = r'''
<script>
/* The Library: the top bar's "Library" button opens it; tapping a book or scroll lifts it and opens that collection
   by pressing its (hidden) tab button, so the existing tab code does the switching. */
(() => {
  const root = document.documentElement, lib = document.getElementById("library"), now = document.getElementById("lib-now");
  const NAMES = __NAMES__;
  const cur = () => ["rev", "judges", "mighty", "prayers", "matthew", "proverbs", "prophets"].find(k => root.classList.contains(k)) || "psalter";
  let back = null;
  function fitTitles() {   // shrink a spine's title until it fits its label, so nothing on a spine is ever cut off
    lib.querySelectorAll(".book .ttl").forEach(t => {
      const box = t.parentElement; let fs = 21; t.style.fontSize = fs + "px";
      while (fs > 12 && (t.scrollHeight > box.clientHeight - 10 || t.offsetHeight > box.clientHeight - 10)) { fs -= 0.5; t.style.fontSize = fs + "px"; }
    });
  }
  function mark() {
    const c = cur();
    lib.querySelectorAll(".pick").forEach(b => b.classList.toggle("current", b.dataset.tab === c));
    now.textContent = NAMES[c];
    now.style.fontFamily = c === "judges" ? "'IM Fell English', Georgia, serif" : "";
  }
  function open() {
    mark(); back = document.activeElement;
    lib.classList.add("on"); lib.setAttribute("aria-hidden", "false"); lib.scrollTop = 0;
    requestAnimationFrame(fitTitles); if (document.fonts) document.fonts.ready.then(fitTitles);
    setTimeout(() => { const b = lib.querySelector(".pick.current") || lib.querySelector(".pick"); try { b.focus({ preventScroll: true }); } catch (e) {} }, 60);
  }
  function close() {
    lib.classList.remove("on"); lib.setAttribute("aria-hidden", "true");
    try { (back || document.getElementById("lib-open")).focus({ preventScroll: true }); } catch (e) {}
  }
  document.getElementById("lib-open").addEventListener("click", open);
  document.getElementById("lib-close").addEventListener("click", close);
  document.addEventListener("keydown", e => { if (e.key === "Escape" && lib.classList.contains("on")) { e.stopPropagation(); close(); } }, true);
  addEventListener("resize", () => { if (lib.classList.contains("on")) fitTitles(); });
  function choose(b) {
    const t = document.getElementById("tab-" + b.dataset.tab); if (t) t.click();
    close(); mark();
    try { scrollTo(0, 0); } catch (e) {}
  }
  lib.querySelectorAll(".pick").forEach(b => b.addEventListener("click", () => {
    if (lib.classList.contains("busy")) return;
    lib.classList.add("busy");
    const done = () => { b.classList.remove("pull"); lib.classList.remove("busy"); };
    if (window.libFlight) { window.libFlight(b, () => choose(b), done); return; }   // the book-opening animation, when present
    b.classList.add("pull");
    const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
    setTimeout(() => { choose(b); done(); }, reduce ? 0 : 450);
  }));
  new MutationObserver(mark).observe(root, { attributes: true, attributeFilter: ["class"] });
  mark();
})();
</script>
'''

import json
NAMES = json.dumps({k: v[1] for k, v in BOOKS.items()}, ensure_ascii=False)
BOOKS_ICON = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 4h3v16H3zM7.5 4h3v16h-3zM12 6.2l2.9-.8 3.9 14.4-2.9.8z"/>'
              '<path d="M2 20.5h20v1.5H2z"/></svg>')
SCROLL_ICON = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 6.5a2.5 2.5 0 0 1 5 0V17h9.5a2.5 2.5 0 0 1-2.5 2.5H8A3 3 0 0 1 5 16.5z"/>'
               '<path d="M10 6.5h7.5a2.5 2.5 0 0 1 2.5 2.5v7h-1.5V9a1 1 0 0 0-1-1H10z"/></svg>')

body = luxe_html() if style == "luxe" else scrolls_html()
LIB_HTML = (f'\n<div class="lib {style}" id="library" role="dialog" aria-modal="true" aria-label="Library" aria-hidden="true">\n'
            f'  <button class="lib-close" id="lib-close" type="button" aria-label="Close the library">✕</button>\n'
            f'  <h2>The Library</h2>\n  <p class="hint">{"Choose a book" if style == "luxe" else "Choose a scroll or book"}</p>\n  {body}\n</div>\n')

once("family=Bellefair", "family=IM+Fell+English&family=Bellefair")
once('<nav class="tabs" role="tablist" aria-label="Collections">',
     '<nav class="tabs" role="tablist" aria-label="Collections">\n  <button class="lib-open" id="lib-open" type="button" aria-haspopup="dialog">'
     + (BOOKS_ICON if style == "luxe" else SCROLL_ICON) + 'Library</button>\n  <span class="lib-now" id="lib-now" aria-live="polite"></span>')
once("</style>", COMMON_CSS + (LUXE_CSS if style == "luxe" else SCROLL_CSS) + "</style>")
once('<div class="art-bg" aria-hidden="true">', LIB_HTML + '<div class="art-bg" aria-hidden="true">')
s = s.rstrip("\n") + "\n" + JS.replace("__NAMES__", NAMES)
open(out, "w", encoding="utf-8").write(s)
print("wrote", out, style)
