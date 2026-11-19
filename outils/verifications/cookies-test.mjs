import { spawn } from 'node:child_process';
const [chrome] = process.argv.slice(2);
const port = 9346;
const proc = spawn(chrome, ['--headless=new', '--disable-gpu', `--remote-debugging-port=${port}`, `--user-data-dir=${process.env.TEMP}/ck-${Date.now()}`, '--no-first-run', 'about:blank'], { stdio: 'ignore' });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
let target; for (let i = 0; i < 50 && !target; i++) { try { target = (await (await fetch(`http://127.0.0.1:${port}/json/list`)).json()).find((t) => t.type === 'page'); } catch {} if (!target) await sleep(200); }
const ws = new WebSocket(target.webSocketDebuggerUrl); await new Promise((r) => ws.addEventListener('open', r));
let id = 0; const pending = new Map(); let loaded = false; const hosts = new Set();
ws.addEventListener('message', (e) => { const m = JSON.parse(e.data); if (m.id && pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); } if (m.method === 'Page.loadEventFired') loaded = true; if (m.method === 'Network.requestWillBeSent') hosts.add(new URL(m.params.request.url).host); });
const send = (method, params = {}) => new Promise((r) => { const i = ++id; pending.set(i, r); ws.send(JSON.stringify({ id: i, method, params })); });
await send('Page.enable'); await send('Network.enable');
for (const u of ['https://laurabojon.fr/', 'https://laurabojon.fr/projets/klotho/', 'https://laurabojon.fr/articles/prix-site-vitrine/']) {
  loaded = false; await send('Page.navigate', { url: u }); for (let i = 0; i < 60 && !loaded; i++) await sleep(200); await sleep(1500);
}
// Retour à l'accueil et défilement jusqu'au formulaire pour charger le captcha
loaded = false; await send('Page.navigate', { url: 'https://laurabojon.fr/#contact' }); for (let i = 0; i < 60 && !loaded; i++) await sleep(200);
await send('Runtime.evaluate', { expression: "document.getElementById('contact').scrollIntoView(), true" }); await sleep(8000);
const ck = (await send('Storage.getCookies')).result.cookies;
const ls = (await send('Runtime.evaluate', { expression: "JSON.stringify({ local: Object.keys(localStorage), session: Object.keys(sessionStorage) })", returnByValue: true })).result.result.value;
const ts = (await send('Runtime.evaluate', { expression: "!!window.turnstile", returnByValue: true })).result.result.value;
console.log('Domaines contactés :', [...hosts].join(', '));
console.log('Captcha chargé :', ts);
console.log('Cookies déposés :', ck.length ? ck.map(c => `${c.name} (${c.domain}, ${c.session ? 'session' : 'expire ' + new Date(c.expires * 1000).toISOString().slice(0, 10)})`).join(' ; ') : 'aucun');
console.log('Stockage local du site :', ls);
ws.close(); proc.kill(); process.exit(0);
