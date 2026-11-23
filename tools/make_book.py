"""The book test page: the luxurious library (make_library.py luxe) plus
  1. an opening animation: the chosen book is lifted off the shelf, turns to show its cover, opens, its pages riffle,
     and its title page grows to fill the screen before the collection appears (tap anywhere to skip);
  2. the Psalter redesigned as a book: a parchment page on the green leather of its cover, a title page with the
     painting set as a framed plate, a gilt player, a contents-page list with a ribbon bookmark.
Only the Psalter's page changes; the other collections keep their own pages.

usage: python3 make_book.py <index.html in> <out.html>
"""
import sys, subprocess, os

src, out = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
tmp = out + ".luxe.tmp"
subprocess.run([sys.executable, os.path.join(here, "make_library.py"), src, tmp, "luxe"], check=True)
s = open(tmp, encoding="utf-8").read(); os.remove(tmp)

def once(old, new):
    global s
    assert s.count(old) == 1, ("expected exactly one", old[:80], s.count(old))
    s = s.replace(old, new, 1)

NOISE = ("url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='140' height='140'%3E%3Cfilter id='n'%3E"
         "%3CfeTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='3' stitchTiles='stitch'/%3E%3CfeColorMatrix values='0 0 0 0 0  0 0 0 0 0  "
         "0 0 0 0 0  0 0 0 .9 0'/%3E%3C/filter%3E%3Crect width='140' height='140' filter='url(%23n)' opacity='.33'/%3E%3C/svg%3E\")")
FIBRE = ("url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='220' height='220'%3E%3Cfilter id='f'%3E"
         "%3CfeTurbulence type='fractalNoise' baseFrequency='.55' numOctaves='2' stitchTiles='stitch'/%3E%3CfeColorMatrix values='0 0 0 0 .35  0 0 0 0 .22  "
         "0 0 0 0 .08  0 0 0 .55 0'/%3E%3C/filter%3E%3Crect width='220' height='220' filter='url(%23f)' opacity='.16'/%3E%3C/svg%3E\")")
MOTTLE = ("url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='300' height='300'%3E%3Cfilter id='m'%3E"
          "%3CfeTurbulence type='fractalNoise' baseFrequency='.008' numOctaves='4' stitchTiles='stitch'/%3E%3CfeColorMatrix values='0 0 0 0 .45  0 0 0 0 .3  "
          "0 0 0 0 .1  0 0 0 .9 -.25'/%3E%3C/filter%3E%3Crect width='300' height='300' filter='url(%23m)' opacity='.35'/%3E%3C/svg%3E\")")
# a gilt rule with a lozenge in the middle, and a small fleuron
RULE = ("url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 180 12'%3E%3Cg fill='none' stroke='%23b8862f' stroke-width='1'%3E"
        "%3Cpath d='M2 6H74M106 6H178'/%3E%3Cpath d='M10 8.5H70M110 8.5H170' opacity='.55'/%3E%3C/g%3E%3Cg fill='%23b8862f'%3E%3Cpath d='M90 1l5 5-5 5-5-5z'/%3E"
        "%3Ccircle cx='79' cy='6' r='1.6'/%3E%3Ccircle cx='101' cy='6' r='1.6'/%3E%3C/g%3E%3C/svg%3E\")")
FLEURON = ("url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 60 20'%3E%3Cg fill='%23b8862f'%3E"
           "%3Cpath d='M30 2c3 4 3 8 0 16-3-8-3-12 0-16z'/%3E%3Cpath d='M28 10C22 4 12 4 6 10c6 2 14 3 22 0zM32 10c6-6 16-6 22 0-6 2-14 3-22 0z' opacity='.85'/%3E"
           "%3Ccircle cx='3' cy='10' r='1.6'/%3E%3Ccircle cx='57' cy='10' r='1.6'/%3E%3C/g%3E%3C/svg%3E\")")

# the Psalter tab is the page with none of the other collections' classes
P = "html:not(.rev,.judges,.mighty,.prayers,.matthew,.proverbs,.prophets)"
GOLD = "linear-gradient(180deg, #fff1bf, #e8c05e 30%, #9b6b1e 60%, #f0d27a 85%, #b38330)"
DARKVARS = ("--bg: #2b2115; --surface: #34291b; --fg: #eee1c4; --muted: #bba57e; --line: #57452b; --accent: #e3b65e; --accent-ink: #20160a;"
            " --page: #30251a; --page-2: #251c12; --rubric: #e08466; --ribbon: #a3262d; --edge-a: #3d3020; --edge-b: #1c140b; --ink-rule: rgba(227,182,94,.55); color-scheme: dark;")

BOOK_CSS = r'''
/* =================== the Psalter as a book =================== */
:root { --leather: #1f3729; --leather-d: #0e1a12; --leather-l: #2c4a37; --gild: #b8862f; --gild-l: #f0d58c; }
__P__ { --bg: #e9dbb6; --surface: #f1e5c5; --fg: #2b1f12; --muted: #6b583e; --line: #cfb88c; --accent: #84520f; --accent-ink: #fbf3df;
  --page: #efe2bf; --page-2: #e3d0a3; --rubric: #9b2b1d; --ribbon: #8d1d23; --edge-a: #f1e5c6; --edge-b: #c2a978; --ink-rule: rgba(155,104,30,.6); color-scheme: light; }
@media (prefers-color-scheme: dark) { __P__:not([data-theme="light"]) { __DARK__ } }
__P__[data-theme="dark"] { __DARK__ }

/* the green leather of the cover, all round the page */
__P__ body { background: radial-gradient(120% 50% at 50% 0%, rgba(120,170,130,.16), transparent 70%), __NOISE__, linear-gradient(var(--leather), var(--leather-d)) fixed;
  background-color: var(--leather-d); padding-left: max(9px, env(safe-area-inset-left, 0px)); padding-right: max(9px, env(safe-area-inset-right, 0px)); }
__P__ .art-bg { display: none; }

/* the top bar: a band of leather with a gilt edge */
__P__ .tabs { background: __NOISE__, linear-gradient(var(--leather-l), var(--leather) 55%, var(--leather-d)); border-bottom: 0;
  box-shadow: inset 0 -1px 0 #6b4a17, inset 0 -3px 0 var(--gild), inset 0 -4px 0 #4a3210, 0 4px 10px rgba(0,0,0,.45);
  margin-inline: calc(-1 * max(9px, env(safe-area-inset-left, 0px))); padding-bottom: 11px; }
__P__ .lib-open, __P__ .tabs .tab.of-tab { color: var(--gild-l); background: rgba(0,0,0,.2); border: 1px solid color-mix(in srgb, var(--gild) 75%, transparent); }
__P__ .lib-open svg { fill: var(--gild-l); }
__P__ .tabs .tab.of-tab svg { fill: var(--gild-l); }
__P__ .lib-now { background: __GOLD__; -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent;
  filter: drop-shadow(0 1px 0 rgba(0,0,0,.6)); letter-spacing: .06em; }

/* the page: parchment, a gilt double rule, the gutter's shadow on the left, the stacked page-edges on the right */
__P__ .wrap { position: relative; margin: 14px auto 30px; padding: 40px 26px 44px 30px; gap: 30px; border-radius: 2px 5px 5px 2px;
  background:
    linear-gradient(90deg, rgba(50,28,8,.30), rgba(50,28,8,.08) 4%, transparent 9%, transparent 95%, rgba(50,28,8,.12)),
    radial-gradient(140% 100% at 50% 45%, transparent 55%, rgba(110,70,25,.22)),
    radial-gradient(closest-side, rgba(150,100,40,.10), transparent) 0 0 / 520px 460px,
    radial-gradient(closest-side, rgba(150,100,40,.08), transparent) 230px 170px / 610px 540px,
    radial-gradient(closest-side, rgba(255,240,205,.08), transparent) 90px 300px / 380px 420px,
    __FIBRE__, var(--page);
  box-shadow: inset 0 0 0 1px rgba(110,75,30,.25),
    1px 1px 0 var(--edge-a), 2px 1px 0 var(--edge-b), 3px 2px 0 var(--edge-a), 4px 2px 0 var(--edge-b), 5px 3px 0 var(--edge-a), 6px 3px 0 var(--edge-b),
    7px 4px 0 #1a1007, 0 14px 34px rgba(0,0,0,.6); }
__P__ .wrap::before { content: ""; position: absolute; inset: 11px 10px 11px 13px; border: 3px double var(--ink-rule); pointer-events: none; border-radius: 1px; }
__P__ .wrap > * { position: relative; }

/* title page */
__P__ header, __P__ body.has-art header { align-items: center; text-align: center; gap: 2px; text-shadow: none; }
__P__ header::before { content: ""; width: 64px; height: 22px; margin-bottom: 6px; background: center / contain no-repeat __FLEURON__; }
__P__ .hebrew { font-size: clamp(66px, 19vw, 98px); line-height: 1.05; padding: 0 6px;
  background: __GOLD__; -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent;
  filter: drop-shadow(0 1px 0 rgba(90,55,10,.45)); }
__P__ h1 { font-size: 27px; letter-spacing: .2em; text-transform: uppercase; margin-top: 4px; color: var(--fg); }
__P__ h1::after { content: ""; display: block; width: 180px; height: 12px; margin: 10px auto 2px; background: center / contain no-repeat __RULE__; }
__P__ .sub, __P__ body.has-art .sub { font-family: var(--body); font-style: italic; font-size: 16px; letter-spacing: .01em; color: var(--muted); }
.artplate { display: none; }
__P__ body.has-art .artplate { display: block; position: relative; width: 100%; aspect-ratio: 4 / 3; margin-top: 18px; padding: 7px; border-radius: 2px;
  background: linear-gradient(135deg, #f7e6a6, #b5862f 28%, #f2d47c 50%, #8c6220 74%, #e4c26c);
  box-shadow: 0 4px 10px rgba(50,28,6,.4), inset 0 0 0 1px rgba(80,52,12,.7), inset 0 0 0 3px rgba(255,240,190,.35); }
.artplate .pin { position: absolute; inset: 7px; overflow: hidden; background: #2a2014; box-shadow: 0 0 0 1px #4a3210; }
.artplate img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; object-position: center 60%; opacity: 0; transition: opacity 1.2s ease; }
.artplate img.on { opacity: 1; }
.artplate .pin::after { content: ""; position: absolute; inset: 0; box-shadow: inset 0 0 18px rgba(0,0,0,.45); pointer-events: none; }

/* the player: a gilt band, a gold medallion */
__P__ .player, __P__ body.has-art .player { background: linear-gradient(color-mix(in srgb, var(--page-2) 75%, transparent), color-mix(in srgb, var(--page-2) 25%, transparent));
  -webkit-backdrop-filter: none; backdrop-filter: none; border: 0; border-radius: 0; padding: 20px 6px 18px;
  border-top: 3px double var(--ink-rule); border-bottom: 3px double var(--ink-rule); }
__P__ .now-label { color: var(--rubric); font-weight: 700; }
__P__ .now-title { font-size: 28px; }
__P__ .play { width: 68px; height: 68px; color: #2a1a0a;
  background: radial-gradient(circle at 35% 28%, #fff6cf, #ecc76a 28%, #b88830 60%, #77511a);
  box-shadow: 0 0 0 2px #6b4a17, 0 0 0 4px #e3c06a, 0 0 0 5px #5a3d12, 0 5px 12px rgba(50,28,5,.45); }
__P__ .play svg { filter: drop-shadow(0 1px 0 rgba(255,240,190,.6)); }
__P__ .icon-btn { border: 1.5px solid var(--gild); color: var(--fg); background: radial-gradient(circle, transparent 62%, color-mix(in srgb, var(--gild) 18%, transparent));
  box-shadow: inset 0 0 0 3px transparent, inset 0 0 0 4px color-mix(in srgb, var(--gild) 35%, transparent); }
__P__ .mode { border-color: var(--gild); }
__P__ .mode button[aria-pressed="true"] { background: linear-gradient(var(--leather-l), var(--leather-d)); color: var(--gild-l); }
__P__ .fsbtn, __P__ .clipbtn { border: 1px solid var(--gild); color: var(--accent); background: color-mix(in srgb, var(--page) 60%, transparent); }
__P__ .seek input { accent-color: var(--gild); }

/* contents: red numerals, dotted leaders, a silk ribbon on the psalm you're on */
__P__ .wrap > section[aria-label="Psalms"], __P__ body.has-art .wrap > section[aria-label="Psalms"],
__P__ .suggest, __P__ body.has-art .suggest, __P__ footer, __P__ body.has-art footer {
  background: none; -webkit-backdrop-filter: none; backdrop-filter: none; border: 0; border-radius: 0; padding: 0; }
__P__ .list-head { flex-direction: column; align-items: center; gap: 2px; border-bottom: 0; padding-bottom: 6px; text-transform: none; letter-spacing: .02em; }
__P__ .list-head > span:first-child { font-family: var(--display); font-size: 30px; letter-spacing: .16em; text-transform: uppercase; color: var(--rubric); }
__P__ .list-head > span:first-child::before { content: "The "; }
__P__ #total { font-family: var(--body); font-style: italic; font-size: 15px; color: var(--muted); }
__P__ .list-head::after { content: ""; width: 180px; height: 12px; margin-top: 8px; background: center / contain no-repeat __RULE__; }
__P__ #list > li { position: relative; }
__P__ .track { grid-template-columns: 42px 1fr auto; gap: 10px; align-items: start; padding: 13px 2px 12px;
  border-bottom: 1px solid color-mix(in srgb, var(--line) 75%, transparent); }
__P__ .track:hover { background: color-mix(in srgb, var(--page-2) 55%, transparent); }
__P__ .num b { color: var(--rubric); font-size: 28px; }
__P__ .num span { color: var(--accent); }
__P__ .t-line { display: flex; align-items: baseline; gap: 6px; font-size: 18px; line-height: 1.35; }
__P__ .t-line::after { content: ""; flex: 1 0 14px; height: 0; border-bottom: 2px dotted color-mix(in srgb, var(--muted) 50%, transparent); }
__P__ .t-mood { font-family: var(--body); font-style: normal; letter-spacing: .01em; font-size: 15px; }
__P__ .dur { margin-top: 4px; color: var(--fg); font-family: var(--body); font-size: 16px; }
__P__ .track.current .num b { color: var(--rubric); }
__P__ .track.current .t-line { color: var(--accent); font-weight: 500; }
__P__ .track.current::before { content: ""; position: absolute; left: -27px; top: -10px; width: 13px; height: calc(100% + 18px); z-index: 1;
  background: linear-gradient(90deg, color-mix(in srgb, var(--ribbon) 55%, #000), var(--ribbon) 35%, color-mix(in srgb, var(--ribbon) 72%, #fff) 52%, var(--ribbon) 68%, color-mix(in srgb, var(--ribbon) 55%, #000));
  clip-path: polygon(0 0, 100% 0, 100% 100%, 50% 84%, 0 100%); filter: drop-shadow(1px 2px 1px rgba(0,0,0,.35)); }

/* suggestions: written on the page */
__P__ .suggest h2 { color: var(--rubric); text-align: center; letter-spacing: .06em; }
__P__ .suggest h2::after { content: ""; display: block; width: 180px; height: 12px; margin: 8px auto 0; background: center / contain no-repeat __RULE__; }
__P__ .s-form, __P__ body.has-art .s-form { background: transparent; border: 0; padding: 4px 0 0; }
__P__ .s-form input, __P__ .s-form textarea { background: transparent; border: 0; border-bottom: 1.5px solid color-mix(in srgb, var(--muted) 60%, transparent); border-radius: 0; padding: 6px 2px; }
__P__ .s-form textarea { line-height: 30px; padding-top: 0;
  background: repeating-linear-gradient(transparent 0 29px, color-mix(in srgb, var(--muted) 38%, transparent) 29px 30px); }
__P__ .send { background: linear-gradient(var(--leather-l), var(--leather-d)); color: var(--gild-l); border: 1px solid var(--gild); }
__P__ .send.alt { background: transparent; color: var(--accent); }

/* colophon */
__P__ footer { align-items: center; text-align: center; font-family: var(--body); font-style: italic; font-size: 14px; }
__P__ footer::before { content: ""; width: 60px; height: 20px; margin-bottom: 4px; background: center / contain no-repeat __FLEURON__; }

/* the bar at the bottom while playing: leather and gold */
__P__ .mini { --fg: #f2e4c0; --muted: #c8b48c; --accent: #e8c064; --accent-ink: #22170a;
  background: __NOISE__, linear-gradient(var(--leather-l), var(--leather) 55%, var(--leather-d)); border: 1px solid var(--gild);
  box-shadow: inset 0 0 0 3px rgba(0,0,0,.2), inset 0 0 0 4px color-mix(in srgb, var(--gild) 40%, transparent), 0 10px 30px rgba(0,0,0,.45); }
__P__ .mini-play { background: radial-gradient(circle at 35% 28%, #fff6cf, #ecc76a 28%, #b88830 60%, #77511a); color: #2a1a0a; box-shadow: 0 0 0 2px #5a3d12; }


/* ---------- finishing: one button style, equal widths, a centred player, a gilt seek bar ---------- */
/* every button is a small gilt frame: a gold edge with a fine hairline just inside it */
__P__ .fsbtn, __P__ .clipbtn, __P__ .mode, __P__ .send, __P__ .lib-open, __P__ .tabs .tab.of-tab {
  border-radius: 5px; border: 1px solid var(--gild); outline: 1px solid color-mix(in srgb, var(--gild) 38%, transparent); outline-offset: -5px;
  box-shadow: 0 1px 0 rgba(255,240,200,.08) inset, 0 2px 4px rgba(30,16,4,.18); }
__P__ .lib-open, __P__ .tabs .tab.of-tab { outline-offset: -4px; min-height: 42px; }
__P__ .player, __P__ body.has-art .player { background: none; padding: 26px 4px 22px; }
__P__ .now { flex-direction: column; text-align: center; gap: 14px; }
__P__ .now-text { align-items: center; gap: 3px; }
__P__ .now-label { font-family: var(--ui); font-size: 12px; letter-spacing: .2em; }
__P__ .now-title { font-size: 30px; letter-spacing: .02em; }
__P__ .now-line { font-size: 18px; }
__P__ .play { width: 78px; height: 78px; }
__P__ .play svg { width: 30px; height: 30px; }
__P__ .seek { gap: 12px; font-size: 14px; letter-spacing: .02em; }
__P__ .seek input { -webkit-appearance: none; appearance: none; background: transparent; height: 34px; --p: 0%; cursor: pointer; }
__P__ .seek input::-webkit-slider-runnable-track { height: 4px; border-radius: 2px;
  background: linear-gradient(90deg, #8c6220, var(--gild) calc(var(--p) - 1px), color-mix(in srgb, var(--fg) 16%, transparent) var(--p));
  box-shadow: inset 0 1px 1px rgba(0,0,0,.25); }
__P__ .seek input::-webkit-slider-thumb { -webkit-appearance: none; width: 20px; height: 20px; margin-top: -8px; border-radius: 50%; border: 0;
  background: radial-gradient(circle at 35% 30%, #fff6cf, #ecc76a 32%, #b88830 65%, #77511a);
  box-shadow: 0 0 0 1.5px #5a3d12, 0 2px 4px rgba(30,16,4,.45); }
__P__ .seek input::-moz-range-track { height: 4px; border-radius: 2px; background: color-mix(in srgb, var(--fg) 16%, transparent); }
__P__ .seek input::-moz-range-progress { height: 4px; border-radius: 2px; background: var(--gild); }
__P__ .seek input::-moz-range-thumb { width: 20px; height: 20px; border: 0; border-radius: 50%;
  background: radial-gradient(circle at 35% 30%, #fff6cf, #ecc76a 32%, #b88830 65%, #77511a); box-shadow: 0 0 0 1.5px #5a3d12; }
__P__ .controls { flex-direction: column; align-items: stretch; gap: 16px; }
__P__ .skip { justify-content: center; gap: 14px; }
__P__ .icon-btn { width: 50px; height: 50px; border: 1px solid var(--gild); outline: 1px solid color-mix(in srgb, var(--gild) 38%, transparent); outline-offset: -5px;
  background: none; box-shadow: 0 2px 4px rgba(30,16,4,.15); }
__P__ .icon-btn svg { width: 22px; height: 22px; }
__P__ .mode { display: flex; width: 100%; padding: 5px; gap: 4px; background: none; }
__P__ .mode button { flex: 1; min-height: 44px; border-radius: 2px; font-family: var(--ui); font-size: 16px; font-weight: 500; letter-spacing: .03em; color: var(--muted); }
__P__ .mode button[aria-pressed="true"] { box-shadow: inset 0 0 0 1px color-mix(in srgb, var(--gild) 55%, transparent), 0 1px 3px rgba(0,0,0,.3); }
__P__ .fsbtn, __P__ .clipbtn { align-self: stretch; width: 100%; justify-content: center; min-height: 54px; padding: 12px 18px;
  font-size: 17px; font-weight: 500; letter-spacing: .03em; color: var(--accent); background: none; }
__P__ .fsbtn svg, __P__ .clipbtn svg { width: 19px; height: 19px; }
__P__ .player .status { text-align: center; }
__P__ .now-title, __P__ .now-line, __P__ .t-line { text-wrap: pretty; }
/* suggestions: the two buttons side by side, the same width */
__P__ .s-row:not([hidden]) { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
__P__ .send { min-height: 54px; padding: 12px 10px; border-radius: 5px; text-align: center; display: grid; place-items: center; font-size: 16px; letter-spacing: .02em; }
__P__ .send:only-child { grid-column: 1 / -1; }
__P__ .s-form label { font-family: var(--body); font-size: 16px; font-weight: 500; }
/* the contents: numbers centred in their column, a little more air between entries */
__P__ .num { align-items: center; }
__P__ .track { padding: 15px 2px 14px; }
__P__ .t-mood { margin-top: 2px; }

/* ---------- the full-screen view as an illustrated page: the painting set as a framed plate, the words printed below ---------- */
__P__ .fs { color: var(--fg); background:
    linear-gradient(90deg, rgba(50,28,8,.26), transparent 7%, transparent 94%, rgba(50,28,8,.12)),
    radial-gradient(140% 100% at 50% 45%, transparent 55%, rgba(110,70,25,.24)),
    radial-gradient(closest-side, rgba(150,100,40,.10), transparent) 0 0 / 520px 460px,
    radial-gradient(closest-side, rgba(150,100,40,.08), transparent) 230px 170px / 610px 540px,
    __FIBRE__, var(--page); }
__P__ .fs::before { content: ""; position: absolute; pointer-events: none; border: 3px double var(--ink-rule);
  inset: calc(9px + env(safe-area-inset-top)) 9px calc(9px + env(safe-area-inset-bottom)) 9px; }
__P__ .fs-top { order: 0; justify-content: center; padding: calc(22px + env(safe-area-inset-top)) 70px 4px; min-height: 64px; }
__P__ .fs-x { position: absolute; left: 20px; top: calc(16px + env(safe-area-inset-top)); width: 42px; height: 42px; color: var(--accent);
  background: none; border: 1px solid var(--gild); outline: 1px solid color-mix(in srgb, var(--gild) 38%, transparent); outline-offset: -5px; }
__P__ .fs-x svg { width: 16px; height: 16px; }
__P__ .fs-head { align-items: center; text-align: center; }
__P__ .fs-label { display: none; }
__P__ .fs-title { font-family: var(--display); font-size: 13px; letter-spacing: .16em; white-space: nowrap; text-transform: uppercase; color: var(--muted); }
__P__ .fs-title::before { content: "The Psalter  ·  "; white-space: pre; }
__P__ .fs-title::after { content: ""; display: block; width: 150px; height: 10px; margin: 7px auto 0; background: center / contain no-repeat __RULE__; }
/* the plate */
__P__ .fs-bg { order: 1; position: relative; inset: auto; flex: none; align-self: center; margin-top: 10px;
  width: min(calc(100% - 48px), calc(42dvh * 4 / 3), 620px); aspect-ratio: 4 / 3; overflow: hidden; border: 7px solid transparent; border-radius: 2px;
  background: linear-gradient(#2a2014, #2a2014) padding-box, linear-gradient(135deg, #f7e6a6, #b5862f 28%, #f2d47c 50%, #8c6220 74%, #e4c26c) border-box;
  box-shadow: 0 5px 14px rgba(50,28,6,.4), 0 0 0 1px rgba(80,52,12,.6); }
__P__ .fs-bg:not(.art) { display: none; }
__P__ .fs-bg.art::after { background: none; box-shadow: inset 0 0 0 1px #4a3210, inset 0 0 20px rgba(0,0,0,.45); }
__P__ .fs-cap { order: 2; flex: none; text-align: center; margin-top: 10px; font-family: var(--ui); font-size: 13px; font-weight: 700; letter-spacing: .2em;
  text-transform: uppercase; color: var(--rubric); min-height: 1.3em; }
/* the words, printed on the page */
__P__ .fs-words { order: 3; padding: 8px max(30px, 8vw) 12px; }
__P__ .fs-ref { display: none; }
__P__ .fs-line { font-family: var(--body); font-size: clamp(25px, 6.6vw, 42px); line-height: 1.34; color: var(--fg); text-shadow: none; max-width: 21ch;
  filter: blur(1.5px); transition: opacity .6s ease, filter .9s ease; }
__P__ .fs-line.on { filter: none; }
__P__ .fs-line.vs::first-letter { color: var(--rubric); font-family: var(--display); font-size: 1.25em; }
/* the controls, in gold */
__P__ .fs-bottom { order: 4; padding: 0 28px calc(26px + env(safe-area-inset-bottom)); gap: 8px; }
__P__ .fs-seek { color: var(--muted); opacity: 1; }
__P__ .fs-seek input { -webkit-appearance: none; appearance: none; background: transparent; height: 34px; --p: 0%; }
__P__ .fs-seek input::-webkit-slider-runnable-track { height: 4px; border-radius: 2px;
  background: linear-gradient(90deg, #8c6220, var(--gild) calc(var(--p) - 1px), color-mix(in srgb, var(--fg) 16%, transparent) var(--p)); box-shadow: inset 0 1px 1px rgba(0,0,0,.25); }
__P__ .fs-seek input::-webkit-slider-thumb { -webkit-appearance: none; width: 20px; height: 20px; margin-top: -8px; border-radius: 50%; border: 0;
  background: radial-gradient(circle at 35% 30%, #fff6cf, #ecc76a 32%, #b88830 65%, #77511a); box-shadow: 0 0 0 1.5px #5a3d12, 0 2px 4px rgba(30,16,4,.45); }
__P__ .fs-seek input::-moz-range-track { height: 4px; border-radius: 2px; background: color-mix(in srgb, var(--fg) 16%, transparent); }
__P__ .fs-seek input::-moz-range-progress { height: 4px; border-radius: 2px; background: var(--gild); }
__P__ .fs-seek input::-moz-range-thumb { width: 20px; height: 20px; border: 0; border-radius: 50%; background: radial-gradient(circle at 35% 30%, #fff6cf, #ecc76a 32%, #b88830 65%, #77511a); }
__P__ .fs-ctl { justify-content: center; gap: 12px; }
__P__ .fs-ctl button { width: 50px; height: 50px; color: var(--fg); border: 1px solid var(--gild); outline: 1px solid color-mix(in srgb, var(--gild) 38%, transparent); outline-offset: -5px; }
__P__ .fs-ctl svg { width: 22px; height: 22px; }
__P__ .fs-ctl .jump svg { width: 26px; height: 26px; }
__P__ .fs-ctl .fs-play { width: 74px; height: 74px; margin: 0 4px; border: 0; outline: 0; color: #2a1a0a;
  background: radial-gradient(circle at 35% 28%, #fff6cf, #ecc76a 28%, #b88830 60%, #77511a);
  box-shadow: 0 0 0 2px #6b4a17, 0 0 0 4px #e3c06a, 0 0 0 5px #5a3d12, 0 5px 12px rgba(50,28,5,.45); }
__P__ .fs-ctl .fs-play svg { width: 30px; height: 30px; }
@media (max-height: 700px) { __P__ .fs-bg { width: min(calc(100% - 48px), calc(36dvh * 4 / 3)); } __P__ .fs-line { font-size: clamp(22px, 5.8vw, 36px); } }
@media (prefers-reduced-motion: reduce) { __P__ .fs-line { filter: none; transition: opacity .3s; } }
@media (max-width: 380px) { __P__ .wrap { padding-left: 26px; padding-right: 20px; } __P__ .track.current::before { left: -23px; } }
'''
for k, v in {"__P__": P, "__DARK__": DARKVARS, "__NOISE__": NOISE, "__FIBRE__": FIBRE, "__MOTTLE__": MOTTLE, "__RULE__": RULE,
             "__FLEURON__": FLEURON, "__GOLD__": GOLD}.items():
    BOOK_CSS = BOOK_CSS.replace(k, v)

# ======================================================================================================================
# Every other book gets the same treatment, in its own leather. Each book is its own page (shown in a frame); its test
# copy is written next to it as <dir>/book-test.html, and this test page's frames load those copies.
# ======================================================================================================================
def mix(hexa, hexb, f):   # f of a, (1-f) of b
    a = [int(hexa[k:k+2], 16) for k in (1, 3, 5)]; b = [int(hexb[k:k+2], 16) for k in (1, 3, 5)]
    return "#" + "".join(f"{round(x * f + y * (1 - f)):02x}" for x, y in zip(a, b))
OTHERS = {   # tab key: (folder, book name, leather dark, leather, ribbon)
    "rev":      ("revelation", "Revelation",         "#1d0907", "#5e2016", "#a3262d"),
    "judges":   ("judges",     "Judges by the Fire", "#2a1608", "#5a3212", "#b4541c"),
    "mighty":   ("mighty",     "The Mighty Men",     "#121212", "#36302a", "#8d1d23"),
    "prayers":  ("prayers",    "Prayers",            "#10152a", "#2e3a68", "#3b4f9e"),
    "matthew":  ("matthew",    "Matthew",            "#141b0e", "#43542c", "#5d7f2f"),
    "proverbs": ("proverbs",   "Proverbs",           "#0c1c1a", "#21524b", "#1f7c70"),
    "prophets": ("prophets",   "The Prophets",       "#220d14", "#5a2333", "#8a2d55"),
}
def leather_vars(dark, mid, ribbon=None):
    v = f"--leather: {mid}; --leather-d: {dark}; --leather-l: {mix(mid, '#ffffff', .86)};"
    return v + (f" --ribbon: {ribbon};" if ribbon else "")

# the top bar and the playing bar, in the open book's leather
H = "html:is(.rev,.judges,.mighty,.prayers,.matthew,.proverbs,.prophets)"
TOP_ALL_CSS = "\n/* =================== the top bar and the playing bar in every book's own leather =================== */\n"
TOP_ALL_CSS += "".join(f"html.{k} {{ {leather_vars(v[2], v[3])} }}\n" for k, v in OTHERS.items())
TOP_ALL_CSS += r"""
__H__ .tabs { background: __NOISE__, linear-gradient(var(--leather-l), var(--leather) 55%, var(--leather-d)); border-bottom: 0;
  box-shadow: inset 0 -1px 0 #6b4a17, inset 0 -3px 0 var(--gild), inset 0 -4px 0 #4a3210, 0 4px 10px rgba(0,0,0,.45); padding-bottom: 11px; }
__H__ .lib-open, __H__ .tabs .tab.of-tab { color: var(--gild-l); background: rgba(0,0,0,.2); border: 1px solid var(--gild); border-radius: 5px; min-height: 42px;
  outline: 1px solid color-mix(in srgb, var(--gild) 38%, transparent); outline-offset: -4px; }
__H__ .lib-open svg, __H__ .tabs .tab.of-tab svg { fill: var(--gild-l); }
__H__ .lib-now { background: __GOLD__; -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent;
  filter: drop-shadow(0 1px 0 rgba(0,0,0,.6)); letter-spacing: .06em; }
__H__ .mini.rbar { --fg: #f2e4c0; --muted: #c8b48c; --accent: #e8c064; --accent-ink: #22170a;
  background: __NOISE__, linear-gradient(var(--leather-l), var(--leather) 55%, var(--leather-d)); border: 1px solid var(--gild);
  box-shadow: inset 0 0 0 3px rgba(0,0,0,.2), inset 0 0 0 4px color-mix(in srgb, var(--gild) 40%, transparent), 0 10px 30px rgba(0,0,0,.45); }
__H__ .mini.rbar .mini-play { background: radial-gradient(circle at 35% 28%, #fff6cf, #ecc76a 28%, #b88830 60%, #77511a); color: #2a1a0a; box-shadow: 0 0 0 2px #5a3d12; }
""".replace("__H__", H).replace("__NOISE__", NOISE).replace("__GOLD__", GOLD)
# the playing bar from another book, shown over the Psalter, wears the leather of the book it's from
TOP_ALL_CSS += "".join(f'.mini.rbar[data-from="{k}"] {{ {leather_vars(v[2], v[3])} }}\n' for k, v in OTHERS.items())
TOP_ALL_CSS += '.mini.rbar[data-from="psalter"] { --leather: #1f3729; --leather-d: #0e1a12; --leather-l: #2c4a37; }\n'

FLIGHT_CSS = r'''
/* =================== opening a book =================== */
.flight { position: fixed; inset: 0; z-index: 70; perspective: 1500px; overflow: hidden; cursor: pointer; -webkit-tap-highlight-color: transparent; }
.fl-dim { position: absolute; inset: 0; background: radial-gradient(70% 60% at 50% 50%, rgba(30,18,8,.55), rgba(8,4,2,.9)); opacity: 0; }
.fl-stage { position: absolute; left: 50%; top: 50%; width: 0; height: 0; transform-style: preserve-3d; }
.fl-book { position: absolute; transform-style: preserve-3d; }
.fl-face, .fl-cover, .fl-leaf { position: absolute; -webkit-backface-visibility: hidden; backface-visibility: hidden; }
.fl-cover, .fl-leaf { transform-style: preserve-3d; -webkit-backface-visibility: visible; backface-visibility: visible; transform-origin: 0 50%; }
.fl-leather { background: radial-gradient(70% 40% at 35% 25%, rgba(255,255,255,.08), transparent 70%), __NOISE__, linear-gradient(160deg, var(--mid), var(--dark) 80%); }
.fl-cover .out { inset: 0; border-radius: 2px 6px 6px 2px; box-shadow: inset 6px 0 10px rgba(0,0,0,.45), inset -2px 0 3px rgba(255,255,255,.08); }
.fl-cover .out::before { content: ""; position: absolute; inset: 9%; border: 1px solid var(--gilt); box-shadow: 0 0 0 3px rgba(0,0,0,.2), 0 0 0 4px color-mix(in srgb, var(--gilt) 55%, transparent),
  inset 0 0 0 3px rgba(0,0,0,.2), inset 0 0 0 4px color-mix(in srgb, var(--gilt) 55%, transparent); }
.fl-cover .cn { position: absolute; width: 17%; aspect-ratio: 1; background: linear-gradient(135deg, #fff1bf, #d6aa4c 35%, #7a5519 70%, #e9c66a);
  clip-path: polygon(0 0, 100% 0, 100% 22%, 22% 22%, 22% 100%, 0 100%); filter: drop-shadow(0 1px 1px rgba(0,0,0,.6)); }
.fl-cover .cn.tl { left: 3%; top: 2.5%; } .fl-cover .cn.tr { right: 3%; top: 2.5%; transform: scaleX(-1); }
.fl-cover .cn.bl { left: 3%; bottom: 2.5%; transform: scaleY(-1); } .fl-cover .cn.br { right: 3%; bottom: 2.5%; transform: scale(-1); }
.fl-cover .clasp { position: absolute; right: -3%; top: 44%; width: 15%; height: 12%; border-radius: 3px 0 0 3px;
  background: linear-gradient(#f5dc8c, #b5862f 45%, #6b4a17); box-shadow: 0 1px 3px rgba(0,0,0,.6); }
.fl-cover .ct { position: absolute; left: 12%; right: 12%; top: 15%; text-align: center; font: 400 1.15em/1.1 Bellefair, Georgia, serif; letter-spacing: .12em;
  text-transform: uppercase; background: __GOLD__; -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent; filter: drop-shadow(0 1px 0 rgba(0,0,0,.7)); }
.fl-cover .cmk { position: absolute; left: 0; right: 0; bottom: 15%; text-align: center; font: 500 1.05em/1 Alegreya, Georgia, serif;
  background: __GOLD__; -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent; filter: drop-shadow(0 1px 0 rgba(0,0,0,.7)); }
.fl-cover .cmed { position: absolute; left: 50%; top: 50%; width: 44%; aspect-ratio: 1; transform: translate(-50%, -50%); border-radius: 50%; display: grid; place-items: center; color: var(--gilt);
  box-shadow: inset 0 0 0 2px var(--gilt), inset 0 0 0 6px rgba(0,0,0,.25), inset 0 0 0 7px color-mix(in srgb, var(--gilt) 55%, transparent), 0 0 18px -6px var(--glow); }
.fl-cover .cmed svg { width: 56%; height: 56%; fill: none; stroke: currentColor; stroke-width: 1.4; stroke-linecap: round; stroke-linejoin: round; filter: drop-shadow(0 1px 0 rgba(0,0,0,.7)); }
.fl-cover .cmed .gem { position: absolute; top: -6%; left: 50%; width: 13%; aspect-ratio: 1; margin-left: -6.5%; border-radius: 50%;
  background: radial-gradient(circle at 35% 30%, #fff 0 8%, color-mix(in srgb, var(--gem) 55%, #fff) 16%, var(--gem) 55%, color-mix(in srgb, var(--gem) 50%, #000));
  box-shadow: 0 0 0 2px #d9ac4f, 0 0 0 3px #6b4a17; }
.fl-cover .in, .fl-paper { background: radial-gradient(130% 100% at 50% 50%, transparent 60%, rgba(110,70,25,.25)), __FIBRE__, #efe2bf; }
.fl-cover .in { inset: 0; transform: rotateY(180deg); border-radius: 6px 2px 2px 6px;
  background: radial-gradient(circle at 30% 30%, rgba(255,255,255,.08) 0 2px, transparent 3px) 0 0 / 14px 14px, linear-gradient(160deg, color-mix(in srgb, var(--mid) 70%, #b9a072), color-mix(in srgb, var(--dark) 80%, #5a4630)); }
.fl-leaf { left: 0; top: 1.5%; width: 98.5%; height: 97%; }
.fl-leaf .lf { inset: 0; padding: 12% 11% 12% 13%; }
.fl-leaf .lf.b { transform: rotateY(180deg); padding: 12% 13% 12% 11%; }
/* the page's text lines and its illuminated initial are painted onto the page itself (no separate layers), so in Safari they
   turn with the page instead of floating flat above it */
.fl-leaf .lf.g { background:
    radial-gradient(circle, var(--gilt) 0 .28em, transparent .3em) left 1.35em top 1.75em / 1.8em 1.8em no-repeat,
    linear-gradient(135deg, var(--mid), var(--dark)) left 1.45em top 1.85em / 1.6em 1.6em no-repeat,
    linear-gradient(var(--gilt), var(--gilt)) left 1.35em top 1.75em / 1.8em 1.8em no-repeat,
    repeating-linear-gradient(transparent 0 .42em, rgba(70,45,20,.32) .42em .5em, transparent .5em .68em) left 1.3em top 1.85em / calc(100% - 2.5em) calc(100% - 3.6em) no-repeat,
    linear-gradient(90deg, rgba(40,22,6,.28), transparent 18%), radial-gradient(130% 100% at 50% 50%, transparent 60%, rgba(110,70,25,.25)), __FIBRE__, #efe2bf; }
.fl-leaf .lf.b.g { background:
    radial-gradient(circle, var(--gilt) 0 .28em, transparent .3em) right 1.35em top 1.75em / 1.8em 1.8em no-repeat,
    linear-gradient(135deg, var(--mid), var(--dark)) right 1.45em top 1.85em / 1.6em 1.6em no-repeat,
    linear-gradient(var(--gilt), var(--gilt)) right 1.35em top 1.75em / 1.8em 1.8em no-repeat,
    repeating-linear-gradient(transparent 0 .42em, rgba(70,45,20,.32) .42em .5em, transparent .5em .68em) right 1.3em top 1.85em / calc(100% - 2.5em) calc(100% - 3.6em) no-repeat,
    linear-gradient(270deg, rgba(40,22,6,.28), transparent 18%), radial-gradient(130% 100% at 50% 50%, transparent 60%, rgba(110,70,25,.25)), __FIBRE__, #efe2bf; }
.fl-title { left: 0; top: 1.5%; width: 98.5%; height: 97%; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: .3em; color: #2b1f12; text-align: center;
  background: linear-gradient(90deg, rgba(40,22,6,.3), transparent 12%), radial-gradient(130% 100% at 50% 50%, transparent 60%, rgba(110,70,25,.25)), __FIBRE__, #efe2bf; }
.fl-title::before { content: ""; position: absolute; inset: 5% 5% 5% 7%; border: 2px double rgba(155,104,30,.6); }
.fl-title .tm { font: 400 2.3em/1 Bellefair, Georgia, serif; background: __GOLD__; -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent;
  filter: drop-shadow(0 1px 0 rgba(90,55,10,.4)); padding: 0 .2em; }
.fl-title .tm[lang="grc"] { font-size: 1.35em; }
.fl-title .tt { font: 400 .95em/1.15 Bellefair, Georgia, serif; letter-spacing: .18em; text-transform: uppercase; }
.fl-title .tr { width: 70%; height: .6em; background: center / contain no-repeat __RULE__; }
.fl-title svg { width: 1.6em; height: 1.6em; fill: none; stroke: #9b6b1e; stroke-width: 1.4; stroke-linecap: round; stroke-linejoin: round; }
.fl-back { inset: 0; border-radius: 6px 2px 2px 6px; }
.fl-edge { background: repeating-linear-gradient(90deg, #f6e3a2 0 1px, #b8892f 1px 2px, #e8c76c 2px 3px); box-shadow: inset 0 0 4px rgba(60,35,5,.6); }
.fl-edge.h { background: repeating-linear-gradient(0deg, #f6e3a2 0 1px, #b8892f 1px 2px, #e8c76c 2px 3px); }
.fl-spine.book { position: absolute; flex: none; min-width: 0; margin: 0; transition: none; border-radius: 3px; box-shadow: none; }
.flight .fl-skip { position: absolute; left: 0; right: 0; bottom: calc(22px + env(safe-area-inset-bottom)); text-align: center; font: 14px var(--ui); color: rgba(241,217,168,.7); opacity: 0; letter-spacing: .04em; }
'''
for k, v in {"__NOISE__": NOISE, "__FIBRE__": FIBRE, "__GOLD__": GOLD, "__RULE__": RULE}.items():
    FLIGHT_CSS = FLIGHT_CSS.replace(k, v)

FLIGHT_JS = r'''
<script>
/* Opening a book: the chosen spine is lifted off the shelf and turns to show its cover; the cover opens, the pages
   riffle, and the title page grows until it fills the screen, then the collection fades in. Tap anywhere to skip. */
(() => {
  const N_LEAVES = 6;
  window.libFlight = async (b, choose, done, from) => {
    if (matchMedia("(prefers-reduced-motion: reduce)").matches || !Element.prototype.animate) { choose(); done(); return; }
    const r = from || b.getBoundingClientRect(), vw = innerWidth, vh = innerHeight;
    const W = Math.round(Math.min(vw * 0.44, 260, (vh * 0.5) / 1.42)), H = Math.round(W * 1.42);
    const T = Math.round(Math.max(16, Math.min(W * 0.36, H * r.width / r.height)));
    const vars = ["--dark", "--mid", "--gilt", "--glow", "--gem"].map(v => v + ":" + b.style.getPropertyValue(v)).join(";");
    const title = b.getAttribute("aria-label"), mk = b.querySelector(".mk"), em = b.querySelector("svg.em");
    const lang = mk.getAttribute("lang"), dir = lang === "grc" ? "" : ' dir="rtl"';
    const leaf = i => `<div class="fl-leaf" style="transform:translateZ(${T / 2 - 1.5 - i * 0.7}px)"><div class="fl-face fl-paper lf g"></div><div class="fl-face fl-paper lf b g"></div></div>`;
    const fl = document.createElement("div");
    fl.className = "flight"; fl.setAttribute("aria-hidden", "true");
    fl.innerHTML = `<div class="fl-dim"></div><div class="fl-stage"><div class="fl-book" style="${vars};left:${-W / 2}px;top:${-H / 2}px;width:${W}px;height:${H}px;font-size:${W / 10}px">
        <div class="fl-face fl-leather fl-back" style="transform:rotateY(180deg) translateZ(${T / 2}px)"></div>
        <div class="fl-face fl-edge" style="left:${(W - T) / 2 + 2}px;top:4px;width:${T - 4}px;height:${H - 8}px;transform:rotateY(90deg) translateZ(${W / 2 - 3}px)"></div>
        <div class="fl-face fl-edge h" style="left:2px;top:${(H - T) / 2 + 2}px;width:${W - 5}px;height:${T - 4}px;transform:rotateX(90deg) translateZ(${H / 2 - 4}px)"></div>
        <div class="fl-face fl-edge h" style="left:2px;top:${(H - T) / 2 + 2}px;width:${W - 5}px;height:${T - 4}px;transform:rotateX(-90deg) translateZ(${H / 2 - 4}px)"></div>
        <div class="fl-face fl-title" style="transform:translateZ(${T / 2 - 1.5 - N_LEAVES * 0.7}px)"><span class="tr"></span><span class="tm" lang="${lang}"${dir}></span><span class="tt"></span>${em.outerHTML}<span class="tr"></span></div>
        ${Array.from({ length: N_LEAVES }, (_, i) => leaf(i)).join("")}
        <div class="fl-cover" style="left:0;top:0;width:${W}px;height:${H}px;transform:translateZ(${T / 2}px)">
          <div class="fl-face fl-leather out"><i class="cn tl"></i><i class="cn tr"></i><i class="cn bl"></i><i class="cn br"></i><i class="clasp"></i>
            <span class="ct"></span><span class="cmed"><i class="gem"></i>${em.outerHTML}</span><span class="cmk" lang="${lang}"${dir}></span></div>
          <div class="fl-face in"></div>
        </div>
      </div></div><p class="fl-skip">Tap to skip</p>`;
    fl.querySelector(".fl-title .tm").textContent = mk.textContent;
    fl.querySelector(".fl-title .tt").textContent = title;
    fl.querySelector(".fl-cover .ct").textContent = title;
    fl.querySelector(".fl-cover .cmk").textContent = mk.textContent;
    if (b.dataset.tab === "judges") fl.querySelectorAll(".ct,.tt").forEach(e => e.style.fontFamily = "'IM Fell English', Georgia, serif");
    // the spine itself, as the book's left side
    const sp = b.cloneNode(true); sp.className = "book fl-face fl-spine"; sp.removeAttribute("data-tab"); sp.removeAttribute("aria-label");
    sp.setAttribute("tabindex", "-1"); sp.style.cssText = b.style.cssText + `;left:${(W - T) / 2}px;top:0;width:${T}px;height:${H}px;transform:rotateY(-90deg) translateZ(${W / 2}px)`;
    const fit = H / r.height; sp.style.fontSize = "";   // keep the spine's lettering the size it was on the shelf
    sp.querySelectorAll(".ttl").forEach(t => t.style.fontSize = (parseFloat(b.querySelector(".ttl").style.fontSize || 21) * fit) + "px");
    fl.querySelector(".fl-book").appendChild(sp);
    document.body.appendChild(fl);

    const stage = fl.querySelector(".fl-stage"), book = fl.querySelector(".fl-book"), cover = fl.querySelector(".fl-cover"),
          leaves = [...fl.querySelectorAll(".fl-leaf")], dim = fl.querySelector(".fl-dim"), skipT = fl.querySelector(".fl-skip");
    let skipping = false; const running = new Set();
    const go = (el, frames, ms, opt = {}) => {
      const a = el.animate(frames, { duration: skipping ? 1 : ms, easing: opt.easing || "cubic-bezier(.45,.05,.25,1)", delay: skipping ? 0 : (opt.delay || 0), fill: "both" });
      running.add(a); return a.finished.then(() => running.delete(a), () => running.delete(a));
    };
    fl.addEventListener("click", () => { skipping = true; running.forEach(a => { try { a.finish(); } catch (e) {} }); });

    b.style.visibility = "hidden";
    const s0 = r.height / H, x0 = r.left + r.width / 2 - vw / 2, y0 = r.top + r.height / 2 - vh / 2;
    // 1. lifted off the shelf, turning to show the cover
    go(dim, [{ opacity: 0 }, { opacity: 1 }], 500);
    go(skipT, [{ opacity: 0 }, { opacity: 1 }], 400, { delay: 700 });
    go(stage, [{ transform: `translate(${x0}px, ${y0}px) scale(${s0})` }, { transform: `translate(${x0 * 0.35}px, ${y0 * 0.25 - 60}px) scale(${(s0 + 1) / 2})`, offset: 0.45 },
               { transform: "translate(0px, 0px) scale(1)" }], 720);
    await go(book, [{ transform: "rotateY(90deg)" }, { transform: "rotateY(90deg) rotateX(4deg)", offset: 0.25 }, { transform: "rotateY(35deg) rotateX(8deg) rotateZ(-2deg)", offset: 0.62 },
                    { transform: "rotateY(0deg) rotateX(0deg) rotateZ(0deg)" }], 720);
    // 2. the cover opens; the book slides so the open spread is centred
    go(stage, [{ transform: "translate(0px, 0px) scale(1)" }, { transform: `translate(${W / 2}px, 0px) scale(1)` }], 520, { delay: 40 });
    go(cover, [{ transform: `translateZ(${T / 2}px) rotateY(0deg)` }, { transform: `translateZ(${T / 2}px) rotateY(-180deg) translateZ(1px)` }], 500,
             { easing: "cubic-bezier(.5,0,.3,1)" });
    // 3. the pages riffle
    await Promise.all(leaves.map((lf, i) => go(lf, [
      { transform: `translateZ(${T / 2 - 1.5 - i * 0.7}px) rotateY(0deg)` },
      { transform: `translateZ(${T / 2 - 1.5 - i * 0.7}px) rotateY(-180deg) translateZ(${-(2 + i * 1.4)}px)` }],
      360, { delay: 340 + i * 65, easing: "cubic-bezier(.4,.1,.35,1)" })));
    // 4. the title page fills the screen, and the collection takes its place
    const Z = Math.max(vw / (W * 0.985), vh / (H * 0.97)) * 1.04;
    go(skipT, [{ opacity: 1 }, { opacity: 0 }], 200);
    await go(stage, [{ transform: `translate(${W / 2}px, 0px) scale(1)` }, { transform: `translate(${-W * 0.0075 * Z}px, 0px) scale(${Z})` }], 560,
             { easing: "cubic-bezier(.55,0,.25,1)" });
    choose();
    b.style.visibility = "";
    await go(fl, [{ opacity: 1 }, { opacity: 0 }], 350, { easing: "ease" });
    fl.remove(); done();
  };
})();

/* The seek bar's gilt fill: the page moves the bar itself, so follow its value. */
(() => {
  const sk = document.getElementById("seek"); if (!sk) return;
  const upd = () => sk.style.setProperty("--p", (+sk.value || 0) + "%");
  sk.addEventListener("input", upd); setInterval(upd, 250); upd();
})();


/* The full-screen view as an illustrated page: a caption under the painting ("Psalm 23 · Verse 4"), a red capital at the
   start of each new verse, and the gilt fill on its seek bar. The view itself (made by miniplayer.js) is unchanged. */
(() => {
  const start = () => {
    const fs = document.querySelector(".fs"); if (!fs) return setTimeout(start, 300);
    const bg = fs.querySelector(".fs-bg"), ref = fs.querySelector(".fs-ref"), title = fs.querySelector(".fs-title"),
          lines = [...fs.querySelectorAll(".fs-line")], seek = fs.querySelector(".fs-seek input");
    const cap = document.createElement("div"); cap.className = "fs-cap"; bg.after(cap);
    let lastRef = null, lastOn = null;
    const tidy = () => {
      const r = (ref.textContent || "").trim(), v = r ? r.charAt(0) + r.slice(1).toLowerCase() : "";
      const c = (title.textContent || "") + (v ? "  ·  " + v : ""); if (cap.textContent !== c) cap.textContent = c;
      const on = lines.find(l => l.classList.contains("on"));
      if (on && (on !== lastOn || on.dataset.t !== on.textContent)) {   // a new line has just been printed
        on.classList.toggle("vs", (r !== lastRef || !r) && /^[\s"“‘'(]*[A-Z]/.test(on.textContent)); on.dataset.t = on.textContent; lastOn = on; lastRef = r;
      }
      if (seek) seek.style.setProperty("--p", (+seek.value || 0) + "%");
    };
    new MutationObserver(tidy).observe(fs, { subtree: true, childList: true, characterData: true, attributes: true, attributeFilter: ["class"] });
    setInterval(tidy, 250); tidy();
  };
  start();
})();

/* The Psalter's painting, set as a framed plate on its title page: it follows the page's own painting (and its scenes). */
(() => {
  const bg = document.querySelector(".art-bg"), plate = document.getElementById("plate");
  if (!bg || !plate) return;
  const src = [...bg.querySelectorAll("img")], dst = [...plate.querySelectorAll("img")];
  const sync = () => src.forEach((im, i) => {
    const u = im.getAttribute("src"); if (u && dst[i].getAttribute("src") !== u) dst[i].setAttribute("src", u);
    dst[i].className = im.className;
  });
  new MutationObserver(sync).observe(bg, { subtree: true, attributes: true, attributeFilter: ["src", "class"] });
  sync();
})();
</script>
'''


KEEP_CSS = r"""
/* =================== keep playing across books =================== */
/* while another book is open, the Psalter's own page is put away (it sits under the other book anyway) */
html:is(.rev,.judges,.mighty,.prayers,.matthew,.proverbs,.prophets) .wrap { display: none; }
.mini.rbar .mini-text { cursor: pointer; }
.mini.rbar .mini-book { color: var(--accent); }
html.fs-child .mini.rbar { display: none !important; }
"""

KEEP_JS = r"""
<script>
/* Keep playing across books. Starting a reading in one book and then opening another no longer pauses it: it plays on,
   and a bar at the bottom of the screen keeps its controls (play/pause, previous/next, 15-second jumps, the seek bar,
   full screen) and says which book it's from. Pressing play in the book you've opened stops the other one, and the bar
   becomes that book's own. Tapping the bar's title flies you back to the book it's playing from.
   Every book is its own page with its own player; this works through each page's own controls, so their playing logic
   is untouched. */
(() => {
  const T = window.__tabs; if (!T) return;
  window.keepPlaying = true;
  const lib = document.getElementById("library");
  const NAME = k => { const b = lib && lib.querySelector(`.pick[data-tab="${k}"]`); return b ? b.getAttribute("aria-label") : k; };
  const docOf = k => {
    if (k === "psalter") return document;
    try { const f = T.fr(k); return f && f.getAttribute("src") && f.contentDocument && f.contentDocument.getElementById("play") ? f.contentDocument : null; } catch (e) { return null; }
  };
  const label = d => ((d && d.getElementById("now-label")) || {}).textContent || "";
  const isOn = d => /playing|loading/i.test(label(d));
  const isActive = d => !!d && (/playing|loading|paused/i.test(label(d)) || (((d.getElementById("play-icon") || {}).innerHTML || "").includes("h4.5")));
  function pauseBook(k) {
    if (k === "psalter") { try { if (typeof playing !== "undefined" && (playing || loading)) pause(); } catch (e) {} return; }
    try { const w = T.fr(k).contentWindow; if (w && typeof w.pause === "function") w.pause(); } catch (e) {}
  }
  const secs = t => { const m = String(t || "").trim().split(":").map(Number); return m.length === 2 ? m[0] * 60 + m[1] : m.length === 3 ? m[0] * 3600 + m[1] * 60 + m[2] : NaN; };

  // the bar: a copy of this page's own bar, wired to whichever book is playing
  let rbar = null, rseek = null, dragging = false;
  function build() {
    const native = document.querySelector("body > .mini:not(.rbar)"); if (!native) return false;
    rbar = native.cloneNode(true); rbar.classList.add("rbar"); rbar.classList.remove("on"); rbar.hidden = true;
    rbar.setAttribute("aria-label", "Now playing in another book");
    rbar.querySelector(".mini-text").title = "Go back to this book";
    document.body.appendChild(rbar);
    rseek = rbar.querySelector(".mini-seek");
    const od = () => docOf(owner), ev = (d, n) => new d.defaultView.Event(n, { bubbles: true });
    rbar.querySelector(".mini-play").addEventListener("click", () => { const d = od(); d && d.getElementById("play").click(); });
    rbar.querySelectorAll("[data-go]").forEach(b => b.addEventListener("click", () => { const d = od(), t = d && d.getElementById(b.dataset.go); if (t) t.click(); }));
    rbar.querySelectorAll("[data-jump]").forEach(b => b.addEventListener("click", () => {
      const d = od(); if (!d) return; const sk = d.getElementById("seek"), dur = secs((d.getElementById("t-dur") || {}).textContent);
      if (!(dur > 0)) return;
      const to = Math.max(0, Math.min(dur - 0.5, sk.value / 100 * dur + 15 * +b.dataset.jump));
      sk.value = (to / dur * 100).toFixed(3); sk.dispatchEvent(ev(d, "input")); sk.dispatchEvent(ev(d, "change"));
    }));
    rseek.addEventListener("input", () => { dragging = true; rseek.style.setProperty("--p", rseek.value + "%");
      const d = od(); if (d) { const sk = d.getElementById("seek"); sk.value = rseek.value; sk.dispatchEvent(ev(d, "input")); } });
    rseek.addEventListener("change", () => { const d = od(); if (d) { const sk = d.getElementById("seek"); sk.value = rseek.value; sk.dispatchEvent(ev(d, "change")); } dragging = false; });
    rbar.querySelector(".mini-fs").addEventListener("click", () => {
      const k = owner, d = od(); if (!d) return;
      goTo(k, false);   // open the playing book, then its own full-screen view
      setTimeout(() => { const b = k === "psalter" ? document.querySelector("body > .mini:not(.rbar) .mini-fs") : d.querySelector(".mini-fs"); if (b) b.click(); }, 60);
    });
    rbar.querySelector(".mini-text").addEventListener("click", () => {
      const k = owner; if (!k) return;
      const spine = lib && lib.querySelector(`.pick[data-tab="${k}"]`), t = rbar.querySelector(".mini-title").getBoundingClientRect();
      const from = { left: t.left + 8, top: t.top - 70, width: 34, height: 120 };
      if (spine && window.libFlight && !matchMedia("(prefers-reduced-motion: reduce)").matches) window.libFlight(spine, () => goTo(k, true), () => {}, from);
      else goTo(k, true);
    });
    return true;
  }
  function goTo(k, toPlayer) {   // open book k (by pressing its tab), and show its player
    const b = document.getElementById(T.TABS[k].btn); if (b) b.click();
    if (!toPlayer) return;
    requestAnimationFrame(() => { const d = docOf(k), p = d && d.querySelector(".player");
      try { if (p) p.scrollIntoView({ block: "start" }); if (k === "psalter") scrollBy(0, -80); } catch (e) {} });
  }

  // a style sheet in each book's page: hides that page's own bar when it isn't the one to show, and leaves room for ours
  function setStyle(d, css) {
    let st = d.getElementById("kp-style");
    if (!st) { st = d.createElement("style"); st.id = "kp-style"; (d.head || d.documentElement).appendChild(st); }
    if (st.textContent !== css) st.textContent = css;
  }

  let owner = null; const was = {};
  function tick() {
    if (!rbar && !build()) return;
    const cur = T.cur;
    // who is playing: whichever book most recently started; starting one stops the others
    for (const k of T.ORDER) {
      const d = docOf(k), on = isOn(d);
      if (d && !d.__kp) { d.__kp = true; d.addEventListener("play", () => setTimeout(tick, 0), true); }
      if (on && (!was[k] || !owner) && owner !== k) {
        owner = k;
        for (const j of T.ORDER) if (j !== k && isOn(docOf(j))) pauseBook(j);
      }
      was[k] = on;
    }
    // a book you've left must not keep its full-screen view open behind the one you're in
    for (const k of T.ORDER) {
      if (k === cur || k === "psalter") continue;
      const d = docOf(k), x = d && d.querySelector(".fs.on .fs-x"); if (x) x.click();
    }
    if (cur === "psalter" || !(docOf(cur) && docOf(cur).querySelector(".fs.on"))) document.documentElement.classList.remove("fs-child");
    const od = owner && docOf(owner), showR = !!od && owner !== cur && isActive(od) && !document.documentElement.classList.contains("fs-child");
    if (rbar.hidden !== !showR) { rbar.hidden = !showR; rbar.classList.toggle("on", showR); } if (owner && rbar.dataset.from !== owner) rbar.dataset.from = owner;
    const pad = showR ? `body { padding-bottom: ${rbar.offsetHeight + 24}px !important; }` : "";
    for (const k of T.ORDER) {
      const d = docOf(k); if (!d) continue;
      const hideOwn = k !== cur || (owner && owner !== k);
      const sel = k === "psalter" ? "body > .mini:not(.rbar)" : ".mini";
      setStyle(d, (hideOwn ? `${sel} { display: none !important; }` : "") + (k === cur ? pad : ""));
    }
    if (!showR) return;
    const pi = od.getElementById("play-icon"), mi = rbar.querySelector(".mini-play svg");
    if (pi && mi.innerHTML !== pi.innerHTML) mi.innerHTML = pi.innerHTML;
    const tt = (od.getElementById("now-title") || {}).textContent || "";
    const ti = rbar.querySelector(".mini-title"); if (ti.textContent !== tt) ti.textContent = tt;
    const lab = label(od), state = /loading/i.test(lab) ? "Loading" : /paused/i.test(lab) || !/playing/i.test(lab) ? "Paused" : "";
    const nm = od.querySelector(".mini.on .mini-meta"), verse = nm ? ((nm.textContent.match(/Verse [^·]+/) || [""])[0]).trim() : "";
    const time = ((od.getElementById("t-cur") || {}).textContent || "0:00") + " / " + ((od.getElementById("t-dur") || {}).textContent || "");
    const meta = (state ? `<b>${state}</b> · ` : "") + `<span class="mini-book">${NAME(owner)}</span>` + (verse ? " · " + verse : "") + " · " + time;
    const mm = rbar.querySelector(".mini-meta"); if (mm.innerHTML !== meta) mm.innerHTML = meta;
    const sk = od.getElementById("seek"); if (sk && !dragging) { rseek.value = sk.value; rseek.style.setProperty("--p", rseek.value + "%"); }
  }
  setInterval(tick, 200);
  document.addEventListener("play", () => setTimeout(tick, 0), true);
  tick();
})();
</script>
"""



# ---- paper for the full-screen page ----
TOOTH = ("url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='260' height='260'%3E%3Cfilter id='t' x='0' y='0' width='100%25' height='100%25'%3E"
         "%3CfeTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='3' stitchTiles='stitch' result='n'/%3E"
         "%3CfeDiffuseLighting in='n' lighting-color='%23fff' surfaceScale='.9' result='l'%3E%3CfeDistantLight azimuth='135' elevation='58'/%3E%3C/feDiffuseLighting%3E"
         "%3CfeComponentTransfer%3E%3CfeFuncR type='linear' slope='.4' intercept='.64'/%3E%3CfeFuncG type='linear' slope='.4' intercept='.64'/%3E%3CfeFuncB type='linear' slope='.4' intercept='.64'/%3E%3C/feComponentTransfer%3E"
         "%3C/filter%3E%3Crect width='260' height='260' filter='url(%23t)'/%3E%3C/svg%3E\")")
FIBRES = ("url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='420' height='420'%3E%3Cfilter id='f'%3E"   # the paper's cloudy formation
          "%3CfeTurbulence type='fractalNoise' baseFrequency='.016' numOctaves='4' seed='11' stitchTiles='stitch'/%3E"
          "%3CfeColorMatrix values='0 0 0 0 .45  0 0 0 0 .32  0 0 0 0 .16  0 0 0 1.5 -.62'/%3E%3C/filter%3E%3Crect width='420' height='420' filter='url(%23f)' opacity='.3'/%3E%3C/svg%3E\")")
FLECKS = ("url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='330' height='330'%3E%3Cfilter id='k'%3E"
          "%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='1' seed='3' stitchTiles='stitch'/%3E"
          "%3CfeColorMatrix values='0 0 0 0 .3  0 0 0 0 .2  0 0 0 0 .1  0 0 0 8 -6.1'/%3E%3C/filter%3E%3Crect width='330' height='330' filter='url(%23k)' opacity='.35'/%3E%3C/svg%3E\")")
PAPER = ("radial-gradient(circle at 61px 143px, rgba(150,95,30,.18) 0 2.5px, rgba(150,95,30,.06) 4.5px, transparent 6px) 0 0 / 370px 530px,"   # foxing: a few age spots
         " radial-gradient(circle at 203px 37px, rgba(140,90,30,.15) 0 1.5px, transparent 3.5px) 0 0 / 430px 610px,"
         " radial-gradient(ellipse 8px 6px at 29px 388px, rgba(150,95,30,.11), transparent) 0 0 / 310px 470px,"
         " radial-gradient(140% 100% at 50% 45%, transparent 48%, rgba(110,68,22,.30)),"                                    # aged edges
         " radial-gradient(closest-side, rgba(150,100,40,.13), transparent) 0 0 / 430px 380px,"                             # mottling
         " radial-gradient(closest-side, rgba(150,100,40,.10), transparent) 190px 140px / 520px 470px,"
         " radial-gradient(closest-side, rgba(255,246,222,.12), transparent) 80px 260px / 330px 360px,"
         f" {FLECKS}, {FIBRES}, {TOOTH}, var(--page)")
PAPER_BLEND = "normal, normal, normal, normal, normal, normal, normal, normal, normal, multiply, normal"

BOOKPAGE_CSS = r"""
/* =================== the full-screen view as a page of the book, turning with the scenes =================== */
__P__ .fs { background: radial-gradient(120% 50% at 50% 0%, rgba(120,170,130,.16), transparent 70%), __NOISE__, linear-gradient(var(--leather), var(--leather-d)); }
__P__ .fs::before { display: none; }
__P__ .fs .fs-head, __P__ .fs .fs-bg, __P__ .fs .fs-cap, __P__ .fs .fs-words { display: none !important; }
__P__ .fs-top { order: 0; min-height: 0; justify-content: flex-start; padding: calc(8px + env(safe-area-inset-top)) 14px 8px; }
__P__ .fs-x { position: static; width: 40px; height: 40px; color: var(--gild-l); border-color: color-mix(in srgb, var(--gild) 80%, transparent); }
__P__ .fs-bottom { --fg: #f2e4c0; --muted: #c8b48c; color: var(--fg); padding-top: 10px; }
__P__ .fs-bottom .fs-ctl button { color: var(--fg); }
.bk { order: 2; position: relative; flex: 1 1 auto; min-height: 0; margin: 0 10px 20px 8px; }
/* the open book: leather boards with a tooled gold line, the facing page curving down into the spine, the page block */
.bk-boards { position: absolute; inset: 0; border-radius: 4px 10px 10px 4px;
  background: radial-gradient(120% 70% at 30% 20%, rgba(255,255,255,.08), transparent 60%), __NOISE__, linear-gradient(165deg, var(--leather-l), var(--leather) 45%, var(--leather-d));
  box-shadow: 0 18px 36px rgba(0,0,0,.6), 0 2px 4px rgba(0,0,0,.4), inset 0 1px 0 rgba(255,255,255,.1), inset 0 0 0 1px rgba(0,0,0,.45); }
.bk-boards::after { content: ""; position: absolute; inset: 4px; border-radius: 3px 8px 8px 3px; border: 1px solid color-mix(in srgb, var(--gild) 75%, transparent);
  box-shadow: inset 0 0 0 2px rgba(0,0,0,.25), inset 0 0 0 3px color-mix(in srgb, var(--gild) 35%, transparent); }
.bk-left { position: absolute; top: 10px; bottom: 12px; left: 9px; width: 25px; border-radius: 3px 0 0 3px;
  background: linear-gradient(90deg, rgba(255,250,235,.10), rgba(60,34,10,.12) 45%, rgba(40,20,5,.55) 92%, rgba(20,10,2,.75)), __FIBRE__, var(--page-2);
  box-shadow: -1px 1px 0 var(--edge-a), -2px 1px 0 var(--edge-b), -3px 2px 0 var(--edge-a), -4px 2px 0 var(--edge-b), -5px 3px 0 #1a1007; }
.bk-ribbon { position: absolute; left: 50px; bottom: -14px; width: 12px; height: 34px;
  background: linear-gradient(90deg, color-mix(in srgb, var(--ribbon) 55%, #000), var(--ribbon) 35%, color-mix(in srgb, var(--ribbon) 72%, #fff) 52%, var(--ribbon) 68%, color-mix(in srgb, var(--ribbon) 55%, #000));
  clip-path: polygon(0 0, 100% 0, 100% 100%, 50% 80%, 0 100%); filter: drop-shadow(1px 2px 1px rgba(0,0,0,.4)); }
/* the page is always paper: in dark mode, the same parchment a little warmer and dimmer, as if read by lamplight */
@media (prefers-color-scheme: dark) { html:not([data-theme="light"]) .bk { __LAMPPAPER__ } }
html[data-theme="dark"] .bk { __LAMPPAPER__ }
.bk-stack { position: absolute; top: 8px; right: 11px; bottom: 12px; left: 34px; border-radius: 0 4px 4px 0;
  box-shadow: 1px 1px 0 var(--edge-a), 2px 1px 0 var(--edge-b), 3px 2px 0 var(--edge-a), 4px 2px 0 var(--edge-b), 5px 3px 0 var(--edge-a), 6px 3px 0 var(--edge-b),
    7px 4px 0 #1a1007, -2px 0 6px rgba(0,0,0,.35); }
.bk-pages { position: absolute; inset: 0; }
.bk-pg { z-index: 1; }
.bk-pg.top { z-index: 3; }
.bk-flap { position: absolute; left: 0; top: 0; width: 100%; height: 100%; z-index: 5; transform-origin: 0 0; pointer-events: none; filter: brightness(.95); }
.bk-flap .ghost { position: absolute; inset: 0; opacity: .12; }
.bk-cast { position: absolute; inset: 0; overflow: hidden; pointer-events: none; z-index: 2; }
.bk-cast.on-top { z-index: 4; }
.bk-flap .bk-cast { z-index: 1; overflow: visible; }
.bk-bar { position: absolute; left: 0; top: 0; transform-origin: 0 0; pointer-events: none; }
.bk-stack { contain: layout paint style; }
/* the humming bars on the playing row moved by height, which re-lays out the whole page every frame; scale them instead,
   and rest them while the book is open over them */
.track.current.playing .hum i { height: 13px; transform-origin: 50% 100%; animation-name: humS; will-change: transform; }
@keyframes humS { 0%,100% { transform: scaleY(.31) } 50% { transform: scaleY(1) } }
html:has(.fs.on) .track.current.playing .hum i { animation-play-state: paused; }
.bk-clip { position: absolute; left: 0; top: 0; overflow: hidden; transform-origin: 0 0; pointer-events: none; will-change: transform; }
.bk-clip.front { z-index: 3; }
.bk-clip.flap { z-index: 5; }
.bk-clip > .bk-face, .bk-bar { will-change: transform; }
.bk-clip .bk-cast.on-top { position: absolute; }
.bk-face { position: absolute; inset: 0; overflow: hidden; border-radius: 0 4px 4px 0;
  background: linear-gradient(90deg, rgba(50,28,8,.32), rgba(50,28,8,.09) 4%, transparent 10%, transparent 95%, rgba(50,28,8,.12)), __PAPER__;
  background-blend-mode: normal, __PAPERBLEND__; }
.bk-back { transform: rotateY(180deg);
  background: linear-gradient(270deg, rgba(50,28,8,.32), rgba(50,28,8,.09) 4%, transparent 10%), __PAPER__;
  background-blend-mode: normal, __PAPERBLEND__; filter: brightness(.93); }
.bk-in { position: absolute; inset: 0; display: flex; flex-direction: column; padding: 14px 18px 10px 24px; color: var(--fg); }
.bk-rh { flex: none; display: flex; justify-content: space-between; gap: 12px; white-space: nowrap; font: 400 11px/1 var(--display); letter-spacing: .2em; text-transform: uppercase; color: var(--muted);
  padding: 2px 2px 7px; border-bottom: 1px solid var(--ink-rule); }
.bk-rh span:last-child { overflow: hidden; text-overflow: ellipsis; }
.bk-hd { flex: none; text-align: center; margin: 12px 0 2px; }
.bk-hd .he { display: block; font: 400 22px/1 Alegreya, Georgia, serif; color: var(--gild); }
.bk-hd .kick { display: block; font: 700 11px/1.3 var(--ui); letter-spacing: .14em; text-transform: uppercase; color: var(--rubric); padding: 0 10px; }
.bk-hd .ti { display: block; margin-top: 4px; font: 400 24px/1.1 var(--display); letter-spacing: .16em; text-transform: uppercase; color: var(--fg); }
.bk-hd .sup { display: block; margin-top: 4px; font: italic 15px/1.35 var(--body); color: var(--muted); transition: color .6s; }
.bk-hd .sup.now { color: var(--fg); }
.bk-pl { flex: none; margin: 12px 4px 0; }
.bk-pl .im { display: block; width: 100%; aspect-ratio: 4 / 3; background: #2a2014 center 60% / cover no-repeat; border: 1px solid #2b1f12; outline: 1px solid var(--ink-rule); outline-offset: 3px; }
.bk-pl .cap { display: block; margin-top: 8px; text-align: center; font: italic 13.5px/1.3 var(--body); color: var(--muted); }
.bk-tx { flex: 1 1 auto; min-height: 0; overflow: hidden; margin-top: 12px; font: 400 clamp(16.5px, 4.5vw, 22px)/1.5 Alegreya, Georgia, serif; text-align: justify;
  -webkit-hyphens: auto; hyphens: auto; color: color-mix(in srgb, var(--fg) 52%, transparent); }
.bk-tx .bk-v { display: inline; text-align: inherit; transition: color .6s ease; }
.bk-tx .bk-v.now { color: var(--fg); }
.bk-tx .bk-n { display: inline; font: 700 .58em/1 var(--ui); color: var(--rubric); margin: 0 .22em 0 .1em; vertical-align: .55em; }
.bk-tx .bk-dc { float: left; font: 400 3.05em/.82 var(--display); color: var(--rubric); margin: .06em .1em 0 0; }
.bk-fo { flex: none; text-align: center; font: 400 13px/1 var(--display); letter-spacing: .1em; color: var(--muted); padding-top: 6px; }
.bk-measure { visibility: hidden; pointer-events: none; }
@media (max-height: 700px) { .bk-pl { margin-top: 8px; } .bk-pl .im { aspect-ratio: 16 / 9; } .bk-hd { margin-top: 6px; } .bk-hd .ti { font-size: 20px; } }
"""
LAMPPAPER = ("--page: #c7b287; --page-2: #b9a377; --fg: #221609; --muted: #54422a; --rubric: #852516; --gild: #8a611c;"
             " --ink-rule: rgba(105,68,20,.6); --edge-a: #cfbb91; --edge-b: #93794a; color-scheme: light;")
for k, v in {"__P__": P, "__NOISE__": NOISE, "__FIBRE__": FIBRE, "__LAMPPAPER__": LAMPPAPER, "__PAPER__": PAPER, "__PAPERBLEND__": PAPER_BLEND}.items():
    BOOKPAGE_CSS = BOOKPAGE_CSS.replace(k, v)

BOOKPAGE_JS = r"""
<script>
/* The full-screen view as a page of the book. The reading is laid out as pages: each scene's painting is printed at
   the head of the page where that scene begins, with the verses set below it as a paragraph; the verse being read is in
   full ink, the rest a little lighter. When the reading reaches the next page (a new scene, or the text runs on) the
   page turns; seeking back turns it back. The view's controls and opening/closing are miniplayer.js's own. */
(() => {
  const start = () => {
    const fs = document.querySelector(".fs"); if (!fs || typeof TRACKS === "undefined") return setTimeout(start, 300);
    const bottom = fs.querySelector(".fs-bottom");
    const bk = document.createElement("div"); bk.className = "bk"; bk.setAttribute("aria-live", "off");
    bk.innerHTML = '<div class="bk-boards"></div><div class="bk-ribbon"></div><div class="bk-left"></div>' +
      '<div class="bk-stack"><div class="bk-face bk-measure"><div class="bk-in"></div></div><div class="bk-pages"></div></div>';
    fs.insertBefore(bk, bottom);
    const stack = bk.querySelector(".bk-pages"), box = bk.querySelector(".bk-stack"), measure = bk.querySelector(".bk-measure .bk-in");
    const BOOKNAME = "__BOOKNAME__", DIR = "__DIR__";
    const vKey = typeof verseKey === "function" ? verseKey : (v => { const m = String(v).match(/^(?:(\d+):)?(\d+)/); return m ? (+(m[1] || 0)) * 1000 + +m[2] : -1; });
    const SCN = typeof SCENES !== "undefined" ? SCENES : {}, ARTS = typeof ART !== "undefined" ? ART : {};
    let CL = null; fetch((DIR ? "../" : "") + "clip/clips.json").then(r => r.ok ? r.json() : null).then(d => { CL = d; }).catch(() => {});
    const esc = x => String(x).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
    const reduce = () => matchMedia("(prefers-reduced-motion: reduce)").matches;

    let book = null, shown = -1, size = "";
    // ---- laying the reading out as pages ----
    function verses(t) {
      const e = CL && CL[(DIR ? DIR + "/" : "") + t.file], segs = e && e.segs;
      const vs = [], sup = [];
      if (segs) for (const [a, b, lab, text] of segs) {
        if (lab === "title") { if (!/^psalm\s+[\w-]+\.?$/i.test(text.trim())) sup.push({ text, start: a }); continue; }
        const last = vs[vs.length - 1];
        vs.push({ label: lab, key: vKey(lab), text, start: a, end: b, first: !last || last.label !== lab });
      }
      return { vs, sup, ok: !!segs, lines: !!e && e.unit === "line" };
    }
    function pageHTML(t, pg, idx) {
      let h = `<div class="bk-rh"><span>${esc(BOOKNAME)}</span><span>${esc(t.title)}</span></div>`;
      const kick = DIR ? `<span class="kick">${esc(t.mood || "")}</span>` : `<span class="he" lang="he" dir="rtl">${esc(t.he || "")}</span>`;
      if (pg.head) h += `<div class="bk-hd">${kick}<span class="ti">${esc(t.title)}</span>` +
        (pg.sup ? `<span class="sup">${esc(pg.sup)}</span>` : "") + `</div>`;
      if (pg.pic) h += `<figure class="bk-pl"><span class="im" style="background-image:url('${pg.pic}')"></span>${pg.cap ? `<figcaption class="cap">${esc(pg.cap)}</figcaption>` : ""}</figure>`;
      h += `<div class="bk-tx">` + (pg.verses.length ? pg.verses.map((v, i) => {
        let tx = esc(v.text);
        const dc = pg.head && i === 0 && v.first;
        if (dc && /^[A-Za-z]/.test(v.text)) tx = `<span class="bk-dc">${esc(v.text[0])}</span>` + esc(v.text.slice(1));
        return `<span class="bk-v" data-v="${esc(v.label)}">${dc || !v.first || book_lines ? "" : `<span class="bk-n">${esc(v.label.replace(/^\d+:/, ""))}</span>`}${tx} </span>`;
      }).join("") : (pg.line ? `<span class="bk-v now">${esc(pg.line)}</span>` : "")) + `</div><div class="bk-fo">${idx + 1}</div>`;
      return h;
    }
    function fits() { const tx = measure.querySelector(".bk-tx"); return !tx || tx.scrollHeight <= tx.clientHeight + 1; }
    let book_lines = false;
    function layout(t) {
      const { vs, sup, ok, lines } = verses(t); book_lines = lines;
      const seq = (SCN[t.n] || [["1", ARTS[t.n] || null]]).map(([from, img]) => ({ key: vKey(from), img }));
      const chunks = seq.map(c => ({ img: c.img, vs: [] }));
      for (const v of vs) { let ci = 0; seq.forEach((c, i) => { if (c.key <= v.key) ci = i; }); chunks[ci].vs.push(v); }
      const pages = [];
      chunks.forEach((c, ci) => {
        if (ci > 0 && !c.vs.length) return;
        const a = c.vs[0], b = c.vs[c.vs.length - 1];
        let pg = { head: ci === 0, sup: ci === 0 ? sup.map(x => x.text).join(" ") : "", pic: c.img,
                   cap: a && !lines ? (DIR ? `${BOOKNAME} ` + (/:/.test(a.label) ? "" : `${t.n}:`) : `${t.title}:`) + `${a.label}${b && b.label !== a.label ? "–" + b.label.replace(/^\d+:/, "") : ""}` : "", verses: [], line: ok ? "" : t.line };
        const render = () => { measure.innerHTML = pageHTML(t, pg, pages.length); };
        const flush = () => { pages.push(pg); pg = { head: false, pic: null, verses: [] }; };
        for (const piece of c.vs) {
          pg.verses.push(piece); render(); if (fits()) continue;
          pg.verses.pop();
          if (pg.verses.length || pg.pic || pg.head) flush();          // carry on at the top of the next page
          pg.verses.push(piece); render(); if (fits()) continue;
          pg.verses.pop();                                             // longer than a whole page: break it between words
          const words = piece.text.split(/\s+/), dur = Math.max(.1, (piece.end || piece.start + 1) - piece.start);
          let w = 0, first = piece.first;
          while (w < words.length) {
            const part = Object.assign({}, piece, { first, text: words[w], start: piece.start + dur * w / words.length });
            pg.verses.push(part); w++;
            while (w < words.length) { const prev = part.text; part.text = prev + " " + words[w]; render(); if (!fits()) { part.text = prev; break; } w++; }
            if (w < words.length) { flush(); first = false; }
          }
        }
        pages.push(pg);
      });
      if (!pages.length) pages.push({ head: true, pic: ARTS[t.n] || null, verses: [], line: t.line });
      pages.forEach(pg => { if (pg.pic) { const im = new Image(); im.src = pg.pic; } });
      return { file: t.file, t, pages, sup, ok };
    }
    // ---- which page the reading is on, and which verse is being read ----
    function where() {
      const now = position();
      let lab = null, pi = 0;
      book.pages.forEach((pg, i) => pg.verses.forEach(v => { if (v.start <= now + 0.12) { lab = v.label; pi = i; } }));
      return { pi, lab, inSup: lab === null && book.sup.some(s => s.start <= now + 0.12) };
    }
    // ---- a printed page ----
    function makePage(i) {
      const el = document.createElement("div"); el.className = "bk-face bk-pg";
      el.innerHTML = `<div class="bk-in">${pageHTML(book.t, book.pages[i], i)}</div>`;
      return el;
    }
    // ---- turning a page: the corner lifts and the page folds over along a crease that sweeps across it. The part past
    //      the crease is drawn as the back of the sheet, mirrored across the crease (with the print faintly showing
    //      through), and the fold casts a shadow on the page being uncovered. All flat 2D, so it holds up in Safari. ----
    let turn = null;
    const poly = pts => pts.length ? "polygon(" + pts.map(p => p[0].toFixed(1) + "px " + p[1].toFixed(1) + "px").join(",") + ")" : "polygon(0 0, 0 0, 0 0)";
    function half(W, H, M, n, sign) {   // the part of the page where sign * (X - M)·n <= 0
      const pts = [[0, 0], [W, 0], [W, H], [0, H]], f = q => sign * ((q[0] - M[0]) * n[0] + (q[1] - M[1]) * n[1]), out = [];
      for (let k = 0; k < 4; k++) {
        const a = pts[k], b = pts[(k + 1) % 4], fa = f(a), fb = f(b);
        if (fa <= 0) out.push(a);
        if ((fa < 0 && fb > 0) || (fa > 0 && fb < 0)) { const u = fa / (fa - fb); out.push([a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u]); }
      }
      return out;
    }
    function bar(el, M, n, L, h, side) {   // a strip lying along the crease, on the + side of it (side 1) or the - side (side -1)
      const phi = Math.atan2(-n[0], n[1]);
      el.style.width = L + "px"; el.style.height = h + "px";
      el.style.transform = `translate(${M[0]}px, ${M[1]}px) rotate(${phi}rad) translate(${-L / 2}px, ${side > 0 ? 0 : -h}px)`;
    }
    // Each frame only moves things (translate/rotate/reflect), never re-cuts or repaints them: the pages are painted
    // once, and the phone's graphics chip slides them. The page's visible part sits in a huge box whose edge lies on
    // the crease; turning just rotates and slides that box, and moves the page inside it the opposite way.
    function edgeBox(box, inner, M, n, S, reflect) {
      const phi = Math.atan2(n[1], n[0]);
      box.style.transform = `translate(${M[0]}px, ${M[1]}px) rotate(${phi}rad) translate(${-S}px, ${-S / 2}px)`;   // its right edge is the crease
      const k = M[0] * n[0] + M[1] * n[1];
      inner.style.transform = `translate(${S}px, ${S / 2}px) rotate(${-phi}rad) translate(${-M[0]}px, ${-M[1]}px)` +
        (reflect ? ` matrix(${1 - 2 * n[0] * n[0]}, ${-2 * n[0] * n[1]}, ${-2 * n[0] * n[1]}, ${1 - 2 * n[1] * n[1]}, ${2 * k * n[0]}, ${2 * k * n[1]})` : "");
    }
    function setTurn(T, t) {
      const W = T.W, H = T.H, S = T.S;
      const C = [W, H], P = [W - 2 * W * Math.max(t, 0.0005), H - 0.26 * H * Math.sin(Math.PI * t)];
      let n = [C[0] - P[0], C[1] - P[1]]; const len = Math.hypot(n[0], n[1]) || 1; n = [n[0] / len, n[1] / len];
      const M = [(C[0] + P[0]) / 2, (C[1] + P[1]) / 2];
      edgeBox(T.frontBox, T.front, M, n, S, false);
      edgeBox(T.flapBox, T.flap, M, n, S, true);
      const L = 3 * (W + H), s = Math.pow(Math.sin(Math.PI * Math.min(1, t * 1.15)), 1.6);
      bar(T.castBar, M, n, L, 70, 1);  T.castBar.style.opacity = s;          // on the page being uncovered
      bar(T.cast2Bar, M, n, L, 26, -1); T.cast2Bar.style.opacity = s * .8;  // on the page itself, under the lifted part
      bar(T.flapBar, M, n, L, Math.max(40, W * .35), 1);                     // the curve of the sheet near the fold
    }
    function startTurn(front, under, forward, done) {
      const W = box.clientWidth, H = box.clientHeight, S = 2.5 * (W + H);
      const sized = el => { el.style.inset = "auto"; el.style.left = el.style.top = "0px"; el.style.width = W + "px"; el.style.height = H + "px"; el.style.transformOrigin = "0 0"; };
      const clipBox = cls => { const b = document.createElement("div"); b.className = "bk-clip " + cls; b.style.width = b.style.height = S + "px"; return b; };
      // the page being turned, in its box
      const frontBox = clipBox("front"); stack.appendChild(frontBox); frontBox.appendChild(front); sized(front);
      // the back of the sheet: the page mirrored across the crease, print faintly showing through
      const flap = document.createElement("div"); flap.className = "bk-face bk-flap"; sized(flap);
      const ghost = front.querySelector(".bk-in").cloneNode(true); ghost.classList.add("ghost"); flap.appendChild(ghost);
      const mk = (cls, grad) => { const c = document.createElement("div"); c.className = "bk-cast " + cls; const b = document.createElement("div"); b.className = "bk-bar"; b.style.background = grad; c.appendChild(b); return [c, b]; };
      const [cast, castBar] = mk("", "linear-gradient(rgba(20,10,2,.30), rgba(20,10,2,.10) 30%, transparent)");
      const [cast2, cast2Bar] = mk("on-top", "linear-gradient(transparent, rgba(20,10,2,.22))");
      const [flapShade, flapBar] = mk("", "linear-gradient(rgba(30,16,4,.30), rgba(255,250,235,.10) 35%, rgba(30,16,4,.10) 80%, transparent)");
      flap.appendChild(flapShade);
      const flapBox = clipBox("flap"); flapBox.appendChild(flap);
      stack.insertBefore(cast, frontBox); frontBox.appendChild(cast2); sized(cast2); stack.appendChild(flapBox);
      const T = { W, H, S, front, under, flap, frontBox, flapBox, cast, cast2, castBar, cast2Bar, flapBar, raf: 0, done: null };
      const ms = 1050; let t0 = 0; const ease = u => u < .5 ? 4 * u * u * u : 1 - Math.pow(-2 * u + 2, 3) / 2;
      T.done = () => {
        cancelAnimationFrame(T.raf);
        front.style.cssText = ""; stack.insertBefore(front, frontBox);     // the page goes back to an ordinary page
        [frontBox, flapBox, cast].forEach(e => e.remove()); done(); turn = null;
      };
      const frame = now => { const u = Math.min(1, (now - t0) / ms), e = ease(u); setTurn(T, forward ? e : 1 - e); if (u < 1) T.raf = requestAnimationFrame(frame); else T.done(); };
      setTurn(T, forward ? 0 : 1); turn = T;
      T.raf = requestAnimationFrame(() => { T.raf = requestAnimationFrame(now => { t0 = now; frame(now); }); });
    }
    let leaf = null;
    let ready = null;   // the next page, built ahead of time and lying under the current one
    const decoded = {};
    function prepare(i) {
      if (!book || i >= book.pages.length || (ready && ready.i === i && ready.book === book)) return;
      if (ready) ready.el.remove();
      const pic = book.pages[i].pic;
      if (pic && !decoded[pic]) { const im = new Image(); im.src = pic; decoded[pic] = im.decode ? im.decode().catch(() => {}) : 1; }
      const el = makePage(i); stack.insertBefore(el, stack.firstChild); ready = { i, el, book };
    }
    function showPage(i, animate) {
      if (turn) turn.done();
      let nu;
      if (ready && ready.i === i && ready.book === book) { nu = ready.el; ready = null; } else nu = makePage(i);
      if (ready) { ready.el.remove(); ready = null; }
      const old = leaf, forward = i > shown;
      if (!old || !animate || reduce()) { stack.innerHTML = ""; stack.appendChild(nu); leaf = nu; shown = i; clearTimeout(showPage.tm); showPage.tm = setTimeout(() => prepare(i + 1), 600); return; }
      if (forward) { stack.insertBefore(nu, old); startTurn(old, nu, true, () => old.remove()); }      // the current page curls over, uncovering the next
      else { stack.appendChild(nu); startTurn(nu, old, false, () => old.remove()); }                  // going back: the earlier page curls back over
      leaf = nu; shown = i;
      clearTimeout(showPage.tm); showPage.tm = setTimeout(() => { if (!turn) prepare(shown + 1); else showPage.tm = setTimeout(() => prepare(shown + 1), 1200); }, 1300);
    }
    function mark(w) {
      if (!leaf) return;
      leaf.querySelectorAll(".bk-tx .bk-v").forEach(v => v.classList.toggle("now", v.dataset.v === w.lab));
      const sp = leaf.querySelector(".bk-hd .sup"); if (sp) sp.classList.toggle("now", w.inSup);
    }
    function tick() {
      if (!fs.classList.contains("on") || document.documentElement.matches(".rev,.judges,.mighty,.prayers,.matthew,.proverbs,.prophets")) return;
      const t = TRACKS[cur()]; if (!t) return;
      const sz = bk.clientWidth + "x" + bk.clientHeight;
      if (!book || book.file !== t.file || sz !== size || (!book.ok && CL)) {
        if (!bk.clientHeight) return;
        const fresh = !book || book.file !== t.file;
        size = sz; book = layout(t); shown = -1; leaf = null; ready = null; stack.innerHTML = "";
        showPage(where().pi, false); if (fresh) bk.dataset.file = t.file;
      }
      const w = where();
      if (w.pi !== shown) showPage(w.pi, true);
      mark(w);
    }
    if (document.fonts) { document.fonts.addEventListener("loadingdone", () => { size = ""; }); document.fonts.ready.then(() => { size = ""; }); }
    window.__bkAudit = () => {   // lays out every reading here and reports any page whose text runs off it
      const bad = [];
      for (const t of TRACKS) { const b = layout(t); b.pages.forEach((pg, i) => { measure.innerHTML = pageHTML(t, pg, i); if (!fits()) bad.push(t.title + " p" + (i + 1)); }); }
      return { tracks: TRACKS.length, bad };
    };
    setInterval(tick, 150);
    new MutationObserver(() => setTimeout(tick, 0)).observe(fs, { attributes: true, attributeFilter: ["class"] });
  };
  start();
})();
</script>
"""

once('<div class="sub">Read by Psalm Reader II over a humming choir</div>',
     '<div class="sub">Read by Psalm Reader II over a humming choir</div>\n    <figure class="artplate" id="plate" aria-hidden="true"><span class="pin"><img alt=""><img alt=""></span></figure>')

# the clip maker (and the Listen offline sheet, which shares its look): a parchment page lying open on the book's leather
CLIP_CSS = r"""
/* =================== the clip maker as a page of the book =================== */
html .cm { --page: #efe2bf; --page-2: #e3d0a3; --fg: #2b1f12; --muted: #6b583e; --rubric: #9b2b1d; --gild: #b8862f; --gild-l: #f0d58c;
  --ink-rule: rgba(155,104,30,.6); --edge-a: #f1e5c6; --edge-b: #c2a978; --line: rgba(155,104,30,.45); --surface: rgba(255,248,226,.45);
  --accent: #84520f; --accent-ink: #2a1a0a; color-scheme: light; color: var(--fg);
  background: radial-gradient(120% 50% at 50% 0%, rgba(255,255,255,.07), transparent 70%), __NOISE__, linear-gradient(var(--leather), var(--leather-d));
  background-color: var(--leather-d); padding-left: max(10px, env(safe-area-inset-left, 0px)); padding-right: max(10px, env(safe-area-inset-right, 0px)); }
@media (prefers-color-scheme: dark) { html:not([data-theme="light"]) .cm { __LAMPPAPER__ --line: rgba(105,68,20,.5); --surface: rgba(240,225,190,.3); --accent: #6e430c; } }
html[data-theme="dark"] .cm { __LAMPPAPER__ --line: rgba(105,68,20,.5); --surface: rgba(240,225,190,.3); --accent: #6e430c; }

html .cm-in { position: relative; margin: 58px auto 10px; padding: 46px 22px 34px 26px; gap: 18px; border-radius: 2px 5px 5px 2px;
  background: linear-gradient(90deg, rgba(50,28,8,.28), rgba(50,28,8,.07) 4%, transparent 9%, transparent 95%, rgba(50,28,8,.1)), __PAPER__;
  background-color: var(--page); background-blend-mode: normal, __PAPERBLEND__;
  box-shadow: inset 0 0 0 1px rgba(110,75,30,.25), 1px 1px 0 var(--edge-a), 2px 1px 0 var(--edge-b), 3px 2px 0 var(--edge-a), 4px 2px 0 var(--edge-b),
    5px 3px 0 var(--edge-a), 6px 3px 0 var(--edge-b), 7px 4px 0 #1a1007, 0 14px 34px rgba(0,0,0,.6); }
html .cm-in::before { content: ""; position: absolute; inset: 9px 8px 9px 11px; border: 3px double var(--ink-rule); pointer-events: none; }
html .cm-in::after { content: var(--cm-rh, "The Psalter"); position: absolute; left: 26px; right: 22px; top: 22px; text-align: center; padding-bottom: 7px;
  border-bottom: 1px solid var(--ink-rule); font: 400 11px/1 var(--display); letter-spacing: .2em; text-transform: uppercase; color: var(--muted); }
html .cm-in > * { position: relative; }
html .cm-in > .cm-head { position: static; }
#cm [hidden] { display: none !important; }   /* the result and progress bar were showing before any video was made */

/* heading: fleuron, title in capitals, gilt rule; the close button a gilt ring on the leather above the page */
html .cm-head { flex-direction: column; justify-content: center; gap: 0; text-align: center; }
html .cm-head::before { content: ""; width: 58px; height: 19px; margin-bottom: 4px; background: center / contain no-repeat __FLEURON__; }
html .cm-head::after { content: ""; width: 170px; height: 11px; margin-top: 9px; background: center / contain no-repeat __RULE__; }
html .cm-head h2 { font: 400 25px/1.15 var(--display); letter-spacing: .17em; text-transform: uppercase; color: var(--fg); }
html .cm-x { position: absolute; left: 0; top: -52px; width: 42px; height: 42px; min-height: 0; padding: 0; border-radius: 50%; font-size: 0; color: var(--gild-l);
  background: rgba(0,0,0,.22); border: 1px solid color-mix(in srgb, var(--gild) 85%, transparent); outline: 1px solid color-mix(in srgb, var(--gild) 38%, transparent); outline-offset: -5px; }
html .cm-x::before { content: ""; position: absolute; inset: 0; margin: auto; width: 15px; height: 15px;
  background: linear-gradient(45deg, transparent 45%, currentColor 45% 55%, transparent 55%), linear-gradient(-45deg, transparent 45%, currentColor 45% 55%, transparent 55%); }
html .cm-lede, html .of-net { margin: -4px 4px 0; text-align: center; font: italic 16px/1.45 var(--body); color: var(--muted); }

/* the choices: small red capitals over a ruled line of ink */
html .cm-field { font: 700 11px/1.3 var(--ui); letter-spacing: .14em; text-transform: uppercase; color: var(--rubric); gap: 5px; }
html .cm-field select { -webkit-appearance: none; appearance: none; font: 400 19px/1.3 var(--body); letter-spacing: 0; text-transform: none; color: var(--fg);
  border: 0; border-bottom: 1px solid var(--ink-rule); border-radius: 0; padding: 10px 30px 10px 4px; min-height: 46px;
  background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 12 8'%3E%3Cpath d='M1 1.5l5 5 5-5' fill='none' stroke='%23a07424' stroke-width='1.6'/%3E%3C/svg%3E") right 6px center / 12px 8px no-repeat,
    linear-gradient(transparent, var(--surface)); }
html .cm-len { margin: -6px 0 0; text-align: center; font: italic 15px/1.3 var(--body); color: var(--muted); }

/* square or tall: two gilt-framed tabs; the chosen one is a piece of leather with gilt letters */
html .cm-shape button, html .cm-btn { font: 400 16px/1.2 var(--body); color: var(--fg); border-radius: 6px; background: color-mix(in srgb, var(--page) 55%, transparent);
  border: 1px solid var(--gild); outline: 1px solid color-mix(in srgb, var(--gild) 38%, transparent); outline-offset: -5px; }
html .cm-shape button small { font: italic 13px/1.2 var(--body); color: var(--muted); }
html .cm-shape button[aria-pressed="true"] { background: __NOISE__, linear-gradient(var(--leather-l), var(--leather) 55%, var(--leather-d)); color: #f6e5b8;
  border-color: var(--gild); box-shadow: 0 2px 6px rgba(40,22,6,.35); outline-color: color-mix(in srgb, var(--gild) 70%, transparent); }
html .cm-shape button[aria-pressed="true"] small { color: #d9c08a; }

/* the preview, set in the page like a plate in a gilt frame */
html .cm-stage { background: none; border: 0; padding: 0; }
html #cm-canvas, html .cm-result video { padding: 6px; border-radius: 2px; box-sizing: border-box;
  background: linear-gradient(135deg, #f7e6a6, #b5862f 28%, #f2d47c 50%, #8c6220 74%, #e4c26c);
  box-shadow: 0 4px 10px rgba(50,28,6,.4), inset 0 0 0 1px rgba(80,52,12,.7); }

/* buttons: gilt-framed; Make the video, Save video and Save are gold */
html .cm-acts { justify-content: center; }
html .cm-btn { min-height: 50px; padding: 12px 22px; font-size: 17px; border-radius: 999px; outline-offset: -6px; }
html .cm-btn.go { border: 0; outline: 0; color: #2a1a0a; font-weight: 600; text-shadow: 0 1px 0 rgba(255,240,190,.6);
  background: linear-gradient(180deg, #fff1bf, #ecc76a 32%, #b88830 70%, #d9b25a);
  box-shadow: 0 0 0 1px #6b4a17, 0 0 0 3px #e3c06a, 0 0 0 4px #5a3d12, 0 4px 10px rgba(50,28,5,.4); }
html .cm-prog { font: italic 14px/1 var(--body); color: var(--muted); }
html .cm-prog progress { accent-color: var(--gild); }
html .cm-status { text-align: center; font: italic 16px/1.4 var(--body); color: var(--rubric); }
html .cm-result { border-top: 3px double var(--ink-rule); }
html .cm-saved { font: 16px/1.4 var(--body); text-align: center; }
html .cm-help { font: 15px/1.5 var(--body); color: var(--muted); }

/* Listen offline uses the same sheet: its boxes become ruled panels on the page */
html .of-box, html .of-col { background: var(--surface); border: 1px solid var(--ink-rule); border-radius: 3px; }
html .of-box h3 { font: 400 19px/1.2 var(--display); letter-spacing: .12em; text-transform: uppercase; color: var(--fg); }
html .of-box p, html .of-box ol, html .of-sum { font-family: var(--body); font-size: 16px; }
html .of-net.off { color: var(--rubric); font-style: normal; font-weight: 600; }
"""
for k, v in {"__NOISE__": NOISE, "__LAMPPAPER__": LAMPPAPER, "__PAPER__": PAPER, "__PAPERBLEND__": PAPER_BLEND, "__FLEURON__": FLEURON, "__RULE__": RULE}.items():
    CLIP_CSS = CLIP_CSS.replace(k, v)
CLIP_CSS += "".join(f'html.{k} .cm {{ --cm-rh: "{v[1]}"; }}\n' for k, v in OTHERS.items())

# the new icon, on the test page only (the live page keeps the old one until it's approved)
once('<link rel="apple-touch-icon" href="apple-touch-icon.png">', '<link rel="apple-touch-icon" href="icon-test/apple-touch-icon.png">')
once('<link rel="icon" href="icon-512.png">', '<link rel="icon" type="image/png" sizes="48x48" href="icon-test/favicon-48.png"><link rel="icon" type="image/png" sizes="192x192" href="icon-test/icon-192.png">')
once("</style>", BOOK_CSS + FLIGHT_CSS + KEEP_CSS + BOOKPAGE_CSS + TOP_ALL_CSS + CLIP_CSS + "</style>")
# switching books no longer pauses what is playing (the keep-playing script decides what pauses, and when)
once("    for (const k of ORDER) if (k !== which) pauseTab(k);", "    if (!window.keepPlaying) for (const k of ORDER) if (k !== which) pauseTab(k);")
# let the keep-playing script reach the tabs
once("  show(start, false);\n})();", "  show(start, false);\n  window.__tabs = { show, fr, TABS, ORDER, get cur() { return cur; } };\n})();")
s = s.rstrip("\n") + "\n" + FLIGHT_JS + KEEP_JS + BOOKPAGE_JS.replace("__BOOKNAME__", "The Psalter").replace("__DIR__", "")
# this test page opens each book test copy
import time
STAMP = time.strftime("%Y%m%d%H%M%S")   # a new address each build, so phones fetch the books' pages fresh, not an older saved copy
for k, v in OTHERS.items(): once(f'src: "{v[0]}/index.html"', f'src: "{v[0]}/book-test.html?v={STAMP}"')
s = s.replace("<title>The Psalter</title>", "<title>The Psalter</title>", 1)
open(out, "w", encoding="utf-8").write(s)
print("wrote", out)

# ---------- each book's own page, as a book ----------
import re
SEEK_JS = FLIGHT_JS[FLIGHT_JS.index("/* The seek bar's gilt fill"):FLIGHT_JS.index("/* The full-screen view as an illustrated page")]
PLATE_JS = FLIGHT_JS[FLIGHT_JS.index("/* The Psalter's painting, set as a framed plate"):FLIGHT_JS.index("</script>")]
FONTS = ('<link href="https://fonts.googleapis.com/css2?family=Bellefair&family=Alegreya:ital,wght@0,400;0,500;0,700;1,400;1,500'
         '&family=Alegreya+Sans:wght@400;500;700&display=swap" rel="stylesheet">')
base = os.path.dirname(os.path.abspath(src))
for k, (folder, name, dark, mid, ribbon) in OTHERS.items():
    path = os.path.join(base, folder, "index.html")
    b = open(path, encoding="utf-8").read()
    def one(old, new):
        global b
        assert b.count(old) == 1, (folder, old[:60], b.count(old))
        b = b.replace(old, new, 1)
    one("<style>", FONTS + "\n<style>")
    css = (BOOK_CSS + f"\nhtml:root:root:root {{ {leather_vars(dark, mid, ribbon)} }}\n" + BOOKPAGE_CSS)
    if folder == "revelation":   # its title is Greek, and much longer than the Hebrew ones
        css += f"\n{P} .hebrew {{ font-size: clamp(40px, 12.5vw, 80px); }}\n"
    one("</style>", css + "</style>")
    m = re.search(r'<div class="sub">.*?</div>', b, re.S); assert m, folder
    b = b[:m.end()] + '\n    <figure class="artplate" id="plate" aria-hidden="true"><span class="pin"><img alt=""><img alt=""></span></figure>' + b[m.end():]
    b = b.rstrip("\n") + "\n<script>\n" + SEEK_JS + PLATE_JS + "</script>\n" + BOOKPAGE_JS.replace("__BOOKNAME__", name).replace("__DIR__", folder)
    open(os.path.join(base, folder, "book-test.html"), "w", encoding="utf-8").write(b)
    print("wrote", folder + "/book-test.html")
