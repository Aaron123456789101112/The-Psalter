/* Mini player. Every tab has a big player near the top of the page. Once something has been started, scrolling it off
   the screen used to take the controls away with it. This keeps a small copy pinned to the bottom of the screen while
   the big player is out of sight and a recording is playing, paused part-way, or loading. It works purely through the
   big player's own controls (play, prev, next, the seek bar), so each tab's playing logic is untouched.
   It also adds "back 15 seconds" and "forward 15 seconds" buttons, to the big player (beside previous/next) and to the
   bar (either side of its seek bar). They move the page's own seek bar, the same as dragging it. */
(() => {
  const $ = id => document.getElementById(id);
  const big = document.querySelector('.player'), play = $('play'), icon = $('play-icon'), seek = $('seek');
  if (!big || !play || !icon || !seek) return;

  const css = document.createElement('style');
  css.textContent = `
.mini { position: fixed; left: 0; right: 0; bottom: 0; z-index: 20; display: none;
  background: var(--surface); color: var(--fg); border-top: 1px solid var(--line); box-shadow: 0 -6px 18px rgba(0,0,0,.12);
  padding: 8px 12px calc(8px + env(safe-area-inset-bottom)); }
.mini.on { display: block; }
.mini-row { max-width: 720px; margin: 0 auto; display: flex; align-items: center; gap: 10px; }
.mini-play { flex: none; width: 46px; height: 46px; border-radius: 50%; border: 0; background: var(--accent); color: var(--accent-ink);
  display: grid; place-items: center; cursor: pointer; }
.mini-play svg { width: 22px; height: 22px; fill: currentColor; }
.mini-btn { flex: none; width: 40px; height: 40px; border: 0; background: none; color: var(--fg); display: grid; place-items: center; cursor: pointer; }
.mini-btn svg { width: 22px; height: 22px; fill: currentColor; }
.mini-text { flex: 1; min-width: 0; display: flex; flex-direction: column; cursor: pointer; }
.mini-label { font-family: var(--ui); font-size: 11px; text-transform: uppercase; letter-spacing: .12em; color: var(--muted); }
.mini-title { font-family: var(--display); font-size: 18px; line-height: 1.2; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.mini-seekrow { max-width: 720px; margin: 4px auto 0; display: flex; align-items: center; gap: 6px; }
.mini-seek { flex: 1; min-width: 0; accent-color: var(--accent); }
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

  const bar = document.createElement('div');
  bar.className = 'mini'; bar.setAttribute('role', 'region'); bar.setAttribute('aria-label', 'Now playing');
  bar.innerHTML = `
  <div class="mini-row">
    <button class="mini-play" type="button" aria-label="Play or pause"><svg viewBox="0 0 24 24" aria-hidden="true"></svg></button>
    <div class="mini-text" title="Show the full player"><span class="mini-label"></span><span class="mini-title"></span></div>
    <button class="mini-btn" data-go="prev" type="button" aria-label="Previous"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 5h2v14H6zM20 5v14L9.5 12z"/></svg></button>
    <button class="mini-btn" data-go="next" type="button" aria-label="Next"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M16 5h2v14h-2zM4 5v14l10.5-7z"/></svg></button>
  </div>
  <div class="mini-seekrow">
    <button class="mini-btn jump" data-jump="-1" type="button" aria-label="Back 15 seconds">${back}</button>
    <input class="mini-seek" type="range" min="0" max="100" step="0.1" value="0" aria-label="Position">
    <button class="mini-btn jump" data-jump="1" type="button" aria-label="Forward 15 seconds">${fwd}</button>
  </div>`;
  document.body.appendChild(bar);

  const mIcon = bar.querySelector('.mini-play svg'), mLabel = bar.querySelector('.mini-label'),
        mTitle = bar.querySelector('.mini-title'), mSeek = bar.querySelector('.mini-seek');
  bar.querySelector('.mini-play').addEventListener('click', () => play.click());
  bar.querySelectorAll('[data-go]').forEach(b => b.addEventListener('click', () => { const t = $(b.dataset.go); if (t) t.click(); }));
  bar.querySelectorAll('[data-jump]').forEach(b => b.addEventListener('click', () => jump(JUMP * +b.dataset.jump)));
  bar.querySelector('.mini-text').addEventListener('click', () => big.scrollIntoView({ behavior: 'smooth', block: 'start' }));
  let dragging = false;
  mSeek.addEventListener('input', () => { dragging = true; seek.value = mSeek.value; seek.dispatchEvent(new Event('input', { bubbles: true })); });
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
    document.body.style.paddingBottom = show ? (bar.offsetHeight + 8) + 'px' : '';
    if (!show) return;
    if (mIcon.innerHTML !== icon.innerHTML) mIcon.innerHTML = icon.innerHTML;
    mLabel.textContent = ($('now-label') || {}).textContent || '';
    mTitle.textContent = ($('now-title') || {}).textContent || '';
    if (!dragging) mSeek.value = seek.value;
  }
  setInterval(sync, 250);
})();
