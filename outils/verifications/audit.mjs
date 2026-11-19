import { spawn } from 'node:child_process';
const [chrome, url, outDir] = process.argv.slice(2);
const port = 9340;
const proc = spawn(chrome, ['--headless=new', '--disable-gpu', `--remote-debugging-port=${port}`, `--user-data-dir=${outDir}/profile-audit-${Date.now()}`, '--no-first-run', 'about:blank'], { stdio: 'ignore' });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
let target; for (let i = 0; i < 50 && !target; i++) { try { target = (await (await fetch(`http://127.0.0.1:${port}/json/list`)).json()).find((t) => t.type === 'page'); } catch {} if (!target) await sleep(200); }
const ws = new WebSocket(target.webSocketDebuggerUrl); await new Promise((r) => ws.addEventListener('open', r));
let id = 0; const pending = new Map(); let loaded = false; const errors = []; const requests = new Map();
ws.addEventListener('message', (e) => { const m = JSON.parse(e.data);
  if (m.id && pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); }
  if (m.method === 'Page.loadEventFired') loaded = true;
  if (m.method === 'Runtime.exceptionThrown') errors.push(m.params.exceptionDetails.text);
  if (m.method === 'Log.entryAdded' && m.params.entry.level === 'error') errors.push(m.params.entry.text.slice(0, 120));
  if (m.method === 'Network.responseReceived') requests.set(m.params.requestId, { url: m.params.response.url, type: m.params.type });
  if (m.method === 'Network.loadingFinished' && requests.has(m.params.requestId)) requests.get(m.params.requestId).bytes = m.params.encodedDataLength; });
const send = (method, params = {}) => new Promise((r) => { const i = ++id; pending.set(i, r); ws.send(JSON.stringify({ id: i, method, params })); });
const evaluate = async (expr) => (await send('Runtime.evaluate', { expression: expr, awaitPromise: true, returnByValue: true })).result?.result?.value;
await send('Page.enable'); await send('Runtime.enable'); await send('Log.enable'); await send('Network.enable');
await send('Network.setCacheDisabled', { cacheDisabled: true });
// Conditions proches du test mobile de Lighthouse : 4G lente + processeur ralenti x4
await send('Network.emulateNetworkConditions', { offline: false, latency: 150, downloadThroughput: 1.6 * 1024 * 1024 / 8, uploadThroughput: 750 * 1024 / 8 });
await send('Emulation.setCPUThrottlingRate', { rate: 4 });
await send('Emulation.setDeviceMetricsOverride', { width: 412, height: 823, deviceScaleFactor: 1.75, mobile: true });
await send('Page.addScriptToEvaluateOnNewDocument', { source: `window.__lcp = 0; window.__cls = 0;
  new PerformanceObserver(l => { for (const e of l.getEntries()) window.__lcp = e.startTime; }).observe({ type: 'largest-contentful-paint', buffered: true });
  new PerformanceObserver(l => { for (const e of l.getEntries()) if (!e.hadRecentInput) window.__cls += e.value; }).observe({ type: 'layout-shift', buffered: true });` });
loaded = false; await send('Page.navigate', { url }); for (let i = 0; i < 150 && !loaded; i++) await sleep(200);
await sleep(3000);
const perf = await evaluate(`(() => { const fcp = performance.getEntriesByName('first-contentful-paint')[0]; return { fcp: Math.round(fcp ? fcp.startTime : 0), lcp: Math.round(window.__lcp), cls: +window.__cls.toFixed(3), load: Math.round(performance.getEntriesByType('navigation')[0].loadEventEnd) }; })()`);
const blocking = await evaluate(`[...document.querySelectorAll('head link[rel=stylesheet], head script[src]:not([async]):not([defer])')].map(e => (e.href || e.src).replace(location.origin, ''))`);
const seo = await evaluate(`(() => { const m = (n) => document.querySelector(n)?.getAttribute('content') || document.querySelector(n)?.getAttribute('href') || null;
  const h = [...document.querySelectorAll('h1,h2,h3')].map(e => e.tagName); let order = true; for (let i = 1; i < h.length; i++) if (+h[i][1] - +h[i-1][1] > 1) order = false;
  let ld = 'absent'; try { const s = document.querySelector('script[type="application/ld+json"]'); if (s) { JSON.parse(s.textContent); ld = 'valide'; } } catch (e) { ld = 'invalide'; }
  return { titre: document.title, longueurTitre: document.title.length, description: m('meta[name=description]'), longueurDescription: (m('meta[name=description]') || '').length,
    canonical: m('link[rel=canonical]'), langue: document.documentElement.lang, robots: m('meta[name=robots]'), h1: document.querySelectorAll('h1').length, ordreTitresOK: order,
    ogImage: m('meta[property="og:image"]'), twitterCard: m('meta[name="twitter:card"]'), ogSiteName: m('meta[property="og:site_name"]'), donneesStructurees: ld,
    imagesSansAlt: [...document.images].filter(i => !i.hasAttribute('alt')).length, liensSansTexte: [...document.links].filter(a => !a.textContent.trim() && !a.getAttribute('aria-label')).length,
    mots: document.body.innerText.split(/\s+/).length }; })()`);
const a11y = await evaluate(`(() => ({ champsSansLibelle: [...document.querySelectorAll('input:not([type=hidden]),select,textarea')].filter(e => !e.labels?.length && !e.getAttribute('aria-label') && !e.closest('[aria-hidden=true]')).map(e => e.id),
  boutonsSansNom: [...document.querySelectorAll('button')].filter(b => !b.textContent.trim() && !b.getAttribute('aria-label') && !b.querySelector('.visually-hidden')).length }))()`);
const reqs = [...requests.values()];
const total = reqs.reduce((s, r) => s + (r.bytes || 0), 0);
const byHost = {}; for (const r of reqs) { const h = new URL(r.url).host; byHost[h] = (byHost[h] || 0) + (r.bytes || 0); }
console.log('PERFORMANCE (mobile, 4G lente, CPU x4) :', JSON.stringify(perf));
console.log('Ressources bloquant l\'affichage :', JSON.stringify(blocking));
console.log(`Poids total : ${(total / 1024).toFixed(0)} Ko en ${reqs.length} requêtes ; par domaine :`, JSON.stringify(Object.fromEntries(Object.entries(byHost).map(([h, b]) => [h, Math.round(b / 1024) + ' Ko']))));
console.log('SEO :', JSON.stringify(seo, null, 1));
console.log('ACCESSIBILITÉ :', JSON.stringify(a11y));
console.log('Erreurs console :', JSON.stringify(errors.slice(0, 5)));
ws.close(); proc.kill(); process.exit(0);
