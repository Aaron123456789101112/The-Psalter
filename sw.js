/* The Psalter's service worker. Lets the app open and play with no connection.
   - The pages, the clip list and the icons are kept in the "shell" cache. They are fetched fresh whenever there is a
     connection, so new psalms show up as soon as they're published, and the cache copy is used only when offline.
   - Recordings are kept only when the listener saves them (the Offline sheet in index.html writes them into the
     "psalter-audio" cache). A saved recording is always played from the phone, including the byte ranges an
     <audio> element asks for. Anything not saved goes to the network as normal.
   - The Google fonts are kept the first time they load, so offline pages still look right. */
const SHELL = 'psalter-shell-v6';
const AUDIO = 'psalter-audio';
const FONTS = 'psalter-fonts';
const PAGES = ['./', 'index.html', 'revelation/index.html', 'judges/index.html', 'mighty/index.html', 'prayers/index.html',
  'matthew/index.html', 'proverbs/index.html', 'prophets/index.html', 'clip/clips.json', 'manifest.webmanifest',
  'icon-192.png', 'icon-512.png', 'apple-touch-icon.png', 'miniplayer.js', 'listen.js'];

self.addEventListener('install', e => {
  e.waitUntil((async () => {
    const c = await caches.open(SHELL);
    // one at a time, so a single failure doesn't stop the rest
    for (const p of PAGES) { try { const r = await fetch(p, { cache: 'reload' }); if (r.ok) await c.put(p, r); } catch (err) {} }
    await self.skipWaiting();
  })());
});

self.addEventListener('activate', e => {
  e.waitUntil((async () => {
    for (const k of await caches.keys()) if (k.startsWith('psalter-shell-') && k !== SHELL) await caches.delete(k);
    await self.clients.claim();
  })());
});

const withTimeout = (p, ms) => new Promise((ok, bad) => { const t = setTimeout(() => bad(new Error('timeout')), ms); p.then(v => { clearTimeout(t); ok(v); }, e => { clearTimeout(t); bad(e); }); });

async function fromShell(req) {
  const c = await caches.open(SHELL);
  try {
    const r = await withTimeout(fetch(req), 6000);
    if (r.ok) { c.put(req.mode === 'navigate' ? new URL(req.url).pathname : req, r.clone()); return r; }
    const hit = await c.match(req, { ignoreSearch: true }); return hit || r;
  } catch (err) {
    const u = new URL(req.url);
    const hit = await c.match(req, { ignoreSearch: true }) || await c.match(u.pathname, { ignoreSearch: true })
      || (u.pathname.endsWith('/') ? await c.match(u.pathname + 'index.html') : null)
      || (req.mode === 'navigate' ? await c.match('./') : null);
    if (hit) return hit;
    return new Response('You are offline, and this page has not been saved yet.', { status: 503, headers: { 'Content-Type': 'text/plain; charset=utf-8' } });
  }
}

async function fromAudio(req) {
  const c = await caches.open(AUDIO);
  const hit = await c.match(req.url, { ignoreSearch: true, ignoreVary: true });
  if (!hit) {
    try { return await fetch(req); }
    catch (err) { return new Response('', { status: 504, statusText: 'Offline and not saved' }); }
  }
  const range = req.headers.get('range');
  if (!range) return hit;
  const blob = await hit.blob(), size = blob.size;
  const m = /bytes=(\d*)-(\d*)/.exec(range);
  let start = 0, end = size - 1;
  if (m) {
    if (m[1] === '' && m[2] !== '') { start = Math.max(0, size - +m[2]); }   // the last N bytes
    else { start = +m[1] || 0; if (m[2] !== '') end = Math.min(+m[2], size - 1); }
  }
  if (start >= size || start > end) return new Response('', { status: 416, headers: { 'Content-Range': 'bytes */' + size } });
  return new Response(blob.slice(start, end + 1), { status: 206, statusText: 'Partial Content', headers: {
    'Content-Type': hit.headers.get('Content-Type') || 'audio/mpeg', 'Content-Length': String(end - start + 1),
    'Content-Range': 'bytes ' + start + '-' + end + '/' + size, 'Accept-Ranges': 'bytes' } });
}

async function fromFonts(req) {
  const c = await caches.open(FONTS);
  const hit = await c.match(req);
  const fresh = fetch(req).then(r => { if (r.ok || r.type === 'opaque') c.put(req, r.clone()); return r; }).catch(() => null);
  return hit || (await fresh) || new Response('', { status: 504 });
}

self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const u = new URL(req.url);
  if (u.hostname === 'fonts.googleapis.com' || u.hostname === 'fonts.gstatic.com') { e.respondWith(fromFonts(req)); return; }
  if (u.origin !== self.location.origin || !u.pathname.startsWith(new URL(self.registration.scope).pathname)) return;
  if (/\.mp3$/i.test(u.pathname)) { e.respondWith(fromAudio(req)); return; }
  e.respondWith(fromShell(req));
});
