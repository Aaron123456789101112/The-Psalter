/* Listening helpers, loaded on every tab (from miniplayer.js).
   1. Keep playing. When the phone pauses a recording by itself (a call, Siri, another app's sound) or the connection
      drops for a while (driving through bad signal), the recording picks up again where it stopped: it is retried
      for as long as needed, until the listener presses pause. A pause the listener asked for is never undone.
   2. My list (the top page only): pick readings from any collection, put them in order, and play them one after
      another from a single player in the top page, which is the part of the app a phone keeps alive longest. The
      list and the place in it are remembered, so it carries on from the same spot if the phone closes the app. The
      whole list can be saved to the phone before a drive (this uses the Offline storage, sw.js).
   3. A "+" on every reading in every tab adds it to the list (and shows a tick when it is already there). */
(() => {
  if (window.__listenJs) return; window.__listenJs = true;
  const TOP = (() => { try { return window.top && window.top.document && window.top; } catch (e) { return null; } })();
  const isTop = window === window.top;

  // ------------------------------------------------------------------ 1. keep playing
  const MP = HTMLMediaElement.prototype, origPlay = MP.play, origPause = MP.pause;
  const guarded = new WeakSet();
  MP.pause = function () { this.__byUser = true; return origPause.apply(this, arguments); };
  MP.play = function () {
    this.__byUser = false; this.__started = true; this.__tries = 0; guard(this);
    try { if (!this.__queue && TOP && TOP.PsalterQueue) TOP.PsalterQueue.otherStarted(window); } catch (e) {}
    return origPlay.apply(this, arguments);
  };
  const wanted = el => el.__started && !el.__byUser && !el.ended && !!el.getAttribute('src');
  function retryLater(el, why) {
    clearTimeout(el.__retryT);
    const n = el.__tries = (el.__tries || 0) + 1;
    const wait = Math.min(30000, [700, 1500, 3000, 5000, 8000, 12000, 20000][n - 1] || 30000);
    el.__retryT = setTimeout(() => recover(el, why), wait);
  }
  function recover(el, why) {
    if (!wanted(el)) return;
    if (!el.paused && el.readyState >= 3 && why !== 'stuck') { el.__tries = 0; return; }
    const at = el.__lastT || el.currentTime || 0;
    if (why === 'error' || why === 'stuck' || el.error) {           // the stream broke: open it again at the same place
      const s = el.getAttribute('src');
      el.addEventListener('loadedmetadata', () => { try { el.currentTime = at; } catch (e) {} }, { once: true });
      el.src = s;
    }
    const p = origPlay.call(el);
    if (p && p.then) p.then(() => { el.__tries = 0; }, () => retryLater(el, why));
  }
  function guard(el) {
    if (guarded.has(el)) return; guarded.add(el);
    el.addEventListener('timeupdate', () => { if (!el.seeking && el.currentTime > 0) el.__lastT = el.currentTime; el.__moved = Date.now(); });
    el.addEventListener('pause', () => { if (wanted(el)) retryLater(el, 'pause'); });
    el.addEventListener('error', () => { if (wanted(el)) retryLater(el, 'error'); });
    el.addEventListener('playing', () => { el.__tries = 0; clearTimeout(el.__retryT); });
    const watchStall = () => {                         // stuck loading for 15 s: the connection has gone; reopen it
      clearTimeout(el.__stallT);
      el.__stallT = setTimeout(() => { if (wanted(el) && Date.now() - (el.__moved || 0) > 14000) recover(el, 'stuck'); }, 15000);
    };
    el.addEventListener('waiting', watchStall); el.addEventListener('stalled', watchStall);
    all.add(el);
  }
  const all = new Set();
  const nudge = () => { for (const el of all) if (wanted(el) && el.paused) { el.__tries = 0; recover(el, el.error ? 'error' : 'pause'); } };
  addEventListener('online', nudge);
  addEventListener('pageshow', nudge);
  document.addEventListener('visibilitychange', () => { if (!document.hidden) nudge(); });

  // ------------------------------------------------------------------ 3. "+" on every reading
  const pageKey = (location.pathname.match(/\/(revelation|judges|prayers|matthew|proverbs|prophets|mighty)\//) || [])[1] || 'psalter';
  function addButtons() {
    const Q = TOP && TOP.PsalterQueue; if (!Q) return;
    let T; try { T = (0, eval)('TRACKS'); } catch (e) { return; }
    if (!Array.isArray(T)) return;
    T.forEach((t, i) => {
      const row = document.getElementById('track-' + i); if (!row || !row.parentElement) return;
      const url = new URL(t.file, location.href).href;
      let b = row.parentElement.querySelector(':scope > .q-add');
      if (!b) {
        b = document.createElement('button'); b.type = 'button'; b.className = 'q-add';
        b.addEventListener('click', e => { e.stopPropagation(); Q.toggle({ u: url, t: t.title, k: pageKey, d: t.dur || 0 }); });
        row.after(b);
      }
      const on = Q.has(url);
      b.classList.toggle('on', on);
      b.setAttribute('aria-label', (on ? 'Remove from my list: ' : 'Add to my list: ') + t.title);
      b.innerHTML = on ? '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12.5l4.2 4.2L19 7"/></svg>'
                       : '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 5v14M5 12h14"/></svg>';
    });
  }
  const css = document.createElement('style');
  css.textContent = `
li:has(> .q-add) { display: flex; align-items: stretch; }
li:has(> .q-add) > .track { flex: 1; min-width: 0; }
.q-add { flex: none; width: 48px; border: 0; background: none; color: var(--muted); cursor: pointer; display: grid; place-items: center; border-radius: 10px; }
.q-add svg { width: 22px; height: 22px; fill: none; stroke: currentColor; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; }
.q-add.on { color: var(--accent); }
.q-add:focus-visible { outline: 2px solid var(--accent); outline-offset: -2px; }`;
  document.head.appendChild(css);
  const startButtons = () => {
    addButtons();
    const list = document.getElementById('list');
    if (list && 'MutationObserver' in window) new MutationObserver(() => { clearTimeout(startButtons.t); startButtons.t = setTimeout(addButtons, 50); }).observe(list, { childList: true });
    addEventListener('psalter-queue', addButtons);
  };

  if (!isTop) {
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', () => setTimeout(startButtons, 0)); else setTimeout(startButtons, 0);
    return;
  }

  // ------------------------------------------------------------------ 2. my list (top page only)
  const $ = id => document.getElementById(id);
  const KEY = 'psalter-list';
  const NAMES = { psalter: 'The Psalter', rev: 'Revelation', revelation: 'Revelation', judges: 'Judges', mighty: 'Mighty Men', prayers: 'Prayers',
    matthew: 'Matthew', proverbs: 'Proverbs', prophets: 'The Prophets' };
  const COLS = [['psalter', 'The Psalter', 'index.html'], ['revelation', 'Revelation', 'revelation/index.html'], ['judges', 'Judges by the Fire', 'judges/index.html'],
    ['mighty', 'The Mighty Men of David', 'mighty/index.html'], ['prayers', 'Prayers', 'prayers/index.html'], ['matthew', 'Matthew', 'matthew/index.html'],
    ['proverbs', 'Proverbs', 'proverbs/index.html'], ['prophets', 'The Prophets', 'prophets/index.html']];
  let S = { items: [], i: 0, t: 0 };
  try { const v = JSON.parse(localStorage.getItem(KEY) || 'null'); if (v && Array.isArray(v.items)) S = { items: v.items, i: +v.i || 0, t: +v.t || 0 }; } catch (e) {}
  if (S.i >= S.items.length) { S.i = 0; S.t = 0; }
  let savedAt = 0;
  const save = (now) => { if (!now && Date.now() - savedAt < 3000) return; savedAt = Date.now(); try { localStorage.setItem(KEY, JSON.stringify(S)); } catch (e) {} };
  const fmt = s => { s = Math.max(0, Math.round(s || 0)); const h = Math.floor(s / 3600), m = Math.floor(s % 3600 / 60), x = s % 60;
    return h ? h + ':' + String(m).padStart(2, '0') + ':' + String(x).padStart(2, '0') : m + ':' + String(x).padStart(2, '0'); };
  const long = s => { const m = Math.round(s / 60); return m >= 60 ? Math.floor(m / 60) + ' h ' + (m % 60) + ' min' : m + ' min'; };

  const qa = new Audio(); qa.preload = 'auto'; qa.__queue = true;
  let loadedIdx = -1, engaged = false, lastOther = null;

  function frames() { return [...document.querySelectorAll('iframe')]; }
  function tellAll() {
    try { dispatchEvent(new Event('psalter-queue')); } catch (e) {}
    for (const f of frames()) { try { f.contentWindow.dispatchEvent(new Event('psalter-queue')); } catch (e) {} }
  }
  function pauseOthers() {
    try { if (typeof window.pause === 'function') window.pause(); } catch (e) {}
    for (const f of frames()) { try { const w = f.contentWindow; if (w && typeof w.pause === 'function') w.pause(); } catch (e) {} }
  }
  function lighten() {   // free the memory of tabs that aren't on screen, so the phone is less likely to close the app
    for (const f of frames()) {
      if (!f.getAttribute('src') || f.offsetParent !== null || getComputedStyle(f).display !== 'none') continue;
      try { f.src = 'about:blank'; f.removeAttribute('src'); } catch (e) {}
    }
  }

  async function qplay(i, at) {
    if (!S.items.length) return;
    if (i != null) { S.i = Math.max(0, Math.min(S.items.length - 1, i)); S.t = at || 0; }
    pauseOthers(); engaged = true;
    const it = S.items[S.i];
    if (loadedIdx !== S.i || qa.getAttribute('src') !== it.u) {
      qa.src = it.u; loadedIdx = S.i;
      const t0 = S.t; if (t0 > 0) qa.addEventListener('loadedmetadata', () => { try { qa.currentTime = t0; } catch (e) {} }, { once: true });
    } else if (Math.abs(qa.currentTime - S.t) > 1 && S.t > 0) { try { qa.currentTime = S.t; } catch (e) {} }
    session(); paint(); save(true);
    try { await qa.play(); } catch (e) { if (e && e.name === 'NotAllowedError') status('Press play to start.'); }
    paint(); setTimeout(lighten, 4000);
  }
  function qpause() { qa.pause(); S.t = qa.currentTime || S.t; save(true); paint(); }
  function qnext() { if (S.i + 1 < S.items.length) qplay(S.i + 1, 0); }
  function qprev() { if ((qa.currentTime || 0) > 5) { qa.currentTime = 0; S.t = 0; paint(); } else if (S.i > 0) qplay(S.i - 1, 0); }
  qa.addEventListener('ended', () => {
    if (S.i + 1 < S.items.length) qplay(S.i + 1, 0);
    else { S.i = 0; S.t = 0; loadedIdx = -1; save(true); paint(); status('Finished the list.'); }
  });
  qa.addEventListener('timeupdate', () => { if (!qa.seeking && loadedIdx === S.i) { S.t = qa.currentTime; save(); } tick(); });
  for (const ev of ['play', 'pause', 'playing', 'waiting']) qa.addEventListener(ev, paint);

  // the lock screen and car controls belong to the top page; send them to whatever is playing
  function other() { try { return lastOther && lastOther.document ? lastOther : window; } catch (e) { return window; } }
  function session() {
    if (!('mediaSession' in navigator)) return;
    try {
      const it = engaged && S.items[S.i];
      if (it) navigator.mediaSession.metadata = new MediaMetadata({ title: it.t, artist: NAMES[it.k] || 'The Psalter', album: 'My list · ' + (S.i + 1) + ' of ' + S.items.length,
        artwork: [{ src: new URL('icon-512.png', location.href).href, sizes: '512x512', type: 'image/png' }] });
      navigator.mediaSession.playbackState = engaged ? (qa.paused ? 'paused' : 'playing') : navigator.mediaSession.playbackState;
    } catch (e) {}
  }
  const call = (w, name, ...a) => { try { if (w && typeof w[name] === 'function') return w[name](...a); } catch (e) {} };
  try {
    if ('mediaSession' in navigator) {
      const ms = navigator.mediaSession;
      const set = (a, f) => { try { ms.setActionHandler(a, f); } catch (e) {} };
      set('play', () => { if (engaged) qplay(); else call(other(), 'start'); });
      set('pause', () => { if (engaged) qpause(); else call(other(), 'pause'); });
      set('nexttrack', () => { if (engaged) qnext(); else call(other(), 'next', false); });
      set('previoustrack', () => { if (engaged) qprev(); else call(other(), 'prev'); });
      set('seekto', d => { if (engaged) { try { qa.currentTime = d.seekTime || 0; } catch (e) {} } else seekOther(d.seekTime || 0, true); });
      set('seekbackward', d => { if (engaged) qa.currentTime = Math.max(0, qa.currentTime - (d.seekOffset || 15)); else seekOther(-(d.seekOffset || 15)); });
      set('seekforward', d => { if (engaged) qa.currentTime = Math.min(qa.duration || 1e9, qa.currentTime + (d.seekOffset || 15)); else seekOther(d.seekOffset || 15); });
    }
  } catch (e) {}
  function seekOther(v, absolute) {   // through the tab's own seek bar, the way miniplayer.js does it
    const w = other(); if (!w) return;
    try {
      const d = w.document, seek = d.getElementById('seek'), dur = (d.getElementById('t-dur') || {}).textContent || '';
      const total = dur.split(':').map(Number).reduce((a, b) => a * 60 + b, 0); if (!(total > 0)) return;
      const now = seek.value / 100 * total, to = Math.max(0, Math.min(total - 0.5, absolute ? v : now + v));
      seek.value = (to / total * 100).toFixed(3);
      seek.dispatchEvent(new Event('input', { bubbles: true })); seek.dispatchEvent(new Event('change', { bubbles: true }));
    } catch (e) {}
  }

  window.PsalterQueue = {
    has: u => S.items.some(x => x.u === u),
    toggle(item) {
      const k = S.items.findIndex(x => x.u === item.u);
      if (k >= 0) removeAt(k); else { S.items.push(item); save(true); changed(); toast('Added to your list: ' + item.t); }
    },
    otherStarted(w) {   // a tab's own player started: it takes over from the list
      lastOther = w;
      if (engaged) { qa.pause(); S.t = qa.currentTime || S.t; engaged = false; save(true); paint(); }
      // mirror the tab's lock-screen title in the top page
      setTimeout(() => { try { const m = w.navigator.mediaSession && w.navigator.mediaSession.metadata;
        if (m && w !== window) navigator.mediaSession.metadata = new MediaMetadata({ title: m.title, artist: m.artist, album: m.album }); } catch (e) {} }, 300);
    },
  };
  function removeAt(k) {
    const wasCur = k === S.i;
    S.items.splice(k, 1);
    if (k < S.i) S.i--;
    if (wasCur) { if (engaged && !qa.paused) { qa.pause(); } loadedIdx = -1; S.t = 0; if (S.i >= S.items.length) S.i = 0; engaged = engaged && S.items.length > 0; }
    if (!S.items.length) { qa.pause(); qa.removeAttribute('src'); qa.load(); engaged = false; S = { items: [], i: 0, t: 0 }; }
    save(true); changed();
  }
  function move(k, d) {
    const j = k + d; if (j < 0 || j >= S.items.length) return;
    [S.items[k], S.items[j]] = [S.items[j], S.items[k]];
    if (S.i === k) S.i = j; else if (S.i === j) S.i = k;
    if (loadedIdx === k) loadedIdx = j; else if (loadedIdx === j) loadedIdx = k;
    save(true); changed();
  }
  function changed() { tellAll(); paint(); if (!$('q').hidden) renderSheet(); }

  // ------------------------------------------------------------------ the bar and the sheet
  const style = document.createElement('style');
  style.textContent = `
.tab.q-tab { display: inline-flex; align-items: center; gap: 6px; }
.tab.q-tab svg { width: 16px; height: 16px; fill: none; stroke: currentColor; stroke-width: 2; stroke-linecap: round; }
.tab.q-tab .q-count { font-variant-numeric: tabular-nums; min-width: 1.4em; padding: 0 5px; border-radius: 999px; background: var(--accent); color: var(--accent-ink); font-size: 12px; line-height: 1.5; text-align: center; }
.tab.q-tab .q-count:empty { display: none; }
.qbar { position: fixed; left: 0; right: 0; bottom: 0; z-index: 25; display: none; box-sizing: border-box;
  padding: 10px max(12px, env(safe-area-inset-left)) calc(10px + env(safe-area-inset-bottom)) max(12px, env(safe-area-inset-right));
  background: color-mix(in srgb, var(--surface) 96%, transparent); -webkit-backdrop-filter: blur(14px); backdrop-filter: blur(14px);
  border-top: 1px solid var(--line); color: var(--fg); box-shadow: 0 -8px 24px rgba(0,0,0,.12); }
.qbar.on { display: block; }
.qbar-in { max-width: 720px; margin: 0 auto; display: flex; flex-direction: column; gap: 4px; }
.qbar-row { display: flex; align-items: center; gap: 8px; }
.qbar-text { flex: 1; min-width: 0; display: flex; flex-direction: column; cursor: pointer; background: none; border: 0; color: inherit; text-align: left; padding: 0; font: inherit; }
.qbar-label { font-family: var(--ui); font-size: 12px; letter-spacing: .12em; text-transform: uppercase; color: var(--accent); }
.qbar-title { font-family: var(--display); font-size: 19px; line-height: 1.2; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.qbar button.qb { flex: none; width: 46px; height: 46px; border: 0; border-radius: 50%; background: none; color: var(--fg); display: grid; place-items: center; cursor: pointer; }
.qbar button.qb svg { width: 24px; height: 24px; fill: currentColor; }
.qbar button.qb.play { width: 52px; height: 52px; background: var(--accent); color: var(--accent-ink); }
.qbar button.qb:focus-visible, .qbar-text:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
.qbar-seek { display: flex; align-items: center; gap: 10px; font-family: var(--ui); font-size: 13px; color: var(--muted); font-variant-numeric: tabular-nums; }
.qbar-seek input { flex: 1; min-width: 0; accent-color: var(--accent); height: 26px; }
html.fs-child .qbar { display: none !important; }
html.q-on .mini { bottom: calc(var(--qbar-h, 0px) + 8px) !important; }
#q [hidden] { display: none !important; }
.q-list { list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 8px; }
.q-item { display: flex; align-items: center; gap: 6px; border: 1px solid var(--line); border-radius: 12px; background: var(--surface); padding: 6px 6px 6px 12px; }
.q-item.cur { border-color: var(--accent); }
.q-item .q-n { flex: none; width: 1.6em; font-family: var(--ui); font-weight: 700; color: var(--accent); font-variant-numeric: tabular-nums; }
.q-item .q-txt { flex: 1; min-width: 0; display: flex; flex-direction: column; background: none; border: 0; color: inherit; text-align: left; font: inherit; cursor: pointer; padding: 4px 0; }
.q-item .q-t { font-family: var(--display); font-size: 19px; line-height: 1.2; }
.q-item .q-m { font-family: var(--ui); font-size: 13.5px; color: var(--muted); }
.q-item .q-m b { color: var(--accent); font-weight: 600; }
.q-item button.qi { flex: none; width: 40px; height: 40px; border-radius: 50%; border: 0; background: none; color: var(--muted); cursor: pointer; display: grid; place-items: center; }
.q-item button.qi svg { width: 20px; height: 20px; fill: none; stroke: currentColor; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; }
.q-item button.qi:disabled { opacity: .25; cursor: default; }
.q-item button.qi:focus-visible, .q-item .q-txt:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
.q-empty { font-family: var(--ui); font-size: 16px; color: var(--muted); margin: 0; padding: 14px 16px; border: 1px dashed var(--line); border-radius: 12px; }
.q-actions { display: flex; flex-wrap: wrap; gap: 10px; }
.q-h3 { font-family: var(--display); font-weight: 400; font-size: 24px; margin: 8px 0 0; }
.q-cols { display: flex; flex-direction: column; gap: 10px; }
.q-col { border: 1px solid var(--line); border-radius: 14px; background: var(--surface); }
.q-col > summary { list-style: none; cursor: pointer; padding: 14px 16px; font-family: var(--display); font-size: 21px; display: flex; justify-content: space-between; align-items: center; gap: 10px; }
.q-col > summary::-webkit-details-marker { display: none; }
.q-col > summary span { font-family: var(--ui); font-size: 14px; color: var(--muted); }
.q-col[open] > summary { border-bottom: 1px solid var(--line); }
.q-tracks { list-style: none; margin: 0; padding: 4px 6px 8px; }
.q-tr { display: flex; align-items: center; gap: 8px; width: 100%; border: 0; background: none; color: inherit; text-align: left; cursor: pointer; padding: 10px 10px; border-radius: 10px; font: inherit; }
.q-tr:focus-visible { outline: 2px solid var(--accent); outline-offset: -2px; }
.q-tr .q-t { flex: 1; min-width: 0; font-family: var(--body); font-size: 17px; }
.q-tr .q-d { font-family: var(--ui); font-size: 14px; color: var(--muted); font-variant-numeric: tabular-nums; }
.q-tr svg { flex: none; width: 22px; height: 22px; fill: none; stroke: var(--muted); stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; }
.q-tr.on svg { stroke: var(--accent); }
.q-tr.on .q-t { color: var(--accent); }
.q-toast { position: fixed; left: 50%; bottom: calc(var(--qbar-h, 0px) + 24px + env(safe-area-inset-bottom)); transform: translateX(-50%); z-index: 45; max-width: calc(100% - 32px);
  font-family: var(--ui); font-size: 15px; padding: 10px 16px; border-radius: 999px; background: var(--fg); color: var(--bg); box-shadow: 0 6px 20px rgba(0,0,0,.2);
  opacity: 0; transition: opacity .25s; pointer-events: none; }
.q-toast.on { opacity: 1; }`;
  document.head.appendChild(style);

  const I = {
    play: '<path d="M7 4.5v15l13-7.5z"/>', pause: '<path d="M6 4.5h4.5v15H6zM13.5 4.5H18v15h-4.5z"/>',
    prev: '<path d="M6 5h2v14H6zM20 5v14L9 12z"/>', next: '<path d="M16 5h2v14h-2zM4 5v14l11-7z"/>',
    up: '<path d="M12 19V5M6 11l6-6 6 6"/>', down: '<path d="M12 5v14M6 13l6 6 6-6"/>', x: '<path d="M6 6l12 12M18 6L6 18"/>',
    plus: '<path d="M12 5v14M5 12h14"/>', tick: '<path d="M5 12.5l4.2 4.2L19 7"/>', list: '<path d="M4 6h16M4 12h16M4 18h10"/>',
  };
  // tab bar button
  const tabBtn = document.createElement('button');
  tabBtn.className = 'tab q-tab'; tabBtn.id = 'q-open'; tabBtn.type = 'button'; tabBtn.setAttribute('aria-haspopup', 'dialog');
  tabBtn.innerHTML = `<svg viewBox="0 0 24 24" aria-hidden="true">${I.list}</svg>My list <span class="q-count"></span>`;
  const ofBtn = $('of-open'), bar0 = document.querySelector('.tabs');
  if (ofBtn) ofBtn.before(tabBtn); else if (bar0) bar0.appendChild(tabBtn);
  tabBtn.addEventListener('click', openSheet);

  // the bar
  const bar = document.createElement('div'); bar.className = 'qbar'; bar.setAttribute('role', 'region'); bar.setAttribute('aria-label', 'My list player');
  bar.innerHTML = `<div class="qbar-in"><div class="qbar-row">
    <button class="qbar-text" type="button" aria-label="Open my list"><span class="qbar-label"></span><span class="qbar-title"></span></button>
    <button class="qb" data-a="prev" type="button" aria-label="Previous in my list"><svg viewBox="0 0 24 24" aria-hidden="true">${I.prev}</svg></button>
    <button class="qb play" data-a="play" type="button" aria-label="Play my list"><svg viewBox="0 0 24 24" aria-hidden="true">${I.play}</svg></button>
    <button class="qb" data-a="next" type="button" aria-label="Next in my list"><svg viewBox="0 0 24 24" aria-hidden="true">${I.next}</svg></button>
  </div><div class="qbar-seek"><span class="q-cur">0:00</span><input type="range" min="0" max="1000" value="0" step="1" aria-label="Position"><span class="q-dur">0:00</span></div></div>`;
  document.body.appendChild(bar);
  const spacer = document.createElement('div'); spacer.setAttribute('aria-hidden', 'true'); document.body.appendChild(spacer);
  const bseek = bar.querySelector('input'); let dragging = false;
  bar.querySelector('.qbar-text').addEventListener('click', openSheet);
  bar.addEventListener('click', e => { const b = e.target.closest('.qb'); if (!b) return; const a = b.dataset.a;
    if (a === 'play') { if (engaged && !qa.paused) qpause(); else qplay(); } else if (a === 'next') qnext(); else qprev(); });
  bseek.addEventListener('input', () => { dragging = true; bar.querySelector('.q-cur').textContent = fmt(bseek.value / 1000 * (qa.duration || curDur())); });
  bseek.addEventListener('change', () => { dragging = false; const t = bseek.value / 1000 * (qa.duration || curDur());
    if (loadedIdx === S.i) { try { qa.currentTime = t; } catch (e) {} } S.t = t; save(true); tick(); });
  const curDur = () => (S.items[S.i] || {}).d || 0;

  let barShown = false;
  function layout() {
    const h = barShown && !document.documentElement.classList.contains('fs-child') ? bar.offsetHeight : 0;
    document.documentElement.classList.toggle('q-on', barShown);
    document.documentElement.style.setProperty('--qbar-h', h + 'px');
    spacer.style.height = h ? (h + 16) + 'px' : '0';
    for (const f of frames()) {
      const top = f.style.top || '0px';
      if (h) f.style.setProperty('height', `calc(100dvh - ${top} - ${h}px)`, 'important'); else f.style.removeProperty('height');
    }
    if (!h) try { dispatchEvent(new Event('resize')); } catch (e) {}   // the tab code puts its own heights back
  }
  function paint() {
    const n = S.items.length;
    tabBtn.querySelector('.q-count').textContent = n ? String(n) : '';
    const show = n > 0 && (engaged || S.t > 0 || S.i > 0);
    if (show !== barShown) { barShown = show; bar.classList.toggle('on', show); layout(); }
    if (!n) return;
    const it = S.items[S.i], on = engaged && !qa.paused;
    bar.querySelector('.qbar-label').textContent = 'My list · ' + (S.i + 1) + ' of ' + n + (engaged ? (on ? '' : ' · paused') : ' · ready to resume');
    bar.querySelector('.qbar-title').textContent = it.t;
    const pb = bar.querySelector('.qb.play'); pb.innerHTML = `<svg viewBox="0 0 24 24" aria-hidden="true">${on ? I.pause : I.play}</svg>`;
    pb.setAttribute('aria-label', on ? 'Pause my list' : 'Play my list');
    bar.querySelector('[data-a="prev"]').disabled = S.i === 0 && (qa.currentTime || 0) < 5;
    bar.querySelector('[data-a="next"]').disabled = S.i + 1 >= n;
    session(); tick();
    if (!$('q').hidden) paintSheetState();
  }
  function tick() {
    if (!barShown || dragging) return;
    const d = (loadedIdx === S.i && qa.duration) || curDur(), t = loadedIdx === S.i ? qa.currentTime : S.t;
    bseek.value = d ? Math.round(t / d * 1000) : 0;
    bar.querySelector('.q-cur').textContent = fmt(t); bar.querySelector('.q-dur').textContent = fmt(d);
  }
  setInterval(() => { if (engaged && !qa.paused) tick(); }, 500);
  addEventListener('resize', () => { if (barShown) setTimeout(layout, 0); });
  if ('MutationObserver' in window) new MutationObserver(() => { if (barShown) layout(); }).observe(document.documentElement, { attributes: true, attributeFilter: ['class'] });

  let toastEl = null, toastT = 0;
  function toast(msg) {
    if (!toastEl) { toastEl = document.createElement('div'); toastEl.className = 'q-toast'; toastEl.setAttribute('role', 'status'); document.body.appendChild(toastEl); }
    toastEl.textContent = msg; toastEl.classList.add('on'); clearTimeout(toastT); toastT = setTimeout(() => toastEl.classList.remove('on'), 1800);
  }

  // the sheet
  const sheet = document.createElement('section');
  sheet.className = 'cm'; sheet.id = 'q'; sheet.hidden = true; sheet.setAttribute('role', 'dialog'); sheet.setAttribute('aria-modal', 'true'); sheet.setAttribute('aria-labelledby', 'q-h');
  sheet.innerHTML = `<div class="cm-in">
    <div class="cm-head"><h2 id="q-h">My list</h2><button class="cm-x" id="q-close" type="button">Close</button></div>
    <p class="cm-lede">Pick what to listen to, from any collection, and it plays straight through, one after another. Handy before a drive.</p>
    <p class="of-sum" id="q-sum"></p>
    <ol class="q-list" id="q-items"></ol>
    <div class="q-actions">
      <button class="cm-btn go" id="q-play" type="button">Play my list</button>
      <button class="cm-btn" id="q-save" type="button" hidden>Save it on this phone</button>
      <button class="cm-btn" id="q-clear" type="button">Clear the list</button>
    </div>
    <div class="cm-prog" id="q-prog" hidden><progress id="q-bar" max="1" value="0"></progress><span id="q-ptext"></span></div>
    <p class="cm-status" id="q-status" role="status"></p>
    <p class="cm-help" id="q-savehelp" hidden>Saving puts the recordings on the phone, so the list keeps playing where there is no signal. They stay saved until you remove them on the Offline page.</p>
    <h3 class="q-h3">Add readings</h3>
    <p class="cm-help">Open a collection and tap a reading to add it. Tap it again to take it off. You can also tap the + beside any reading on its own tab.</p>
    <div class="q-cols" id="q-cols"></div>
  </div>`;
  document.body.appendChild(sheet);
  const status = m => { const s = $('q-status'); if (s) s.textContent = m || ''; if (m && sheet.hidden) toast(m); };
  $('q-close').addEventListener('click', closeSheet);
  sheet.addEventListener('keydown', e => { if (e.key === 'Escape') closeSheet(); });
  $('q-play').addEventListener('click', () => { if (engaged && !qa.paused) qpause(); else { closeSheet(); qplay(); } });
  $('q-clear').addEventListener('click', () => { if (!S.items.length) return; if (!confirm('Clear your whole list?')) return;
    qa.pause(); qa.removeAttribute('src'); qa.load(); engaged = false; loadedIdx = -1; S = { items: [], i: 0, t: 0 }; save(true); changed(); });
  $('q-save').addEventListener('click', saveList);
  let lastFocus = null;
  function openSheet() { lastFocus = document.activeElement; sheet.hidden = false; document.documentElement.classList.add('cm-open'); renderSheet(); loadCatalog(); $('q-close').focus(); }
  function closeSheet() { sheet.hidden = true; document.documentElement.classList.remove('cm-open'); try { lastFocus && lastFocus.focus(); } catch (e) {} }

  let saved = new Set();
  const canSave = () => 'caches' in window && !!(navigator.serviceWorker && navigator.serviceWorker.controller);
  async function readSaved() {
    saved = new Set(); if (!('caches' in window)) return;
    try { const c = await caches.open('psalter-audio'); for (const r of await c.keys()) saved.add(r.url); } catch (e) {}
  }
  function renderSheet() {
    const ol = $('q-items'); ol.innerHTML = '';
    if (!S.items.length) {
      const p = document.createElement('li'); p.className = 'q-empty'; p.textContent = 'Your list is empty. Add readings below.'; ol.appendChild(p);
    }
    S.items.forEach((it, k) => {
      const li = document.createElement('li'); li.className = 'q-item' + (k === S.i && (engaged || S.t > 0) ? ' cur' : '');
      li.innerHTML = `<span class="q-n">${k + 1}</span><button class="q-txt" type="button"><span class="q-t"></span><span class="q-m"></span></button>
        <button class="qi" data-a="up" type="button" aria-label="Move up"${k === 0 ? ' disabled' : ''}><svg viewBox="0 0 24 24" aria-hidden="true">${I.up}</svg></button>
        <button class="qi" data-a="down" type="button" aria-label="Move down"${k === S.items.length - 1 ? ' disabled' : ''}><svg viewBox="0 0 24 24" aria-hidden="true">${I.down}</svg></button>
        <button class="qi" data-a="x" type="button" aria-label="Remove"><svg viewBox="0 0 24 24" aria-hidden="true">${I.x}</svg></button>`;
      li.querySelector('.q-t').textContent = it.t;
      li.querySelector('.q-txt').setAttribute('aria-label', 'Play ' + it.t);
      li.querySelector('.q-txt').addEventListener('click', () => { closeSheet(); qplay(k, k === S.i ? S.t : 0); });
      li.querySelector('[data-a="up"]').addEventListener('click', () => move(k, -1));
      li.querySelector('[data-a="down"]').addEventListener('click', () => move(k, 1));
      li.querySelector('[data-a="x"]').addEventListener('click', () => removeAt(k));
      ol.appendChild(li);
    });
    paintSheetState();
    readSaved().then(paintSheetState);
    renderCols();
  }
  function paintSheetState() {
    const n = S.items.length, total = S.items.reduce((a, x) => a + (x.d || 0), 0);
    $('q-sum').textContent = n ? n + (n === 1 ? ' reading · ' : ' readings · ') + long(total) : '';
    $('q-items').querySelectorAll('.q-item').forEach((li, k) => {
      const it = S.items[k]; if (!it) return;
      const here = k === S.i && (engaged || S.t > 0), m = li.querySelector('.q-m');
      m.innerHTML = '';
      if (here) { const b = document.createElement('b'); b.textContent = (engaged && !qa.paused ? 'Playing' : 'Up to ' + fmt(S.t)) + ' · '; m.appendChild(b); }
      m.appendChild(document.createTextNode((NAMES[it.k] || '') + ' · ' + fmt(it.d) + (saved.has(it.u) ? ' · saved on phone' : '')));
      li.classList.toggle('cur', here);
    });
    $('q-play').disabled = !n;
    $('q-play').textContent = engaged && !qa.paused ? 'Pause' : (S.t > 0 || S.i > 0 ? 'Carry on with my list' : 'Play my list');
    $('q-clear').disabled = !n;
    const unsaved = S.items.filter(x => !saved.has(x.u)).length;
    $('q-save').hidden = !canSave() || !n || !unsaved || saving;
    $('q-save').textContent = unsaved === n ? 'Save it on this phone' : 'Save the rest on this phone';
    $('q-savehelp').hidden = $('q-save').hidden;
  }
  let saving = false;
  async function saveList() {
    if (saving) return; saving = true; paintSheetState();
    const todo = S.items.filter(x => !saved.has(x.u)); let done = 0, failed = 0;
    $('q-prog').hidden = false; $('q-bar').value = 0; status('');
    try {
      const c = await caches.open('psalter-audio');
      for (const it of todo) {
        $('q-ptext').textContent = (done + 1) + ' of ' + todo.length + ': ' + it.t;
        try { const r = await fetch(it.u, { cache: 'no-store' }); if (!r.ok) throw new Error('HTTP ' + r.status); await c.put(it.u, r); saved.add(it.u); }
        catch (e) { failed++; }
        done++; $('q-bar').value = done / todo.length; paintSheetState();
      }
    } catch (e) { failed = todo.length; }
    saving = false; $('q-prog').hidden = true;
    status(failed ? failed + ' couldn’t be saved. Check the connection and press Save again.' : 'Saved. Your list will play even with no signal.');
    paintSheetState();
  }

  // every collection's readings, read from the tab pages themselves
  let catalog = null, catalogLoading = false;
  const unq = s => s.replace(/\\(.)/g, '$1');
  function parseTracks(html, base) {
    const a = html.indexOf('const TRACKS = ['); if (a < 0) return [];
    const b = html.indexOf('\n];', a), body = html.slice(a, b < 0 ? undefined : b), out = [];
    for (const m of body.matchAll(/\{[^\n]*?file:\s*"([^"]+)"[^\n]*\}/g)) {
      const line = m[0], t = /title:\s*"((?:[^"\\]|\\.)*)"/.exec(line), d = /dur:\s*(\d+)/.exec(line), g = /group:\s*"((?:[^"\\]|\\.)*)"/.exec(line);
      out.push({ t: t ? unq(t[1]) : m[1], u: new URL(m[1], base).href, d: d ? +d[1] : 0, g: g ? unq(g[1]) : '' });
    }
    return out;
  }
  async function loadCatalog() {
    if (catalog || catalogLoading) return; catalogLoading = true;
    $('q-cols').innerHTML = '<p class="cm-help">Loading the collections…</p>';
    const out = [];
    for (const [k, name, page] of COLS) {
      const base = new URL(page, location.href); let tracks = [];
      if (k === 'psalter') { try { const T = (0, eval)('TRACKS'); tracks = T.map(t => ({ t: t.title, u: new URL(t.file, location.href).href, d: t.dur || 0, g: '' })); } catch (e) {} }
      if (!tracks.length) { try { const r = await fetch(base.href); if (r.ok) tracks = parseTracks(await r.text(), base); } catch (e) {} }
      out.push({ k, name, tracks });
    }
    catalog = out; catalogLoading = false; renderCols();
  }
  function renderCols() {
    if (!catalog) return;
    const box = $('q-cols'), open = new Set([...box.querySelectorAll('details[open]')].map(d => d.dataset.k));
    box.innerHTML = '';
    for (const c of catalog) {
      if (!c.tracks.length) continue;
      const d = document.createElement('details'); d.className = 'q-col'; d.dataset.k = c.k; if (open.has(c.k)) d.open = true;
      const inList = c.tracks.filter(t => PsalterQueue.has(t.u)).length;
      d.innerHTML = `<summary></summary><ul class="q-tracks"></ul>`;
      d.querySelector('summary').innerHTML = `${esc(c.name)}<span>${inList ? inList + ' in your list · ' : ''}${c.tracks.length}</span>`;
      const ul = d.querySelector('ul');
      for (const t of c.tracks) {
        const li = document.createElement('li'), b = document.createElement('button'), on = PsalterQueue.has(t.u);
        b.type = 'button'; b.className = 'q-tr' + (on ? ' on' : '');
        b.innerHTML = `<svg viewBox="0 0 24 24" aria-hidden="true">${on ? I.tick : I.plus}</svg><span class="q-t"></span><span class="q-d">${fmt(t.d)}</span>`;
        b.querySelector('.q-t').textContent = (t.g ? t.g + ' · ' : '') + t.t;
        b.setAttribute('aria-pressed', String(on));
        b.addEventListener('click', () => PsalterQueue.toggle({ u: t.u, t: t.t, k: c.k, d: t.d }));
        li.appendChild(b); ul.appendChild(li);
      }
      box.appendChild(d);
    }
  }
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]);

  paint();
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', () => setTimeout(startButtons, 0)); else setTimeout(startButtons, 0);
  // tabs that load later get their + buttons from their own copy of this file; tell them the list once they're up
  for (const f of frames()) f.addEventListener('load', () => setTimeout(tellAll, 200));
})();
