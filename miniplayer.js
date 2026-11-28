/* Mini player. Every tab has a big player near the top of the page. Once something has been started, scrolling it off
   the screen used to take the controls away with it. This keeps a small copy pinned to the bottom of the screen while
   the big player is out of sight and a recording is playing, paused part-way, or loading. It works purely through the
   big player's own controls (play, prev, next, the seek bar), so each tab's playing logic is untouched.
   It also adds "back 15 seconds" and "forward 15 seconds" buttons, to the big player (beside previous/next) and to the
   bar (either side of its seek bar). They move the page's own seek bar, the same as dragging it.
   And a "Full screen" button: the reading's painting (Psalter, when it has one) or a dark background, the words as they are
   spoken (from clip/clips.json, the clip maker's timings), and big controls that again drive the page's own player. */
(() => {
  const $ = id => document.getElementById(id);
  const big = document.querySelector('.player'), play = $('play'), icon = $('play-icon'), seek = $('seek');
  if (!big || !play || !icon || !seek) return;

  const css = document.createElement('style');
  css.textContent = `
.mini { position: fixed; left: 0; right: 0; bottom: calc(8px + env(safe-area-inset-bottom)); z-index: 20; display: none;
  width: min(720px, calc(100% - 16px)); margin: 0 auto; box-sizing: border-box; padding: 10px 12px 8px;
  background: color-mix(in srgb, var(--surface) 94%, transparent); -webkit-backdrop-filter: blur(14px); backdrop-filter: blur(14px);
  color: var(--fg); border: 1px solid var(--line); border-radius: 18px; box-shadow: 0 10px 30px rgba(0,0,0,.18), 0 1px 3px rgba(0,0,0,.08); }
.mini.on { display: block; }
.mini-row { display: flex; align-items: center; gap: 12px; }
.mini-play { flex: none; width: 48px; height: 48px; border-radius: 50%; border: 0; background: var(--accent); color: var(--accent-ink);
  display: grid; place-items: center; cursor: pointer; box-shadow: 0 2px 6px color-mix(in srgb, var(--accent) 35%, transparent); }
.mini-play svg { width: 22px; height: 22px; fill: currentColor; }
.mini-btn { flex: none; width: 44px; height: 44px; border: 0; border-radius: 50%; background: none; color: var(--fg); display: grid; place-items: center; cursor: pointer; }
.mini-btn:active, .mini-play:active { transform: scale(.94); }
.mini-btn:focus-visible, .mini-play:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
.mini-btn svg { width: 22px; height: 22px; fill: currentColor; }
.mini-fs svg { fill: none; stroke: currentColor; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; }
.mini-text { flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 1px; cursor: pointer; }
.mini-title { font-family: var(--display); font-size: 18px; line-height: 1.2; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.mini-meta { font-family: var(--ui); font-size: 13.5px; color: var(--muted); font-variant-numeric: tabular-nums; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.mini-meta b { font-weight: 600; color: var(--accent); }
.mini-seekrow { display: flex; align-items: center; gap: 2px; margin-top: 4px; }
.mini-seek { flex: 1; min-width: 0; height: 30px; margin: 0 6px; background: transparent; -webkit-appearance: none; appearance: none; --p: 0%; cursor: pointer; }
.mini-seek::-webkit-slider-runnable-track { height: 4px; border-radius: 2px;
  background: linear-gradient(to right, var(--accent) var(--p), color-mix(in srgb, var(--fg) 16%, transparent) var(--p)); }
.mini-seek::-webkit-slider-thumb { -webkit-appearance: none; width: 16px; height: 16px; margin-top: -6px; border-radius: 50%; background: var(--accent);
  box-shadow: 0 1px 4px rgba(0,0,0,.25); }
.mini-seek::-moz-range-track { height: 4px; border-radius: 2px; background: color-mix(in srgb, var(--fg) 16%, transparent); }
.mini-seek::-moz-range-progress { height: 4px; border-radius: 2px; background: var(--accent); }
.mini-seek::-moz-range-thumb { width: 16px; height: 16px; border: 0; border-radius: 50%; background: var(--accent); }
.mini-seek:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; border-radius: 4px; }
.jump svg { width: 24px; height: 24px; fill: none; stroke: currentColor; stroke-width: 1.8; stroke-linecap: round; stroke-linejoin: round; }
.jump svg text { fill: currentColor; stroke: none; font: 700 7.5px system-ui, sans-serif; text-anchor: middle; }
.icon-btn.jump svg { width: 22px; height: 22px; fill: none; stroke: var(--fg); }
.icon-btn.jump svg text { fill: var(--fg); }`;
  document.head.appendChild(css);

  const JUMP = 15;   // seconds
  const back = `<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4.5 12a7.5 7.5 0 1 0 2.2-5.3"/><path d="M6.5 2.8v4h4"/><text x="12.6" y="15.2">${JUMP}</text></svg>`;
  const fwd = `<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M19.5 12a7.5 7.5 0 1 1-2.2-5.3"/><path d="M17.5 2.8v4h-4"/><text x="11.4" y="15.2">${JUMP}</text></svg>`;
  const secs = t => { const p = (t || '').trim().split(':').map(Number); return p.some(isNaN) ? NaN : p.reduce((a, b) => a*60 + b, 0); };
  function jump(d) {   // move the page's own seek bar by d seconds, exactly as if it had been dragged there
    const dur = secs(($('t-dur') || {}).textContent);
    if (!(dur > 0)) return;
    const now = seek.value / 100 * dur, to = Math.max(0, Math.min(dur - 0.5, now + d));
    seek.value = (to / dur * 100).toFixed(3);
    seek.dispatchEvent(new Event('input', { bubbles: true }));
    seek.dispatchEvent(new Event('change', { bubbles: true }));
  }
  const skipRow = big.querySelector('.skip'), prevBtn = $('prev');
  if (skipRow && prevBtn) {
    const mk = (d, html, label) => { const b = document.createElement('button'); b.type = 'button'; b.className = 'icon-btn jump';
      b.setAttribute('aria-label', label); b.innerHTML = html; b.addEventListener('click', () => jump(d)); return b; };
    prevBtn.after(mk(-JUMP, back, `Back ${JUMP} seconds`), mk(JUMP, fwd, `Forward ${JUMP} seconds`));
  }


  // ------------------------------------------------------------------ full-screen player with subtitles
  const TABDIR = (location.pathname.match(/\/(revelation|judges|prayers|matthew|proverbs|prophets|mighty)\//) || [])[1] || '';
  const PRE = TABDIR ? TABDIR + '/' : '';
  let CLIPS = null, clipsWanted = false;
  function loadClips() {
    if (clipsWanted) return; clipsWanted = true;
    fetch((TABDIR ? '../' : '') + 'clip/clips.json').then(r => r.json()).then(d => { CLIPS = d; }).catch(() => { clipsWanted = false; });
  }
  const g = name => { try { return (0, eval)(name); } catch (e) { return undefined; } };   // the page's own top-level player state
  const curTrack = () => { const T = g('TRACKS'), c = g('cur'); try { return T && c ? T[c()] : null; } catch (e) { return null; } };
  function nowTime() {   // seconds into the current reading
    const pos = g('position'); try { if (typeof pos === 'function') { const v = pos(); if (isFinite(v)) return v; } } catch (e) {}
    const dur = secs(($('t-dur') || {}).textContent); return dur > 0 ? seek.value / 100 * dur : 0;
  }
  const css2 = document.createElement('style');
  css2.textContent = `
.fsbtn { align-self: flex-start; display: inline-flex; align-items: center; gap: 8px; font-family: var(--ui); font-size: 16px; font-weight: 500;
  min-height: 44px; padding: 10px 18px; border-radius: 999px; border: 1px solid var(--line); background: transparent; color: var(--fg); cursor: pointer; }
.fsbtn svg { width: 18px; height: 18px; fill: none; stroke: currentColor; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; }
.fsbtn:focus-visible { outline: 2px solid var(--accent); outline-offset: 3px; }
.fs { position: fixed; inset: 0; z-index: 40; display: none; flex-direction: column; color: #f3eee2; overflow: hidden;
  background: #0f120e; font-family: var(--body, Georgia, serif); -webkit-user-select: none; user-select: none; }
.fs.on { display: flex; }
.fs { opacity: 0; transition: opacity .8s ease; }
.fs.show { opacity: 1; }
@media (prefers-reduced-motion: reduce) { .fs { transition: none; } }
.fs-bg { position: absolute; inset: 0; background: radial-gradient(120% 80% at 50% 62%, color-mix(in srgb, var(--accent) 22%, #10130f) 0%, #0b0d0a 75%); }
.fs-bg img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; object-position: center 60%; transform: scale(1.04);
  animation: fs-drift 60s ease-in-out infinite alternate; }
@keyframes fs-drift { from { transform: scale(1.04) translateY(0); } to { transform: scale(1.1) translateY(-1.5%); } }
@media (prefers-reduced-motion: reduce) { .fs-bg img { animation: none; } }
.fs-bg img.fade { opacity: 0; transition: opacity 1.2s ease; } .fs-bg img.fade.on { opacity: 1; }
@media (prefers-reduced-motion: reduce) { .fs-bg img.fade { transition: none; } }
.fs-bg.art::after { content: ""; position: absolute; inset: 0;
  background: linear-gradient(to bottom, rgba(12,14,11,.62) 0%, rgba(12,14,11,.38) 30%, rgba(12,14,11,.52) 62%, rgba(12,14,11,.86) 100%); }
.fs-top { position: relative; display: flex; align-items: center; gap: 12px; padding: calc(12px + env(safe-area-inset-top)) 16px 0; }
.fs-x { flex: none; width: 48px; height: 48px; border-radius: 50%; border: 1px solid rgba(255,255,255,.35); background: rgba(0,0,0,.25);
  color: inherit; display: grid; place-items: center; cursor: pointer; }
.fs-x svg { width: 20px; height: 20px; stroke: currentColor; stroke-width: 2.2; stroke-linecap: round; fill: none; }
.fs-head { min-width: 0; display: flex; flex-direction: column; }
.fs-label { font-family: var(--ui, system-ui); font-size: 12px; letter-spacing: .14em; text-transform: uppercase; opacity: .75; }
.fs-title { font-family: var(--display, Georgia, serif); font-size: 22px; line-height: 1.2; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.fs-words { position: relative; flex: 1; display: grid; place-items: center; padding: 16px max(20px, 6vw); }
.fs-line { grid-area: 1 / 1; max-width: 22ch; text-align: center; font-size: clamp(28px, 7.4vw, 52px); line-height: 1.32; text-wrap: balance;
  text-shadow: 0 2px 18px rgba(0,0,0,.65), 0 1px 3px rgba(0,0,0,.6); opacity: 0; transition: opacity .45s ease; }
.fs-line.on { opacity: 1; }
.fs-ref { position: absolute; top: 8px; left: 0; right: 0; text-align: center; font-family: var(--ui, system-ui); font-size: 14px; letter-spacing: .12em;
  opacity: .9; color: color-mix(in srgb, var(--accent) 55%, #fff); text-shadow: 0 1px 8px rgba(0,0,0,.7); }
.fs-bottom { position: relative; padding: 0 16px calc(18px + env(safe-area-inset-bottom)); display: flex; flex-direction: column; gap: 10px; max-width: 640px; width: 100%; margin: 0 auto; }
.fs-seek { display: flex; align-items: center; gap: 12px; font-family: var(--ui, system-ui); font-size: 14px; font-variant-numeric: tabular-nums; opacity: .9; }
.fs-seek input { flex: 1; min-width: 0; accent-color: var(--accent); height: 30px; }
.fs-ctl { display: flex; align-items: center; justify-content: space-between; }
.fs-ctl button { border: 0; background: none; color: inherit; width: 56px; height: 56px; display: grid; place-items: center; cursor: pointer; border-radius: 50%; }
.fs-ctl svg { width: 28px; height: 28px; fill: currentColor; }
.fs-ctl .jump svg { width: 30px; height: 30px; fill: none; stroke: currentColor; }
.fs-ctl .jump svg text { fill: currentColor; stroke: none; }
.fs-ctl .fs-play { width: 76px; height: 76px; background: var(--accent); color: var(--accent-ink); }
.fs-ctl .fs-play svg { width: 32px; height: 32px; }
html.fs-child .tabs { display: none !important; }
html.fs-child .cframe { top: 0 !important; height: 100dvh !important; }`;
  document.head.appendChild(css2);

  const fs = document.createElement('div');
  fs.className = 'fs'; fs.setAttribute('role', 'dialog'); fs.setAttribute('aria-modal', 'true'); fs.setAttribute('aria-label', 'Full-screen player');
  fs.innerHTML = `
  <div class="fs-bg"></div>
  <div class="fs-top">
    <button class="fs-x" type="button" aria-label="Close full screen"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg></button>
    <div class="fs-head"><span class="fs-label"></span><span class="fs-title"></span></div>
  </div>
  <div class="fs-words" aria-live="off"><div class="fs-ref"></div><div class="fs-line"></div><div class="fs-line"></div></div>
  <div class="fs-bottom">
    <div class="fs-seek"><span class="fs-cur">0:00</span><input type="range" min="0" max="100" step="0.1" value="0" aria-label="Position"><span class="fs-dur">0:00</span></div>
    <div class="fs-ctl">
      <button type="button" data-go="prev" aria-label="Previous"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 5h2v14H6zM20 5v14L9.5 12z"/></svg></button>
      <button type="button" class="jump" data-j="-1" aria-label="Back ${JUMP} seconds">${back}</button>
      <button type="button" class="fs-play" aria-label="Play or pause"><svg viewBox="0 0 24 24" aria-hidden="true"></svg></button>
      <button type="button" class="jump" data-j="1" aria-label="Forward ${JUMP} seconds">${fwd}</button>
      <button type="button" data-go="next" aria-label="Next"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M16 5h2v14h-2zM4 5v14l10.5-7z"/></svg></button>
    </div>
  </div>`;
  document.body.appendChild(fs);
  const F = sel => fs.querySelector(sel);
  const fBg = F('.fs-bg'), fLines = fs.querySelectorAll('.fs-line'), fRef = F('.fs-ref'), fSeek = F('.fs-seek input');
  F('.fs-play').addEventListener('click', () => play.click());
  fs.querySelectorAll('[data-go]').forEach(b => b.addEventListener('click', () => { const t = $(b.dataset.go); if (t) t.click(); }));
  fs.querySelectorAll('[data-j]').forEach(b => b.addEventListener('click', () => jump(JUMP * +b.dataset.j)));
  let fDrag = false;
  fSeek.addEventListener('input', () => { fDrag = true; seek.value = fSeek.value; seek.dispatchEvent(new Event('input', { bubbles: true })); });
  fSeek.addEventListener('change', () => { seek.value = fSeek.value; seek.dispatchEvent(new Event('change', { bubbles: true })); fDrag = false; });

  let fsOpen = false, wakeLock = null, artShown = undefined, lineShown = null, flip = 0;
  let hideT = 0;
  async function openFs(auto) {
    loadClips(); fsOpen = true; clearTimeout(hideT); fs.classList.add('on'); requestAnimationFrame(() => requestAnimationFrame(() => fs.classList.add('show')));
    document.documentElement.style.overflow = 'hidden';
    try { if (auto === true) throw 0; await (document.documentElement.requestFullscreen?.({ navigationUI: 'hide' }) || Promise.reject()); }
    catch (e) { try { if (window.parent !== window) parent.document.documentElement.classList.add('fs-child'); } catch (e2) {} }
    try { wakeLock = await navigator.wakeLock?.request('screen'); } catch (e) {}
    artShown = undefined; lineShown = null; fsSync(); if (auto !== true) F('.fs-x').focus();
  }
  function closeFs() {
    if (!fsOpen) return; fsOpen = false; fs.classList.remove('show'); hideT = setTimeout(() => fs.classList.remove('on'), 650);
    document.documentElement.style.overflow = ''; armRest();
    try { if (document.fullscreenElement) document.exitFullscreen(); } catch (e) {}
    try { if (window.parent !== window) parent.document.documentElement.classList.remove('fs-child'); } catch (e) {}
    try { wakeLock && wakeLock.release(); } catch (e) {} wakeLock = null;
  }
  F('.fs-x').addEventListener('click', closeFs);
  document.addEventListener('keydown', e => { if (fsOpen && e.key === 'Escape') closeFs(); });
  document.addEventListener('fullscreenchange', () => { if (!document.fullscreenElement && fsOpen) closeFs(); });
  document.addEventListener('visibilitychange', async () => { if (fsOpen && document.visibilityState === 'visible' && !wakeLock) { try { wakeLock = await navigator.wakeLock?.request('screen'); } catch (e) {} } });

  function verseLabel(v) { return v && v !== 'title' && /^\d/.test(v) ? 'Verse ' + v : ''; }
  function segAt() {   // [index, segs, file] of the piece being spoken now (or the last one begun)
    const t = curTrack(), file = t ? PRE + t.file : null, segs = CLIPS && file && CLIPS[file] ? CLIPS[file].segs : null;
    if (!segs) return [-1, null, file];
    const now = nowTime(); let k = -1;
    for (let i = 0; i < segs.length; i++) { if (segs[i][0] <= now + 0.12) k = i; else break; }
    return [k, segs, file];
  }
  function setLine(text) {
    if (text === lineShown) return; lineShown = text;
    const a = fLines[flip], b = fLines[flip = 1 - flip];
    a.classList.remove('on'); if (text) { b.textContent = text; b.classList.add('on'); }
  }
  function fsSync() {
    if (!fsOpen) return;
    const t = curTrack(), file = t ? PRE + t.file : null;
    F('.fs-label').textContent = ($('now-label') || {}).textContent || '';
    F('.fs-title').textContent = ($('now-title') || {}).textContent || '';
    if (F('.fs-play svg').innerHTML !== icon.innerHTML) F('.fs-play svg').innerHTML = icon.innerHTML;
    F('.fs-cur').textContent = ($('t-cur') || {}).textContent || '';
    F('.fs-dur').textContent = ($('t-dur') || {}).textContent || '';
    if (!fDrag) fSeek.value = seek.value;
    // background: the Psalter's painting for this psalm, if it has one
    // (a psalm with several scenes follows the page's current one, artNow, and cross-fades like the page)
    let art = null; try { const A = g('ART'); art = A && t && A[t.n] ? (g('artNow') || A[t.n]) : null; } catch (e) {}
    if (art !== artShown) {
      const first = artShown === undefined; artShown = art; fBg.classList.toggle('art', !!art);
      if (first || !art) fBg.innerHTML = '';
      if (art) {
        const im = new Image(); im.alt = ''; if (!first) im.className = 'fade';
        im.onload = () => {
          if (artShown !== art) return;
          requestAnimationFrame(() => im.classList.add('on'));
          fBg.querySelectorAll('img').forEach(x => { if (x !== im) setTimeout(() => x.remove(), 1300); });
        };
        im.src = art; fBg.appendChild(im);
      }
    }
    // the words being spoken now (held through short pauses, as in the clip maker)
    const [k, segs] = segAt();
    if (!segs) { fRef.textContent = ''; setLine(t ? t.line || '' : ''); return; }
    const now = nowTime(); let text = '';
    if (k >= 0) { const [s0, e0] = segs[k], nx = segs[k + 1] ? segs[k + 1][0] : Infinity; if (now < Math.min(nx - 0.12, e0 + 3.0)) text = segs[k][3]; }
    fRef.textContent = CLIPS[file].unit === 'verse' && k >= 0 ? verseLabel(segs[k][2]).toUpperCase() : '';
    setLine(text);
  }
  setInterval(fsSync, 100);

  // resting view: while something plays and nobody scrolls or touches for 6 s, the page fades into the full-screen player.
  // A swipe, a scroll or the close button brings the page back; the controls work as normal while it shows.
  const REST_MS = 6000; let restT = 0, lastY = scrollY;
  function blocked() {
    const open = d => { try { return !!d.querySelector('.cm:not([hidden])'); } catch (e) { return false; } };
    return open(document) || (window.parent !== window && open(parent.document));
  }
  const canRest = () => !fsOpen && document.visibilityState === 'visible' && big.offsetParent !== null && !blocked()
    && /playing|loading/i.test(($('now-label') || {}).textContent || '');
  function armRest() { clearTimeout(restT); restT = setTimeout(() => { if (canRest()) openFs(true); else armRest(); }, REST_MS); }
  function activity(e) {
    if (e.type === 'scroll') { const moved = Math.abs(scrollY - lastY) > 24; lastY = scrollY; if (!moved) return; }
    armRest();
  }
  for (const ev of ['scroll', 'wheel', 'keydown', 'pointerdown', 'touchstart']) addEventListener(ev, activity, { capture: true, passive: true });
  // leaving it: a swipe or wheel on the full-screen player (not on its seek bar) closes it
  let ty = null;
  fs.addEventListener('touchstart', e => { ty = e.target.closest('input') ? null : e.touches[0].clientY; }, { passive: true });
  fs.addEventListener('touchmove', e => { if (ty != null && Math.abs(e.touches[0].clientY - ty) > 40) { ty = null; closeFs(); } }, { passive: true });
  fs.addEventListener('wheel', e => { if (Math.abs(e.deltaY) > 20) closeFs(); }, { passive: true });
  armRest();

  if (skipRow) {
    const fb = document.createElement('button'); fb.type = 'button'; fb.className = 'fsbtn';
    fb.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 9V4h5M20 9V4h-5M4 15v5h5M20 15v5h-5"/></svg>Full screen';
    fb.addEventListener('click', () => openFs(false));
    const clip = big.querySelector('.clipbtn'); if (clip) clip.before(fb); else big.appendChild(fb);
    big.addEventListener('pointerenter', loadClips, { once: true });
  }

  const bar = document.createElement('div');
  bar.className = 'mini'; bar.setAttribute('role', 'region'); bar.setAttribute('aria-label', 'Now playing');
  bar.innerHTML = `
  <div class="mini-row">
    <button class="mini-play" type="button" aria-label="Play or pause"><svg viewBox="0 0 24 24" aria-hidden="true"></svg></button>
    <div class="mini-text" title="Show the full player"><span class="mini-title"></span><span class="mini-meta"></span></div>
    <button class="mini-btn mini-fs" type="button" aria-label="Full screen"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 9V4h5M20 9V4h-5M4 15v5h5M20 15v5h-5"/></svg></button>
  </div>
  <div class="mini-seekrow">
    <button class="mini-btn" data-go="prev" type="button" aria-label="Previous"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 5h2v14H6zM20 5v14L9.5 12z"/></svg></button>
    <button class="mini-btn jump" data-jump="-1" type="button" aria-label="Back 15 seconds">${back}</button>
    <input class="mini-seek" type="range" min="0" max="100" step="0.1" value="0" aria-label="Position">
    <button class="mini-btn jump" data-jump="1" type="button" aria-label="Forward 15 seconds">${fwd}</button>
    <button class="mini-btn" data-go="next" type="button" aria-label="Next"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M16 5h2v14h-2zM4 5v14l10.5-7z"/></svg></button>
  </div>`;
  document.body.appendChild(bar);

  const mIcon = bar.querySelector('.mini-play svg'),
        mTitle = bar.querySelector('.mini-title'), mSeek = bar.querySelector('.mini-seek'), mMeta = bar.querySelector('.mini-meta');
  bar.querySelector('.mini-play').addEventListener('click', () => play.click());
  bar.querySelectorAll('[data-go]').forEach(b => b.addEventListener('click', () => { const t = $(b.dataset.go); if (t) t.click(); }));
  bar.querySelectorAll('[data-jump]').forEach(b => b.addEventListener('click', () => jump(JUMP * +b.dataset.jump)));
  bar.querySelector('.mini-text').addEventListener('click', () => big.scrollIntoView({ behavior: 'smooth', block: 'start' }));
  bar.querySelector('.mini-fs').addEventListener('click', () => openFs(false));
  let dragging = false;
  mSeek.addEventListener('input', () => { dragging = true; mSeek.style.setProperty('--p', mSeek.value + '%'); seek.value = mSeek.value; seek.dispatchEvent(new Event('input', { bubbles: true })); });
  mSeek.addEventListener('change', () => { seek.value = mSeek.value; seek.dispatchEvent(new Event('change', { bubbles: true })); dragging = false; });

  let bigVisible = true;
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(es => { bigVisible = es[es.length - 1].isIntersecting; sync(); }, { threshold: 0 }).observe(big);
  }
  const active = () => {   // something has been started: playing, loading, or paused part-way through
    const l = ($('now-label') || {}).textContent || '';
    return /playing|loading|paused/i.test(l) || icon.innerHTML.includes('h4.5');
  };
  function sync() {
    const show = !bigVisible && active();
    bar.classList.toggle('on', show);
    document.body.style.paddingBottom = show ? (bar.offsetHeight + 24) + 'px' : '';
    if (!show) return;
    if (mIcon.innerHTML !== icon.innerHTML) mIcon.innerHTML = icon.innerHTML;
    mTitle.textContent = ($('now-title') || {}).textContent || '';
    loadClips();
    const [k, segs, file] = segAt(), vl = segs && CLIPS[file].unit === 'verse' && k >= 0 ? verseLabel(segs[k][2]) : '';
    const lab = (($('now-label') || {}).textContent || '').trim(), state = /loading/i.test(lab) ? 'Loading' : /paused/i.test(lab) ? 'Paused' : '';
    const parts = [vl, (($('t-cur') || {}).textContent || '0:00') + ' / ' + (($('t-dur') || {}).textContent || '')].filter(Boolean);
    mMeta.innerHTML = (state ? '<b>' + state + '</b> \u00b7 ' : '') + parts.join(' \u00b7 ');
    if (!dragging) mSeek.value = seek.value;
    mSeek.style.setProperty('--p', mSeek.value + '%');
  }
  setInterval(sync, 250);
})();

/* listen.js: keeps a recording going through interruptions and lost signal, and adds My list (see that file). */
(() => { const s = document.createElement('script'); s.src = new URL('listen.js', document.currentScript ? document.currentScript.src : location.href).href; document.head.appendChild(s); })();
